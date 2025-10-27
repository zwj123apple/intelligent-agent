"""
配置文件 - 存储API密钥和系统配置
"""

import os
from pathlib import Path

# ============== 基础配置 ==============
# 项目根目录
BASE_DIR = Path(__file__).parent

# 数据存储目录
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============== API配置 ==============
# 通义千问配置
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "sk-610e45d1dfef4ac0b42791b9784141ef")
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-plus"  # 可选: qwen-turbo, qwen-max, qwen-plus

# 天气API配置 (和风天气)
# 注册地址: https://dev.qweather.com/
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_qweather_api_key")
WEATHER_API_URL = "https://devapi.qweather.com/v7"

# 翻译API配置 (百度翻译)
# 注册地址: https://fanyi-api.baidu.com/
BAIDU_TRANSLATE_APP_ID = os.getenv("BAIDU_TRANSLATE_APP_ID", "your_app_id")
BAIDU_TRANSLATE_SECRET_KEY = os.getenv("BAIDU_TRANSLATE_SECRET_KEY", "your_secret_key")
BAIDU_TRANSLATE_API_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"

# 搜索API配置 (Serper Google Search API)
# 注册地址: https://serper.dev/
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "your_serper_api_key")
SERPER_API_URL = "https://google.serper.dev/search"

# 或使用 SerpAPI
# 注册地址: https://serpapi.com/
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "your_serpapi_key")

# 或使用 Bing Search API
# 注册地址: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API_KEY", "your_bing_api_key")
BING_SEARCH_API_URL = "https://api.bing.microsoft.com/v7.0/search"

# 情感分析API配置 (可选，也可使用本地模型)
# 百度情感分析
BAIDU_NLP_API_KEY = os.getenv("BAIDU_NLP_API_KEY", "your_nlp_api_key")
BAIDU_NLP_SECRET_KEY = os.getenv("BAIDU_NLP_SECRET_KEY", "your_nlp_secret_key")

# ============== 记忆配置 ==============
# 短期记忆限制（对话轮数）
SHORT_TERM_MEMORY_LIMIT = 10

# 记忆文件路径
MEMORY_FILE = DATA_DIR / "memory.json"
NOTES_FILE = DATA_DIR / "notes.txt"
TODOS_FILE = DATA_DIR / "todos.json"
REMINDERS_FILE = DATA_DIR / "reminders.txt"

# ============== 系统配置 ==============
# 是否启用流式响应
ENABLE_STREAMING = True

# 日志级别
LOG_LEVEL = "INFO"

# 最大文件读取行数
MAX_FILE_READ_LINES = 50

# ============== 工具配置 ==============
# 是否使用真实API（如果为False，使用模拟数据）
USE_REAL_WEATHER_API = False  # 设置为True启用真实天气API
USE_REAL_SEARCH_API = False   # 设置为True启用真实搜索API
USE_REAL_TRANSLATE_API = False  # 设置为True启用真实翻译API
USE_REAL_SENTIMENT_API = False  # 设置为True启用真实情感分析API

# ============== 语言映射 ==============
# 翻译语言代码映射（百度翻译）
LANGUAGE_CODE_MAP = {
    "中文": "zh",
    "英语": "en",
    "英文": "en",
    "日语": "jp",
    "日文": "jp",
    "韩语": "kor",
    "韩文": "kor",
    "法语": "fra",
    "法文": "fra",
    "德语": "de",
    "德文": "de",
    "西班牙语": "spa",
    "俄语": "ru",
    "阿拉伯语": "ara",
    "泰语": "th",
    "越南语": "vie",
}

# ============== 打印配置信息 ==============
def print_config():
    """打印配置信息（隐藏敏感信息）"""
    print("=" * 60)
    print("📋 当前配置:")
    print(f"  模型: {QWEN_MODEL}")
    print(f"  数据目录: {DATA_DIR}")
    print(f"  短期记忆限制: {SHORT_TERM_MEMORY_LIMIT} 轮")
    print(f"  流式响应: {'启用' if ENABLE_STREAMING else '禁用'}")
    print("\n🔌 API状态:")
    print(f"  天气API: {'✓ 已启用' if USE_REAL_WEATHER_API else '✗ 使用模拟数据'}")
    print(f"  搜索API: {'✓ 已启用' if USE_REAL_SEARCH_API else '✗ 使用模拟数据'}")
    print(f"  翻译API: {'✓ 已启用' if USE_REAL_TRANSLATE_API else '✗ 使用模拟数据'}")
    print(f"  情感分析API: {'✓ 已启用' if USE_REAL_SENTIMENT_API else '✗ 使用本地分析'}")
    print("=" * 60)


if __name__ == "__main__":
    print_config()