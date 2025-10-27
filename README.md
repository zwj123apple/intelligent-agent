\# 🚀 通义千问智能Agent系统 v2.0



一个功能完整的智能# 🚀 通义千问智能Agent系统 v2.0



一个功能完整的智能Agent系统，支持单Agent快速响应和多Agent团队协作，集成通义千问大模型、知识库管理、真实API调用等功能。



\## ✨ 核心特性



\### 🤖 双模式运行

\- \*\*单Agent模式\*\* - 个人助手，快速响应日常任务

\- \*\*多Agent模式\*\* - 团队协作，处理复杂项目



\### 💡 主要功能

\- 🔄 \*\*流式响应\*\* - 实时打字机效果输出

\- 🧠 \*\*智能记忆\*\* - 短期/长期记忆管理，用户画像

\- 🛠️ \*\*19种工具\*\* - 覆盖搜索、计算、翻译、文件、知识库等

\- 📚 \*\*知识库系统\*\* - 文档管理、全文检索、知识图谱

\- 👥 \*\*多Agent协作\*\* - 6个专业Agent分工合作

\- 🌐 \*\*真实API集成\*\* - 天气、搜索、翻译等API

\- 💾 \*\*数据持久化\*\* - 自动保存对话和知识



\## 📁 项目结构



```

intelligent-agent/

├── config.py                 # 配置文件（API密钥、系统配置）

├── tools.py                  # 工具实现（19种工具 + 真实API）

├── memory.py                 # 记忆管理模块

├── agent.py                  # 单Agent核心逻辑

├── knowledge\_base.py         # 知识库系统

├── kb\_tools.py              # 知识库工具集成

├── multi\_agent.py           # 多Agent协作系统

├── multi\_agent\_examples.py  # 多Agent使用示例

├── main.py                  # 主程序入口（双模式）

├── requirements.txt         # 依赖包列表

├── README.md               # 项目文档（本文件）

├── KNOWLEDGE\_BASE\_GUIDE.md # 知识库使用指南

├── MULTI\_AGENT\_GUIDE.md    # 多Agent系统指南

├── .env.example            # 环境变量模板

├── .gitignore              # Git忽略文件

└── data/                   # 数据存储目录

&nbsp;   ├── memory.json         # 对话记忆

&nbsp;   ├── knowledge\_base/     # 知识库数据

&nbsp;   ├── notes.txt          # 笔记

&nbsp;   ├── todos.json         # 待办事项

&nbsp;   └── reminders.txt      # 提醒事项

```



\## 🚀 快速开始



\### 1. 安装依赖



```bash

pip install -r requirements.txt

```



\### 2. 配置API密钥



编辑 `config.py` 文件，设置API密钥：



```python

\# 通义千问API（必需）

QWEN\_API\_KEY = "your\_qwen\_api\_key"



\# 以下API为可选，不配置则使用模拟数据

WEATHER\_API\_KEY = "your\_weather\_api\_key"      # 和风天气

SERPER\_API\_KEY = "your\_serper\_api\_key"        # Google搜索

BAIDU\_TRANSLATE\_APP\_ID = "your\_app\_id"        # 百度翻译

BAIDU\_TRANSLATE\_SECRET\_KEY = "your\_secret"

```



\### 3. 运行程序



```bash

python main.py

```



系统会提示选择模式：

\- \*\*模式1：单Agent\*\* - 适合日常对话和简单任务

\- \*\*模式2：多Agent\*\* - 适合复杂任务和深度分析



\## 🤖 单Agent模式



\### 功能特点

\- ⚡ 快速响应

\- 💬 流式对话

\- 🧠 记忆管理

\- 🛠️ 19种工具



\### 使用示例



```python

💬 你: 现在几点？北京天气怎么样？



🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 get\_current\_time

&nbsp; ✅ 结果: 2024-01-15 14:30:25

&nbsp; 📍 调用 search\_weather

&nbsp;    参数: {'city': '北京'}

&nbsp; ✅ 结果: 北京天气：晴天，温度 15°C...



🤖 助手: 现在是下午2点30分。北京今天天气晴朗...

```



\### 支持的工具



| 分类 | 工具 | 功能 |

|-----|------|------|

| \*\*基础工具\*\* | get\_current\_time | 获取当前时间 |

| | calculate | 数学计算 |

| \*\*信息查询\*\* | search\_weather | 天气查询 |

| | search\_web | 网络搜索 |

| \*\*语言处理\*\* | translate\_text | 文本翻译 |

| | analyze\_sentiment | 情感分析 |

| \*\*文件操作\*\* | save\_note | 保存笔记 |

| | read\_file | 读取文件 |

| | get\_file\_info | 文件信息 |

| \*\*任务管理\*\* | create\_todo | 创建待办 |

| | set\_reminder | 设置提醒 |

| \*\*知识库\*\* | add\_knowledge | 添加知识 |

| | search\_knowledge | 搜索知识 |

| | get\_knowledge\_detail | 知识详情 |

| | list\_knowledge\_categories | 列出分类 |

| | get\_knowledge\_stats | 知识统计 |

| | import\_knowledge\_from\_file | 导入文件 |

| | search\_knowledge\_graph | 知识图谱 |

| | export\_knowledge\_base | 导出知识库 |



\## 👥 多Agent模式



\### 6个专业Agent



| Agent | 角色 | 擅长领域 | 可用工具 |

|-------|-----|---------|---------|

| \*\*协调者\*\* | 总指挥 | 任务规划、结果整合 | - |

| \*\*研究员\*\* | 信息搜集 | 网络搜索、调研 | search\_web, search\_knowledge |

| \*\*分析师\*\* | 数据分析 | 统计分析、洞察提取 | calculate, analyze\_sentiment |

| \*\*写作者\*\* | 内容创作 | 文档撰写、内容总结 | add\_knowledge, save\_note |

| \*\*程序员\*\* | 代码开发 | 代码编写、技术实现 | calculate, read\_file |

| \*\*评审者\*\* | 质量检查 | 评估改进、质量保证 | - |



\### 协作流程



```

用户任务 → 协调者(规划)

&nbsp;          ↓

&nbsp;    \[子任务分配]

&nbsp;          ↓

&nbsp; 研究员 → 分析师 → 写作者

&nbsp;          ↓

&nbsp;      评审者(检查)

&nbsp;          ↓

&nbsp;    协调者(整合)

&nbsp;          ↓

&nbsp;      最终结果

```



\### 使用示例



```python

💬 任务: 研究AI大模型发展趋势，分析应用场景，撰写技术报告



🧠 \[协调者] 正在分析任务并制定执行计划...



📊 执行计划:

&nbsp; 任务分析: 该任务需要研究、分析和写作三个环节

&nbsp; 子任务数: 3



======================================================================

📍 步骤 1: \[RESEARCHER]

&nbsp;  任务: 搜集AI大模型的最新进展和应用案例

======================================================================

⏳ \[研究员] 正在处理...

✅ \[研究员] 完成

&nbsp;  结果预览: AI大模型在2024年持续发展，主要进展包括...



======================================================================

📍 步骤 2: \[ANALYST]

&nbsp;  任务: 分析技术趋势和应用场景

======================================================================

⏳ \[分析师] 正在处理...

✅ \[分析师] 完成



======================================================================

📍 步骤 3: \[WRITER]

&nbsp;  任务: 撰写技术报告

======================================================================

⏳ \[写作者] 正在处理...

✅ \[写作者] 完成



🔄 \[协调者] 正在整合所有结果...

🔍 \[评审者] 正在进行质量检查...



✨ 任务完成

======================================================================



📝 最终结果:

\[完整的技术报告内容...]



💡 评审意见:

报告结构清晰，内容全面。建议补充具体案例...

```



\## 📚 知识库系统



\### 核心功能

\- 📝 文档管理（增删改查）

\- 🏷️ 标签和分类

\- 🔍 全文搜索

\- 🧠 知识图谱

\- 📊 统计分析

\- 📥📤 批量导入导出



\### 使用示例



```python

\# 添加知识

💬 你: 帮我记住：Python装饰器是一种设计模式，可以在不修改函数的情况下扩展功能



\# 搜索知识

💬 你: 搜索Python相关的知识



\# 查看统计

💬 你: 查看知识库统计



\# 知识图谱

💬 你: 在知识图谱中搜索"Python"，看看有哪些关联

```



详细使用方法请参考 \[知识库使用指南](KNOWLEDGE\_BASE\_GUIDE.md)



\## 💡 使用场景



\### 单Agent适合场景

\- 日常对话交流

\- 快速信息查询

\- 简单计算任务

\- 笔记记录

\- 知识查询



\### 多Agent适合场景

\- 研究报告生成

\- 代码开发项目

\- 数据分析任务

\- 内容创作

\- 技术方案设计

\- 知识整理



\## 🎯 实战示例



\### 示例1：研究报告（多Agent）



```python

任务: 研究量子计算的发展现状，分析技术挑战，撰写研究报告



执行流程:

1\. 研究员 - 搜集量子计算相关信息

2\. 分析师 - 分析技术发展趋势

3\. 写作者 - 撰写研究报告

4\. 评审者 - 质量检查

5\. 协调者 - 整合结果



输出: 完整的研究报告 + 评审意见

```



\### 示例2：知识管理（单Agent + 知识库）



```python

\# 1. 添加学习笔记

💬 你: 帮我记住今天学习的内容：Python生成器使用yield关键字，可以节省内存。标签：Python,生成器



\# 2. 搜索复习

💬 你: 搜索Python相关的学习笔记



\# 3. 查看学习进度

💬 你: 查看知识库统计，看看我学了多少内容



\# 4. 导出复习材料

💬 你: 导出知识库，我要复习

```



\### 示例3：数据分析（多Agent）



```python

任务: 分析电商平台用户行为数据，识别流失原因，提出改进建议



执行流程:

1\. 研究员 - 调研行业最佳实践

2\. 分析师 - 分析用户行为数据

3\. 分析师 - 识别关键指标和流失原因

4\. 写作者 - 撰写分析报告

5\. 评审者 - 评审分析质量



输出: 数据分析报告 + 可执行建议

```



\## 📝 命令参考



\### 通用命令

```bash

help              # 查看帮助

mode single       # 切换到单Agent模式

mode multi        # 切换到多Agent模式

config            # 显示配置信息

exit / quit       # 退出程序

```



\### 单Agent模式命令

```bash

memory            # 查看记忆统计

search <关键词>   # 搜索记忆

clear             # 清空短期记忆

export            # 导出记忆

```



\### 多Agent模式命令

```bash

status            # 查看系统状态

examples          # 查看示例任务

```



\## 🌐 API集成



\### 已集成的真实API



| 服务 | 用途 | 注册地址 | 免费额度 |

|------|------|---------|---------|

| 通义千问 | 大模型 | https://dashscope.aliyun.com/ | 按量计费 |

| 和风天气 | 天气查询 | https://dev.qweather.com/ | 1000次/天 |

| Serper | Google搜索 | https://serper.dev/ | 2500次/月 |

| 百度翻译 | 文本翻译 | https://fanyi-api.baidu.com/ | 200万字符/月 |

| 百度NLP | 情感分析 | https://ai.baidu.com/ | 50000次/天 |



\### 配置说明



在 `config.py` 中配置API开关：



```python

USE\_REAL\_WEATHER\_API = True    # 启用真实天气API

USE\_REAL\_SEARCH\_API = True     # 启用真实搜索API

USE\_REAL\_TRANSLATE\_API = True  # 启用真实翻译API

USE\_REAL\_SENTIMENT\_API = False # 使用本地情感分析

```



\## 🔧 高级功能



\### 1. 自定义Agent



```python

from multi\_agent import BaseAgent, AgentRole



class DataScientistAgent(BaseAgent):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       system\_prompt = "你是数据科学家..."

&nbsp;       tools = \["calculate", "analyze\_sentiment"]

&nbsp;       super().\_\_init\_\_("数据科学家", AgentRole.ANALYST, 

&nbsp;                       system\_prompt, tools)



\# 集成到系统

system = MultiAgentSystem()

system.agents\["data\_scientist"] = DataScientistAgent()

```



\### 2. 批量知识导入



```python

from knowledge\_base import KnowledgeBase



kb = KnowledgeBase()

\# 从目录批量导入

count = kb.import\_from\_directory("/path/to/docs", 

&nbsp;                               category="学习笔记")

print(f"导入了 {count} 篇文档")

```



\### 3. 知识图谱可视化



```python

kb = KnowledgeBase()

kg = kb.knowledge\_graph



\# 查看实体关系

entity = kg.get\_entity("Python")

related = kg.get\_related\_entities("Python", max\_depth=2)

relationships = kg.get\_entity\_relationships("Python")

```



\## 📊 性能优化建议



1\. \*\*记忆管理\*\*

&nbsp;  - 定期清理过期记忆

&nbsp;  - 控制短期记忆数量



2\. \*\*知识库\*\*

&nbsp;  - 合理使用标签和分类

&nbsp;  - 定期导出备份



3\. \*\*多Agent\*\*

&nbsp;  - 清晰的任务描述

&nbsp;  - 避免过度复杂的任务链



4\. \*\*API调用\*\*

&nbsp;  - 控制调用频率

&nbsp;  - 合理使用缓存



\## 🐛 故障排查



\### 问题1：API调用失败

\*\*解决方案：\*\*

```python

\# 检查配置

from config import print\_config

print\_config()



\# 测试API连接

from tools import Tools

tools = Tools()

result = tools.search\_weather("北京")  # 测试天气API

```



\### 问题2：知识库加载失败

\*\*解决方案：\*\*

```bash

\# 检查数据目录

ls data/knowledge\_base/



\# 重新初始化

rm -rf data/knowledge\_base/

python main.py  # 自动重建

```



\### 问题3：多Agent无响应

\*\*解决方案：\*\*

\- 启用详细输出: `verbose=True`

\- 检查任务描述是否清晰

\- 查看错误日志



\## 📈 更新日志



\### v2.0 (当前版本)

\- ✅ 新增多Agent协作系统

\- ✅ 集成知识库管理

\- ✅ 支持双模式运行

\- ✅ 19种工具集成

\- ✅ 真实API支持



\### v1.0

\- ✅ 基础单Agent实现

\- ✅ 工具调用系统

\- ✅ 记忆管理

\- ✅ 流式响应



\## 🚀 未来规划



\- \[ ] Web可视化界面

\- \[ ] 向量检索（语义搜索）

\- \[ ] Agent学习和优化

\- \[ ] 更多专业Agent

\- \[ ] 分布式部署

\- \[ ] 实时监控面板

\- \[ ] 插件系统

\- \[ ] 多模态支持



\## 📚 文档资源



\- \[知识库使用指南](KNOWLEDGE\_BASE\_GUIDE.md)

\- \[多Agent系统指南](MULTI\_AGENT\_GUIDE.md)

\- \[API集成说明](config.py)

\- \[工具开发指南](tools.py)



\## 🤝 贡献指南



欢迎提交Issue和Pull Request！



\## 📄 许可证



MIT License



\## 💬 联系方式



如有问题，请提交GitHub Issue。



---



\*\*开始使用智能Agent系统，体验AI协作的力量！\*\* 🚀✨Agent系统，支持单Agent快速响应和多Agent团队协作，集成通义千问大模型、知识库管理、真实API调用等功能。



\## ✨ 核心特性



\### 🤖 双模式运行

\- \*\*单Agent模式\*\* - 个人助手，快速响应日常任务

\- \*\*多Agent模式\*\* - 团队协作，处理复杂项目



\### 💡 主要功能

\- 🔄 \*\*流式响应\*\* - 实时打字机效果输出

\- 🧠 \*\*智能记忆\*\* - 短期/长期记忆管理，用户画像

\- 🛠️ \*\*19种工具\*\* - 覆盖搜索、计算、翻译、文件、知识库等

\- 📚 \*\*知识库系统\*\* - 文档管理、全文检索、知识图谱

\- 👥 \*\*多Agent协作\*\* - 6个专业Agent分工合作

\- 🌐 \*\*真实API集成\*\* - 天气、搜索、翻译等API

\- 💾 \*\*数据持久化\*\* - 自动保存对话和知识



\## 📁 项目结构



```

intelligent-agent/

├── config.py                 # 配置文件（API密钥、系统配置）

├── tools.py                  # 工具实现（19种工具 + 真实API）

├── memory.py                 # 记忆管理模块

├── agent.py                  # 单Agent核心逻辑

├── knowledge\_base.py         # 知识库系统

├── kb\_tools.py              # 知识库工具集成

├── multi\_agent.py           # 多Agent协作系统

├── multi\_agent\_examples.py  # 多Agent使用示例

├── main.py                  # 主程序入口（双模式）

├── requirements.txt         # 依赖包列表

├── README.md               # 项目文档（本文件）

├── KNOWLEDGE\_BASE\_GUIDE.md # 知识库使用指南

├── MULTI\_AGENT\_GUIDE.md    # 多Agent系统指南

├── .env.example            # 环境变量模板

├── .gitignore              # Git忽略文件

└── data/                   # 数据存储目录

&nbsp;   ├── memory.json         # 对话记忆

&nbsp;   ├── knowledge\_base/     # 知识库数据

&nbsp;   ├── notes.txt          # 笔记

&nbsp;   ├── todos.json         # 待办事项

&nbsp;   └── reminders.txt      # 提醒事项

```



\## 🚀 快速开始



\### 1. 安装依赖



```bash

pip install -r requirements.txt

```



\### 2. 配置API密钥



编辑 `config.py` 文件，设置API密钥：



```python

\# 通义千问API（必需）

QWEN\_API\_KEY = "your\_qwen\_api\_key"



\# 以下API为可选，不配置则使用模拟数据

WEATHER\_API\_KEY = "your\_weather\_api\_key"      # 和风天气

SERPER\_API\_KEY = "your\_serper\_api\_key"        # Google搜索

BAIDU\_TRANSLATE\_APP\_ID = "your\_app\_id"        # 百度翻译

BAIDU\_TRANSLATE\_SECRET\_KEY = "your\_secret"

```



\### 3. 运行程序



```bash

python main.py

```



系统会提示选择模式：

\- \*\*模式1：单Agent\*\* - 适合日常对话和简单任务

\- \*\*模式2：多Agent\*\* - 适合复杂任务和深度分析



\## 🤖 单Agent模式



\### 功能特点

\- ⚡ 快速响应

\- 💬 流式对话

\- 🧠 记忆管理

\- 🛠️ 19种工具



\### 使用示例



```python

💬 你: 现在几点？北京天气怎么样？



🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 get\_current\_time

&nbsp; ✅ 结果: 2024-01-15 14:30:25

&nbsp; 📍 调用 search\_weather

&nbsp;    参数: {'city': '北京'}

&nbsp; ✅ 结果: 北京天气：晴天，温度 15°C...



🤖 助手: 现在是下午2点30分。北京今天天气晴朗...

```



\### 支持的工具



| 分类 | 工具 | 功能 |

|-----|------|------|

| \*\*基础工具\*\* | get\_current\_time | 获取当前时间 |

| | calculate | 数学计算 |

| \*\*信息查询\*\* | search\_weather | 天气查询 |

| | search\_web | 网络搜索 |

| \*\*语言处理\*\* | translate\_text | 文本翻译 |

| | analyze\_sentiment | 情感分析 |

| \*\*文件操作\*\* | save\_note | 保存笔记 |

| | read\_file | 读取文件 |

| | get\_file\_info | 文件信息 |

| \*\*任务管理\*\* | create\_todo | 创建待办 |

| | set\_reminder | 设置提醒 |

| \*\*知识库\*\* | add\_knowledge | 添加知识 |

| | search\_knowledge | 搜索知识 |

| | get\_knowledge\_detail | 知识详情 |

| | list\_knowledge\_categories | 列出分类 |

| | get\_knowledge\_stats | 知识统计 |

| | import\_knowledge\_from\_file | 导入文件 |

| | search\_knowledge\_graph | 知识图谱 |

| | export\_knowledge\_base | 导出知识库 |



\## 👥 多Agent模式



\### 6个专业Agent



| Agent | 角色 | 擅长领域 | 可用工具 |

|-------|-----|---------|---------|

| \*\*协调者\*\* | 总指挥 | 任务规划、结果整合 | - |

| \*\*研究员\*\* | 信息搜集 | 网络搜索、调研 | search\_web, search\_knowledge |

| \*\*分析师\*\* | 数据分析 | 统计分析、洞察提取 | calculate, analyze\_sentiment |

| \*\*写作者\*\* | 内容创作 | 文档撰写、内容总结 | add\_knowledge, save\_note |

| \*\*程序员\*\* | 代码开发 | 代码编写、技术实现 | calculate, read\_file |

| \*\*评审者\*\* | 质量检查 | 评估改进、质量保证 | - |



\### 协作流程



```

用户任务 → 协调者(规划)

&nbsp;          ↓

&nbsp;    \[子任务分配]

&nbsp;          ↓

&nbsp; 研究员 → 分析师 → 写作者

&nbsp;          ↓

&nbsp;      评审者(检查)

&nbsp;          ↓

&nbsp;    协调者(整合)

&nbsp;          ↓

&nbsp;      最终结果

```



\### 使用示例



```python

💬 任务: 研究AI大模型发展趋势，分析应用场景，撰写技术报告



🧠 \[协调者] 正在分析任务并制定执行计划...



📊 执行计划:

&nbsp; 任务分析: 该任务需要研究、分析和写作三个环节

&nbsp; 子任务数: 3



======================================================================

📍 步骤 1: \[RESEARCHER]

&nbsp;  任务: 搜集AI大模型的最新进展和应用案例

======================================================================

⏳ \[研究员] 正在处理...

✅ \[研究员] 完成

&nbsp;  结果预览: AI大模型在2024年持续发展，主要进展包括...



======================================================================

📍 步骤 2: \[ANALYST]

&nbsp;  任务: 分析技术趋势和应用场景

======================================================================

⏳ \[分析师] 正在处理...

✅ \[分析师] 完成



======================================================================

📍 步骤 3: \[WRITER]

&nbsp;  任务: 撰写技术报告

======================================================================

⏳ \[写作者] 正在处理...

✅ \[写作者] 完成



🔄 \[协调者] 正在整合所有结果...

🔍 \[评审者] 正在进行质量检查...



✨ 任务完成

======================================================================



📝 最终结果:

\[完整的技术报告内容...]



💡 评审意见:

报告结构清晰，内容全面。建议补充具体案例...

```



\## 📚 知识库系统



\### 核心功能

\- 📝 文档管理（增删改查）

\- 🏷️ 标签和分类

\- 🔍 全文搜索

\- 🧠 知识图谱

\- 📊 统计分析

\- 📥📤 批量导入导出



\### 使用示例



```python

\# 添加知识

💬 你: 帮我记住：Python装饰器是一种设计模式，可以在不修改函数的情况下扩展功能



\# 搜索知识

💬 你: 搜索Python相关的知识



\# 查看统计

💬 你: 查看知识库统计



\# 知识图谱

💬 你: 在知识图谱中搜索"Python"，看看有哪些关联

```



详细使用方法请参考 \[知识库使用指南](KNOWLEDGE\_BASE\_GUIDE.md)



\## 💡 使用场景



\### 单Agent适合场景

\- 日常对话交流

\- 快速信息查询

\- 简单计算任务

\- 笔记记录

\- 知识查询



\### 多Agent适合场景

\- 研究报告生成

\- 代码开发项目

\- 数据分析任务

\- 内容创作

\- 技术方案设计

\- 知识整理



\## 🎯 实战示例



\### 示例1：研究报告（多Agent）



```python

任务: 研究量子计算的发展现状，分析技术挑战，撰写研究报告



执行流程:

1\. 研究员 - 搜集量子计算相关信息

2\. 分析师 - 分析技术发展趋势

3\. 写作者 - 撰写研究报告

4\. 评审者 - 质量检查

5\. 协调者 - 整合结果



输出: 完整的研究报告 + 评审意见

```



\### 示例2：知识管理（单Agent + 知识库）



```python

\# 1. 添加学习笔记

💬 你: 帮我记住今天学习的内容：Python生成器使用yield关键字，可以节省内存。标签：Python,生成器



\# 2. 搜索复习

💬 你: 搜索Python相关的学习笔记



\# 3. 查看学习进度

💬 你: 查看知识库统计，看看我学了多少内容



\# 4. 导出复习材料

💬 你: 导出知识库，我要复习

```



\### 示例3：数据分析（多Agent）



```python

任务: 分析电商平台用户行为数据，识别流失原因，提出改进建议



执行流程:

1\. 研究员 - 调研行业最佳实践

2\. 分析师 - 分析用户行为数据

3\. 分析师 - 识别关键指标和流失原因

4\. 写作者 - 撰写分析报告

5\. 评审者 - 评审分析质量



输出: 数据分析报告 + 可执行建议

```



\## 📝 命令参考



\### 通用命令

```bash

help              # 查看帮助

mode single       # 切换到单Agent模式

mode multi        # 切换到多Agent模式

config            # 显示配置信息

exit / quit       # 退出程序

```



\### 单Agent模式命令

```bash

memory            # 查看记忆统计

search <关键词>   # 搜索记忆

clear             # 清空短期记忆

export            # 导出记忆

```



\### 多Agent模式命令

```bash

status            # 查看系统状态

examples          # 查看示例任务

```



\## 🌐 API集成



\### 已集成的真实API



| 服务 | 用途 | 注册地址 | 免费额度 |

|------|------|---------|---------|

| 通义千问 | 大模型 | https://dashscope.aliyun.com/ | 按量计费 |

| 和风天气 | 天气查询 | https://dev.qweather.com/ | 1000次/天 |

| Serper | Google搜索 | https://serper.dev/ | 2500次/月 |

| 百度翻译 | 文本翻译 | https://fanyi-api.baidu.com/ | 200万字符/月 |

| 百度NLP | 情感分析 | https://ai.baidu.com/ | 50000次/天 |



\### 配置说明



在 `config.py` 中配置API开关：



```python

USE\_REAL\_WEATHER\_API = True    # 启用真实天气API

USE\_REAL\_SEARCH\_API = True     # 启用真实搜索API

USE\_REAL\_TRANSLATE\_API = True  # 启用真实翻译API

USE\_REAL\_SENTIMENT\_API = False # 使用本地情感分析

```



\## 🔧 高级功能



\### 1. 自定义Agent



```python

from multi\_agent import BaseAgent, AgentRole



class DataScientistAgent(BaseAgent):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       system\_prompt = "你是数据科学家..."

&nbsp;       tools = \["calculate", "analyze\_sentiment"]

&nbsp;       super().\_\_init\_\_("数据科学家", AgentRole.ANALYST, 

&nbsp;                       system\_prompt, tools)



\# 集成到系统

system = MultiAgentSystem()

system.agents\["data\_scientist"] = DataScientistAgent()

```



\### 2. 批量知识导入



```python

from knowledge\_base import KnowledgeBase



kb = KnowledgeBase()

\# 从目录批量导入

count = kb.import\_from\_directory("/path/to/docs", 

&nbsp;                               category="学习笔记")

print(f"导入了 {count} 篇文档")

```



\### 3. 知识图谱可视化



```python

kb = KnowledgeBase()

kg = kb.knowledge\_graph



\# 查看实体关系

entity = kg.get\_entity("Python")

related = kg.get\_related\_entities("Python", max\_depth=2)

relationships = kg.get\_entity\_relationships("Python")

```



\## 📊 性能优化建议



1\. \*\*记忆管理\*\*

&nbsp;  - 定期清理过期记忆

&nbsp;  - 控制短期记忆数量



2\. \*\*知识库\*\*

&nbsp;  - 合理使用标签和分类

&nbsp;  - 定期导出备份



3\. \*\*多Agent\*\*

&nbsp;  - 清晰的任务描述

&nbsp;  - 避免过度复杂的任务链



4\. \*\*API调用\*\*

&nbsp;  - 控制调用频率

&nbsp;  - 合理使用缓存



\## 🐛 故障排查



\### 问题1：API调用失败

\*\*解决方案：\*\*

```python

\# 检查配置

from config import print\_config

print\_config()



\# 测试API连接

from tools import Tools

tools = Tools()

result = tools.search\_weather("北京")  # 测试天气API

```



\### 问题2：知识库加载失败

\*\*解决方案：\*\*

```bash

\# 检查数据目录

ls data/knowledge\_base/



\# 重新初始化

rm -rf data/knowledge\_base/

python main.py  # 自动重建

```



\### 问题3：多Agent无响应

\*\*解决方案：\*\*

\- 启用详细输出: `verbose=True`

\- 检查任务描述是否清晰

\- 查看错误日志



\## 📈 更新日志



\### v2.0 (当前版本)

\- ✅ 新增多Agent协作系统

\- ✅ 集成知识库管理

\- ✅ 支持双模式运行

\- ✅ 19种工具集成

\- ✅ 真实API支持



\### v1.0

\- ✅ 基础单Agent实现

\- ✅ 工具调用系统

\- ✅ 记忆管理

\- ✅ 流式响应



\## 🚀 未来规划



\- \[ ] Web可视化界面

\- \[ ] 向量检索（语义搜索）

\- \[ ] Agent学习和优化

\- \[ ] 更多专业Agent

\- \[ ] 分布式部署

\- \[ ] 实时监控面板

\- \[ ] 插件系统

\- \[ ] 多模态支持



\## 📚 文档资源



\- \[知识库使用指南](KNOWLEDGE\_BASE\_GUIDE.md)

\- \[多Agent系统指南](MULTI\_AGENT\_GUIDE.md)

\- \[API集成说明](config.py)

\- \[工具开发指南](tools.py)



\## 🤝 贡献指南



欢迎提交Issue和Pull Request！



\## 📄 许可证



MIT License



\## 💬 联系方式



如有问题，请提交GitHub Issue。



---



\*\*开始使用智能Agent系统，体验AI协作的力量！\*\* 🚀✨

