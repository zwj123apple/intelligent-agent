# 创建一个临时测试文件 test_quick.py
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# 添加一条知识
doc_id = kb.add_document(
    content="这是一条测试知识",
    title="测试文档",
    category="测试",
    tags=["测试"]
)

print(f"✅ 成功添加文档，ID: {doc_id}")

# 查看统计
stats = kb.get_statistics()
print(f"📊 文档总数: {stats['total_documents']}")

# 搜索
results = kb.search("测试")
print(f"🔍 搜索到 {len(results)} 条结果")