"""
工具实现 - 集成真实API + 知识库
"""

import os
import json
import hashlib
import random
from datetime import datetime
from typing import Dict, Optional
import requests
from config import *
from kb_tools import KnowledgeBaseTools


class Tools:
    """Agent可用的工具集合"""

    def __init__(self):
        # 初始化知识库工具
        self.kb_tools = KnowledgeBaseTools()

    # ============== 基础工具 ==============
    @staticmethod
    def get_current_time() -> str:
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate(expression: str) -> str:
        """计算数学表达式"""
        try:
            allowed_chars = set("0123456789+-*/()%. ")
            if not all(c in allowed_chars for c in expression):
                return "错误: 表达式包含非法字符"
            
            result = eval(expression)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"

    # ============== 天气查询 ==============
    @staticmethod
    def search_weather(city: str) -> str:
        """查询天气 - 支持真实API"""
        if not USE_REAL_WEATHER_API:
            weathers = {
                "北京": "晴天，气温 15-25°C，空气质量良好",
                "上海": "多云，气温 18-26°C，湿度较大",
                "深圳": "小雨，气温 22-28°C，注意携带雨具",
                "广州": "阴天，气温 20-27°C",
                "杭州": "晴转多云，气温 16-24°C"
            }
            return weathers.get(city, f"{city}的天气：晴天，气温适宜")
        
        try:
            location_url = f"{WEATHER_API_URL}/city/lookup"
            location_params = {"location": city, "key": WEATHER_API_KEY}
            location_response = requests.get(location_url, params=location_params, timeout=5)
            location_data = location_response.json()
            
            if location_data.get("code") != "200" or not location_data.get("location"):
                return f"未找到城市: {city}"
            
            location_id = location_data["location"][0]["id"]
            
            weather_url = f"{WEATHER_API_URL}/weather/now"
            weather_params = {"location": location_id, "key": WEATHER_API_KEY}
            weather_response = requests.get(weather_url, params=weather_params, timeout=5)
            weather_data = weather_response.json()
            
            if weather_data.get("code") != "200":
                return f"获取天气失败: {weather_data.get('code')}"
            
            now = weather_data["now"]
            return (f"{city}天气：{now['text']}，"
                   f"温度 {now['temp']}°C，"
                   f"体感温度 {now['feelsLike']}°C，"
                   f"湿度 {now['humidity']}%，"
                   f"风向 {now['windDir']}，风力 {now['windScale']}级")
        
        except Exception as e:
            return f"查询天气失败: {str(e)}"

    # ============== 网络搜索 ==============
    @staticmethod
    def search_web(query: str) -> str:
        """网络搜索 - 支持真实API"""
        if not USE_REAL_SEARCH_API:
            mock_results = {
                "天气": "根据搜索结果，今天全国大部分地区天气晴朗，气温适宜。",
                "新闻": "最新科技新闻：AI大模型技术持续突破，多模态应用日益广泛。",
                "AI": "人工智能领域最新进展：大语言模型在各行业落地应用，智能体成为研究热点。",
                "股票": "A股今日收盘，上证指数上涨0.5%，科技板块表现活跃。",
                "Python": "Python 3.12版本发布，带来性能优化和新特性。"
            }
            
            for key, value in mock_results.items():
                if key in query:
                    return value
            
            return f"搜索'{query}'的结果：找到相关信息若干条（模拟数据）"
        
        try:
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            payload = {"q": query, "num": 5}
            
            response = requests.post(SERPER_API_URL, headers=headers, json=payload, timeout=10)
            data = response.json()
            
            if "organic" in data and data["organic"]:
                results = []
                for item in data["organic"][:3]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    results.append(f"• {title}\n  {snippet}")
                
                return "搜索结果：\n" + "\n\n".join(results)
            else:
                return f"未找到关于'{query}'的搜索结果"
        
        except Exception as e:
            return f"搜索失败: {str(e)}"

    # ============== 文本翻译 ==============
    @staticmethod
    def translate_text(text: str, target_lang: str = "英语") -> str:
        """翻译文本 - 支持真实API"""
        if not USE_REAL_TRANSLATE_API:
            translations = {
                "你好": {"英语": "Hello", "日语": "こんにちは", "法语": "Bonjour"},
                "谢谢": {"英语": "Thank you", "日语": "ありがとう", "法语": "Merci"},
                "再见": {"英语": "Goodbye", "日语": "さようなら", "法语": "Au revoir"}
            }
            
            if text in translations and target_lang in translations[text]:
                return f"翻译结果：{translations[text][target_lang]}"
            
            return f"[模拟翻译] '{text}' → {target_lang}: (Translation result)"
        
        try:
            from_lang = "auto"
            to_lang = LANGUAGE_CODE_MAP.get(target_lang, "en")
            
            salt = str(random.randint(32768, 65536))
            sign_str = BAIDU_TRANSLATE_APP_ID + text + salt + BAIDU_TRANSLATE_SECRET_KEY
            sign = hashlib.md5(sign_str.encode()).hexdigest()
            
            params = {
                "q": text, "from": from_lang, "to": to_lang,
                "appid": BAIDU_TRANSLATE_APP_ID, "salt": salt, "sign": sign
            }
            
            response = requests.get(BAIDU_TRANSLATE_API_URL, params=params, timeout=5)
            data = response.json()
            
            if "trans_result" in data:
                translated = data["trans_result"][0]["dst"]
                return f"翻译结果：{translated}"
            else:
                return f"翻译失败: 错误代码 {data.get('error_code', '未知错误')}"
        
        except Exception as e:
            return f"翻译失败: {str(e)}"

    # ============== 情感分析 ==============
    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """情感分析 - 支持真实API或本地分析"""
        if not USE_REAL_SENTIMENT_API:
            positive_words = ["开心", "高兴", "好", "棒", "喜欢", "爱", "优秀", 
                            "完美", "赞", "美好", "快乐", "幸福", "满意"]
            negative_words = ["难过", "伤心", "差", "讨厌", "恨", "糟糕", 
                            "失望", "痛苦", "悲伤", "愤怒", "生气", "不满"]
            
            pos_count = sum(1 for word in positive_words if word in text)
            neg_count = sum(1 for word in negative_words if word in text)
            
            total = pos_count + neg_count
            if total == 0:
                sentiment = "中性"
                confidence = 0.5
            elif pos_count > neg_count:
                sentiment = "积极"
                confidence = pos_count / total
            else:
                sentiment = "消极"
                confidence = neg_count / total
            
            return (f"情感分析结果：{sentiment} "
                   f"(置信度: {confidence:.2%}, "
                   f"正面词: {pos_count}, 负面词: {neg_count})")
        
        try:
            token_url = "https://aip.baidubce.com/oauth/2.0/token"
            token_params = {
                "grant_type": "client_credentials",
                "client_id": BAIDU_NLP_API_KEY,
                "client_secret": BAIDU_NLP_SECRET_KEY
            }
            token_response = requests.post(token_url, params=token_params, timeout=5)
            access_token = token_response.json().get("access_token")
            
            sentiment_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={access_token}"
            headers = {"Content-Type": "application/json"}
            payload = {"text": text}
            
            response = requests.post(sentiment_url, headers=headers, json=payload, timeout=5)
            data = response.json()
            
            if "items" in data and data["items"]:
                item = data["items"][0]
                sentiment = item["sentiment"]
                confidence = item["confidence"]
                
                sentiment_map = {0: "消极", 1: "中性", 2: "积极"}
                return f"情感分析结果：{sentiment_map[sentiment]} (置信度: {confidence:.2%})"
            else:
                return "情感分析失败"
        
        except Exception as e:
            return f"情感分析失败: {str(e)}"

    # ============== 文件操作 ==============
    @staticmethod
    def save_note(content: str) -> str:
        """保存笔记"""
        try:
            with open(NOTES_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now()}] {content}\n")
            return "✅ 笔记已保存"
        except Exception as e:
            return f"❌ 保存失败: {str(e)}"

    @staticmethod
    def read_file(filepath: str, max_lines: int = MAX_FILE_READ_LINES) -> str:
        """读取文件内容"""
        try:
            if not os.path.exists(filepath):
                return f"❌ 文件不存在: {filepath}"
            
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()[:max_lines]
                content = "".join(lines)
            
            if len(lines) == max_lines:
                return f"📄 文件内容 (前{max_lines}行):\n{content}\n... (文件较长，已截断)"
            else:
                return f"📄 文件内容:\n{content}"
        except Exception as e:
            return f"❌ 读取文件失败: {str(e)}"

    @staticmethod
    def get_file_info(filepath: str) -> str:
        """获取文件信息"""
        try:
            if not os.path.exists(filepath):
                return f"❌ 文件不存在: {filepath}"
            
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.2f} MB"
            
            return (f"📄 文件信息:\n"
                   f"  路径: {filepath}\n"
                   f"  大小: {size_str}\n"
                   f"  修改时间: {mtime}")
        except Exception as e:
            return f"❌ 获取文件信息失败: {str(e)}"

    # ============== 任务管理 ==============
    @staticmethod
    def create_todo(task: str, priority: str = "medium") -> str:
        """创建待办事项"""
        try:
            todo_item = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "task": task,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            }
            
            todos = []
            if TODOS_FILE.exists():
                with open(TODOS_FILE, "r", encoding="utf-8") as f:
                    todos = json.load(f)
            
            todos.append(todo_item)
            
            with open(TODOS_FILE, "w", encoding="utf-8") as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
            
            priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🔴"}
            return f"✅ 已创建待办事项：{priority_emoji.get(priority, '⚪')} {task}"
        except Exception as e:
            return f"❌ 创建待办失败: {str(e)}"

    @staticmethod
    def set_reminder(time_str: str, content: str) -> str:
        """设置提醒"""
        try:
            with open(REMINDERS_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n⏰ 提醒时间: {time_str}\n")
                f.write(f"📝 内容: {content}\n")
                f.write(f"🕐 创建于: {datetime.now()}\n")
                f.write("-" * 40 + "\n")
            return f"✅ 已设置提醒：{time_str} - {content}"
        except Exception as e:
            return f"❌ 设置提醒失败: {str(e)}"

    # ============== 知识库工具 ==============
    def add_knowledge(self, content: str, title: str = None, 
                     category: str = "未分类", tags: str = None) -> str:
        """添加知识到知识库"""
        return self.kb_tools.add_knowledge(content, title, category, tags)

    def search_knowledge(self, query: str, category: str = None, limit: int = 5) -> str:
        """搜索知识库"""
        return self.kb_tools.search_knowledge(query, category, limit)

    def get_knowledge_detail(self, doc_id: str) -> str:
        """获取知识详情"""
        return self.kb_tools.get_knowledge_detail(doc_id)

    def list_knowledge_categories(self) -> str:
        """列出知识库分类"""
        return self.kb_tools.list_knowledge_categories()

    def get_knowledge_stats(self) -> str:
        """获取知识库统计"""
        return self.kb_tools.get_knowledge_stats()

    def import_knowledge_from_file(self, filepath: str, category: str = "导入") -> str:
        """从文件导入知识"""
        return self.kb_tools.import_knowledge_from_file(filepath, category)

    def search_knowledge_graph(self, entity_name: str) -> str:
        """搜索知识图谱"""
        return self.kb_tools.search_knowledge_graph(entity_name)

    def export_knowledge_base(self, output_file: str = None) -> str:
        """导出知识库"""
        return self.kb_tools.export_knowledge_base(output_file)


# 导入知识库工具配置
from kb_tools import KB_TOOLS_CONFIG

# 合并工具配置
TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除和基本数学运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "要计算的数学表达式，例如：'2+2' 或 '10*5+3'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_weather",
            "description": "查询指定城市的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，例如：北京、上海、深圳"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "在网络上搜索信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词或问题"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "翻译文本到指定语言",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "要翻译的文本"},
                    "target_lang": {"type": "string", "description": "目标语言，例如：英语、日语、法语", "default": "英语"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_sentiment",
            "description": "分析文本的情感倾向（积极、消极、中性）",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "要分析的文本内容"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "保存用户的笔记或重要信息到笔记文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "要保存的笔记内容"}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "要读取的文件路径"},
                    "max_lines": {"type": "integer", "description": "最大读取行数", "default": 50}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_info",
            "description": "获取文件的详细信息（大小、修改时间等）",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "文件路径"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_todo",
            "description": "创建待办事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "待办任务描述"},
                    "priority": {"type": "string", "description": "优先级：low、medium、high", "enum": ["low", "medium", "high"], "default": "medium"}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "设置提醒事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_str": {"type": "string", "description": "提醒时间，例如：'明天下午3点' 或 '2024-01-01 10:00'"},
                    "content": {"type": "string", "description": "提醒内容"}
                },
                "required": ["time_str", "content"]
            }
        }
    }
] + KB_TOOLS_CONFIG  # 合并知识库工具配置