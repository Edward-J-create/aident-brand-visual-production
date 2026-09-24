# aident-brand-visual-production

用于在缺少品牌视觉素材时，**生产**营销图片套件与视频制作套件的 Agent Skill。上游对接 **aident-brand-marketing-pack**（文案、分类、质量门禁、云文档与成片库）。

HTML 布局模板 + 可替换 token/插槽 的**封装粒度**对齐 Edward 的 **aident-ppt-skill**。尺寸和版式以本 Skill 已打包的模板为准。设计源文件不随包发布。

## 分工

- **营销包**：文案、brief、冻结交接、云文档、原文件入库
- **本 Skill**：按已打包的模板尺寸出图/分镜/镜头表，导出 QA，回传 return 包
- **不做**：撰写包内文案；声称云端营销包已完成；用生成模型重绘真 logo；把分镜当成成片 MP4

## 可替换模型

| 层 | 机制 | 如何替换 |
|---|---|---|
| 颜色 | CSS 变量 + `tokens.json` 角色 | 品牌 payload 的 `colors.*`（勿把客户色写死进共享模板） |
| 文案 | `data-slot` 文本插槽 | payload `text.*` |
| 图像 | logo / hero / UI 等 `data-slot` | payload `images.*` 指向**已提供**文件 |
| 字体 | `--font-primary` / `--font-display` | payload `fonts.*`；可选合规本地字体，见 `assets/fonts/licenses/README.md` |
| 尺寸 | `size-kit.yaml` | 已知 `tpl-*` ID 不可改尺寸 |

详见 `references/editable-slots.md`。

## 首选静态出图流程

从冻结的 `aident-brand-marketing-pack` handoff 批量启动生产：

```bash
python scripts/prepare_pack_run.py \
  --handoff examples/both-from-pack-handoff.yaml \
  --out /tmp/abvp-return \
  --png
```

桥接脚本会校验 approved copy、source asset、rights、template ID 与 slot binding，生成逐素材 payload、填充后的 HTML、分镜/镜头表和 return manifest。自动出图后仍保持 `in-production`，直到完成视觉与品牌 QA。详见 `references/pack-bridge.md`。

单张模板渲染：

```bash
python scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster
```

有 Playwright/Chromium 时可加 `--png`。无 Playwright 时仍输出填好的 HTML + `EXPORT.md`。

本地图片路径失效时会警告并保持槽位为空，不再把破图图标输出到 PNG。最终图不得保留“Supplied…”一类说明占位；浅色/深色画面必须使用品牌已批准的对应 logo 变体，不能临时改色真 logo。

功能海报必须提供右下角 `text.url`，中间主视觉通过可替换的 `images.ui-screenshot`（或 `hero`）传入。需要强调第二行时，必须单独绑定 `text.headline-accent`，由模板施加更鲜明的渐变。大标题最多两行；右下角网址短域名保持 Outfit 400 / 56px，只在超出保留宽度时缩小，不通过加粗解决。

## 模式

`image-kit` / `video-kit` / `both` / `qa-only`

## 尺寸套件

见 `assets/templates/size-kit.yaml`：视频封面 1920×1080、功能海报 1242×1660、Banner 1270×760、X/YouTube/LinkedIn 横幅、头像 400×400、Logo 槽位、分镜帧 1920×1080 等。静态图 HTML 模板在 `assets/templates/html/`。

## 校验

```bash
python scripts/validate_package.py
```

字体以清单+许可说明为主，未授权字体二进制不得入库；宿主需自行安装 Outfit 等，或按文档覆盖 font-family token。
