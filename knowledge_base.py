"""
个人知识库系统 - 支持文档管理、向量检索、知识图谱
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib

from config import DATA_DIR


class Document:
    """文档类"""
    
    def __init__(self, 
                 content: str, 
                 metadata: Dict[str, Any] = None,
                 doc_id: str = None):
        self.doc_id = doc_id or self._generate_id(content)
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.tags = []
        self.embedding = None  # 向量嵌入（如果使用向量检索）
    
    @staticmethod
    def _generate_id(content: str) -> str:
        """生成文档ID"""
        return hashlib.md5(
            f"{content}{time.time()}".encode()
        ).hexdigest()[:16]
    
    def add_tag(self, tag: str):
        """添加标签"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "doc_id": self.doc_id,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Document':
        """从字典创建"""
        doc = cls(
            content=data["content"],
            metadata=data.get("metadata", {}),
            doc_id=data["doc_id"]
        )
        doc.created_at = data.get("created_at", doc.created_at)
        doc.updated_at = data.get("updated_at", doc.updated_at)
        doc.tags = data.get("tags", [])
        return doc


class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self):
        self.entities = {}  # 实体: {name: {type, properties, related}}
        self.relationships = []  # 关系: [{from, to, type, properties}]
    
    def add_entity(self, name: str, entity_type: str, properties: Dict = None):
        """添加实体"""
        if name not in self.entities:
            self.entities[name] = {
                "type": entity_type,
                "properties": properties or {},
                "related": set()
            }
    
    def add_relationship(self, 
                        from_entity: str, 
                        to_entity: str, 
                        rel_type: str,
                        properties: Dict = None):
        """添加关系"""
        # 确保实体存在
        if from_entity not in self.entities:
            self.add_entity(from_entity, "unknown")
        if to_entity not in self.entities:
            self.add_entity(to_entity, "unknown")
        
        # 添加关系
        relationship = {
            "from": from_entity,
            "to": to_entity,
            "type": rel_type,
            "properties": properties or {},
            "created_at": datetime.now().isoformat()
        }
        self.relationships.append(relationship)
        
        # 更新实体的关联
        self.entities[from_entity]["related"].add(to_entity)
        self.entities[to_entity]["related"].add(from_entity)
    
    def get_entity(self, name: str) -> Optional[Dict]:
        """获取实体"""
        return self.entities.get(name)
    
    def get_related_entities(self, name: str, max_depth: int = 1) -> List[str]:
        """获取关联实体"""
        if name not in self.entities:
            return []
        
        related = set()
        current_level = {name}
        
        for _ in range(max_depth):
            next_level = set()
            for entity in current_level:
                if entity in self.entities:
                    related.update(self.entities[entity]["related"])
                    next_level.update(self.entities[entity]["related"])
            current_level = next_level
        
        related.discard(name)  # 移除自己
        return list(related)
    
    def search_entities(self, query: str, entity_type: str = None) -> List[str]:
        """搜索实体"""
        results = []
        query_lower = query.lower()
        
        for name, entity in self.entities.items():
            # 类型过滤
            if entity_type and entity["type"] != entity_type:
                continue
            
            # 名称匹配
            if query_lower in name.lower():
                results.append(name)
        
        return results
    
    def get_entity_relationships(self, entity_name: str) -> List[Dict]:
        """获取实体的所有关系"""
        relationships = []
        for rel in self.relationships:
            if rel["from"] == entity_name or rel["to"] == entity_name:
                relationships.append(rel)
        return relationships
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        # 将set转换为list以便序列化
        entities_dict = {}
        for name, entity in self.entities.items():
            entity_copy = entity.copy()
            entity_copy["related"] = list(entity_copy["related"])
            entities_dict[name] = entity_copy
        
        return {
            "entities": entities_dict,
            "relationships": self.relationships
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeGraph':
        """从字典创建"""
        kg = cls()
        
        # 恢复实体
        for name, entity in data.get("entities", {}).items():
            entity_copy = entity.copy()
            entity_copy["related"] = set(entity_copy["related"])
            kg.entities[name] = entity_copy
        
        # 恢复关系
        kg.relationships = data.get("relationships", [])
        
        return kg


class KnowledgeBase:
    """个人知识库"""
    
    def __init__(self, kb_dir: Path = None):
        self.kb_dir = kb_dir or DATA_DIR / "knowledge_base"
        self.kb_dir.mkdir(exist_ok=True, parents=True)
        
        self.documents: Dict[str, Document] = {}
        self.knowledge_graph = KnowledgeGraph()
        self.categories = {}  # 分类: {category: [doc_ids]}
        self.index = {}  # 倒排索引: {word: [doc_ids]}
        
        # 加载知识库
        self.load()
    
    # ============== 文档管理 ==============
    
    def add_document(self, 
                     content: str, 
                     title: str = None,
                     category: str = "未分类",
                     tags: List[str] = None,
                     source: str = None) -> str:
        """添加文档"""
        metadata = {
            "title": title or f"文档_{len(self.documents) + 1}",
            "category": category,
            "source": source
        }
        
        doc = Document(content=content, metadata=metadata)
        
        # 添加标签
        if tags:
            for tag in tags:
                doc.add_tag(tag)
        
        # 保存文档
        self.documents[doc.doc_id] = doc
        
        # 更新分类
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(doc.doc_id)
        
        # 更新索引
        self._update_index(doc)
        
        # 自动提取知识（简单实现）
        self._extract_knowledge(doc)
        
        # 持久化
        self.save()
        
        return doc.doc_id
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """获取文档"""
        return self.documents.get(doc_id)
    
    def update_document(self, doc_id: str, content: str = None, **metadata):
        """更新文档"""
        if doc_id not in self.documents:
            return False
        
        doc = self.documents[doc_id]
        
        if content:
            doc.content = content
            self._update_index(doc)
        
        if metadata:
            doc.metadata.update(metadata)
        
        doc.updated_at = datetime.now().isoformat()
        self.save()
        return True
    
    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        if doc_id not in self.documents:
            return False
        
        doc = self.documents[doc_id]
        
        # 从分类中移除
        category = doc.metadata.get("category", "未分类")
        if category in self.categories:
            self.categories[category].remove(doc.id)
        
        # 从索引中移除
        for word in self._tokenize(doc.content):
            if word in self.index and doc_id in self.index[word]:
                self.index[word].remove(doc_id)
        
        # 删除文档
        del self.documents[doc_id]
        
        self.save()
        return True
    
    # ============== 搜索功能 ==============
    
    def search(self, 
               query: str, 
               category: str = None,
               tags: List[str] = None,
               limit: int = 10) -> List[Document]:
        """搜索文档"""
        results = []
        query_words = set(self._tokenize(query.lower()))
        
        for doc_id, doc in self.documents.items():
            # 分类过滤
            if category and doc.metadata.get("category") != category:
                continue
            
            # 标签过滤
            if tags and not any(tag in doc.tags for tag in tags):
                continue
            
            # 内容匹配
            doc_words = set(self._tokenize(doc.content.lower()))
            score = len(query_words & doc_words) / len(query_words) if query_words else 0
            
            # 标题匹配加权
            if "title" in doc.metadata:
                title_words = set(self._tokenize(doc.metadata["title"].lower()))
                title_score = len(query_words & title_words) / len(query_words) if query_words else 0
                score += title_score * 2  # 标题匹配权重更高
            
            if score > 0:
                results.append((score, doc))
        
        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [doc for score, doc in results[:limit]]
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词（中英文）"""
        import re
        # 分离中英文
        words = []
        
        # 英文单词
        eng_words = re.findall(r'[a-zA-Z]+', text)
        words.extend([w.lower() for w in eng_words if len(w) > 1])
        
        # 中文字符（简单按字符分）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        for chars in chinese_chars:
            # 简单按2-3字切分
            for i in range(len(chars)):
                if i + 2 <= len(chars):
                    words.append(chars[i:i+2])
                if i + 3 <= len(chars):
                    words.append(chars[i:i+3])
        
        return words
    
    def _update_index(self, doc: Document):
        """更新倒排索引"""
        words = self._tokenize(doc.content.lower())
        for word in set(words):  # 去重
            if word not in self.index:
                self.index[word] = []
            if doc.doc_id not in self.index[word]:
                self.index[word].append(doc.doc_id)
    
    # ============== 知识提取 ==============
    
    def _extract_knowledge(self, doc: Document):
        """从文档中提取知识（简单实现）"""
        content = doc.content
        
        # 提取关键词作为实体
        words = self._tokenize(content)
        word_freq = {}
        for word in words:
            if len(word) > 1:  # 过滤单字
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 选择高频词作为实体
        important_words = sorted(
            word_freq.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        for word, freq in important_words:
            self.knowledge_graph.add_entity(
                word, 
                "keyword",
                {"frequency": freq, "source_doc": doc.doc_id}
            )
        
        # 简单的共现关系
        for i, (word1, _) in enumerate(important_words):
            for word2, _ in important_words[i+1:]:
                self.knowledge_graph.add_relationship(
                    word1, 
                    word2, 
                    "co_occurrence",
                    {"doc_id": doc.doc_id}
                )
    
    # ============== 统计分析 ==============
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "total_documents": len(self.documents),
            "total_categories": len(self.categories),
            "total_entities": len(self.knowledge_graph.entities),
            "total_relationships": len(self.knowledge_graph.relationships),
            "categories": {
                cat: len(docs) 
                for cat, docs in self.categories.items()
            },
            "total_index_words": len(self.index)
        }
    
    def get_popular_tags(self, limit: int = 10) -> List[tuple]:
        """获取热门标签"""
        tag_count = {}
        for doc in self.documents.values():
            for tag in doc.tags:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        
        return sorted(
            tag_count.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:limit]
    
    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        """获取最近的文档"""
        docs = sorted(
            self.documents.values(),
            key=lambda x: x.created_at,
            reverse=True
        )
        return docs[:limit]
    
    # ============== 导入导出 ==============
    
    def import_from_file(self, filepath: str, category: str = "导入") -> int:
        """从文件导入"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(filepath)
            title = os.path.splitext(filename)[0]
            
            self.add_document(
                content=content,
                title=title,
                category=category,
                source=filepath
            )
            return 1
        except Exception as e:
            print(f"导入失败: {str(e)}")
            return 0
    
    def import_from_directory(self, dirpath: str, category: str = "导入") -> int:
        """从目录批量导入"""
        count = 0
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                if file.endswith(('.txt', '.md', '.markdown')):
                    filepath = os.path.join(root, file)
                    count += self.import_from_file(filepath, category)
        return count
    
    def export_to_markdown(self, output_file: str):
        """导出为Markdown"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 个人知识库\n\n")
            f.write(f"导出时间: {datetime.now()}\n\n")
            
            # 按分类导出
            for category, doc_ids in self.categories.items():
                f.write(f"## {category}\n\n")
                
                for doc_id in doc_ids:
                    doc = self.documents[doc_id]
                    f.write(f"### {doc.metadata.get('title', doc_id)}\n\n")
                    f.write(f"**创建时间**: {doc.created_at}\n\n")
                    
                    if doc.tags:
                        f.write(f"**标签**: {', '.join(doc.tags)}\n\n")
                    
                    f.write(f"{doc.content}\n\n")
                    f.write("---\n\n")
    
    # ============== 持久化 ==============
    
    def save(self):
        """保存知识库"""
        data = {
            "documents": {
                doc_id: doc.to_dict() 
                for doc_id, doc in self.documents.items()
            },
            "knowledge_graph": self.knowledge_graph.to_dict(),
            "categories": self.categories,
            "index": self.index,
            "saved_at": datetime.now().isoformat()
        }
        
        kb_file = self.kb_dir / "knowledge_base.json"
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """加载知识库"""
        kb_file = self.kb_dir / "knowledge_base.json"
        
        if not kb_file.exists():
            return
        
        try:
            with open(kb_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载文档
            self.documents = {
                doc_id: Document.from_dict(doc_data)
                for doc_id, doc_data in data.get("documents", {}).items()
            }
            
            # 加载知识图谱
            kg_data = data.get("knowledge_graph", {})
            if kg_data:
                self.knowledge_graph = KnowledgeGraph.from_dict(kg_data)
            
            # 加载分类和索引
            self.categories = data.get("categories", {})
            self.index = data.get("index", {})
            
            print(f"✅ 知识库加载成功 (保存于: {data.get('saved_at', '未知')})")
            
        except Exception as e:
            print(f"⚠️ 加载知识库失败: {str(e)}")