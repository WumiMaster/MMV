# 喵喵语音 🐾

浏览器端精简版 Discord，专注**频道实时语音** + **频道图文文字交流**。

## 技术栈

- **后端**：Python FastAPI + SQLAlchemy + SQLite
- **前端**：Vue 3 + Vite + Tailwind CSS
- **认证**：JWT Token
- **UI 风格**：iOS26 液态玻璃拟态（粉色 + 绿色）

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 或 pnpm

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库并创建默认管理员
python seed.py

# 启动后端服务
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

后端运行在 `http://localhost:8000`

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 `http://localhost:5173`

### 3. 登录

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

> 请登录后及时修改密码！

## 项目结构

```
workspace/
├── backend/                 # 后端（FastAPI）
│   ├── src/
│   │   ├── config/          # 数据库配置
│   │   ├── controllers/     # 控制器
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # 路由（auth、admin）
│   │   ├── services/        # 业务逻辑
│   │   ├── middlewares/     # 中间件（认证）
│   │   ├── utils/           # 工具函数
│   │   └── main.py          # 应用入口
│   ├── seed.py              # 数据库种子脚本
│   ├── requirements.txt     # Python 依赖
│   └── .env.example         # 环境变量模板
├── frontend/                # 前端（Vue3）
│   ├── src/
│   │   ├── api/             # HTTP 请求封装
│   │   ├── components/      # 公共组件
│   │   ├── pages/           # 页面组件
│   │   ├── stores/          # 状态管理（Pinia）
│   │   ├── hooks/           # 自定义 Hooks
│   │   ├── utils/           # 工具函数
│   │   ├── styles/          # 全局样式
│   │   ├── router.js        # 路由配置
│   │   └── main.js          # 应用入口
│   └── package.json
├── docs/                    # 文档
│   ├── prototype.html       # 静态原型
│   └── ui-prototype.md      # UI 原型说明
└── claude.md                # 产品需求文档（PRD）
```

## 开发阶段

- [x] 阶段1：基础框架 + 登录注册 + 管理员后台 + 基础 UI
- [x] 阶段2：频道创建、文字子频道、图文聊天、消息留存策略
- [x] 阶段3：WebRTC 实时语音子频道（P2P 模式）
- [ ] 阶段4：悬浮多窗口系统、动画优化
- [ ] 阶段5：BUG 修复、移动端适配
