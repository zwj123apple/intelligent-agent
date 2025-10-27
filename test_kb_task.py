"""
测试知识库任务 - 验证多Agent是否正确保存知识
"""

from multi_agent import MultiAgentSystem
from knowledge_base import KnowledgeBase
import time


def test_knowledge_task():
    """测试构建Python学习知识库的任务"""
    
    print("=" * 70)
    print("🧪 测试：构建Python学习知识库")
    print("=" * 70)
    
    # 创建多Agent系统
    print("\n1️⃣ 初始化多Agent系统...")
    system = MultiAgentSystem()
    
    # 定义任务
    task = """
    请帮我构建Python学习知识库：
    1. 研究Python的核心知识点（基础语法、数据结构、面向对象等）
    2. 分析学习路径和难度层次
    3. 将整理好的知识保存到知识库
    4. 给出学习建议
    
    要求：每个知识点都要用add_knowledge工具保存到知识库
    """
    
    print("\n2️⃣ 执行任务...")
    print("-" * 70)
    
    # 执行任务
    result = system.execute_task(task, verbose=True)
    
    print("\n" + "=" * 70)
    print("✅ 任务执行完成")
    print("=" * 70)
    
    # 等待一下确保文件写入
    time.sleep(1)
    
    # 检查知识库
    print("\n3️⃣ 检查知识库内容...")
    print("-" * 70)
    
    try:
        kb = KnowledgeBase()
        stats = kb.get_statistics()
        
        print(f"\n📊 知识库统计:")
        print(f"  • 文档总数: {stats['total_documents']}")
        print(f"  • 分类数量: {stats['total_categories']}")
        
        if stats['total_documents'] > 0:
            print(f"\n✅ 成功！知识已保存到知识库")
            
            # 显示最近添加的文档
            recent = kb.get_recent_documents(5)
            print(f"\n📝 最近添加的 {len(recent)} 篇文档:")
            for doc in recent:
                title = doc.metadata.get('title', doc.doc_id)
                category = doc.metadata.get('category', '未分类')
                preview = doc.content[:60].replace('\n', ' ')
                print(f"\n  【{category}】{title}")
                print(f"  ID: {doc.doc_id}")
                print(f"  预览: {preview}...")
            
            # 搜索Python相关内容
            print(f"\n🔍 搜索 'Python' 相关内容:")
            search_results = kb.search("Python", limit=3)
            print(f"  找到 {len(search_results)} 条结果")
            
        else:
            print(f"\n⚠️ 知识库仍然为空")
            print("\n可能的原因:")
            print("  1. Agent没有调用add_knowledge工具")
            print("  2. 工具调用失败")
            print("  3. 知识库保存失败")
            
            print("\n💡 建议:")
            print("  • 查看上面的执行日志，确认是否调用了add_knowledge")
            print("  • 手动测试：运行 python main.py")
            print("  • 输入：帮我记住：Python是一门编程语言")
    
    except Exception as e:
        print(f"\n❌ 检查知识库失败: {str(e)}")
        import traceback
        traceback.print_exc()


def manual_add_test():
    """手动添加测试数据"""
    print("\n" + "=" * 70)
    print("🧪 手动添加测试数据到知识库")
    print("=" * 70)
    
    try:
        kb = KnowledgeBase()
        
        # 添加测试文档
        test_docs = [
            {
                "title": "Python基础语法",
                "category": "Python学习",
                "content": """Python基础语法包括：
1. 变量和数据类型
2. 运算符
3. 条件语句（if/elif/else）
4. 循环语句（for/while）
5. 函数定义和调用
""",
                "tags": ["Python", "基础", "语法"]
            },
            {
                "title": "Python数据结构",
                "category": "Python学习",
                "content": """Python常用数据结构：
1. 列表(List) - 可变序列
2. 元组(Tuple) - 不可变序列
3. 字典(Dict) - 键值对映射
4. 集合(Set) - 无序不重复元素集
""",
                "tags": ["Python", "数据结构"]
            },
            {
                "title": "Python学习路径",
                "category": "Python学习",
                "content": """推荐的Python学习路径：
阶段1：基础语法（1-2周）
阶段2：数据结构和算法（2-3周）
阶段3：面向对象编程（1-2周）
阶段4：常用库和框架（持续学习）
阶段5：项目实践（持续）
""",
                "tags": ["Python", "学习路径", "规划"]
            }
        ]
        
        print(f"\n正在添加 {len(test_docs)} 篇测试文档...")
        
        for doc_data in test_docs:
            doc_id = kb.add_document(
                content=doc_data["content"],
                title=doc_data["title"],
                category=doc_data["category"],
                tags=doc_data["tags"]
            )
            print(f"  ✅ 已添加: {doc_data['title']} (ID: {doc_id})")
        
        print(f"\n✅ 成功添加 {len(test_docs)} 篇文档到知识库")
        
        # 显示统计
        stats = kb.get_statistics()
        print(f"\n📊 当前知识库统计:")
        print(f"  • 文档总数: {stats['total_documents']}")
        print(f"  • 分类: {list(stats['categories'].keys())}")
        
    except Exception as e:
        print(f"\n❌ 添加失败: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("\n请选择操作:")
    print("  1. 测试多Agent知识库任务（会调用API）")
    print("  2. 手动添加测试数据（不调用API）")
    print("  3. 查看当前知识库状态")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == '1':
        test_knowledge_task()
    elif choice == '2':
        manual_add_test()
    elif choice == '3':
        from kb_viewer import quick_check
        quick_check()
    else:
        print("无效选择")


if __name__ == "__main__":
    main()