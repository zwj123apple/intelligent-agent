"""
知识库工具 - 集成到Agent系统
"""

from typing import Dict, List
from knowledge_base import KnowledgeBase


class KnowledgeBaseTools:
    """知识库工具集"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
    
    @staticmethod
    def add_knowledge(content: str, 
                     title: str = None,
                     category: str = "未分类",
                     tags: str = None) -> str:
        """
        添加知识到知识库
        
        Args:
            content: 知识内容
            title: 标题
            category: 分类
            tags: 标签（逗号分隔）
        """
        try:
            kb = KnowledgeBase()
            
            tag_list = []
            if tags:
                tag_list = [t.strip() for t in tags.split(',')]
            
            doc_id = kb.add_document(
                content=content,
                title=title,
                category=category,
                tags=tag_list
            )
            
            return f"✅ 知识已添加到知识库\n" \
                   f"   ID: {doc_id}\n" \
                   f"   标题: {title or '无'}\n" \
                   f"   分类: {category}\n" \
                   f"   标签: {', '.join(tag_list) if tag_list else '无'}"
        
        except Exception as e:
            return f"❌ 添加失败: {str(e)}"
    
    @staticmethod
    def search_knowledge(query: str, 
                        category: str = None,
                        limit: int = 5) -> str:
        """
        搜索知识库
        
        Args:
            query: 搜索关键词
            category: 限定分类
            limit: 返回结果数量
        """
        try:
            kb = KnowledgeBase()
            results = kb.search(
                query=query,
                category=category,
                limit=limit
            )
            
            if not results:
                return f"🔍 未找到与 '{query}' 相关的知识"
            
            response = f"🔍 找到 {len(results)} 条相关知识:\n\n"
            
            for i, doc in enumerate(results, 1):
                title = doc.metadata.get('title', f'文档_{doc.doc_id}')
                category = doc.metadata.get('category', '未分类')
                preview = doc.content[:100] + "..." if len(doc.content) > 100 else doc.content
                
                response += f"{i}. 【{category}】{title}\n"
                response += f"   {preview}\n"
                response += f"   ID: {doc.doc_id}\n"
                
                if doc.tags:
                    response += f"   标签: {', '.join(doc.tags)}\n"
                
                response += "\n"
            
            return response.strip()
        
        except Exception as e:
            return f"❌ 搜索失败: {str(e)}"
    
    @staticmethod
    def get_knowledge_detail(doc_id: str) -> str:
        """
        获取知识详情
        
        Args:
            doc_id: 文档ID
        """
        try:
            kb = KnowledgeBase()
            doc = kb.get_document(doc_id)
            
            if not doc:
                return f"❌ 未找到ID为 {doc_id} 的知识"
            
            title = doc.metadata.get('title', '无标题')
            category = doc.metadata.get('category', '未分类')
            
            response = f"📄 知识详情\n\n"
            response += f"标题: {title}\n"
            response += f"分类: {category}\n"
            response += f"创建时间: {doc.created_at}\n"
            response += f"更新时间: {doc.updated_at}\n"
            
            if doc.tags:
                response += f"标签: {', '.join(doc.tags)}\n"
            
            if doc.metadata.get('source'):
                response += f"来源: {doc.metadata['source']}\n"
            
            response += f"\n内容:\n{doc.content}"
            
            return response
        
        except Exception as e:
            return f"❌ 获取失败: {str(e)}"
    
    @staticmethod
    def list_knowledge_categories() -> str:
        """列出所有分类"""
        try:
            kb = KnowledgeBase()
            stats = kb.get_statistics()
            
            if not stats['categories']:
                return "📚 知识库暂无分类"
            
            response = "📚 知识库分类:\n\n"
            
            for category, count in sorted(
                stats['categories'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                response += f"  • {category}: {count} 篇\n"
            
            response += f"\n总计: {stats['total_documents']} 篇文档"
            
            return response
        
        except Exception as e:
            return f"❌ 获取失败: {str(e)}"
    
    @staticmethod
    def get_knowledge_stats() -> str:
        """获取知识库统计"""
        try:
            kb = KnowledgeBase()
            stats = kb.get_statistics()
            
            response = "📊 知识库统计:\n\n"
            response += f"  📄 文档总数: {stats['total_documents']}\n"
            response += f"  📁 分类数量: {stats['total_categories']}\n"
            response += f"  🧠 实体数量: {stats['total_entities']}\n"
            response += f"  🔗 关系数量: {stats['total_relationships']}\n"
            response += f"  📇 索引词数: {stats['total_index_words']}\n"
            
            # 热门标签
            popular_tags = kb.get_popular_tags(5)
            if popular_tags:
                response += "\n🏷️ 热门标签:\n"
                for tag, count in popular_tags:
                    response += f"  • {tag}: {count}\n"
            
            # 最近文档
            recent_docs = kb.get_recent_documents(3)
            if recent_docs:
                response += "\n📝 最近添加:\n"
                for doc in recent_docs:
                    title = doc.metadata.get('title', doc.doc_id)
                    response += f"  • {title}\n"
            
            return response
        
        except Exception as e:
            return f"❌ 获取失败: {str(e)}"
    
    @staticmethod
    def import_knowledge_from_file(filepath: str, category: str = "导入") -> str:
        """
        从文件导入知识
        
        Args:
            filepath: 文件路径
            category: 分类名称
        """
        try:
            kb = KnowledgeBase()
            count = kb.import_from_file(filepath, category)
            
            if count > 0:
                return f"✅ 成功导入 {count} 篇文档到分类 [{category}]"
            else:
                return "❌ 导入失败，请检查文件路径"
        
        except Exception as e:
            return f"❌ 导入失败: {str(e)}"
    
    @staticmethod
    def search_knowledge_graph(entity_name: str) -> str:
        """
        搜索知识图谱
        
        Args:
            entity_name: 实体名称
        """
        try:
            kb = KnowledgeBase()
            entity = kb.knowledge_graph.get_entity(entity_name)
            
            if not entity:
                # 尝试搜索相似实体
                similar = kb.knowledge_graph.search_entities(entity_name)
                if similar:
                    return f"未找到实体 '{entity_name}'，你是否要找:\n  " + "\n  ".join(similar[:5])
                else:
                    return f"❌ 未找到实体 '{entity_name}'"
            
            response = f"🧠 实体: {entity_name}\n\n"
            response += f"类型: {entity['type']}\n"
            
            if entity['properties']:
                response += f"属性: {entity['properties']}\n"
            
            # 获取关系
            relationships = kb.knowledge_graph.get_entity_relationships(entity_name)
            if relationships:
                response += f"\n🔗 关系 ({len(relationships)} 条):\n"
                for rel in relationships[:10]:  # 最多显示10条
                    if rel['from'] == entity_name:
                        response += f"  • {entity_name} --[{rel['type']}]--> {rel['to']}\n"
                    else:
                        response += f"  • {rel['from']} --[{rel['type']}]--> {entity_name}\n"
            
            # 获取关联实体
            related = kb.knowledge_graph.get_related_entities(entity_name, max_depth=1)
            if related:
                response += f"\n📌 关联实体:\n  " + "\n  ".join(related[:10])
            
            return response
        
        except Exception as e:
            return f"❌ 搜索失败: {str(e)}"
    
    @staticmethod
    def export_knowledge_base(output_file: str = None) -> str:
        """
        导出知识库
        
        Args:
            output_file: 输出文件路径
        """
        try:
            kb = KnowledgeBase()
            
            if output_file is None:
                from datetime import datetime
                output_file = f"knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
            kb.export_to_markdown(output_file)
            
            return f"✅ 知识库已导出到: {output_file}"
        
        except Exception as e:
            return f"❌ 导出失败: {str(e)}"


# 知识库工具配置（添加到 TOOLS_CONFIG）
KB_TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "add_knowledge",
            "description": "添加知识到个人知识库，用于保存重要信息、学习笔记、文档等",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "知识内容"
                    },
                    "title": {
                        "type": "string",
                        "description": "知识标题",
                        "default": None
                    },
                    "category": {
                        "type": "string",
                        "description": "分类，例如：学习笔记、工作文档、个人心得等",
                        "default": "未分类"
                    },
                    "tags": {
                        "type": "string",
                        "description": "标签，多个标签用逗号分隔，例如：Python,编程,教程",
                        "default": None
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "在个人知识库中搜索相关知识",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词或问题"
                    },
                    "category": {
                        "type": "string",
                        "description": "限定搜索的分类",
                        "default": None
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_knowledge_detail",
            "description": "获取知识库中某个文档的详细内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "文档ID"
                    }
                },
                "required": ["doc_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_knowledge_categories",
            "description": "列出知识库的所有分类及文档数量",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_knowledge_stats",
            "description": "获取知识库的统计信息，包括文档数、分类、热门标签等",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "import_knowledge_from_file",
            "description": "从文件导入知识到知识库",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "要导入的文件路径"
                    },
                    "category": {
                        "type": "string",
                        "description": "导入到的分类名称",
                        "default": "导入"
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_graph",
            "description": "在知识图谱中搜索实体及其关系",
            "parameters": {
                "type": "object",
                "properties": {
                    "entity_name": {
                        "type": "string",
                        "description": "要搜索的实体名称"
                    }
                },
                "required": ["entity_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_knowledge_base",
            "description": "将知识库导出为Markdown文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "output_file": {
                        "type": "string",
                        "description": "输出文件路径",
                        "default": None
                    }
                },
                "required": []
            }
        }
    }
]