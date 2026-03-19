# DocFeed

> Feed your AI the freshest docs.

AI 编程助手（Cursor、Claude、ChatGPT 等）虽然强大，但它们的训练数据往往是过时的。让它们写 Vue 3.4 的代码，可能会给你 Vue 2 的写法。

**DocFeed** 解决了这个问题。选择你使用的框架和版本，勾选需要的文档模块，一键生成格式化好的上下文片段，粘贴到你的 AI 工具中——让 AI 基于最新的官方文档写代码。

## 功能特性

- **框架选择** — 支持 Vue 3、Vue Router 4、Pinia
- **模块筛选** — 按需勾选 guide、api、examples 等文档模块，支持全选
- **一键生成** — 将所有选中文档合并为格式化的上下文文本
- **一键复制** — 生成结果直接复制到剪贴板，粘贴进任意 AI 工具
- **实时统计** — 显示文件数量和内容大小（KB）
- **暗色主题** — 默认深色 UI，保护眼睛

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite |
| 后端 | Python + FastAPI + Uvicorn |
| 文档来源 | GitHub API v3 |
| 前端部署 | Vercel |
| 后端部署 | Railway |

## 项目结构

```
DocFeed/
├── backend/                      # 后端服务
│   ├── app/
│   │   ├── main.py              # FastAPI 应用入口，CORS 中间件
│   │   ├── config.py            # 配置管理（Pydantic Settings）
│   │   ├── models/
│   │   │   └── schemas.py       # 数据模型（DocFile, DocModule 等）
│   │   ├── routers/
│   │   │   └── docs.py          # API 路由（/frameworks, /generate）
│   │   └── services/
│   │       ├── fetcher.py       # GitHub API 文档抓取
│   │       └── processor.py     # Markdown 格式化与上下文构建
│   ├── main.py                  # 开发启动入口
│   ├── pyproject.toml           # Python 项目配置
│   └── .env.example             # 环境变量模板
│
├── frontend/                     # 前端应用
│   ├── src/
│   │   ├── App.vue              # 主页面组件
│   │   ├── main.ts              # Vue 应用入口
│   │   ├── style.css            # 全局样式（暗色主题）
│   │   ├── api/
│   │   │   └── index.ts         # Axios HTTP 客户端
│   │   └── types/
│   │       └── index.ts         # TypeScript 类型定义
│   ├── package.json
│   └── vite.config.ts
│
├── GOAL.md                       # 项目目标与规划
├── LICENSE                       # MIT 许可证
└── README.md
```

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- pnpm
- [uv](https://github.com/astral-sh/uv)（推荐的 Python 包管理器）

### 后端

```bash
cd backend

# 安装依赖
uv pip install -e .

# 配置环境变量（可选，但推荐配置 GitHub Token 以提高 API 速率限制）
cp .env.example .env
# 编辑 .env，填入你的 GitHub Personal Access Token

# 启动开发服务器
python main.py
# 服务运行在 http://localhost:8000
```

### 前端

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm run dev
# 应用运行在 http://localhost:5173

# 构建生产版本
pnpm run build
```

## 环境变量

### 后端

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GITHUB_TOKEN` | GitHub Personal Access Token，用于提高 API 速率限制（60 → 5000 次/小时） | 无 |
| `DEBUG` | 调试模式 | `false` |
| `CORS_ORIGINS` | 允许的 CORS 来源 | `["*"]` |

### 前端

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VITE_API_BASE_URL` | 后端 API 地址 | `/api` |

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/frameworks` | 获取所有支持的框架及其模块列表 |
| GET | `/api/frameworks/{id}/modules` | 获取指定框架的模块列表 |
| POST | `/api/generate` | 根据选择的模块生成格式化上下文 |
| GET | `/health` | 健康检查 |

## 文档来源

所有文档均通过 GitHub API 从各框架的官方仓库实时拉取：

| 框架 | 仓库 | 文档目录 |
|------|------|----------|
| Vue 3 | `vuejs/docs` | `src/` |
| Vue Router 4 | `vuejs/router` | `packages/docs/` |
| Pinia | `vuejs/pinia` | `packages/docs/` |

## 许可证

[MIT](LICENSE) &copy; Kaede