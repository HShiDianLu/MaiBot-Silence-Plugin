from src.common.logger import get_logger
import sys

logger = get_logger("Silence")

MODULE_COLORS = {
    # 核心模块
    "main": "\033[1;97m",  # 亮白色+粗体 (主程序)
    "api": "\033[92m",  # 亮绿色
    "emoji": "\033[38;5;214m",  # 橙黄色，偏向橙色但与replyer和action_manager不同
    "chat": "\033[92m",  # 亮蓝色
    "config": "\033[93m",  # 亮黄色
    "common": "\033[95m",  # 亮紫色
    "tools": "\033[96m",  # 亮青色
    "lpmm": "\033[96m",
    "plugin_system": "\033[91m",  # 亮红色
    "person_info": "\033[32m",  # 绿色
    "individuality": "\033[94m",  # 显眼的亮蓝色
    "manager": "\033[35m",  # 紫色
    "llm_models": "\033[36m",  # 青色
    "remote": "\033[38;5;242m",  # 深灰色，更不显眼
    "planner": "\033[36m",
    "memory": "\033[34m",
    "hfc": "\033[38;5;81m",  # 稍微暗一些的青色，保持可读
    "action_manager": "\033[38;5;208m",  # 橙色，不与replyer重复
    # 关系系统
    "relation": "\033[38;5;139m",  # 柔和的紫色，不刺眼
    # 聊天相关模块
    "normal_chat": "\033[38;5;81m",  # 亮蓝绿色
    "heartflow": "\033[38;5;175m",  # 柔和的粉色，不显眼但保持粉色系
    "sub_heartflow": "\033[38;5;207m",  # 粉紫色
    "subheartflow_manager": "\033[38;5;201m",  # 深粉色
    "background_tasks": "\033[38;5;240m",  # 灰色
    "chat_message": "\033[38;5;45m",  # 青色
    "chat_stream": "\033[38;5;51m",  # 亮青色
    "sender": "\033[38;5;67m",  # 稍微暗一些的蓝色，不显眼
    "message_storage": "\033[38;5;33m",  # 深蓝色
    "expressor": "\033[38;5;166m",  # 橙色
    # 专注聊天模块
    "replyer": "\033[38;5;166m",  # 橙色
    "memory_activator": "\033[34m",  # 绿色
    # 插件系统
    "plugins": "\033[31m",  # 红色
    "plugin_api": "\033[33m",  # 黄色
    "plugin_manager": "\033[38;5;208m",  # 红色
    "base_plugin": "\033[38;5;202m",  # 橙红色
    "send_api": "\033[38;5;208m",  # 橙色
    "base_command": "\033[38;5;208m",  # 橙色
    "component_registry": "\033[38;5;214m",  # 橙黄色
    "stream_api": "\033[38;5;220m",  # 黄色
    "config_api": "\033[38;5;226m",  # 亮黄色
    "heartflow_api": "\033[38;5;154m",  # 黄绿色
    "action_apis": "\033[38;5;118m",  # 绿色
    "independent_apis": "\033[38;5;82m",  # 绿色
    "llm_api": "\033[38;5;46m",  # 亮绿色
    "database_api": "\033[38;5;10m",  # 绿色
    "utils_api": "\033[38;5;14m",  # 青色
    "message_api": "\033[38;5;6m",  # 青色
    # 管理器模块
    "async_task_manager": "\033[38;5;129m",  # 紫色
    "mood": "\033[38;5;135m",  # 紫红色
    "local_storage": "\033[38;5;141m",  # 紫色
    "willing": "\033[38;5;147m",  # 浅紫色
    # 工具模块
    "tool_use": "\033[38;5;172m",  # 橙褐色
    "tool_executor": "\033[38;5;172m",  # 橙褐色
    "base_tool": "\033[38;5;178m",  # 金黄色
    # 工具和实用模块
    "prompt_build": "\033[38;5;105m",  # 紫色
    "chat_utils": "\033[38;5;111m",  # 蓝色
    "chat_image": "\033[38;5;117m",  # 浅蓝色
    "maibot_statistic": "\033[38;5;129m",  # 紫色
    # 特殊功能插件
    "mute_plugin": "\033[38;5;240m",  # 灰色
    "core_actions": "\033[38;5;117m",  # 深红色
    "tts_action": "\033[38;5;58m",  # 深黄色
    "doubao_pic_plugin": "\033[38;5;64m",  # 深绿色
    # Action组件
    "no_reply_action": "\033[38;5;214m",  # 亮橙色，显眼但不像警告
    "reply_action": "\033[38;5;46m",  # 亮绿色
    "base_action": "\033[38;5;250m",  # 浅灰色
    # 数据库和消息
    "database_model": "\033[38;5;94m",  # 橙褐色
    "maim_message": "\033[38;5;140m",  # 紫褐色
    # 日志系统
    "logger": "\033[38;5;8m",  # 深灰色
    "confirm": "\033[1;93m",  # 黄色+粗体
    # 模型相关
    "model_utils": "\033[38;5;164m",  # 紫红色
    "relationship_fetcher": "\033[38;5;170m",  # 浅紫色
    "relationship_builder": "\033[38;5;93m",  # 浅蓝色
    
    #s4u
    "context_web_api": "\033[38;5;240m",  # 深灰色
    "S4U_chat": "\033[92m",  # 深灰色
    "Silence": "\033[38;5;197m", # 红色
}

MODULE_ALIASES = {
    # 示例映射
    "individuality": "人格特质",
    "emoji": "表情包",
    "no_reply_action": "摸鱼",
    "reply_action": "回复",
    "action_manager": "动作",
    "memory_activator": "记忆",
    "tool_use": "工具",
    "expressor": "表达方式",
    "database_model": "数据库",
    "mood": "情绪",
    "memory": "记忆",
    "tool_executor": "工具",
    "hfc": "聊天节奏",
    "chat": "所见",
    "plugin_manager": "插件",
    "relationship_builder": "关系",
    "llm_models": "模型",
    "person_info": "人物",
    "chat_stream": "聊天流",
    "planner": "规划器",
    "replyer": "言语",
    "config": "配置",
    "main": "主程序",
    "Silence": "沉默插件",
}

RESET_COLOR = "\033[0m"

# 模仿你现有的补丁方法
def apply_logger_color_patch_once():
    """确保logger颜色补丁只应用一次"""
    
    # 检查是否已经打过补丁 - 用和你一样的方式
    if hasattr(apply_logger_color_patch_once, "_logger_patch_applied") and apply_logger_color_patch_once._logger_patch_applied:
        return
    
    try:
        # 获取logger模块
        logger_module = sys.modules.get('src.common.logger')
        if not logger_module:
            logger.warning("Logger模块未找到，跳过颜色补丁")
            return
        
        # 直接把配置注入到logger模块里 - 就像你给ChatConfig加属性一样
        logger_module.MODULE_COLORS = MODULE_COLORS
        logger_module.MODULE_ALIASES = MODULE_ALIASES
        logger_module.RESET_COLOR = RESET_COLOR
        
        # 标记补丁已应用 - 用和你一样的方式
        apply_logger_color_patch_once._logger_patch_applied = True
        # logger.info("Logger颜色补丁已应用")
        
    except Exception as e:
        logger.error(f"应用logger颜色补丁失败: {str(e)}")