"""
主程序 - 智能Agent交互界面
"""

import sys
from agent import QwenAgent
from config import print_config


def print_welcome():
    """打印欢迎信息"""
    print("=" * 70)
    print("🚀 通义千问智能Agent系统".center(70))
    print("=" * 70)
    print("\n✨ 功能特性:")
    print("  ✓ 流式响应 - 实时输出对话内容")
    print("  ✓ 对话记忆 - 智能管理上下文")
    print("  ✓ 工具调用 - 支持11种实用工具")
    print("  ✓ API集成 - 支持真实API调用")
    print("\n🔧 可用工具:")
    tools = [
        ("get_current_time", "获取当前时间"),
        ("calculate", "数学计算"),
        ("search_weather", "查询天气"),
        ("search_web", "网络搜索"),
        ("translate_text", "文本翻译"),
        ("analyze_sentiment", "情感分析"),
        ("save_note", "保存笔记"),
        ("read_file", "读取文件"),
        ("get_file_info", "文件信息"),
        ("create_todo", "创建待办"),
        ("set_reminder", "设置提醒")
    ]
    
    for i, (name, desc) in enumerate(tools, 1):
        print(f"  {i:2d}. {name:20s} - {desc}")
    
    print("\n💡 命令列表:")
    commands = [
        ("help", "查看帮助和使用示例"),
        ("memory", "查看记忆统计"),
        ("search <关键词>", "搜索记忆"),
        ("clear", "清空短期记忆"),
        ("export", "导出记忆到文件"),
        ("config", "显示配置信息"),
        ("exit/quit", "退出程序")
    ]
    
    for cmd, desc in commands:
        print(f"  • {cmd:20s} - {desc}")
    
    print("=" * 70)


def print_help():
    """打印帮助信息"""
    print("\n📖 使用示例:")
    examples = [
        ("基础对话", "你好，今天天气怎么样？"),
        ("获取时间", "现在几点了？"),
        ("数学计算", "帮我计算 (123 + 456) * 789"),
        ("天气查询", "北京今天天气如何？"),
        ("网络搜索", "搜索最新的AI新闻"),
        ("文本翻译", "把'你好世界'翻译成英语"),
        ("情感分析", "分析情感：今天真是美好的一天！"),
        ("保存笔记", "帮我记住：明天下午3点开会"),
        ("创建待办", "创建高优先级待办：完成项目报告"),
        ("设置提醒", "提醒我明天下午3点开会"),
        ("文件操作", "读取notes.txt文件内容"),
    ]
    
    for category, example in examples:
        print(f"\n  【{category}】")
        print(f"  💬 {example}")


def handle_command(agent: QwenAgent, user_input: str) -> bool:
    """
    处理系统命令
    
    Returns:
        True if should continue, False if should exit
    """
    command = user_input.lower().strip()
    
    # 退出命令
    if command in ["exit", "quit", "退出"]:
        agent.save_memory()
        print("\n👋 再见！记忆已保存。")
        return False
    
    # 帮助命令
    if command == "help":
        print_help()
        return True
    
    # 记忆统计
    if command == "memory":
        agent.show_memory_stats()
        return True
    
    # 搜索记忆
    if command.startswith("search "):
        keyword = command.replace("search ", "").strip()
        if keyword:
            agent.search_memory(keyword)
        else:
            print("⚠️ 请提供搜索关键词")
        return True
    
    # 清空记忆
    if command == "clear":
        agent.clear_memory("short")
        return True
    
    if command == "clear all":
        confirm = input("⚠️ 确定要清空所有记忆吗？(yes/no): ")
        if confirm.lower() in ["yes", "y"]:
            agent.clear_memory("all")
        return True
    
    # 导出记忆
    if command == "export":
        agent.export_memory()
        return True
    
    # 显示配置
    if command == "config":
        print_config()
        return True
    
    # 不是命令，返回None表示需要作为对话处理
    return None


def main():
    """主函数"""
    # 打印欢迎信息
    print_welcome()
    
    # 初始化Agent
    try:
        agent = QwenAgent()
    except Exception as e:
        print(f"\n❌ Agent初始化失败: {str(e)}")
        print("请检查配置文件中的API密钥是否正确")
        sys.exit(1)
    
    # 主循环
    print("\n💬 开始对话... (输入 'help' 查看帮助，'exit' 退出)\n")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("💬 你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            result = handle_command(agent, user_input)
            
            # 如果是退出命令
            if result is False:
                break
            
            # 如果是其他命令
            if result is True:
                continue
            
            # 否则作为对话处理
            agent.chat_stream(user_input)
            
        except KeyboardInterrupt:
            print("\n\n⚠️ 检测到中断信号...")
            agent.save_memory()
            print("👋 再见！记忆已保存。")
            break
            
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()