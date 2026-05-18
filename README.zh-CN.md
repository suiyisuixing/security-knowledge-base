# 安全知识库与智能体记忆实验室

![CI](https://github.com/suiyisuixing/security-knowledge-base/actions/workflows/ci.yml/badge.svg)

**v3.0-rc** —— 一个本地网络安全知识库、检索、安全策略、智能体记忆、任务路由和评估平台，
用于授权安全学习、防御分析和安全漏洞发现推理。

本系统不支持未授权扫描或漏洞利用。它支持本地实验、自有资产和明确授权范围内的信息收集规划、
低风险安全检查规划与安全验证流程。

---

## 审阅者快速路径

1. 加载知识领域 (`GET /knowledge/domains`)
2. 搜索一个安全概念 (`POST /knowledge/search`)
3. 提出一个基于知识的问题 (`POST /knowledge/ask`)
4. 对一个安全敏感请求进行分类 (`POST /safety/classify`)
5. 查看项目/技能映射 (`GET /skills`, `GET /projects`)
6. 生成学习路径 (`POST /learning-path/generate`)
7. 构建授权工作流计划 (`POST /workflow/authorized-plan`)
8. 把任务路由到 A/B/C/D (`POST /router/route-task`)
9. 运行智能体评估 (`POST /benchmark/run`)
10. 生成智能体就绪报告 (`POST /report/agent-readiness`)

前端面板对每一步都有对应的卡片。

---

## 特性

- 6 大领域共 32+ 篇本地 Markdown 知识文档
- 每篇带 YAML front matter 与 `safe_use` / `forbidden_use`
- 类 BM25 的 TF-IDF 检索（不依赖外部库与向量库）
- 带引用和安全说明的知识 grounded 应答构建器
- 19 类安全策略分类器（allowed / needs confirmation / blocked）
- 智能体记忆（学习画像、技能进度、完成实验）
- 16 个技能与 A/B/C/D 四个项目的映射
- AI 安全、检测、漏洞情报、代码审查 4 条学习路径
- 授权工作流规划器（本地实验、自有资产、授权范围）
- A/B/C/D 任务路由器
- 8 个漏洞推理模板
- 6 类共 60+ 个 benchmark 任务
- 知识质量评分与引用质量评估
- 三类报告：知识覆盖、安全策略、智能体就绪
- React + Vite 前端 dashboard（card / table / pre 块）
- 360+ pytest 测试，GitHub Actions CI

---

## 与 A/B/C/D 的关系

| 项目 | 定位 | 仓库 |
|---|---|---|
| llm-security-lab | AI / RAG 安全评估 | https://github.com/suiyisuixing/llm-security-lab |
| security-log-ai-assistant | 检测工程 / SOC | https://github.com/suiyisuixing/security-log-ai-assistant |
| vulnerability-intelligence-lab | 漏洞情报 / 技能数据集 | https://github.com/suiyisuixing/vulnerability-intelligence-lab |
| **security-knowledge-base** | **知识、安全策略、记忆、路由** | https://github.com/suiyisuixing/security-knowledge-base |

本项目（D）是其他三个项目的知识层、安全策略层、智能体记忆层和任务路由层。

---

## 架构

- `backend/app/` —— FastAPI 服务（23 个模块）
- `knowledge/` —— 带 YAML 元数据的本地 Markdown 知识库
- `data/` —— 安全策略、技能 taxonomy、项目注册表、benchmark、模板
- `memory/` —— 智能体记忆（不含任何敏感数据）
- `frontend/` —— React + Vite dashboard
- `tests/` —— pytest 套件（25 文件，360+ 测试）
- `docs/` —— 架构、威胁模型、安全策略、审阅者指南等
- `reports/` —— 安全报告
- `tools/` —— 本地开发检查脚本
- `.github/workflows/ci.yml` —— 后端测试 + 前端构建

---

## 快速开始

### 创建虚拟环境

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base
py -3.11 -m venv .venv
```

### 安装后端依赖

```cmd
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

### 启动后端

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base\backend
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 安装并启动前端

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base\frontend
npm install --registry=https://registry.npmmirror.com
npm run dev
```

### 运行测试

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe -m pytest
```

### 构建前端

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base\frontend
npm run build
```

### 本地一键检查

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe tools\run_checks.py
```

---

## 安全边界

- 不执行真实扫描
- 不调用真实 LLM API
- 不接入真实外部 API（NVD / CISA / EPSS / GitHub Advisory / OSV）
- 不访问真实目标
- 不进行凭证攻击、武器化漏洞利用、持久化、规避检测、数据外传、破坏性操作、恶意软件

## 开发说明

本项目是一个 AI 辅助学习与工程实践项目。项目架构、安全知识模型、安全策略设计、测试目标、
验证流程和最终审查均由作者主导。AI 工具主要用于规划、文档支持、调试指导和审查辅助，
所有仓库提交和项目决策均由作者管理。

## 局限性

- 仅本地使用，不用于生产部署
- 检索使用简单 TF-IDF，语义检索故意未纳入
- 记忆与报告用于教学展示

## 作品集用途

把本项目作为审阅其他三个项目的知识、安全策略与路由层。按上面的“审阅者快速路径”依次操作即可。
