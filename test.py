"""
完整的Agent系统 - 使用通义千问模型
包含：流式响应、对话历史、短期/长期记忆、多工具调用
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI

# ============== 配置部分 ==============
# 请设置你的通义千问API Key
API_KEY = "sk-610e45d1dfef4ac0b42791b9784141ef"  # 替换为你的API Key
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


# ============== 工具定义 ==============
class Tools:
    """定义Agent可以使用的工具"""

    @staticmethod
    def get_current_time() -> str:
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate(expression: str) -> str:
        """计算数学表达式"""
        try:
            result = eval(expression)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"

    @staticmethod
    def search_weather(city: str) -> str:
        """查询天气（模拟）"""
        # 实际应用中这里应该调用真实的天气API
        weathers = {
            "北京": "晴天，气温 15-25°C",
            "上海": "多云，气温 18-26°C",
            "深圳": "小雨，气温 22-28°C"
        }
        return weathers.get(city, f"{city}的天气信息：晴天，气温适宜")

    @staticmethod
    def save_note(content: str) -> str:
        """保存笔记到文件"""
        try:
            with open("notes.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now()}] {content}\n")
            return "笔记已保存"
        except Exception as e:
            return f"保存失败: {str(e)}"

    @staticmethod
    def search_web(query: str) -> str:
        """模拟网络搜索"""
        # 实际应用中应该调用真实的搜索API
        mock_results = {
            "天气": "根据搜索结果，今天全国大部分地区天气晴朗",
            "新闻": "最新科技新闻：AI技术持续发展，大模型应用日益广泛",
            "股票": "A股今日收盘，上证指数上涨0.5%",
        }
        for key, value in mock_results.items():
            if key in query:
                return value
        return f"搜索'{query}'的结果：找到相关信息若干条（模拟数据）"

    @staticmethod
    def set_reminder(time_str: str, content: str) -> str:
        """设置提醒"""
        try:
            with open("reminders.txt", "a", encoding="utf-8") as f:
                f.write(f"\n提醒时间: {time_str}\n内容: {content}\n创建于: {datetime.now()}\n")
            return f"已设置提醒：{time_str} - {content}"
        except Exception as e:
            return f"设置提醒失败: {str(e)}"

    @staticmethod
    def translate_text(text: str, target_lang: str = "英语") -> str:
        """翻译文本（模拟）"""
        # 实际应该调用翻译API
        translations = {
            "你好": {"英语": "Hello", "日语": "こんにちは", "法语": "Bonjour"},
            "谢谢": {"英语": "Thank you", "日语": "ありがとう", "法语": "Merci"},
        }
        if text in translations and target_lang in translations[text]:
            return translations[text][target_lang]
        return f"[模拟翻译] '{text}' 翻译为{target_lang}：(Translation result)"

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """情感分析"""
        positive_words = ["开心", "高兴", "好", "棒", "喜欢", "爱"]
        negative_words = ["难过", "伤心", "差", "讨厌", "恨", "糟糕"]
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            return f"情感分析结果：积极情绪 (正面词汇: {pos_count}, 负面词汇: {neg_count})"
        elif neg_count > pos_count:
            return f"情感分析结果：消极情绪 (正面词汇: {pos_count}, 负面词汇: {neg_count})"
        else:
            return f"情感分析结果：中性情绪 (正面词汇: {pos_count}, 负面词汇: {neg_count})"

    @staticmethod
    def get_file_info(filepath: str) -> str:
        """获取文件信息"""
        try:
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                return f"文件: {filepath}\n大小: {size} 字节\n修改时间: {mtime}"
            else:
                return f"文件不存在: {filepath}"
        except Exception as e:
            return f"获取文件信息失败: {str(e)}"

    @staticmethod
    def create_todo(task: str, priority: str = "medium") -> str:
        """创建待办事项"""
        try:
            todo_item = {
                "task": task,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            }
            
            todos = []
            if os.path.exists("todos.json"):
                with open("todos.json", "r", encoding="utf-8") as f:
                    todos = json.load(f)
            
            todos.append(todo_item)
            
            with open("todos.json", "w", encoding="utf-8") as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
            
            return f"已创建待办事项：{task} (优先级: {priority})"
        except Exception as e:
            return f"创建待办失败: {str(e)}"

    @staticmethod
    def read_file(filepath: str, max_lines: int = 50) -> str:
        """读取文件内容"""
        try:
            if not os.path.exists(filepath):
                return f"文件不存在: {filepath}"
            
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()[:max_lines]
                content = "".join(lines)
                
            if len(lines) == max_lines:
                return f"文件内容 (前{max_lines}行):\n{content}\n... (文件较长，已截断)"
            else:
                return f"文件内容:\n{content}"
        except Exception as e:
            return f"读取文件失败: {str(e)}"


# 工具配置 - 符合OpenAI格式
TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
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
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除和基本数学运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如：'2+2' 或 '10*5+3'"
                    }
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
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、深圳"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "保存用户的笔记或重要信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "要保存的笔记内容"
                    }
                },
                "required": ["content"]
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
                    "query": {
                        "type": "string",
                        "description": "搜索关键词或问题"
                    }
                },
                "required": ["query"]
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
                    "time_str": {
                        "type": "string",
                        "description": "提醒时间，例如：'明天下午3点' 或 '2024-01-01 10:00'"
                    },
                    "content": {
                        "type": "string",
                        "description": "提醒内容"
                    }
                },
                "required": ["time_str", "content"]
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
                    "text": {
                        "type": "string",
                        "description": "要翻译的文本"
                    },
                    "target_lang": {
                        "type": "string",
                        "description": "目标语言，例如：英语、日语、法语",
                        "default": "英语"
                    }
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
                    "text": {
                        "type": "string",
                        "description": "要分析的文本内容"
                    }
                },
                "required": ["text"]
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
                    "filepath": {
                        "type": "string",
                        "description": "文件路径"
                    }
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
                    "task": {
                        "type": "string",
                        "description": "待办任务描述"
                    },
                    "priority": {
                        "type": "string",
                        "description": "优先级：low、medium、high",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                },
                "required": ["task"]
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
                    "filepath": {
                        "type": "string",
                        "description": "要读取的文件路径"
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "最大读取行数",
                        "default": 50
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]


# ============== 记忆管理 ==============
class Memory:
    """管理对话的短期和长期记忆"""

    def __init__(self, short_term_limit: int = 10):
        self.short_term_limit = short_term_limit
        self.short_term_memory: List[Dict] = []  # 最近的对话
        self.long_term_memory: List[Dict] = []  # 重要信息摘要
        self.user_profile: Dict = {}  # 用户信息

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

    def update_user_profile(self, key: str, value: Any):
        """更新用户画像"""
        self.user_profile[key] = value

    def get_context_messages(self) -> List[Dict]:
        """获取用于API调用的消息列表"""
        messages = []

        # 添加系统提示（包含长期记忆和用户画像）
        system_content = "你是一个智能助手，可以帮助用户完成各种任务。"

        if self.long_term_memory:
            recent_memories = sorted(
                self.long_term_memory,
                key=lambda x: x["importance"],
                reverse=True
            )[:3]
            memory_text = "\n".join([m["summary"] for m in recent_memories])
            system_content += f"\n\n重要信息：\n{memory_text}"

        if self.user_profile:
            profile_text = "\n".join([f"{k}: {v}" for k, v in self.user_profile.items()])
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

    def save_to_file(self, filename: str = "memory.json"):
        """保存记忆到文件"""
        data = {
            "short_term": self.short_term_memory,
            "long_term": self.long_term_memory,
            "user_profile": self.user_profile
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str = "memory.json"):
        """从文件加载记忆"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.short_term_memory = data.get("short_term", [])
                self.long_term_memory = data.get("long_term", [])
                self.user_profile = data.get("user_profile", {})
        except FileNotFoundError:
            pass


# ============== Agent核心 ==============
class QwenAgent:
    """通义千问Agent主类"""

    def __init__(self, api_key: str, base_url: str, model: str = "qwen-plus"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.memory = Memory()
        self.tools = Tools()

        # 加载历史记忆
        self.memory.load_from_file()

        print(f"✅ Agent初始化完成！使用模型: {model}")

    def execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """执行工具调用"""
        try:
            if tool_name == "get_current_time":
                return self.tools.get_current_time()
            elif tool_name == "calculate":
                return self.tools.calculate(tool_args.get("expression", ""))
            elif tool_name == "search_weather":
                return self.tools.search_weather(tool_args.get("city", ""))
            elif tool_name == "save_note":
                return self.tools.save_note(tool_args.get("content", ""))
            elif tool_name == "search_web":
                return self.tools.search_web(tool_args.get("query", ""))
            elif tool_name == "set_reminder":
                return self.tools.set_reminder(
                    tool_args.get("time_str", ""),
                    tool_args.get("content", "")
                )
            elif tool_name == "translate_text":
                return self.tools.translate_text(
                    tool_args.get("text", ""),
                    tool_args.get("target_lang", "英语")
                )
            elif tool_name == "analyze_sentiment":
                return self.tools.analyze_sentiment(tool_args.get("text", ""))
            elif tool_name == "get_file_info":
                return self.tools.get_file_info(tool_args.get("filepath", ""))
            elif tool_name == "create_todo":
                return self.tools.create_todo(
                    tool_args.get("task", ""),
                    tool_args.get("priority", "medium")
                )
            elif tool_name == "read_file":
                return self.tools.read_file(
                    tool_args.get("filepath", ""),
                    tool_args.get("max_lines", 50)
                )
            else:
                return f"未知工具: {tool_name}"
        except Exception as e:
            return f"工具执行错误: {str(e)}"

    def chat_stream(self, user_input: str):
        """流式对话"""
        print(f"\n👤 用户: {user_input}")

        # 添加用户消息到记忆
        self.memory.add_to_short_term("user", user_input)

        # 获取上下文消息
        messages = self.memory.get_context_messages()

        print("🤖 助手: ", end="", flush=True)

        full_response = ""
        tool_calls_dict = {}  # 使用字典存储工具调用，key是index

        try:
            # 第一次API调用（可能返回工具调用）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS_CONFIG,
                stream=True
            )

            # 处理流式响应
            for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta

                # 处理文本内容
                if delta.content:
                    print(delta.content, end="", flush=True)
                    full_response += delta.content

                # 处理工具调用
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        idx = tool_call.index
                        
                        # 如果是新的工具调用，初始化
                        if idx not in tool_calls_dict:
                            tool_calls_dict[idx] = {
                                "index": idx,
                                "id": "",
                                "type": "function",
                                "function": {
                                    "name": "",
                                    "arguments": ""
                                }
                            }
                        
                        # 累积数据
                        if tool_call.id:
                            tool_calls_dict[idx]["id"] = tool_call.id
                        
                        if tool_call.function:
                            if tool_call.function.name:
                                tool_calls_dict[idx]["function"]["name"] = tool_call.function.name
                            if tool_call.function.arguments:
                                tool_calls_dict[idx]["function"]["arguments"] += tool_call.function.arguments

            print()  # 换行

            # 转换为列表
            tool_calls_data = [tool_calls_dict[idx] for idx in sorted(tool_calls_dict.keys())]

            # 如果有工具调用，执行它们
            if tool_calls_data:
                print("\n🔧 执行工具调用...")

                # 添加助手的工具调用消息到历史
                messages.append({
                    "role": "assistant",
                    "content": full_response if full_response else None,
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["function"]["name"],
                                "arguments": tc["function"]["arguments"]
                            }
                        } for tc in tool_calls_data
                    ]
                })

                # 执行每个工具
                for tool_call in tool_calls_data:
                    tool_name = tool_call["function"]["name"]
                    tool_args_str = tool_call["function"]["arguments"]
                    
                    # 尝试解析JSON参数
                    try:
                        tool_args = json.loads(tool_args_str) if tool_args_str else {}
                    except json.JSONDecodeError as e:
                        print(f"  ⚠️ JSON解析错误: {e}")
                        print(f"  原始参数: {tool_args_str}")
                        tool_args = {}

                    print(f"  - 调用 {tool_name}，参数: {tool_args}")

                    # 执行工具
                    tool_result = self.execute_tool(tool_name, tool_args)
                    print(f"  - 结果: {tool_result}")

                    # 添加工具结果到消息
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": tool_result
                    })

                # 第二次API调用，获取最终响应
                print("\n🤖 助手: ", end="", flush=True)
                final_response = ""

                response2 = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )

                for chunk in response2:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        final_response += content

                print()
                full_response = final_response

            # 保存助手响应到记忆
            self.memory.add_to_short_term("assistant", full_response)

            # 自动提取重要信息到长期记忆
            if any(keyword in user_input for keyword in ["我叫", "我的名字", "记住", "重要"]):
                self.memory.add_to_long_term(f"用户说: {user_input}", importance=8)

        except Exception as e:
            error_msg = f"错误: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.memory.add_to_short_term("assistant", error_msg)

    def chat(self, user_input: str) -> str:
        """非流式对话（用于需要返回值的场景）"""
        self.memory.add_to_short_term("user", user_input)
        messages = self.memory.get_context_messages()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS_CONFIG
        )

        assistant_message = response.choices[0].message

        # 处理工具调用
        if assistant_message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]
            })

            for tool_call in assistant_message.tool_calls:
                tool_args = json.loads(tool_call.function.arguments)
                tool_result = self.execute_tool(tool_call.function.name, tool_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

            # 获取最终响应
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            result = final_response.choices[0].message.content
        else:
            result = assistant_message.content

        self.memory.add_to_short_term("assistant", result)
        return result

    def save_memory(self):
        """保存记忆到文件"""
        self.memory.save_to_file()
        print("💾 记忆已保存")

    def show_memory_stats(self):
        """显示记忆统计"""
        print("\n📊 记忆统计:")
        print(f"  - 短期记忆: {len(self.memory.short_term_memory)} 条")
        print(f"  - 长期记忆: {len(self.memory.long_term_memory)} 条")
        print(f"  - 用户画像: {len(self.memory.user_profile)} 项")

        if self.memory.user_profile:
            print("\n👤 用户画像:")
            for key, value in self.memory.user_profile.items():
                print(f"  - {key}: {value}")


# ============== 主程序 ==============
def main():
    """主函数 - 交互式对话"""
    print("=" * 60)
    print("🚀 通义千问 Agent 系统")
    print("=" * 60)
    print("\n功能特性:")
    print("  ✓ 流式响应 - 实时输出对话内容")
    print("  ✓ 对话历史 - 记住最近的对话")
    print("  ✓ 短期记忆 - 自动管理上下文窗口")
    print("  ✓ 长期记忆 - 保存重要信息")
    print("  ✓ 多工具调用 - 支持11种工具")
    print("  ✓ 智能分析 - 情感分析、文件管理")
    print("  ✓ 任务管理 - 待办事项、提醒功能")
    print("\n可用工具:")
    print("  1. get_current_time - 获取当前时间")
    print("  2. calculate - 数学计算")
    print("  3. search_weather - 查询天气")
    print("  4. save_note - 保存笔记")
    print("  5. search_web - 网络搜索（模拟）")
    print("  6. set_reminder - 设置提醒")
    print("  7. translate_text - 文本翻译")
    print("  8. analyze_sentiment - 情感分析")
    print("  9. get_file_info - 文件信息")
    print("  10. create_todo - 创建待办")
    print("  11. read_file - 读取文件")
    print("\n命令:")
    print("  - 输入 'exit' 退出")
    print("  - 输入 'memory' 查看记忆统计")
    print("  - 输入 'clear' 清空短期记忆")
    print("  - 输入 'help' 查看帮助")
    print("=" * 60)

    # 初始化Agent
    agent = QwenAgent(
        api_key=API_KEY,
        base_url=BASE_URL,
        model="qwen-plus"  # 或 qwen-turbo, qwen-max
    )

    # 交互循环
    while True:
        try:
            user_input = input("\n💬 你: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                agent.save_memory()
                print("\n👋 再见！记忆已保存。")
                break

            if user_input.lower() == "memory":
                agent.show_memory_stats()
                continue

            if user_input.lower() == "clear":
                agent.memory.short_term_memory = []
                print("🧹 短期记忆已清空")
                continue

            if user_input.lower() == "help":
                print("\n📖 帮助信息:")
                print("\n示例对话:")
                print("  • '现在几点了？' - 获取当前时间")
                print("  • '帮我计算 123 * 456' - 数学计算")
                print("  • '北京天气怎么样？' - 查询天气")
                print("  • '帮我保存笔记：明天开会' - 保存笔记")
                print("  • '搜索最新的AI新闻' - 网络搜索")
                print("  • '提醒我明天下午3点开会' - 设置提醒")
                print("  • '把这句话翻译成英语：你好' - 文本翻译")
                print("  • '分析情感：今天真是糟糕的一天' - 情感分析")
                print("  • '查看notes.txt文件信息' - 文件信息")
                print("  • '创建待办：完成项目报告' - 创建待办")
                print("  • '读取notes.txt文件' - 读取文件内容")
                continue

            # 流式对话
            agent.chat_stream(user_input)

        except KeyboardInterrupt:
            print("\n\n⚠️ 检测到中断...")
            agent.save_memory()
            print("👋 再见！记忆已保存。")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()