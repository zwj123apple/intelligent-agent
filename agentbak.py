"""
Agent核心逻辑 - 处理对话和工具调用
"""

import json
from typing import Dict
from openai import OpenAI

from config import *
from memory import Memory
from tools import Tools, TOOLS_CONFIG


class QwenAgent:
    """通义千问Agent主类"""

    def __init__(self, 
                 api_key: str = QWEN_API_KEY,
                 base_url: str = QWEN_BASE_URL,
                 model: str = QWEN_MODEL):
        """
        初始化Agent
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.memory = Memory()
        self.tools = Tools()

        # 加载历史记忆
        self.memory.load_from_file()

        print(f"✅ Agent初始化完成！")
        print(f"   模型: {model}")
        print(f"   记忆: {self.memory.get_stats()}")

    def execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """
        执行工具调用
        
        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            
        Returns:
            工具执行结果
        """
        try:
            # 使用反射调用工具方法
            if hasattr(self.tools, tool_name):
                method = getattr(self.tools, tool_name)
                
                # 根据参数调用
                if not tool_args:
                    return method()
                elif len(tool_args) == 1:
                    arg_value = list(tool_args.values())[0]
                    return method(arg_value)
                else:
                    return method(**tool_args)
            else:
                return f"❌ 未知工具: {tool_name}"
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"❌ 工具执行错误: {str(e)}"

    def chat_stream(self, user_input: str):
        """
        流式对话
        
        Args:
            user_input: 用户输入
        """
        print(f"\n👤 用户: {user_input}")

        # 添加用户消息到记忆
        self.memory.add_to_short_term("user", user_input)

        # 获取上下文消息
        messages = self.memory.get_context_messages()

        print("🤖 助手: ", end="", flush=True)

        full_response = ""
        tool_calls_dict = {}  # 使用字典存储工具调用

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

                    print(f"  📍 调用 {tool_name}")
                    if tool_args:
                        print(f"     参数: {tool_args}")

                    # 执行工具
                    tool_result = self.execute_tool(tool_name, tool_args)
                    print(f"  ✅ 结果: {tool_result}")

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
            if full_response:
                self.memory.add_to_short_term("assistant", full_response)

            # 自动提取重要信息到长期记忆
            self._extract_important_info(user_input, full_response)

        except Exception as e:
            error_msg = f"❌ 错误: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.memory.add_to_short_term("assistant", error_msg)

    def chat(self, user_input: str) -> str:
        """
        非流式对话（用于需要返回值的场景）
        
        Args:
            user_input: 用户输入
            
        Returns:
            助手回复
        """
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
        self._extract_important_info(user_input, result)
        
        return result

    def _extract_important_info(self, user_input: str, assistant_response: str):
        """从对话中提取重要信息"""
        # 检测用户自我介绍
        intro_keywords = ["我叫", "我的名字", "我是"]
        for keyword in intro_keywords:
            if keyword in user_input:
                self.memory.add_to_long_term(f"用户说: {user_input}", importance=9)
                # 尝试提取名字
                if "我叫" in user_input:
                    try:
                        name = user_input.split("我叫")[1].split()[0].strip("，。！？")
                        self.memory.update_user_profile("姓名", name)
                    except:
                        pass
                break
        
        # 检测重要信息标记
        if any(kw in user_input for kw in ["记住", "重要", "别忘了"]):
            self.memory.add_to_long_term(f"用户说: {user_input}", importance=8)
        
        # 检测偏好信息
        if any(kw in user_input for kw in ["喜欢", "讨厌", "爱", "恨"]):
            self.memory.add_to_long_term(f"用户偏好: {user_input}", importance=7)

    def save_memory(self):
        """保存记忆到文件"""
        self.memory.save_to_file()
        print("💾 记忆已保存")

    def show_memory_stats(self):
        """显示记忆统计"""
        stats = self.memory.get_stats()
        print("\n📊 记忆统计:")
        print(f"  • 短期记忆: {stats['short_term_count']} 条")
        print(f"  • 长期记忆: {stats['long_term_count']} 条")
        print(f"  • 用户画像: {stats['user_profile_count']} 项")
        print(f"  • 对话轮次: {stats['total_conversations']} 轮")

        if self.memory.user_profile:
            print("\n👤 用户画像:")
            for key, value in self.memory.user_profile.items():
                print(f"  • {key}: {value['value']}")
        
        if self.memory.long_term_memory:
            print("\n🧠 重要记忆 (前5条):")
            top_memories = sorted(
                self.memory.long_term_memory,
                key=lambda x: x["importance"],
                reverse=True
            )[:5]
            for mem in top_memories:
                print(f"  • [{mem['importance']}⭐] {mem['summary']}")

    def clear_memory(self, memory_type: str = "short"):
        """
        清空记忆
        
        Args:
            memory_type: 记忆类型 ('short', 'long', 'all')
        """
        if memory_type == "short":
            self.memory.clear_short_term()
        elif memory_type == "all":
            self.memory.clear_all()
        else:
            print("⚠️ 未知的记忆类型")

    def search_memory(self, keyword: str):
        """搜索记忆"""
        results = self.memory.search_memory(keyword)
        
        if not results:
            print(f"\n🔍 未找到包含 '{keyword}' 的记忆")
            return
        
        print(f"\n🔍 搜索结果 (共 {len(results)} 条):")
        for result in results:
            if result["type"] == "short_term":
                role = {"user": "👤", "assistant": "🤖"}.get(result["role"], "")
                print(f"\n  {role} [{result['timestamp']}]")
                print(f"  {result['content'][:100]}...")
            else:
                print(f"\n  🧠 [{result['importance']}⭐] {result['summary']}")
                print(f"     时间: {result['timestamp']}")

    def export_memory(self, filename: str = None):
        """导出记忆"""
        if filename:
            self.memory.export_to_text(filename)
        else:
            self.memory.export_to_text()