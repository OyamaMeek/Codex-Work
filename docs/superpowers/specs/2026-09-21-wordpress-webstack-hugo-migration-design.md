# WordPress 导航站迁移至 WebStack-Hugo

## 目标

将 `blt-Launchpad/db_daohang_bilunton_20241218_023001_5m3WTa.sql` 中的导航数据迁移为可由 Hugo 构建的 WebStack-Hugo 静态站点。

## 已核实的数据

- 备份使用 WordPress 数据表，主题配置为 WebStack。
- 导航链接保存在 `wp_posts` 与 `wp_postmeta`：链接为 `_sites_link`，描述为 `_sites_sescribe`，排序为 `_sites_order`。
- 备份包含 44 个导航链接记录、12 个带图标与排序信息的分类记录。
- 备份只有 19 个媒体文件路径记录，没有任何上传文件二进制内容。

## 范围

### 包含

- 在 `blt-Launchpad/webstack-hugo/` 创建独立的 WebStack-Hugo 项目。
- 使用 MariaDB 导入副本并通过 SQL 查询读取 WordPress 数据；不以字符串解析 SQL 备份。
- 将标题、链接、描述、分类、分类图标、显示排序迁移至 `data/webstack.yml`。
- 生成站点配置与本地构建说明。
- 在本地运行 Hugo 构建，验证静态文件可生成到 `public/`。

### 不包含

- 迁移 WordPress 用户、评论、文章、隐私政策页面或旧主题代码。
- 恢复缺失的 WordPress 上传图片。
- 创建 GitHub 仓库或发布到任何托管平台。

## 项目结构

```text
blt-Launchpad/
  db_daohang_bilunton_20241218_023001_5m3WTa.sql
  webstack-hugo/
    config.toml
    data/webstack.yml
    themes/WebStack-Hugo/
    README.md
```

`webstack-hugo/` 是独立 Git 项目。上游 WebStack-Hugo 文件作为项目基础，导航内容仅维护在 `data/webstack.yml`；后续新增或编辑导航链接不需要接触模板文件。

## 数据转换

使用临时 MariaDB 实例加载 SQL 备份，通过 WordPress 的文章、元数据、分类与关联表查询导航数据。转换程序需要做到：

1. 只保留拥有非空 `_sites_link` 的已发布导航条目。
2. 采用 `_sites_order` 排序；没有数值时放在相应分类的末尾。
3. 通过术语关系还原分类，并按 `_term_order` 排序。
4. 输出 WebStack-Hugo 所需的 YAML 结构，保持 Unicode 文本、HTTPS 链接与多行描述正确转义。
5. 对没有分类、没有链接或没有标题的数据输出明确错误，避免静默遗漏。

原始 SQL 备份保持只读且不加入新站点 Git 历史。导入数据库的临时数据也不进入版本控制。

## 图片处理

现有备份缺少实际上传图片，无法可靠复原 WordPress Logo。每个站点将使用 WebStack-Hugo 的默认图标展示机制；不臆造或下载替代图片。以后若补充旧站 `wp-content/uploads/`，可将图片映射至 `static/assets/images/logos/` 并在同一数据文件中补充 Logo 字段。

## 验证

- 转换测试使用导入后的真实 SQL 数据，检查 44 个链接记录均被读取且 12 个分类均被生成。
- 验证生成的 YAML 可被 Hugo 读取。
- 运行 `hugo`，确认成功生成 `public/`。
- 检查生成页面包含每个分类标题和每个导航链接 URL。
- 确认 `git status` 不包含 SQL 备份、MariaDB 临时数据、构建产物或任何数据库凭据。

## 风险与处理

- 外部导航链接可能已经失效：迁移保留原始链接，不以可用性猜测替换目标。
- WordPress 媒体文件缺失：使用主题默认图标，记录可选补充路径。
