\# 🚀 通义千问智能Agent系统



一个功能完整的智能Agen# 🚀 通义千问智能Agent系统



一个功能完整的智能Agent系统，集成通义千问大模型，支持多工具调用、对话记忆、真实API集成等功能。



\## ✨ 主要特性



\- 🔄 \*\*流式响应\*\* - 实时输出对话内容

\- 🧠 \*\*智能记忆\*\* - 短期/长期记忆管理，自动提取重要信息

\- 🛠️ \*\*多工具调用\*\* - 支持11种实用工具

\- 🌐 \*\*API集成\*\* - 支持天气、搜索、翻译等真实API

\- 💾 \*\*数据持久化\*\* - 自动保存对话历史和用户画像

\- 🎯 \*\*易于扩展\*\* - 模块化设计，方便添加新工具



\## 📁 项目结构



```

intelligent-agent/

├── config.py           # 配置文件（API密钥、系统配置）

├── tools.py            # 工具实现（集成真实API）

├── memory.py           # 记忆管理模块

├── agent.py            # Agent核心逻辑

├── main.py             # 主程序入口

├── requirements.txt    # 依赖包列表

├── README.md           # 项目文档

└── data/               # 数据存储目录

&nbsp;   ├── memory.json     # 记忆数据

&nbsp;   ├── notes.txt       # 笔记文件

&nbsp;   ├── todos.json      # 待办事项

&nbsp;   └── reminders.txt   # 提醒事项

```



\## 🚀 快速开始



\### 1. 安装依赖



```bash

pip install -r requirements.txt

```



\### 2. 配置API密钥



编辑 `config.py` 文件，设置你的API密钥：



```python

\# 通义千问API（必需）

QWEN\_API\_KEY = "your\_qwen\_api\_key"



\# 以下API为可选，不配置则使用模拟数据

WEATHER\_API\_KEY = "your\_weather\_api\_key"  # 和风天气

SERPER\_API\_KEY = "your\_serper\_api\_key"    # Google搜索

BAIDU\_TRANSLATE\_APP\_ID = "your\_app\_id"     # 百度翻译

BAIDU\_TRANSLATE\_SECRET\_KEY = "your\_secret"

```



\### 3. 启用真实API（可选）



在 `config.py` 中设置：



```python

USE\_REAL\_WEATHER\_API = True    # 启用真实天气API

USE\_REAL\_SEARCH\_API = True     # 启用真实搜索API

USE\_REAL\_TRANSLATE\_API = True  # 启用真实翻译API

```



\### 4. 运行程序



```bash

python main.py

```



\## 🔧 支持的工具



| 工具名称 | 功能描述 | API支持 |

|---------|---------|---------|

| `get\_current\_time` | 获取当前时间 | 本地 |

| `calculate` | 数学计算 | 本地 |

| `search\_weather` | 查询天气 | 和风天气API |

| `search\_web` | 网络搜索 | Serper/SerpAPI/Bing |

| `translate\_text` | 文本翻译 | 百度翻译API |

| `analyze\_sentiment` | 情感分析 | 本地/百度NLP |

| `save\_note` | 保存笔记 | 本地文件 |

| `read\_file` | 读取文件 | 本地文件 |

| `get\_file\_info` | 文件信息 | 本地文件 |

| `create\_todo` | 创建待办 | 本地文件 |

| `set\_reminder` | 设置提醒 | 本地文件 |



\## 💡 使用示例



\### 基础对话

```

💬 你: 你好，现在几点了？

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 get\_current\_time

&nbsp; ✅ 结果: 2024-01-15 14:30:25

🤖 助手: 现在是2024年1月15日下午2点30分25秒。

```



\### 天气查询

```

💬 你: 北京今天天气怎么样？

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 search\_weather

&nbsp;    参数: {'city': '北京'}

&nbsp; ✅ 结果: 北京天气：晴天，温度 15°C，体感温度 13°C...

```



\### 数学计算

```

💬 你: 帮我计算 (123 + 456) \* 789

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 calculate

&nbsp;    参数: {'expression': '(123+456)\*789'}

&nbsp; ✅ 结果: 计算结果: 456831

```



\### 创建待办

```

💬 你: 创建一个高优先级待办：完成项目报告

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 create\_todo

&nbsp;    参数: {'task': '完成项目报告', 'priority': 'high'}

&nbsp; ✅ 结果: ✅ 已创建待办事项：🔴 完成项目报告

```



\## 📝 命令列表



| 命令 | 功能 |

|-----|------|

| `help` | 查看帮助和使用示例 |

| `memory` | 查看记忆统计 |

| `search <关键词>` | 搜索记忆 |

| `clear` | 清空短期记忆 |

| `clear all` | 清空所有记忆 |

| `export` | 导出记忆到文件 |

| `config` | 显示配置信息 |

| `exit` 或 `quit` | 退出程序 |



\## 🌐 API申请指南



\### 1. 通义千问API（必需）

\- 官网: https://dashscope.aliyun.com/

\- 注册阿里云账号

\- 开通DashScope服务

\- 获取API Key



\### 2. 和风天气API（可选）

\- 官网: https://dev.qweather.com/

\- 注册开发者账号

\- 创建应用

\- 免费版：每天1000次调用



\### 3. Google搜索API（可选）

\- Serper.dev: https://serper.dev/

\- SerpAPI: https://serpapi.com/

\- 免费额度：每月100-2500次



\### 4. 百度翻译API（可选）

\- 官网: https://fanyi-api.baidu.com/

\- 注册百度账号

\- 创建应用获取APP ID和密钥

\- 免费版：每月200万字符



\## 🔧 扩展开发



\### 添加新工具



1\. 在 `tools.py` 中添加工具方法：



```python

@staticmethod

def your\_tool\_name(param1: str, param2: int = 0) -> str:

&nbsp;   """工具描述"""

&nbsp;   try:

&nbsp;       # 实现工具逻辑

&nbsp;       result = do\_something(param1, param2)

&nbsp;       return f"结果: {result}"

&nbsp;   except Exception as e:

&nbsp;       return f"错误: {str(e)}"

```



2\. 在 `TOOLS\_CONFIG` 中添加工具配置：



```python

{

&nbsp;   "type": "function",

&nbsp;   "function": {

&nbsp;       "name": "your\_tool\_name",

&nbsp;       "description": "工具功能描述",

&nbsp;       "parameters": {

&nbsp;           "type": "object",

&nbsp;           "properties": {

&nbsp;               "param1": {

&nbsp;                   "type": "string",

&nbsp;                   "description": "参数1描述"

&nbsp;               },

&nbsp;               "param2": {

&nbsp;                   "type": "integer",

&nbsp;                   "description": "参数2描述",

&nbsp;                   "default": 0

&nbsp;               }

&nbsp;           },

&nbsp;           "required": \["param1"]

&nbsp;       }

&nbsp;   }

}

```



\### 自定义记忆策略



在 `memory.py` 中修改记忆管理逻辑：



```python

def custom\_memory\_filter(self, messages):

&nbsp;   """自定义记忆过滤策略"""

&nbsp;   # 实现你的记忆管理逻辑

&nbsp;   pass

```



\## 📊 记忆系统



\### 短期记忆

\- 保存最近的对话历史

\- 自动管理上下文窗口

\- 默认保留10轮对话



\### 长期记忆

\- 自动提取重要信息

\- 按重要性排序

\- 持久化存储



\### 用户画像

\- 自动记录用户信息

\- 支持自定义字段

\- 用于个性化服务



\## 🛡️ 安全建议



1\. \*\*不要提交API密钥到代码仓库\*\*

&nbsp;  - 使用环境变量或单独的配置文件

&nbsp;  - 在 `.gitignore` 中添加 `config.py`



2\. \*\*限制工具权限\*\*

&nbsp;  - 文件操作工具应限制访问范围

&nbsp;  - 网络请求添加超时限制



3\. \*\*输入验证\*\*

&nbsp;  - 对用户输入进行验证和清理

&nbsp;  - 防止注入攻击



\## 📈 性能优化



1\. \*\*记忆管理\*\*

&nbsp;  - 定期清理过期记忆

&nbsp;  - 压缩长期记忆



2\. \*\*API调用\*\*

&nbsp;  - 实现请求缓存

&nbsp;  - 控制调用频率



3\. \*\*并发处理\*\*

&nbsp;  - 支持异步工具调用

&nbsp;  - 批量处理请求



\## 🐛 常见问题



\### Q: API调用失败怎么办？

A: 检查以下几点：

\- API密钥是否正确

\- 网络连接是否正常

\- API额度是否充足

\- 请求参数是否正确



\### Q: 记忆文件在哪里？

A: 默认存储在 `data/` 目录下



\### Q: 如何重置所有数据？

A: 删除 `data/` 目录或运行 `clear all` 命令



\### Q: 支持哪些模型？

A: 通义千问系列：qwen-turbo, qwen-plus, qwen-max



\## 📄 许可证



MIT License



\## 🤝 贡献



欢迎提交Issue和Pull Request！



\## 📮 联系方式



如有问题，请提交GitHub Issue。



---



\*\*祝你使用愉快！\*\* 🎉t系统，集成通义千问大模型，支持多工具调用、对话记忆、真实API集成等功能。



\## ✨ 主要特性



\- 🔄 \*\*流式响应\*\* - 实时输出对话内容

\- 🧠 \*\*智能记忆\*\* - 短期/长期记忆管理，自动提取重要信息

\- 🛠️ \*\*多工具调用\*\* - 支持11种实用工具

\- 🌐 \*\*API集成\*\* - 支持天气、搜索、翻译等真实API

\- 💾 \*\*数据持久化\*\* - 自动保存对话历史和用户画像

\- 🎯 \*\*易于扩展\*\* - 模块化设计，方便添加新工具



\## 📁 项目结构



```

intelligent-agent/

├── config.py           # 配置文件（API密钥、系统配置）

├── tools.py            # 工具实现（集成真实API）

├── memory.py           # 记忆管理模块

├── agent.py            # Agent核心逻辑

├── main.py             # 主程序入口

├── requirements.txt    # 依赖包列表

├── README.md           # 项目文档

└── data/               # 数据存储目录

&nbsp;   ├── memory.json     # 记忆数据

&nbsp;   ├── notes.txt       # 笔记文件

&nbsp;   ├── todos.json      # 待办事项

&nbsp;   └── reminders.txt   # 提醒事项

```



\## 🚀 快速开始



\### 1. 安装依赖



```bash

pip install -r requirements.txt

```



\### 2. 配置API密钥



编辑 `config.py` 文件，设置你的API密钥：



```python

\# 通义千问API（必需）

QWEN\_API\_KEY = "your\_qwen\_api\_key"



\# 以下API为可选，不配置则使用模拟数据

WEATHER\_API\_KEY = "your\_weather\_api\_key"  # 和风天气

SERPER\_API\_KEY = "your\_serper\_api\_key"    # Google搜索

BAIDU\_TRANSLATE\_APP\_ID = "your\_app\_id"     # 百度翻译

BAIDU\_TRANSLATE\_SECRET\_KEY = "your\_secret"

```



\### 3. 启用真实API（可选）



在 `config.py` 中设置：



```python

USE\_REAL\_WEATHER\_API = True    # 启用真实天气API

USE\_REAL\_SEARCH\_API = True     # 启用真实搜索API

USE\_REAL\_TRANSLATE\_API = True  # 启用真实翻译API

```



\### 4. 运行程序



```bash

python main.py

```



\## 🔧 支持的工具



| 工具名称 | 功能描述 | API支持 |

|---------|---------|---------|

| `get\_current\_time` | 获取当前时间 | 本地 |

| `calculate` | 数学计算 | 本地 |

| `search\_weather` | 查询天气 | 和风天气API |

| `search\_web` | 网络搜索 | Serper/SerpAPI/Bing |

| `translate\_text` | 文本翻译 | 百度翻译API |

| `analyze\_sentiment` | 情感分析 | 本地/百度NLP |

| `save\_note` | 保存笔记 | 本地文件 |

| `read\_file` | 读取文件 | 本地文件 |

| `get\_file\_info` | 文件信息 | 本地文件 |

| `create\_todo` | 创建待办 | 本地文件 |

| `set\_reminder` | 设置提醒 | 本地文件 |



\## 💡 使用示例



\### 基础对话

```

💬 你: 你好，现在几点了？

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 get\_current\_time

&nbsp; ✅ 结果: 2024-01-15 14:30:25

🤖 助手: 现在是2024年1月15日下午2点30分25秒。

```



\### 天气查询

```

💬 你: 北京今天天气怎么样？

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 search\_weather

&nbsp;    参数: {'city': '北京'}

&nbsp; ✅ 结果: 北京天气：晴天，温度 15°C，体感温度 13°C...

```



\### 数学计算

```

💬 你: 帮我计算 (123 + 456) \* 789

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 calculate

&nbsp;    参数: {'expression': '(123+456)\*789'}

&nbsp; ✅ 结果: 计算结果: 456831

```



\### 创建待办

```

💬 你: 创建一个高优先级待办：完成项目报告

🤖 助手: 

🔧 执行工具调用...

&nbsp; 📍 调用 create\_todo

&nbsp;    参数: {'task': '完成项目报告', 'priority': 'high'}

&nbsp; ✅ 结果: ✅ 已创建待办事项：🔴 完成项目报告

```



\## 📝 命令列表



| 命令 | 功能 |

|-----|------|

| `help` | 查看帮助和使用示例 |

| `memory` | 查看记忆统计 |

| `search <关键词>` | 搜索记忆 |

| `clear` | 清空短期记忆 |

| `clear all` | 清空所有记忆 |

| `export` | 导出记忆到文件 |

| `config` | 显示配置信息 |

| `exit` 或 `quit` | 退出程序 |



\## 🌐 API申请指南



\### 1. 通义千问API（必需）

\- 官网: https://dashscope.aliyun.com/

\- 注册阿里云账号

\- 开通DashScope服务

\- 获取API Key



\### 2. 和风天气API（可选）

\- 官网: https://dev.qweather.com/

\- 注册开发者账号

\- 创建应用

\- 免费版：每天1000次调用



\### 3. Google搜索API（可选）

\- Serper.dev: https://serper.dev/

\- SerpAPI: https://serpapi.com/

\- 免费额度：每月100-2500次



\### 4. 百度翻译API（可选）

\- 官网: https://fanyi-api.baidu.com/

\- 注册百度账号

\- 创建应用获取APP ID和密钥

\- 免费版：每月200万字符



\## 🔧 扩展开发



\### 添加新工具



1\. 在 `tools.py` 中添加工具方法：



```python

@staticmethod

def your\_tool\_name(param1: str, param2: int = 0) -> str:

&nbsp;   """工具描述"""

&nbsp;   try:

&nbsp;       # 实现工具逻辑

&nbsp;       result = do\_something(param1, param2)

&nbsp;       return f"结果: {result}"

&nbsp;   except Exception as e:

&nbsp;       return f"错误: {str(e)}"

```



2\. 在 `TOOLS\_CONFIG` 中添加工具配置：



```python

{

&nbsp;   "type": "function",

&nbsp;   "function": {

&nbsp;       "name": "your\_tool\_name",

&nbsp;       "description": "工具功能描述",

&nbsp;       "parameters": {

&nbsp;           "type": "object",

&nbsp;           "properties": {

&nbsp;               "param1": {

&nbsp;                   "type": "string",

&nbsp;                   "description": "参数1描述"

&nbsp;               },

&nbsp;               "param2": {

&nbsp;                   "type": "integer",

&nbsp;                   "description": "参数2描述",

&nbsp;                   "default": 0

&nbsp;               }

&nbsp;           },

&nbsp;           "required": \["param1"]

&nbsp;       }

&nbsp;   }

}

```



\### 自定义记忆策略



在 `memory.py` 中修改记忆管理逻辑：



```python

def custom\_memory\_filter(self, messages):

&nbsp;   """自定义记忆过滤策略"""

&nbsp;   # 实现你的记忆管理逻辑

&nbsp;   pass

```



\## 📊 记忆系统



\### 短期记忆

\- 保存最近的对话历史

\- 自动管理上下文窗口

\- 默认保留10轮对话



\### 长期记忆

\- 自动提取重要信息

\- 按重要性排序

\- 持久化存储



\### 用户画像

\- 自动记录用户信息

\- 支持自定义字段

\- 用于个性化服务



\## 🛡️ 安全建议



1\. \*\*不要提交API密钥到代码仓库\*\*

&nbsp;  - 使用环境变量或单独的配置文件

&nbsp;  - 在 `.gitignore` 中添加 `config.py`



2\. \*\*限制工具权限\*\*

&nbsp;  - 文件操作工具应限制访问范围

&nbsp;  - 网络请求添加超时限制



3\. \*\*输入验证\*\*

&nbsp;  - 对用户输入进行验证和清理

&nbsp;  - 防止注入攻击



\## 📈 性能优化



1\. \*\*记忆管理\*\*

&nbsp;  - 定期清理过期记忆

&nbsp;  - 压缩长期记忆



2\. \*\*API调用\*\*

&nbsp;  - 实现请求缓存

&nbsp;  - 控制调用频率



3\. \*\*并发处理\*\*

&nbsp;  - 支持异步工具调用

&nbsp;  - 批量处理请求



\## 🐛 常见问题



\### Q: API调用失败怎么办？

A: 检查以下几点：

\- API密钥是否正确

\- 网络连接是否正常

\- API额度是否充足

\- 请求参数是否正确



\### Q: 记忆文件在哪里？

A: 默认存储在 `data/` 目录下



\### Q: 如何重置所有数据？

A: 删除 `data/` 目录或运行 `clear all` 命令



\### Q: 支持哪些模型？

A: 通义千问系列：qwen-turbo, qwen-plus, qwen-max



\## 📄 许可证



MIT License



\## 🤝 贡献



欢迎提交Issue和Pull Request！



\## 📮 联系方式



如有问题，请提交GitHub Issue。



---



\*\*祝你使用愉快！\*\* 🎉

