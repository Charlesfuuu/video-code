#!/usr/bin/env python3
"""
ReAct Agent 自动化测试脚本
测试三个核心功能：读文件、写文件、执行终端命令
"""
import subprocess
import sys
import os
from pathlib import Path

# 测试配置
PROJECT_DIR = Path(__file__).parent / "test_project"
AGENT_SCRIPT = Path(__file__).parent / "agent.py"


def run_agent_test(task: str, user_input: str = "y") -> tuple[bool, str]:
    """运行 Agent 并返回结果"""
    try:
        # 使用 echo + uv run 的方式输入任务
        cmd = f'cd "{Path(__file__).parent}" && echo -e "{task}\\n{user_input}" | uv run agent.py test_project'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "测试超时"
    except Exception as e:
        return False, f"测试异常: {str(e)}"


def test_read_file():
    """测试 1: 读取文件"""
    print("\n" + "="*60)
    print("测试 1: 读取文件功能")
    print("="*60)

    # 创建测试文件
    test_file = PROJECT_DIR / "read_test.txt"
    test_file.write_text("这是读取测试文件", encoding="utf-8")

    task = "读取 test_project/read_test.txt 文件的内容"
    success, output = run_agent_test(task)

    if success and "这是读取测试文件" in output:
        print("✅ 读取文件测试通过")
        return True
    else:
        print("❌ 读取文件测试失败")
        print(f"输出: {output}")
        return False


def test_write_file():
    """测试 2: 写入文件"""
    print("\n" + "="*60)
    print("测试 2: 写入文件功能")
    print("="*60)

    task = "在 test_project 目录创建 write_test.txt 文件，内容为：测试写入成功"
    success, output = run_agent_test(task)

    write_file = PROJECT_DIR / "write_test.txt"
    if success and write_file.exists():
        content = write_file.read_text(encoding="utf-8")
        if "测试写入成功" in content:
            print("✅ 写入文件测试通过")
            return True

    print("❌ 写入文件测试失败")
    print(f"输出: {output}")
    return False


def test_terminal_command():
    """测试 3: 执行终端命令"""
    print("\n" + "="*60)
    print("测试 3: 执行终端命令功能")
    print("="*60)

    task = "列出 test_project 目录下的所有文件"
    success, output = run_agent_test(task, user_input="y")

    # 检查是否列出了已知文件
    if success and ("test.txt" in output or "output.txt" in output):
        print("✅ 终端命令测试通过")
        return True
    else:
        print("❌ 终端命令测试失败")
        print(f"输出: {output}")
        return False


def test_complex_task():
    """测试 4: 复杂多步骤任务"""
    print("\n" + "="*60)
    print("测试 4: 复杂多步骤任务")
    print("="*60)

    task = "读取 test_project/test.txt 的内容，将内容全部转为大写后写入 uppercase.txt"
    success, output = run_agent_test(task, user_input="y")

    upper_file = PROJECT_DIR / "uppercase.txt"
    if success and upper_file.exists():
        print("✅ 复杂任务测试通过")
        return True
    else:
        print("❌ 复杂任务测试失败")
        print(f"输出: {output}")
        return False


def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("ReAct Agent 自动化测试")
    print("="*60)

    # 确保测试目录存在
    PROJECT_DIR.mkdir(exist_ok=True)

    # 检查环境
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ 未找到 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)

    # 运行测试
    tests = [
        test_read_file,
        test_write_file,
        test_terminal_command,
        test_complex_task,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ 测试执行异常: {e}")
            results.append(False)

    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("❌ 部分测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
