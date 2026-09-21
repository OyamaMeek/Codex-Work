# WordPress 导航站迁移至 WebStack-Hugo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从 WordPress SQL 备份生成包含全部导航数据、可本地构建并附 Cloudflare Pages 部署指南的 WebStack-Hugo 项目。

**Architecture:** 以 `shenweiyan/NavBioIT` 作为完整 Hugo 站点骨架，并保留 `shenweiyan/WebStack-Hugo` 主题。Python 转换工具使用 `sqlglot` 读取 MySQL 的 INSERT 语句，关联 WordPress 的 posts、postmeta、terms 与 taxonomy 表，随后使用 PyYAML 写入主题需要的 `data/webstack.yml`。转换工具只在本地开发时运行，最终站点和 Cloudflare Pages 构建只需要 Hugo。

**Tech Stack:** Hugo、WebStack-Hugo、Python 3、sqlglot、PyYAML、unittest。

**Spec:** `docs/superpowers/specs/2026-09-21-wordpress-webstack-hugo-migration-design.md`

## Global Constraints

- 原始备份 `blt-Launchpad/db_daohang_bilunton_20241218_023001_5m3WTa.sql` 保持只读，绝不复制到新项目或提交至 Git。
- 不迁移 WordPress 用户、文章、评论、隐私政策页面与上传文件路径。
- 使用 `sqlglot` 解析 SQL；不得手写字符串解析器。
- 输出的 `data/webstack.yml` 必须保留 44 条有效导航链接、12 个原始分类与末尾“其他”分组，URL 不得改写。
- 缺失 Logo 时不下载替代图；对应 YAML 条目不写 `logo` 字段。
- 网站项目的 Git 提交仅包含其文件；提交说明遵循 Conventional Commits。

## Review Focus

- SQL 转义字符与 Unicode：输出 YAML 可读取，标题、描述和 URL 不出现截断或转义错误。
- 失效链接：保留数据库中的原 URL，不进行网络探测或替换。
- 没有 `_sites_order` 的条目：排在同分类有数字排序条目之后，并保持数据库出现顺序。
- 分类顺序：`_term_order` 为零的分类按术语 ID 排序，再接升序的非零排序；当前备份的 12 个 `favorites` 分类均为顶级分类。
- 无 `favorites` 分类关系的链接：保留在末尾“其他”分组，不静默丢弃。
- 缺失 Logo：最终 YAML 不含本地不存在的图片路径，Hugo 构建仍成功。

### Task 1: 初始化独立 Hugo 项目

**Files:**
- Create: `blt-Launchpad/webstack-hugo/`（从 `https://github.com/shenweiyan/NavBioIT.git` 克隆）
- Modify: `blt-Launchpad/webstack-hugo/.gitignore`
- Modify: `blt-Launchpad/webstack-hugo/config.toml`

**Interfaces:**
- Consumes: 上游 NavBioIT 站点骨架与 WebStack-Hugo 主题。
- Produces: 具有 `config.toml`、`data/`、`themes/WebStack-Hugo/` 的独立 Hugo 项目目录。

- [ ] **Step 1: 创建项目目录并保留上游来源**

运行：

```bash
git clone --depth 1 https://github.com/shenweiyan/NavBioIT.git blt-Launchpad/webstack-hugo
git -C blt-Launchpad/webstack-hugo remote rename origin upstream
git -C blt-Launchpad/webstack-hugo submodule update --init --recursive
```

预期：`webstack-hugo` 有自己的 `.git`，上游远端名为 `upstream`，主题目录存在。

- [ ] **Step 2: 写入忽略规则与站点基础信息**

在 `.gitignore` 加入以下路径，防止导入副本、Python 缓存和 Hugo 构建产物进入版本控制：

```gitignore
.migration/
__pycache__/
public/
resources/
```

在 `config.toml` 设置：

```toml
baseURL = "/"
languageCode = "zh-CN"
title = "学术科研导航"
theme = "WebStack-Hugo"
```

- [ ] **Step 3: 验证项目结构**

运行：

```bash
test -f blt-Launchpad/webstack-hugo/config.toml
test -d blt-Launchpad/webstack-hugo/data
test -d blt-Launchpad/webstack-hugo/themes/WebStack-Hugo
git -C blt-Launchpad/webstack-hugo status --short
```

预期：前三个检查成功，状态仅显示本任务的配置修改。

- [ ] **Step 4: 提交基础项目**

运行：

```bash
git -C blt-Launchpad/webstack-hugo add -- .gitignore config.toml
git -C blt-Launchpad/webstack-hugo commit -m "chore: initialize webstack hugo site"
```

### Task 2: 使用真实 SQL 备份实现并验证数据转换

**Files:**
- Create: `blt-Launchpad/webstack-hugo/tools/requirements.txt`
- Create: `blt-Launchpad/webstack-hugo/tools/import_wordpress.py`
- Create: `blt-Launchpad/webstack-hugo/tools/test_import_wordpress.py`
- Create: `blt-Launchpad/webstack-hugo/data/webstack.yml`

**Interfaces:**
- Consumes: SQL 文件路径，默认值为 `../db_daohang_bilunton_20241218_023001_5m3WTa.sql`。
- Produces: `build_webstack(path: Path) -> list[dict]` 和 UTF-8 YAML 文件 `data/webstack.yml`。

- [ ] **Step 1: 安装成熟解析与 YAML 库**

在 `tools/requirements.txt` 写入：

```text
PyYAML==6.0.2
sqlglot==26.6.0
```

运行：

```bash
cd blt-Launchpad/webstack-hugo
python3 -m pip install -r tools/requirements.txt
```

- [ ] **Step 2: 写入失败测试**

在 `tools/test_import_wordpress.py` 使用真实备份，定义以下测试：

```python
import unittest
from pathlib import Path

import yaml

from tools.import_wordpress import build_webstack


SQL = Path(__file__).parents[2] / "db_daohang_bilunton_20241218_023001_5m3WTa.sql"


class ImportWordPressTests(unittest.TestCase):
    def test_build_webstack_preserves_navigation_records(self):
        data = build_webstack(SQL)
        links = [link for group in data for link in group["links"]]
        self.assertEqual(44, len(links))
        self.assertEqual(13, len(data))
        self.assertEqual(
            ["基金项目", "科研社区", "问卷调查", "文档翻译", "学历查询", "图书查询", "学术词典", "必备软件", "投稿选刊", "文献下载", "论文课程", "论文查重", "其他"],
            [group["taxonomy"] for group in data],
        )
        self.assertIn("https://cx.cnki.net/main.html#/login", {link["url"] for link in links})

    def test_emitted_yaml_is_valid_and_has_no_missing_logos(self):
        data = build_webstack(SQL)
        rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        self.assertEqual(data, yaml.safe_load(rendered))
        self.assertNotIn("logo", rendered)
```

- [ ] **Step 3: 运行测试并确认失败原因是实现尚不存在**

运行：

```bash
cd blt-Launchpad/webstack-hugo
python3 -m unittest tools/test_import_wordpress.py -v
```

预期：失败信息指出 `import_wordpress` 模块或 `build_webstack` 尚不存在。

- [ ] **Step 4: 实现最小转换器**

在 `tools/import_wordpress.py` 定义 `read_tables`、`build_webstack` 和 `main`。核心数据关系固定为：

```python
POST_ID, POST_TITLE, POST_STATUS, POST_TYPE = 0, 5, 7, 20
META_POST_ID, META_KEY, META_VALUE = 1, 2, 3
TERM_ID, TERM_NAME = 0, 1
TAXONOMY_ID, TAXONOMY_TERM_ID, TAXONOMY_NAME, TAXONOMY_PARENT = 0, 1, 2, 4
RELATIONSHIP_OBJECT_ID, RELATIONSHIP_TAXONOMY_ID = 0, 1
```

实现要求：

```python
def build_webstack(sql_path: Path) -> list[dict]:
    tables = read_tables(sql_path)
    # 仅保留 post_type == "sites"、post_status == "publish" 且 _sites_link 非空的记录。
    # 将 _sites_sescribe 映射为 description，将 _term_ico 映射为 icon。
    # 当前备份的全部 favorites 分类都是顶级分类，输出 {"taxonomy", "icon", "links"}。
    # 每个 link 仅包含 title、url、description。
```

`read_tables` 使用 `sqlglot.parse(sql_text, read="mysql")` 获取 `exp.Insert` 节点，读取节点的字面量值，不通过分割 SQL 文本取得字段。`main` 通过命令行位置参数接收 SQL 路径，通过 `--output` 接收输出路径，默认写入 `data/webstack.yml`，并执行：

```python
yaml.safe_dump(data, output_file, allow_unicode=True, sort_keys=False, width=1000)
```

- [ ] **Step 5: 运行测试并确认通过**

运行：

```bash
cd blt-Launchpad/webstack-hugo
python3 -m unittest tools/test_import_wordpress.py -v
python3 tools/import_wordpress.py ../db_daohang_bilunton_20241218_023001_5m3WTa.sql --output data/webstack.yml
```

预期：两个测试通过，生成的 YAML 有 12 个原始顶级分类、末尾“其他”分组和 44 条导航记录。

- [ ] **Step 6: 提交转换器和数据文件**

运行：

```bash
git -C blt-Launchpad/webstack-hugo add -- tools/requirements.txt tools/import_wordpress.py tools/test_import_wordpress.py data/webstack.yml
git -C blt-Launchpad/webstack-hugo commit -m "feat: import wordpress navigation data"
```

### Task 3: 添加站点说明与部署指南

**Files:**
- Modify: `blt-Launchpad/webstack-hugo/README.md`

**Interfaces:**
- Consumes: `config.toml` 与 `data/webstack.yml`。
- Produces: 新项目使用说明和可复制的 Cloudflare Pages 配置值。

- [ ] **Step 1: 写入项目使用说明**

`README.md` 需要包含：

```markdown
## 本地预览

hugo server --disableFastRender

## 更新导航数据

python3 -m pip install -r tools/requirements.txt
python3 tools/import_wordpress.py ../db_daohang_bilunton_20241218_023001_5m3WTa.sql --output data/webstack.yml
```

还需说明：SQL 备份不进入项目 Git、上传图片未包含于备份、缺失 Logo 采用主题默认显示。

- [ ] **Step 2: 写入 Cloudflare Pages 指南**

在 README 中加入：将项目推送到用户自己的 GitHub 仓库，Cloudflare Pages 选择 `main`，构建命令填 `hugo -b $CF_PAGES_URL`，输出目录填 `public`，将本地 `hugo version` 的版本号填到 Production 和 Preview 的 `HUGO_VERSION`。明确这些为用户在控制台执行的操作。

- [ ] **Step 3: 提交说明**

运行：

```bash
git -C blt-Launchpad/webstack-hugo add -- README.md
git -C blt-Launchpad/webstack-hugo commit -m "docs: add site deployment guide"
```

### Task 4: 构建验证和最终提交

**Files:**
- Create: `blt-Launchpad/webstack-hugo/docs/CHANGELOG.md`

**Interfaces:**
- Consumes: 完成的数据文件、主题与 README。
- Produces: `public/` 静态站点和准确的验证记录。

- [ ] **Step 1: 安装 Hugo 并记录版本**

运行：

```bash
brew install hugo
hugo version
```

预期：Hugo 可执行，版本号写入 README 的 `HUGO_VERSION` 指引。

- [ ] **Step 2: 构建生产站点**

运行：

```bash
cd blt-Launchpad/webstack-hugo
hugo
test -f public/index.html
```

预期：命令退出码为零，`public/index.html` 存在。

- [ ] **Step 3: 以生成内容验证迁移结果**

运行：

```bash
cd blt-Launchpad/webstack-hugo
rg -F "论文查重" public/index.html
rg -F "https://cx.cnki.net/main.html#/login" public/index.html
git status --short
```

预期：前两项命中；`public/`、`.migration/`、原 SQL 备份均未被 Git 追踪。

- [ ] **Step 4: 追加最终验证记录并提交**

创建 `docs/CHANGELOG.md` 并写入当前日期时间、原始需求、已生成的 `data/webstack.yml`、转换工具、README、实际执行的测试、Hugo 版本和已完成的转换器提交哈希；不得提交任何模板文字或虚构结果。运行：

```bash
git -C blt-Launchpad/webstack-hugo add -- docs/CHANGELOG.md
git -C blt-Launchpad/webstack-hugo diff --cached --check
git -C blt-Launchpad/webstack-hugo commit -m "docs: record migration verification"
```

预期：提交不包含 SQL 备份、`.env`、密钥、日志或构建产物。
