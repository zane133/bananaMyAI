# 🍌 Nano Banana Studio

基于 Google Gemini API 的原生图片生成 Web 工具，支持文生图、图片编辑、多轮对话迭代，兼容官方 API 及第三方中转服务。生成的图片自动保存到本地项目目录。

## 快速开始

### 方式一：本地服务器（推荐）

双击 `start.bat` 启动本地服务器，浏览器会自动打开 `http://localhost:8765`。

```
双击 start.bat
```

**优点**：生成的图片自动保存到 `banana/` 目录，无需手动操作。

> 需要已安装 [Python 3](https://www.python.org/downloads/)

### 方式二：直接打开

直接用浏览器打开 `index.html`（无需 Python）。

> 注意：此方式无法自动保存图片到本地目录，保存功能不可用。

---

## 配置

在顶部 Header 填写：

| 字段 | 说明 |
|---|---|
| **Base URL** | 留空使用 Google 官方；第三方中转填入对应地址，如 `https://newapi.aiopus.org` |
| **API Key** | 你的 Gemini API Key 或第三方 Key |

点击「**保存**」后配置持久化，下次打开无需重填。

获取官方 Key：[Google AI Studio](https://aistudio.google.com/)

---

## 功能特性

### 图片生成
- **文生图**：输入提示词，一键生成高质量图片
- **图片编辑**：上传最多 14 张参考图片，配合提示词进行编辑、合成、风格迁移
- **多轮对话**：自动保留上下文，可持续迭代修改（底部快速输入框，Enter 发送）
- **自动保存**：每次生成完成后自动保存到项目目录，文件名格式 `nanobanana_时间戳_序号.png`

### 模型支持

| 模型 | API 标识 | 特点 |
|---|---|---|
| 🍌 **Nano Banana 2** | `gemini-3.1-flash-image-preview` | 速度与质量均衡，推荐首选 |
| 🍌 **Nano Banana Pro** | `gemini-3-pro-image-preview` | 专业素材、高保真文字渲染、4K 输出 |
| 🍌 **Nano Banana** | `gemini-2.5-flash-image` | 高速低延迟，适合批量场景 |

### 输出配置
- **宽高比**：14 种（1:1 / 16:9 / 9:16 / 4:3 / 21:9 / 1:4 / 8:1 等）
- **分辨率**：512 / 1K / 2K / 4K
- **思考等级**：`minimal`（低延迟）/ `high`（高质量）
- **可选项**：显示思考过程、仅输出图片、Google 搜索接地、Google 图片搜索接地

### 交互
- 点击图片放大灯箱预览
- 悬浮图片显示「下载」「用作参考」按钮
- 将已生成图片一键设为下一轮的参考图
- 拖拽上传参考图片
- 错误日志持久显示在对话区，支持一键复制

---

## 文件结构

```
banana/
├── index.html        # 前端页面（单文件，零依赖）
├── server.py         # 本地 HTTP 服务器（图片保存 + 静态文件服务）
├── start.bat         # Windows 一键启动脚本
├── .gitignore
├── README.md
└── nanobanana_*.png  # 自动保存的生成图片（已被 .gitignore 忽略）
```

---

## 提示词技巧

- **描述场景而非关键词**：叙述性段落比关键词堆砌效果更好
- **指定摄影参数**：如「85mm 人像镜头」「黄金时段光线」「浅景深」
- **明确用途**：如「为高端护肤品牌设计徽标」比「设计徽标」效果更好
- **分步指令**：复杂场景可拆分成多步，逐步完善
- **迭代优化**：利用多轮对话小幅调整，如「效果不错，但让颜色更饱和一些」

---

## 技术说明

- 纯前端单页应用，零 npm 依赖，无需构建
- 直接调用 Gemini REST API（`/v1beta/models/{model}:generateContent`）
- 本地服务器基于 Python 标准库，无需安装第三方包
- 兼容两种 API 响应格式：
  - `inlineData`（base64）— 官方 Gemini API 标准格式
  - `![alt](https://...)`— 部分第三方中转 API 返回的 Markdown 图片链接，自动解析展示

---

## License

MIT
