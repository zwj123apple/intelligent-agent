"""
多Agent协作系统 - 使用示例
"""

from multi_agent import (
    MultiAgentSystem,
    run_multi_agent_task,
    create_multi_agent_system
)


def example_1_research_and_write():
    """示例1: 研究并撰写报告"""
    print("\n" + "=" * 70)
    print("示例1: 研究并撰写AI技术报告")
    print("=" * 70)
    
    task = """
    请帮我完成以下任务：
    1. 研究当前AI大语言模型的最新进展
    2. 分析其在实际应用中的优势和挑战
    3. 撰写一份简短的技术报告
    """
    
    result = run_multi_agent_task(task, verbose=True)
    
    print("\n✅ 示例1完成")
    return result


def example_2_code_review():
    """示例2: 代码开发和评审"""
    print("\n" + "=" * 70)
    print("示例2: Python爬虫代码开发")
    print("=" * 70)
    
    task = """
    请帮我：
    1. 设计一个Python网页爬虫的方案
    2. 编写关键代码片段
    3. 进行代码质量评审
    4. 给出使用文档
    """
    
    system = create_multi_agent_system()
    result = system.execute_task(task, verbose=True)
    
    print("\n✅ 示例2完成")
    return result


def example_3_data_analysis():
    """示例3: 数据分析项目"""
    print("\n" + "=" * 70)
    print("示例3: 用户行为数据分析")
    print("=" * 70)
    
    task = """
    假设我们有一份用户行为数据，请：
    1. 设计数据分析的方案
    2. 说明需要关注的关键指标
    3. 提供分析代码示例
    4. 总结可能的洞察和建议
    """
    
    system = create_multi_agent_system()
    result = system.execute_task(task, verbose=True)
    
    print("\n✅ 示例3完成")
    return result


def example_4_knowledge_management():
    """示例4: 知识管理任务"""
    print("\n" + "=" * 70)
    print("示例4: 构建个人学习知识库")
    print("=" * 70)
    
    task = """
    我想建立一个Python学习的知识库，请帮我：
    1. 研究Python学习的关键主题
    2. 分析学习路径和难度分布
    3. 整理成结构化的知识框架
    4. 将框架保存到知识库
    5. 给出学习建议
    """
    
    system = create_multi_agent_system()
    result = system.execute_task(task, verbose=True)
    
    # 显示系统状态
    system.show_status()
    
    print("\n✅ 示例4完成")
    return result


def example_5_simple_task():
    """示例5: 简单任务演示"""
    print("\n" + "=" * 70)
    print("示例5: 简单的信息查询和总结")
    print("=" * 70)
    
    task = "请帮我查询并总结机器学习的基本概念"
    
    system = create_multi_agent_system()
    result = system.execute_task(task, verbose=True)
    
    print("\n✅ 示例5完成")
    return result


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 70)
    print("🎮 多Agent协作系统 - 交互模式")
    print("=" * 70)
    print("\n提示: 输入复杂任务让多个Agent协作完成")
    print("     输入 'status' 查看系统状态")
    print("     输入 'exit' 退出\n")
    
    system = create_multi_agent_system()
    
    while True:
        try:
            user_input = input("💬 请输入任务: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("\n👋 退出交互模式")
                break
            
            if user_input.lower() == 'status':
                system.show_status()
                continue
            
            # 执行任务
            result = system.execute_task(user_input, verbose=True)
            
            print(f"\n{'='*70}")
            print("✨ 任务执行完成")
            print(f"{'='*70}\n")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ 检测到中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")


def demo_agent_communication():
    """演示Agent间通信"""
    print("\n" + "=" * 70)
    print("📡 Agent通信演示")
    print("=" * 70)
    
    from multi_agent import ResearcherAgent, WriterAgent, AgentMessage
    
    # 创建Agent
    researcher = ResearcherAgent("研究员A")
    writer = WriterAgent("写作者B")
    
    # 研究员发送消息
    print("\n1️⃣ 研究员收集信息...")
    research_message = AgentMessage(
        sender="coordinator",
        receiver="researcher",
        content="请搜集关于Python装饰器的信息"
    )
    
    research_result = researcher.process_message(research_message)
    print(f"✅ 研究结果: {research_result[:200]}...\n")
    
    # 写作者基于研究结果创作
    print("2️⃣ 写作者撰写文章...")
    write_message = AgentMessage(
        sender="researcher",
        receiver="writer",
        content=f"基于以下信息撰写一篇教程:\n{research_result}"
    )
    
    write_result = writer.process_message(write_message)
    print(f"✅ 写作结果: {write_result[:200]}...\n")
    
    # 显示Agent状态
    print("📊 Agent状态:")
    print(f"  研究员: 已处理 {len(researcher.message_history)} 条消息")
    print(f"  写作者: 已处理 {len(writer.message_history)} 条消息")


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "=" * 70)
    print("🚀 多Agent协作系统 - 示例集合")
    print("=" * 70)
    
    examples = {
        "1": ("研究并撰写报告", example_1_research_and_write),
        "2": ("代码开发和评审", example_2_code_review),
        "3": ("数据分析项目", example_3_data_analysis),
        "4": ("知识管理任务", example_4_knowledge_management),
        "5": ("简单任务演示", example_5_simple_task),
        "6": ("Agent通信演示", demo_agent_communication),
        "7": ("交互模式", interactive_mode),
    }
    
    print("\n请选择示例:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  0. 运行所有示例")
    print("  q. 退出")
    
    choice = input("\n请输入选项: ").strip()
    
    if choice == 'q':
        print("👋 再见！")
        return
    
    if choice == '0':
        # 运行所有示例
        for key, (name, func) in examples.items():
            if key != '7':  # 跳过交互模式
                try:
                    func()
                    input("\n按Enter继续...")
                except Exception as e:
                    print(f"\n❌ 示例执行失败: {str(e)}")
    elif choice in examples:
        # 运行选定的示例
        name, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"\n❌ 示例执行失败: {str(e)}")
    else:
        print("❌ 无效的选项")


if __name__ == "__main__":
    main()