"""
记忆管理模块 - 管理短期和长期记忆
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from config import SHORT_TERM_MEMORY_LIMIT, MEMORY_FILE


class Memory:
    """管理对话的短期和长期记忆"""

    def __init__(self, short_term_limit: int = SHORT_TERM_MEMORY_LIMIT):
        self.short_term_limit = short_term_limit
        self.short_term_memory: List[Dict] = []  # 最近的对话
        self.long_term_memory: List[Dict] = []  # 重要信息摘要
        self.user_profile: Dict = {}  # 用户信息画像

    def add_to_short_term(self, role: str, content: str):
        """添加到短期记忆"""
        self.short_term_memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # 保持短期记忆在限制范围内
        if len(self.short_term_memory) > self.short_term_limit * 2:
            # 保留系统消息和最近的对话
            system_msgs = [m for m in self.short_term_memory if m["role"] == "system"]
            recent_msgs = [m for m in self.short_term_memory if m["role"] != "system"][-self.short_term_limit * 2:]
            self.short_term_memory = system_msgs + recent_msgs

    def add_to_long_term(self, summary: str, importance: int = 5):
        """添加到长期记忆"""
        self.long_term_memory.append({
            "summary": summary,
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        })
        
        # 保持长期记忆数量在合理范围（最多100条）
        if len(self.long_term_memory) > 100:
            # 按重要性排序，保留前100条
            self.long_term_memory = sorted(
                self.long_term_memory,
                key=lambda x: x["importance"],
                reverse=True
            )[:100]

    def update_user_profile(self, key: str, value: Any):
        """更新用户画像"""
        self.user_profile[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }

    def get_context_messages(self) -> List[Dict]:
        """获取用于API调用的消息列表"""
        messages = []

        # 构建系统提示（包含长期记忆和用户画像）
        system_content = "你是一个智能助手，可以帮助用户完成各种任务。"

        # 添加长期记忆
        if self.long_term_memory:
            recent_memories = sorted(
                self.long_term_memory,
                key=lambda x: x["importance"],
                reverse=True
            )[:5]  # 取最重要的5条
            memory_text = "\n".join([f"- {m['summary']}" for m in recent_memories])
            system_content += f"\n\n重要记忆：\n{memory_text}"

        # 添加用户画像
        if self.user_profile:
            profile_text = "\n".join([
                f"- {k}: {v['value']}" 
                for k, v in self.user_profile.items()
            ])
            system_content += f"\n\n用户信息：\n{profile_text}"

        messages.append({"role": "system", "content": system_content})

        # 添加短期记忆（最近的对话）
        for msg in self.short_term_memory:
            if msg["role"] != "system":
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return messages

    def save_to_file(self, filename: str = None):
        """保存记忆到文件"""
        if filename is None:
            filename = MEMORY_FILE
            
        data = {
            "short_term": self.short_term_memory,
            "long_term": self.long_term_memory,
            "user_profile": self.user_profile,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str = None):
        """从文件加载记忆"""
        if filename is None:
            filename = MEMORY_FILE
            
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.short_term_memory = data.get("short_term", [])
                self.long_term_memory = data.get("long_term", [])
                self.user_profile = data.get("user_profile", {})
                
                saved_at = data.get("saved_at", "未知")
                print(f"✅ 已加载记忆文件 (保存于: {saved_at})")
        except FileNotFoundError:
            print("📝 未找到历史记忆文件，将创建新的记忆")
        except Exception as e:
            print(f"⚠️ 加载记忆文件失败: {str(e)}")

    def clear_short_term(self):
        """清空短期记忆"""
        self.short_term_memory = []
        print("🧹 短期记忆已清空")

    def clear_all(self):
        """清空所有记忆"""
        self.short_term_memory = []
        self.long_term_memory = []
        self.user_profile = {}
        print("🧹 所有记忆已清空")

    def get_stats(self) -> Dict:
        """获取记忆统计信息"""
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "user_profile_count": len(self.user_profile),
            "total_conversations": len([m for m in self.short_term_memory if m["role"] == "user"])
        }

    def search_memory(self, keyword: str) -> List[Dict]:
        """搜索记忆中的关键词"""
        results = []
        
        # 搜索短期记忆
        for msg in self.short_term_memory:
            if keyword.lower() in msg["content"].lower():
                results.append({
                    "type": "short_term",
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"]
                })
        
        # 搜索长期记忆
        for mem in self.long_term_memory:
            if keyword.lower() in mem["summary"].lower():
                results.append({
                    "type": "long_term",
                    "summary": mem["summary"],
                    "importance": mem["importance"],
                    "timestamp": mem["timestamp"]
                })
        
        return results

    def export_to_text(self, filename: str = "memory_export.txt"):
        """导出记忆为文本格式"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("记忆导出\n")
                f.write(f"导出时间: {datetime.now()}\n")
                f.write("=" * 60 + "\n\n")
                
                # 用户画像
                if self.user_profile:
                    f.write("【用户画像】\n")
                    for key, value in self.user_profile.items():
                        f.write(f"  {key}: {value['value']}\n")
                    f.write("\n")
                
                # 长期记忆
                if self.long_term_memory:
                    f.write("【长期记忆】\n")
                    for mem in sorted(self.long_term_memory, 
                                     key=lambda x: x["importance"], 
                                     reverse=True):
                        f.write(f"  [{mem['importance']}⭐] {mem['summary']}\n")
                        f.write(f"    时间: {mem['timestamp']}\n")
                    f.write("\n")
                
                # 短期记忆（对话历史）
                if self.short_term_memory:
                    f.write("【对话历史】\n")
                    for msg in self.short_term_memory:
                        role_name = {"user": "👤 用户", "assistant": "🤖 助手"}.get(msg["role"], msg["role"])
                        f.write(f"\n{role_name} [{msg['timestamp']}]\n")
                        f.write(f"{msg['content']}\n")
                
                f.write("\n" + "=" * 60 + "\n")
            
            print(f"✅ 记忆已导出到: {filename}")
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")