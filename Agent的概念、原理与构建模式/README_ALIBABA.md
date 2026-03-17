# ReAct Agent 项目 - 阿里云百炼版本

## 项目简介

这是一个基于 ReAct (Reasoning + Acting) 模式构建的智能 Agent，已适配阿里云百炼 API。

## 主要修改

### 1. API 配置修改
- **原版本**: 使用 OpenRouter API (`https://openrouter.ai/api/v1`)
- **当前版本**: 使用阿里云百炼 API (`https://dashscope.aliyuncs.com/compatible-mode/v1`)

### 2. 模型切换
- **原版本**: `openai/gpt-4o`
- **当前版本**: `qwen-plus` (阿里云百炼)

### 3. 环境变量支持
优先级顺序：
1. `DASHSCOPE_API_KEY` (阿里云百炼)
2. `OPENROUTER_API_KEY` (OpenRouter，兜底)

### 4. Bug 修复
修复了 `run_terminal_command` 函数返回值问题：
- **原实现**: 只返回 "执行成功" 或错误信息
- **修复后**: 返回实际命令输出 (stdout) 或错误信息

## 功能特性

Agent 支持三个核心工具：

1. **read_file(file_path)** - 读取文件内容
2. **write_to_file(file_path, content)** - 写入文件
3. **run_terminal_command(command)** - 执行终端命令

## 安装依赖

确保已安装 `uv` 包管理器：
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或通过 pip
pip install uv
```

## 环境配置

确保环境变量中已配置阿里云百炼 API Key：
```bash
export DASHSCOPE_API_KEY=sk-xxxxxxxxxx
```

或创建 `.env` 文件：
```
DASHSCOPE_API_KEY=sk-xxxxxxxxxx
```

## 使用方法

### 基本使用
```bash
# 进入项目目录
cd "/Users/fushenlin/Videocode/Agent的概念、原理与构建模式"

# 运行 Agent (需要指定一个项目目录)
uv run agent.py <project_directory>

# 示例
uv run agent.py test_project
```

### 任务示例

启动后会提示输入任务，支持的任务类型：

1. **文件读取**
   ```
   请输入任务：读取 test_project 目录下的 test.txt 文件内容
   ```

2. **文件写入**
   ```
   请输入任务：在 test_project 目录创建 output.txt，内容为：Hello World
   ```

3. **终端命令**
   ```
   请输入任务：列出 test_project 目录下的所有文件
   ```
   注意：执行终端命令时会询问确认 (Y/N)

4. **复杂任务** (多步骤推理)
   ```
   请输入任务：读取 test_project 下所有 txt 文件，统计总字数，写入 summary.txt
   ```

## 自动化测试

项目包含完整的自动化测试脚本：

```bash
python3 test_agent.py
```

测试覆盖：
- ✅ 文件读取功能
- ✅ 文件写入功能
- ✅ 终端命令执行
- ✅ 复杂多步骤任务

## ReAct 工作原理

Agent 使用 Thought → Action → Observation 循环：

1. **Thought** (思考): 分析当前情况，规划下一步
2. **Action** (行动): 调用工具执行操作
3. **Observation** (观察): 获取工具返回结果
4. **Final Answer** (最终答案): 任务完成，给出答案

示例流程：
```
💭 Thought: 我需要读取文件内容
🔧 Action: read_file(/path/to/file.txt)
🔍 Observation: 文件内容是...
💭 Thought: 已获取内容，可以给出答案
✅ Final Answer: 文件内容是...
```

## 依赖项

- Python >= 3.12
- click >= 8.2.1
- openai >= 1.91.0
- python-dotenv >= 1.1.1

## 测试结果

```
通过: 4/4
✅ 所有测试通过！
```

## 注意事项

1. 终端命令执行需要用户手动确认 (输入 Y 继续)
2. 文件路径建议使用绝对路径
3. 多行内容在 Action 中用 `\n` 表示
4. Agent 具有自主推理能力，会自动拆解复杂任务

## 项目结构

```
.
├── agent.py              # 主程序 (ReAct Agent 实现)
├── prompt_template.py    # 系统提示词模板
├── test_agent.py         # 自动化测试脚本
├── pyproject.toml        # 项目配置
├── README.md             # 本文档
└── test_project/         # 测试目录
    ├── test.txt
    ├── output.txt
    └── summary.txt
```

## 许可证

按原项目许可证执行
