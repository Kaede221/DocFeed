````markdown
# DocFeed — Project Goal

## 一句话定位
Feed your AI the freshest docs.
帮助前端开发者把 Vue3 / Vue Router 4 / Pinia 最新官方文档转换成可直接粘贴进 AI 工具的 context 片段，解决 AI 写代码时使用过时文档的问题。

## 目标用户
使用 Cursor、Claude、ChatGPT 等 AI 工具写 Vue 相关代码的前端开发者。

## 核心功能（第一版）
- 支持 Vue3 / Vue Router 4 / Pinia 文档
- 用户选择框架版本 + 勾选需要的模块
- 一键生成格式化好的 context 文本
- 一键复制到剪贴板
- 有公网地址可以直接访问

## 技术栈
- 后端：Python + FastAPI
- 前端：Vue3（独立项目，前后端分离）
- 文档来源：GitHub API 拉取各框架官方文档仓库的 .md 原文件
- 部署：前后端分别部署

## 文档来源仓库
| 框架         | 仓库         | 文档目录       |
| ------------ | ------------ | -------------- |
| Vue 3        | vuejs/docs   | src/           |
| Vue Router 4 | vuejs/router | packages/docs/ |
| Pinia        | vuejs/pinia  | packages/docs/ |

## 项目结构
```
docfeed/
├── backend/
│   ├── main.py              # FastAPI 入口，提供 REST API
│   ├── fetcher.py           # GitHub API 抓取文档逻辑
│   ├── processor.py         # .md 内容切片 + 格式化成 context
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue          # 主页面组件
│   │   ├── main.js
│   │   └── components/      # 拆分的子组件
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── GOAL.md
```

## 开发计划
| 天      | 任务                                                   |
| ------- | ------------------------------------------------------ |
| Day 1   | 跑通 GitHub API，拉取三个仓库的 .md 文件列表，确认结构 |
| Day 2   | 写 fetcher.py + processor.py，实现文档抓取和切片逻辑   |
| Day 3   | 写 FastAPI 接口，返回格式化好的 context 文本           |
| Day 4-5 | 写 Vue3 前端页面，对接后端接口                         |
| Day 6   | 部署前后端，配域名，公网可访问                         |
| Day 7   | 写掘金文章发布，开源到 GitHub                          |

## 第一版不做的东西

- React / Angular 等其他框架
- VS Code 插件
- 用户账号系统
- 自动同步文档更新（手动触发就够）

## 项目名
**DocFeed**
Slogan：Feed your AI the freshest docs.
License：MIT
````