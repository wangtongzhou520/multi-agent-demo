# MCP Sampling Server

这是一个基于 FastMCP 框架的示例项目，展示了如何将服务和工具分离，并提供数据采样功能。

## 项目结构

```
server/
├── main.py           # 程序入口
├── service.py        # MCP服务类
├── pyproject.toml    # 项目依赖配置
├── uv.lock           # 依赖锁定文件
└── tools/            # 工具模块目录
    ├── __init__.py
    ├── calculator.py # 计算器工具
    ├── sampling.py   # 采样工具
    └── registry.py   # 工具注册器
```

## 架构说明

### 分层设计

1. **服务层 (service.py)**
   - 负责初始化 FastMCP 实例
   - 管理服务的启动和配置

2. **工具层 (tools/)**
   - 包含所有业务工具函数
   - 每个工具模块专注于特定领域
   - 通过 registry.py 统一注册到 MCP 实例

3. **入口层 (main.py)**
   - 程序的入口点
   - 创建服务实例并启动服务

### 优势

- **关注点分离**: 工具逻辑与服务逻辑完全分离
- **易于扩展**: 添加新工具只需在 tools/ 目录下创建相应模块
- **易于维护**: 每个模块职责单一，便于维护和测试
- **可重用性**: 工具函数可以在不同服务中重用

## 工具功能

### 计算器工具
提供基本的数学运算功能：
- 加法 (Addition)
- 减法 (Subtraction)
- 乘法 (Multiplication)
- 除法 (Division)

### 采样工具
提供多种数据采样方法：
- 随机采样 (Random Sample)
- 系统采样 (Systematic Sample)
- 分层采样 (Stratified Sample)

## 运行服务

```bash
python main.py
```

服务将在 `http://127.0.0.1:8001` 上启动，并使用 SSE 传输协议。

## 客户端演示

项目包含一个客户端演示程序，展示了如何使用采样工具：

```bash
# 在另一个终端中运行
python demo_sampling.py
```

演示程序将展示如何调用各种采样工具并查看结果。