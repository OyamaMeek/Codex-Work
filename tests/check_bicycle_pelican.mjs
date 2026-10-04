import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';

const file = new URL('../bicycle-rides-pelican.html', import.meta.url);
assert.ok(existsSync(file), '应交付可直接打开的自行车骑鹈鹕 HTML');

export default async function verify(task) {
  const page = task.page('p1');
  await page.goto(file.href);
  const structure = await page.evaluate(() => {
    const svg = document.getElementById('scene');
    const ids = [...svg.querySelectorAll('[id]')].map(node => node.id);
    const xml = new DOMParser().parseFromString(svg.outerHTML, 'image/svg+xml');
    const references = [...svg.querySelectorAll('[href]')].map(node => node.getAttribute('href').slice(1));
    const bike = document.getElementById('bicycle').getBoundingClientRect();
    const pelican = document.getElementById('pelican-body').getBoundingClientRect();
    return {
      validXml: !xml.querySelector('parsererror'), ids, references,
      bikeAboveBird: bike.bottom < pelican.bottom && bike.top < pelican.top,
      overlapsBack: bike.right > pelican.left && bike.left < pelican.right,
      resources: performance.getEntriesByType('resource').length
    };
  });
  assert.ok(structure.validXml);
  assert.equal(new Set(structure.ids).size, structure.ids.length);
  assert.ok(structure.references.every(id => structure.ids.includes(id)));
  assert.ok(structure.bikeAboveBird && structure.overlapsBack, '自行车位于鹈鹕背上');
  assert.equal(structure.resources, 0, '离线动画无外部资源请求');
  const motion = await page.evaluate(async () => {
    const parts = ['front-spokes', 'foot-near', 'travellers', 'road'];
    const read = () => parts.map(id => document.getElementById(id).getAttribute('transform'));
    const before = read();
    await new Promise(resolve => setTimeout(resolve, 250));
    const after = read();
    const invalid = [];
    for (let step = 0; step <= 180; step++) {
      render(step * 4.8 / 180);
      for (const id of parts) {
        const value = document.getElementById(id).getAttribute('transform');
        if (/NaN|Infinity|undefined/.test(value)) invalid.push({ step, id, value });
      }
    }
    render(elapsed);
    return { before, after, invalid };
  });
  motion.before.forEach((value, i) => assert.notEqual(value, motion.after[i], `动画部件 ${i} 随时间推进`));
  assert.deepEqual(motion.invalid, []);
  await page.click('#toggle');
  const stopped = await page.evaluate(async () => {
    const wheel = document.getElementById('front-spokes');
    const before = wheel.getAttribute('transform');
    await new Promise(resolve => setTimeout(resolve, 180));
    return { before, after: wheel.getAttribute('transform'), running: document.getAnimations().filter(a => a.playState === 'running').length };
  });
  assert.equal(stopped.before, stopped.after);
  assert.equal(stopped.running, 0, '暂停同时冻结 CSS 动画');
  await page.click('#toggle');
  const resumed = await page.evaluate(async () => {
    const wheel = document.getElementById('front-spokes');
    const before = wheel.getAttribute('transform');
    await new Promise(resolve => setTimeout(resolve, 180));
    return { before, after: wheel.getAttribute('transform') };
  });
  assert.notEqual(resumed.before, resumed.after);
  for (const width of [320, 390, 1440]) {
    await page.cdp('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: false });
    assert.equal(await page.evaluate(() => innerWidth), width);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${width}px 无水平溢出`);
  }
  await page.cdp('Emulation.setEmulatedMedia', { media: 'screen', features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await page.reload();
  const reduced = await page.evaluate(async () => {
    const wheel = document.getElementById('front-spokes');
    const before = wheel.getAttribute('transform');
    await new Promise(resolve => setTimeout(resolve, 180));
    return { before, after: wheel.getAttribute('transform'), paused: document.getElementById('toggle').getAttribute('aria-pressed'), running: document.getAnimations().filter(a => a.playState === 'running').length };
  });
  assert.equal(reduced.before, reduced.after);
  assert.equal(reduced.paused, 'true');
  assert.equal(reduced.running, 0);
  await page.cdp('Emulation.setEmulatedMedia', { features: [] });
  await page.cdp('Emulation.clearDeviceMetricsOverride');
  console.log(JSON.stringify({ status: 'passed', type: 'browser_behavior', message: '实际验证相对位置、181个周期采样、动作推进、暂停继续、离线资源、窄屏布局和减少动态效果', suggestion: '未进行截图或视觉检查' }));
  await task.finish({ keep: [] });
}
