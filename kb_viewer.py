"""
知识库查看工具 - 方便查看和管理知识库内容
"""

import json
import os
from pathlib import Path
from datetime import datetime
from knowledge_base import KnowledgeBase


def check_kb_exists():
    """检查知识库是否存在"""
    kb_file = Path("data/knowledge_base/knowledge_base.json")
    
    if not kb_file.exists():
        print("❌ 知识库文件不存在")
        print(f"   预期位置: {kb_file.absolute()}")
        print("\n💡 提示：知识库会在首次添加知识时自动创建")
        return False
    
    print(f"✅ 知识库文件存在: {kb_file.absolute()}")
    
    # 显示文件信息
    size = kb_file.stat().st_size
    mtime = datetime.fromtimestamp(kb_file.stat().st_mtime)
    
    if size < 1024:
        size_str = f"{size} B"
    else:
        size_str = f"{size / 1024:.2f} KB"
    
    print(f"   文件大小: {size_str}")
    print(f"   最后更新: {mtime}")
    
    return True


def view_kb_summary():
    """查看知识库摘要"""
    print("\n" + "=" * 70)
    print("📊 知识库摘要")
    print("=" * 70)
    
    try:
        kb = KnowledgeBase()
        stats = kb.get_statistics()
        
        print(f"\n📄 文档总数: {stats['total_documents']}")
        print(f"📁 分类数量: {stats['total_categories']}")
        print(f"🧠 实体数量: {stats['total_entities']}")
        print(f"🔗 关系数量: {stats['total_relationships']}")
        print(f"📇 索引词数: {stats['total_index_words']}")
        
        # 显示分类详情
        if stats['categories']:
            print("\n📚 分类详情:")
            for category, count in sorted(
                stats['categories'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"  • {category}: {count} 篇")
        
        # 显示热门标签
        popular_tags = kb.get_popular_tags(10)
        if popular_tags:
            print("\n🏷️ 热门标签:")
            for tag, count in popular_tags:
                print(f"  • {tag}: {count}")
        
        return kb
    
    except Exception as e:
        print(f"\n❌ 加载知识库失败: {str(e)}")
        return None


def view_all_documents(kb: KnowledgeBase):
    """查看所有文档列表"""
    print("\n" + "=" * 70)
    print("📄 所有文档")
    print("=" * 70)
    
    if not kb.documents:
        print("\n⚠️ 知识库为空，还没有添加任何文档")
        return
    
    # 按创建时间排序
    docs_sorted = sorted(
        kb.documents.values(),
        key=lambda x: x.created_at,
        reverse=True
    )
    
    print(f"\n共 {len(docs_sorted)} 篇文档:\n")
    
    for i, doc in enumerate(docs_sorted, 1):
        title = doc.metadata.get('title', f'文档_{doc.doc_id}')
        category = doc.metadata.get('category', '未分类')
        created = doc.created_at[:19]  # 只显示日期和时间
        preview = doc.content[:80].replace('\n', ' ')
        
        print(f"{i}. [{category}] {title}")
        print(f"   ID: {doc.doc_id}")
        print(f"   创建: {created}")
        if doc.tags:
            print(f"   标签: {', '.join(doc.tags)}")
        print(f"   预览: {preview}...")
        print()


def view_document_detail(kb: KnowledgeBase, doc_id: str):
    """查看文档详情"""
    doc = kb.get_document(doc_id)
    
    if not doc:
        print(f"\n❌ 未找到ID为 {doc_id} 的文档")
        return
    
    print("\n" + "=" * 70)
    print("📄 文档详情")
    print("=" * 70)
    
    title = doc.metadata.get('title', '无标题')
    category = doc.metadata.get('category', '未分类')
    
    print(f"\n标题: {title}")
    print(f"ID: {doc.doc_id}")
    print(f"分类: {category}")
    print(f"创建时间: {doc.created_at}")
    print(f"更新时间: {doc.updated_at}")
    
    if doc.tags:
        print(f"标签: {', '.join(doc.tags)}")
    
    if doc.metadata.get('source'):
        print(f"来源: {doc.metadata['source']}")
    
    print(f"\n{'=' * 70}")
    print("内容:")
    print("=" * 70)
    print(doc.content)
    print()


def view_by_category(kb: KnowledgeBase, category: str = None):
    """按分类查看文档"""
    if category is None:
        # 显示所有分类
        print("\n" + "=" * 70)
        print("📁 按分类查看")
        print("=" * 70)
        
        if not kb.categories:
            print("\n⚠️ 还没有任何分类")
            return
        
        for cat, doc_ids in kb.categories.items():
            print(f"\n📂 {cat} ({len(doc_ids)} 篇)")
            
            for doc_id in doc_ids[:5]:  # 最多显示5篇
                doc = kb.get_document(doc_id)
                if doc:
                    title = doc.metadata.get('title', doc_id)
                    print(f"  • {title}")
            
            if len(doc_ids) > 5:
                print(f"  ... 还有 {len(doc_ids) - 5} 篇")
    else:
        # 显示特定分类
        doc_ids = kb.categories.get(category, [])
        
        if not doc_ids:
            print(f"\n⚠️ 分类 '{category}' 中没有文档")
            return
        
        print(f"\n📂 {category} ({len(doc_ids)} 篇)\n")
        
        for doc_id in doc_ids:
            doc = kb.get_document(doc_id)
            if doc:
                title = doc.metadata.get('title', doc_id)
                preview = doc.content[:60].replace('\n', ' ')
                print(f"• {title}")
                print(f"  {preview}...")
                print()


def search_in_kb(kb: KnowledgeBase, query: str):
    """在知识库中搜索"""
    print(f"\n🔍 搜索: '{query}'")
    print("=" * 70)
    
    results = kb.search(query, limit=10)
    
    if not results:
        print("\n⚠️ 未找到相关内容")
        return
    
    print(f"\n找到 {len(results)} 条结果:\n")
    
    for i, doc in enumerate(results, 1):
        title = doc.metadata.get('title', f'文档_{doc.doc_id}')
        category = doc.metadata.get('category', '未分类')
        preview = doc.content[:100].replace('\n', ' ')
        
        print(f"{i}. [{category}] {title}")
        print(f"   ID: {doc.doc_id}")
        print(f"   {preview}...")
        print()


def export_kb_readable(kb: KnowledgeBase):
    """导出为易读的Markdown格式"""
    output_file = f"knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    kb.export_to_markdown(output_file)
    
    print(f"\n✅ 知识库已导出到: {output_file}")
    print(f"   文件位置: {Path(output_file).absolute()}")


def interactive_viewer():
    """交互式查看器"""
    print("\n" + "=" * 70)
    print("🔍 知识库交互式查看器")
    print("=" * 70)
    
    # 检查知识库
    if not check_kb_exists():
        return
    
    # 加载知识库
    kb = view_kb_summary()
    
    if kb is None:
        return
    
    while True:
        print("\n" + "-" * 70)
        print("选项:")
        print("  1. 查看所有文档")
        print("  2. 按分类查看")
        print("  3. 搜索文档")
        print("  4. 查看文档详情")
        print("  5. 导出知识库")
        print("  6. 刷新统计")
        print("  0. 退出")
        print("-" * 70)
        
        choice = input("\n请选择 (0-6): ").strip()
        
        if choice == '0':
            print("\n👋 退出查看器")
            break
        
        elif choice == '1':
            view_all_documents(kb)
        
        elif choice == '2':
            category = input("\n输入分类名称（留空显示所有）: ").strip()
            if category:
                view_by_category(kb, category)
            else:
                view_by_category(kb)
        
        elif choice == '3':
            query = input("\n输入搜索关键词: ").strip()
            if query:
                search_in_kb(kb, query)
        
        elif choice == '4':
            doc_id = input("\n输入文档ID: ").strip()
            if doc_id:
                view_document_detail(kb, doc_id)
        
        elif choice == '5':
            export_kb_readable(kb)
        
        elif choice == '6':
            kb = view_kb_summary()
        
        else:
            print("\n⚠️ 无效选项")
        
        input("\n按Enter继续...")


def quick_check():
    """快速检查知识库状态"""
    print("\n" + "=" * 70)
    print("🚀 快速检查知识库")
    print("=" * 70)
    
    # 1. 检查文件
    if not check_kb_exists():
        print("\n💡 知识库还未创建，你可以：")
        print("   1. 运行 main.py，使用单Agent模式")
        print("   2. 输入：帮我记住：Python是一门编程语言")
        print("   3. 知识会自动保存到知识库")
        return False
    
    # 2. 加载并显示摘要
    kb = view_kb_summary()
    
    if kb is None:
        return False
    
    # 3. 显示最近文档
    if kb.documents:
        recent = kb.get_recent_documents(3)
        print("\n📝 最近添加的文档:")
        for doc in recent:
            title = doc.metadata.get('title', doc.doc_id)
            print(f"  • {title}")
    
    return True


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("📚 知识库查看工具")
    print("=" * 70)
    
    # 快速检查
    exists = quick_check()
    
    if not exists:
        print("\n❓ 知识库为空或不存在")
        return
    
    # 询问是否进入交互模式
    print("\n" + "-" * 70)
    choice = input("是否进入交互式查看器？(y/n): ").strip().lower()
    
    if choice == 'y':
        interactive_viewer()
    else:
        print("\n💡 提示：")
        print("   • 运行: python kb_viewer.py 查看知识库")
        print("   • 在main.py中使用命令查看知识库统计")


if __name__ == "__main__":
    main()