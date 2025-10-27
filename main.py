"""
主程序 - 智能Agent系统（集成多Agent协作）
"""

import sys
from agent import QwenAgent
from multi_agent import MultiAgentSystem, run_multi_agent_task
from config import print_config


def print_welcome():
    """打印欢迎信息"""
    print("=" * 70)
    print("🚀 通义千问智能Agent系统 v2.0".center(70))
    print("=" * 70)
    print("\n✨ 功能特性:")
    print("  ✓ 单Agent模式 - 个人助手，快速响应")
    print("  ✓ 多Agent模式 - 团队协作，处理复杂任务")
    print("  ✓ 流式响应 - 实时输出对话内容")
    print("  ✓ 对话记忆 - 智能管理上下文")
    print("  ✓ 工具调用 - 支持19种实用工具")
    print("  ✓ 知识库 - 个人知识管理系统")
    print("\n🤖 Agent模式:")
    print("  1️⃣  单Agent模式 - 适合日常对话和简单任务")
    print("  2️⃣  多Agent模式 - 适合复杂任务和深度分析")
    print("\n💡 命令列表:")
    commands = [
        ("help", "查看帮助和使用示例"),
        ("mode <single|multi>", "切换Agent模式"),
        ("memory", "查看记忆统计（单Agent）"),
        ("status", "查看系统状态（多Agent）"),
        ("search <关键词>", "搜索记忆"),
        ("clear", "清空短期记忆"),
        ("export", "导出记忆到文件"),
        ("config", "显示配置信息"),
        ("examples", "查看多Agent示例"),
        ("exit/quit", "退出程序")
    ]
    
    for cmd, desc in commands:
        print(f"  • {cmd:25s} - {desc}")
    
    print("=" * 70)


def print_help():
    """打印帮助信息"""
    print("\n📖 使用指南:")
    
    print("\n【单Agent模式】- 快速响应")
    examples = [
        ("基础对话", "你好，今天天气怎么样？"),
        ("获取时间", "现在几点了？"),
        ("数学计算", "帮我计算 (123 + 456) * 789"),
        ("知识搜索", "在知识库中搜索Python相关内容"),
        ("添加知识", "帮我记住：Python装饰器是一种设计模式"),
    ]
    
    for category, example in examples:
        print(f"\n  【{category}】")
        print(f"  💬 {example}")
    
    print("\n【多Agent模式】- 复杂任务")
    examples = [
        ("研究报告", "研究AI大模型并撰写技术报告"),
        ("代码开发", "设计并实现一个Python爬虫"),
        ("数据分析", "分析用户增长趋势并提出建议"),
        ("知识整理", "整理机器学习的学习路径"),
    ]
    
    for category, example in examples:
        print(f"\n  【{category}】")
        print(f"  💬 {example}")


def handle_command(agent: QwenAgent, 
                   multi_agent_system: MultiAgentSystem,
                   user_input: str, 
                   current_mode: str) -> tuple:
    """
    处理系统命令
    
    Returns:
        (continue_flag, new_mode): continue_flag为False表示退出，new_mode为新模式
    """
    command = user_input.lower().strip()
    
    # 退出命令
    if command in ["exit", "quit", "退出"]:
        if current_mode == "single":
            agent.save_memory()
        print("\n👋 再见！")
        return False, current_mode
    
    # 帮助命令
    if command == "help":
        print_help()
        return True, current_mode
    
    # 切换模式
    if command.startswith("mode "):
        new_mode = command.replace("mode ", "").strip()
        if new_mode in ["single", "multi"]:
            print(f"\n✅ 已切换到 {new_mode.upper()} 模式")
            if new_mode == "single":
                print("   → 单Agent模式：快速响应，适合日常对话")
            else:
                print("   → 多Agent模式：团队协作，适合复杂任务")
            return True, new_mode
        else:
            print("⚠️ 无效模式，请使用 'single' 或 'multi'")
        return True, current_mode
    
    # 单Agent专用命令
    if current_mode == "single":
        if command == "memory":
            agent.show_memory_stats()
            return True, current_mode
        
        if command.startswith("search "):
            keyword = command.replace("search ", "").strip()
            if keyword:
                agent.search_memory(keyword)
            else:
                print("⚠️ 请提供搜索关键词")
            return True, current_mode
        
        if command == "clear":
            agent.clear_memory("short")
            return True, current_mode
        
        if command == "export":
            agent.export_memory()
            return True, current_mode
    
    # 多Agent专用命令
    if current_mode == "multi":
        if command == "status":
            multi_agent_system.show_status()
            return True, current_mode
        
        if command == "examples":
            show_multi_agent_examples()
            return True, current_mode
    
    # 通用命令
    if command == "config":
        print_config()
        return True, current_mode
    
    # 不是命令，返回None表示需要作为对话处理
    return None, current_mode


def show_multi_agent_examples():
    """显示多Agent示例"""
    print("\n📚 多Agent协作示例:\n")
    
    examples = [
        {
            "name": "研究报告",
            "task": "研究当前AI大语言模型的发展趋势，分析应用场景，撰写技术报告",
            "agents": "研究员 → 分析师 → 写作者 → 评审者"
        },
        {
            "name": "代码开发",
            "task": "设计一个网页爬虫方案，编写核心代码，进行代码审查",
            "agents": "研究员 → 程序员 → 评审者 → 写作者"
        },
        {
            "name": "数据分析",
            "task": "分析用户行为数据，识别关键指标，提出增长建议",
            "agents": "研究员 → 分析师 → 写作者"
        },
        {
            "name": "知识管理",
            "task": "构建Python学习知识库，整理学习路径，保存到知识库",
            "agents": "研究员 → 分析师 → 写作者"
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"{i}. 【{ex['name']}】")
        print(f"   任务: {ex['task']}")
        print(f"   流程: {ex['agents']}\n")


def single_agent_mode(agent: QwenAgent):
    """单Agent模式"""
    print("\n🤖 单Agent模式已激活")
    print("   → 适合：日常对话、简单任务、快速响应")
    print("   → 提示：输入 'mode multi' 切换到多Agent模式\n")
    
    while True:
        try:
            user_input = input("💬 你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            result, new_mode = handle_command(agent, None, user_input, "single")
            
            if result is False:
                break
            
            if result is True:
                continue
            
            if new_mode == "multi":
                return "multi"
            
            # 普通对话
            agent.chat_stream(user_input)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ 检测到中断")
            agent.save_memory()
            break
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
    
    return None


def multi_agent_mode(multi_system: MultiAgentSystem):
    """多Agent模式"""
    print("\n👥 多Agent模式已激活")
    print("   → 适合：复杂任务、深度分析、团队协作")
    print("   → 提示：输入 'mode single' 切换到单Agent模式")
    print("   → 提示：输入 'examples' 查看示例\n")
    
    while True:
        try:
            user_input = input("💬 任务: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            result, new_mode = handle_command(None, multi_system, user_input, "multi")
            
            if result is False:
                break
            
            if result is True:
                continue
            
            if new_mode == "single":
                return "single"
            
            # 执行多Agent任务
            multi_system.execute_task(user_input, verbose=True)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ 检测到中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return None


def main():
    """主函数"""
    # 打印欢迎信息
    print_welcome()
    
    # 初始化系统
    try:
        print("\n🔧 正在初始化系统...\n")
        
        # 单Agent
        single_agent = QwenAgent()
        
        # 多Agent系统
        multi_system = MultiAgentSystem()
        
        print("\n✅ 系统初始化完成！\n")
    
    except Exception as e:
        print(f"\n❌ 系统初始化失败: {str(e)}")
        print("请检查配置文件中的API密钥是否正确")
        sys.exit(1)
    
    # 选择模式
    print("请选择工作模式:")
    print("  1. 单Agent模式 (默认)")
    print("  2. 多Agent模式")
    
    choice = input("\n请选择 (1/2，直接回车默认为1): ").strip() or "1"
    
    current_mode = "single" if choice == "1" else "multi"
    
    print(f"\n{'='*70}")
    
    # 主循环
    while True:
        if current_mode == "single":
            result = single_agent_mode(single_agent)
            if result == "multi":
                current_mode = "multi"
                continue
            else:
                break
        else:
            result = multi_agent_mode(multi_system)
            if result == "single":
                current_mode = "single"
                continue
            else:
                break
    
    # 退出前保存
    if current_mode == "single":
        single_agent.save_memory()
    
    print("\n👋 感谢使用！")


if __name__ == "__main__":
    main()