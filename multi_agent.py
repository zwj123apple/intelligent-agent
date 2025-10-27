"""
多Agent协作系统 - 实现多个专业Agent互相配合完成复杂任务
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from openai import OpenAI

from config import QWEN_API_KEY, QWEN_BASE_URL, QWEN_MODEL
from tools import Tools, TOOLS_CONFIG


class AgentRole(Enum):
    """Agent角色定义"""
    COORDINATOR = "coordinator"  # 协调者 - 任务分配和结果整合
    RESEARCHER = "researcher"    # 研究员 - 信息搜集和分析
    ANALYST = "analyst"          # 分析师 - 数据分析和洞察
    WRITER = "writer"            # 写作者 - 内容创作和总结
    CODER = "coder"              # 程序员 - 代码编写和技术实现
    CRITIC = "critic"            # 评审者 - 质量检查和改进建议


class AgentMessage:
    """Agent间的消息"""
    
    def __init__(self, 
                 sender: str,
                 receiver: str,
                 content: str,
                 message_type: str = "request",
                 metadata: Dict = None):
        self.message_id = self._generate_id()
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type  # request, response, broadcast
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
    
    @staticmethod
    def _generate_id():
        import hashlib
        import time
        return hashlib.md5(f"{time.time()}".encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class BaseAgent:
    """基础Agent类"""
    
    def __init__(self, 
                 name: str,
                 role: AgentRole,
                 system_prompt: str,
                 tools: List[str] = None):
        """
        初始化Agent
        
        Args:
            name: Agent名称
            role: Agent角色
            system_prompt: 系统提示词
            tools: 可用工具列表
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.available_tools = tools or []
        
        self.client = OpenAI(
            api_key=QWEN_API_KEY,
            base_url=QWEN_BASE_URL
        )
        self.model = QWEN_MODEL
        self.tools_instance = Tools()
        
        self.message_history: List[AgentMessage] = []
        self.task_history: List[Dict] = []
    
    def process_message(self, message: AgentMessage) -> str:
        """
        处理接收到的消息
        
        Args:
            message: 接收到的消息
            
        Returns:
            处理结果
        """
        self.message_history.append(message)
        
        # 构建对话上下文
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message.content}
        ]
        
        # 获取可用工具配置
        agent_tools = self._get_agent_tools()
        
        try:
            # 调用LLM
            if agent_tools:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=agent_tools
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
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
                
                # 执行工具
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    tool_result = self._execute_tool(tool_name, tool_args)
                    
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
            
            # 记录任务
            self.task_history.append({
                "message_id": message.message_id,
                "task": message.content,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            return result
        
        except Exception as e:
            error_msg = f"处理失败: {str(e)}"
            print(f"❌ [{self.name}] {error_msg}")
            return error_msg
    
    def _get_agent_tools(self) -> List[Dict]:
        """获取Agent可用的工具配置"""
        if not self.available_tools:
            return []
        
        return [
            tool for tool in TOOLS_CONFIG 
            if tool["function"]["name"] in self.available_tools
        ]
    
    def _execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """执行工具"""
        if hasattr(self.tools_instance, tool_name):
            method = getattr(self.tools_instance, tool_name)
            
            if not tool_args:
                return method()
            elif len(tool_args) == 1:
                return method(list(tool_args.values())[0])
            else:
                return method(**tool_args)
        
        return f"未知工具: {tool_name}"
    
    def send_message(self, receiver: str, content: str, 
                    message_type: str = "request") -> AgentMessage:
        """发送消息给其他Agent"""
        message = AgentMessage(
            sender=self.name,
            receiver=receiver,
            content=content,
            message_type=message_type
        )
        return message
    
    def get_status(self) -> Dict:
        """获取Agent状态"""
        return {
            "name": self.name,
            "role": self.role.value,
            "messages_processed": len(self.message_history),
            "tasks_completed": len(self.task_history),
            "available_tools": self.available_tools
        }


class CoordinatorAgent(BaseAgent):
    """协调者Agent - 负责任务分配和结果整合"""
    
    def __init__(self, name: str = "协调者"):
        system_prompt = """你是一个协调者Agent，负责：
1. 理解用户的复杂任务需求
2. 将任务分解为子任务
3. 分配给合适的专业Agent
4. 整合各Agent的工作结果
5. 给出最终的综合答案

你需要思考：
- 这个任务需要哪些专业能力？
- 应该按什么顺序完成子任务？
- 如何整合各部分结果？

可用的专业Agent：
- 研究员(researcher): 搜集信息、调研
- 分析师(analyst): 数据分析、洞察
- 写作者(writer): 内容创作、总结
- 程序员(coder): 代码编写、技术实现
- 评审者(critic): 质量检查、改进建议
"""
        super().__init__(name, AgentRole.COORDINATOR, system_prompt)
    
    def plan_task(self, user_request: str) -> Dict:
        """规划任务执行"""
        planning_prompt = f"""
用户请求：{user_request}

请制定执行计划，输出JSON格式：
{{
    "task_analysis": "任务分析",
    "sub_tasks": [
        {{
            "step": 1,
            "agent": "agent_role",
            "task": "具体任务描述",
            "depends_on": []
        }}
    ],
    "expected_outcome": "预期结果"
}}
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": planning_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            result = response.choices[0].message.content
            
            # 尝试解析JSON
            try:
                # 提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                    return plan
            except:
                pass
            
            # 如果解析失败，返回文本计划
            return {
                "task_analysis": result,
                "sub_tasks": [],
                "expected_outcome": "见任务分析"
            }
        
        except Exception as e:
            print(f"❌ 任务规划失败: {str(e)}")
            return {"error": str(e)}


class ResearcherAgent(BaseAgent):
    """研究员Agent - 负责信息搜集和调研"""
    
    def __init__(self, name: str = "研究员"):
        system_prompt = """你是一个研究员Agent，擅长：
1. 信息搜集和网络搜索
2. 知识库查询
3. 数据收集和整理
4. 背景调研和文献综述

工作原则：
- 全面搜集相关信息
- 多渠道验证信息准确性
- 结构化整理研究结果
- 标注信息来源
"""
        tools = ["search_web", "search_knowledge", "get_current_time"]
        super().__init__(name, AgentRole.RESEARCHER, system_prompt, tools)


class AnalystAgent(BaseAgent):
    """分析师Agent - 负责数据分析和洞察"""
    
    def __init__(self, name: str = "分析师"):
        system_prompt = """你是一个分析师Agent，擅长：
1. 数据分析和统计
2. 趋势识别和预测
3. 逻辑推理和论证
4. 洞察提取和建议

工作原则：
- 基于数据和事实分析
- 使用科学的分析方法
- 提供可操作的洞察
- 清晰表达分析结论
"""
        tools = ["calculate", "analyze_sentiment", "get_knowledge_stats"]
        super().__init__(name, AgentRole.ANALYST, system_prompt, tools)


class WriterAgent(BaseAgent):
    """写作者Agent - 负责内容创作和总结"""
    
    def __init__(self, name: str = "写作者"):
        system_prompt = """你是一个写作者Agent，擅长：
1. 内容创作和撰写
2. 信息整合和总结
3. 报告和文档编写
4. 优化表达和润色

工作原则：
- 清晰准确的表达
- 结构化的内容组织
- 适应不同的写作风格
- 重视可读性和逻辑性
"""
        tools = ["add_knowledge", "save_note", "translate_text"]
        super().__init__(name, AgentRole.WRITER, system_prompt, tools)


class CoderAgent(BaseAgent):
    """程序员Agent - 负责代码编写和技术实现"""
    
    def __init__(self, name: str = "程序员"):
        system_prompt = """你是一个程序员Agent，擅长：
1. 代码编写和实现
2. 算法设计和优化
3. 技术方案设计
4. 代码审查和调试

工作原则：
- 编写清晰可维护的代码
- 遵循最佳实践和规范
- 考虑性能和可扩展性
- 提供详细的技术说明
"""
        tools = ["calculate", "read_file", "get_file_info"]
        super().__init__(name, AgentRole.CODER, system_prompt, tools)


class CriticAgent(BaseAgent):
    """评审者Agent - 负责质量检查和改进建议"""
    
    def __init__(self, name: str = "评审者"):
        system_prompt = """你是一个评审者Agent，擅长：
1. 质量检查和评估
2. 找出问题和不足
3. 提供改进建议
4. 确保输出质量

工作原则：
- 客观公正的评价
- 建设性的批评
- 具体可行的建议
- 关注细节和完整性
"""
        super().__init__(name, AgentRole.CRITIC, system_prompt)


class MultiAgentSystem:
    """多Agent协作系统"""
    
    def __init__(self):
        """初始化多Agent系统"""
        # 创建各个Agent
        self.coordinator = CoordinatorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.coder = CoderAgent()
        self.critic = CriticAgent()
        
        # Agent注册表
        self.agents: Dict[str, BaseAgent] = {
            "coordinator": self.coordinator,
            "researcher": self.researcher,
            "analyst": self.analyst,
            "writer": self.writer,
            "coder": self.coder,
            "critic": self.critic
        }
        
        # 消息队列
        self.message_queue: List[AgentMessage] = []
        
        # 执行历史
        self.execution_history: List[Dict] = []
    
    def execute_task(self, user_request: str, verbose: bool = True) -> str:
        """
        执行用户任务
        
        Args:
            user_request: 用户请求
            verbose: 是否显示详细过程
            
        Returns:
            最终结果
        """
        if verbose:
            print("=" * 70)
            print("🚀 多Agent协作系统启动")
            print("=" * 70)
            print(f"\n📋 用户请求: {user_request}\n")
        
        # 1. 协调者制定计划
        if verbose:
            print("🧠 [协调者] 正在分析任务并制定执行计划...")
        
        plan = self.coordinator.plan_task(user_request)
        
        if "error" in plan:
            return f"❌ 任务规划失败: {plan['error']}"
        
        if verbose:
            print(f"\n📊 执行计划:")
            print(f"  任务分析: {plan.get('task_analysis', '无')[:100]}...")
            if plan.get('sub_tasks'):
                print(f"  子任务数: {len(plan['sub_tasks'])}")
        
        # 2. 执行子任务
        results = {}
        
        if plan.get('sub_tasks'):
            for sub_task in plan['sub_tasks']:
                agent_role = sub_task.get('agent', 'researcher')
                task_desc = sub_task.get('task', '')
                step = sub_task.get('step', 0)
                
                if verbose:
                    print(f"\n{'='*70}")
                    print(f"📍 步骤 {step}: [{agent_role.upper()}]")
                    print(f"   任务: {task_desc}")
                    print(f"{'='*70}")
                
                # 获取对应的Agent
                agent = self.agents.get(agent_role)
                if not agent:
                    if verbose:
                        print(f"⚠️ 未找到Agent: {agent_role}")
                    continue
                
                # 创建消息
                message = AgentMessage(
                    sender="coordinator",
                    receiver=agent_role,
                    content=task_desc,
                    metadata={"step": step, "user_request": user_request}
                )
                
                # Agent处理任务
                if verbose:
                    print(f"⏳ [{agent.name}] 正在处理...")
                
                result = agent.process_message(message)
                results[f"step_{step}"] = {
                    "agent": agent_role,
                    "task": task_desc,
                    "result": result
                }
                
                if verbose:
                    print(f"✅ [{agent.name}] 完成")
                    print(f"   结果预览: {result[:200]}...")
        
        # 3. 整合结果
        if verbose:
            print(f"\n{'='*70}")
            print("🔄 [协调者] 正在整合所有结果...")
        
        # 构建整合提示
        integration_prompt = f"""
用户请求：{user_request}

各Agent的工作结果：
"""
        for key, value in results.items():
            integration_prompt += f"\n{key} - {value['agent']}:\n{value['result']}\n"
        
        integration_prompt += "\n请整合以上结果，给出最终的综合答案。"
        
        final_message = AgentMessage(
            sender="system",
            receiver="coordinator",
            content=integration_prompt
        )
        
        final_result = self.coordinator.process_message(final_message)
        
        # 4. 质量检查（可选）
        if verbose:
            print(f"\n🔍 [评审者] 正在进行质量检查...")
        
        critic_message = AgentMessage(
            sender="coordinator",
            receiver="critic",
            content=f"请评审以下结果的质量并提供改进建议：\n\n{final_result}"
        )
        
        critic_feedback = self.critic.process_message(critic_message)
        
        # 记录执行历史
        self.execution_history.append({
            "request": user_request,
            "plan": plan,
            "results": results,
            "final_result": final_result,
            "critic_feedback": critic_feedback,
            "timestamp": datetime.now().isoformat()
        })
        
        if verbose:
            print(f"\n{'='*70}")
            print("✨ 任务完成")
            print(f"{'='*70}\n")
            print(f"📝 最终结果:\n{final_result}")
            print(f"\n💡 评审意见:\n{critic_feedback}")
        
        return final_result
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "agents": {
                name: agent.get_status() 
                for name, agent in self.agents.items()
            },
            "total_tasks": len(self.execution_history),
            "message_queue_size": len(self.message_queue)
        }
    
    def show_status(self):
        """显示系统状态"""
        status = self.get_system_status()
        
        print("\n📊 多Agent系统状态:")
        print(f"  已完成任务: {status['total_tasks']}")
        print(f"  消息队列: {status['message_queue_size']}")
        
        print("\n🤖 各Agent状态:")
        for name, agent_status in status['agents'].items():
            print(f"\n  [{agent_status['name']}]")
            print(f"    角色: {agent_status['role']}")
            print(f"    已处理消息: {agent_status['messages_processed']}")
            print(f"    已完成任务: {agent_status['tasks_completed']}")
            if agent_status['available_tools']:
                print(f"    可用工具: {', '.join(agent_status['available_tools'][:3])}...")


# 便捷函数
def create_multi_agent_system() -> MultiAgentSystem:
    """创建多Agent系统"""
    return MultiAgentSystem()


def run_multi_agent_task(task: str, verbose: bool = True) -> str:
    """运行多Agent任务"""
    system = create_multi_agent_system()
    return system.execute_task(task, verbose=verbose)