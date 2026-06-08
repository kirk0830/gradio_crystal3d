# Gradio Crystal3D 组件文件结构整理计划

## 概述

将当前项目按照 Gradio 自定义组件的标准规范进行整理，修复配置问题，确保测试通过，创建 README.md，并初始化 Git 仓库推送到远程。

## 可执行文件环境

- conda环境：gradio_crystal3d
- 使用npm时，需要首先将目录`/home/huangyike/soft/node-v18.19.0-linux-x64/bin`添加到PATH，从而可以使用`npm`, `node`等命令
- Python的可执行文件需要参考conda环境来设置，即`/home/huangyike/anaconda3/envs/gradio_crystal3d/bin/python`

## 当前状态分析

### 当前文件结构
```
gradio_crystal3d/
├── backend/
│   └── gradio_crystal3d/
│       ├── __pycache__/
│       ├── templates/
│       ├── crystal3d.py
│       ├── crystal3d.pyi
│       └── __init__.py         ← 导入语句有问题（绝对导入）
├── demo/
│   ├── app.py
│   ├── css.css
│   ├── __init__.py
│   └── space.py
├── dist/                       ← 构建产物，应保留但不应提交
│   ├── gradio_crystal3d-0.0.1-py3-none-any.whl
│   └── gradio_crystal3d-0.0.1.tar.gz
├── examples/                   ← 可合并到 demo/ 或保留
│   ├── example_crystal3d.py
│   └── Si_mp-149.cif
├── frontend/
│   ├── node_modules/           ← 应被 .gitignore 忽略
│   ├── Example.svelte
│   ├── gradio.config.js
│   ├── Index.svelte
│   ├── package.json
│   └── package-lock.json
├── tests/
│   ├── __pycache__/
│   ├── test_component.py
│   └── test_crystal3d.py
├── AGENT.md                    ← 用户特定文档，保留
├── .gitignore                  ← 已存在，需要检查完整性
├── package-lock.json           ← 根目录多余文件，应删除
└── pyproject.toml              ← 配置基本正确
```

### 发现的问题

1. **导入错误**：`backend/gradio_crystal3d/__init__.py` 使用绝对导入 `from gradio_crystal3d.crystal3d import ...`，应改为相对导入 `from .crystal3d import ...`

2. **多余文件**：根目录的 `package-lock.json` 是多余的（前端目录已有）

3. **examples/ 目录**：Gradio 标准结构只有 `demo/` 目录，但保留 `examples/` 作为额外示例也是合理的

4. **README.md**：当前不存在，需要创建

### Gradio 自定义组件标准结构（参考）

```
component_name/
├── frontend/
│   ├── Index.svelte
│   ├── Example.svelte
│   ├── package.json
│   ├── package-lock.json
│   └── gradio.config.js
├── backend/
│   └── gradio_<component_name>/
│       ├── __init__.py
│       └── component.py
│       └── templates/          ← 前端构建产物
├── demo/
│   ├── app.py
│   └── requirements.txt        ← 可选
├── dist/                       ← 构建产物
├── pyproject.toml
├── README.md                   ← 自动生成或手动编写
└── .gitignore
```

## 提议的修改

### 1. 修复导入问题

**文件**：`backend/gradio_crystal3d/__init__.py`

**当前代码**：
```python
from gradio_crystal3d.crystal3d import Crystal3D, create_crystal3d_viewer
```

**修改为**：
```python
from .crystal3d import Crystal3D, create_crystal3d_viewer
```

**原因**：相对导入是 Python 包的标准做法，避免模块名冲突和导入错误。

### 2. 清理多余文件

**删除**：根目录的 `package-lock.json`

**原因**：前端目录已有 `frontend/package-lock.json`，根目录的是多余的。

### 3. 整理 examples/ 目录

**方案**：保留 `examples/` 目录，但将示例 CIF 文件复制到 `demo/` 目录

- 将 `examples/Si_mp-149.cif` 复制到 `demo/Si_mp-149.cif`
- 保留 `examples/example_crystal3d.py` 作为更完整的示例
- 更新 `demo/app.py` 使用 `demo/Si_mp-149.cif` 作为默认示例

**原因**：Gradio 标准结构中 `demo/` 是开发时使用的示例应用，`examples/` 可以作为面向用户的完整示例。

### 4. 更新 .gitignore

**添加内容**：
```gitignore
# Build artifacts (keep dist/ for pip install)
dist/*.whl
dist/*.tar.gz

# Test cache
tests/__pycache__/

# Root package-lock.json (frontend has its own)
/package-lock.json
```

### 5. 创建 README.md

**内容结构**：
1. 项目简介
   - 声明基于 3Dmol.js 通过 vibe coding 实现
   - 功能特性
2. 安装步骤
   - 从源码安装
   - 从 PyPI 安装（未来）
3. 使用方式
   - 快速示例
   - API 参考
4. 开发指南
   - 本地开发
   - 构建和发布
5. 许可证

### 6. 更新 pyproject.toml

**检查并确认**：
- `readme = "README.md"` 指向正确
- 项目 URLs 正确
- 依赖项完整

### 7. Git 初始化和推送

**步骤**：
1. `git init`
2. `git remote add origin https://github.com/kirk0830/gradio_crystal3d.git`
3. `git add .`
4. `git commit -m "Initial commit: Gradio Crystal3D component"`
5. `git push -f origin main` (force push 覆盖远程仓库)

## 假设与决策

### 假设
1. 用户希望保留 `AGENT.md` 作为项目特定的开发规范文档
2. `examples/` 目录作为面向用户的完整示例保留
3. 远程仓库 `https://github.com/kirk0830/gradio_crystal3d` 已创建但内容需要覆盖
4. 项目使用 GPL-3.0 许可证（已在 pyproject.toml 中声明）

### 决策
1. **保留 examples/ 目录**：作为更完整的用户示例，与 demo/ 区分
2. **复制 CIF 文件到 demo/**：让 demo 应用有默认示例文件可用
3. **使用 force push**：用户明确要求覆盖远程仓库内容
4. **不删除 dist/ 目录**：保留构建产物供 pip install 使用，但通过 .gitignore 不提交

## 验证步骤

### 1. 测试验证

运行单元测试确保导入修复后功能正常：
```bash
/home/huangyike/.conda/envs/gradio_crystal3d/bin/python -m unittest tests/test_component.py
```

预期结果：18 个测试全部通过

### 2. 构建验证

运行 Gradio 构建命令确保组件可以正确构建：
```bash
gradio cc build
```

预期结果：生成新的 `.whl` 和 `.tar.gz` 文件

### 3. Git 验证

检查 Git 状态确保所有必要文件已添加：
```bash
git status
git log --oneline -1
```

预期结果：所有源码文件已提交，构建产物和缓存文件已忽略

## 执行顺序

1. 修复 `backend/gradio_crystal3d/__init__.py` 导入问题
2. 删除根目录 `package-lock.json`
3. 复制 `examples/Si_mp-149.cif` 到 `demo/`
4. 更新 `demo/app.py` 使用默认示例
5. 更新 `.gitignore`
6. 创建 `README.md`
7. 运行测试验证
8. Git 初始化和推送
