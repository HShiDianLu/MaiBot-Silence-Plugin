import json
import os
import time
from typing import Dict, List, Optional
from src.plugin_system.apis import component_manage_api
from src.plugin_system.base.component_types import ComponentType
from src.common.logger import get_logger

logger = get_logger("Silence")

class SilenceCore:
    """沉默功能的核心实现 - 简化版"""
    
    _config_file: str = ""
    
    @classmethod
    def init(cls, config_file: str):
        """初始化，设置配置文件路径并确保文件存在"""
        cls._config_file = config_file
        cls._ensure_config_file()
    
    @classmethod
    def _ensure_config_file(cls):
        """确保配置文件存在，如果不存在则创建"""
        try:
            os.makedirs(os.path.dirname(cls._config_file), exist_ok=True)
            if not os.path.exists(cls._config_file):
                with open(cls._config_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                logger.info(f"已创建沉默配置文件: {cls._config_file}")
        except Exception as e:
            logger.error(f"创建配置文件失败: {str(e)}")
            raise
    
    @classmethod
    def _load_data(cls) -> Dict[str, Dict]:
        """从JSON文件加载所有数据"""
        try:
            cls._ensure_config_file()
            with open(cls._config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            return {}
    
    @classmethod
    def _save_data(cls, data: Dict[str, Dict]):
        """保存数据到JSON文件"""
        try:
            with open(cls._config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
    
    @classmethod
    def is_silenced(cls, stream_id: str) -> bool:
        """
        核心方法：检查指定聊天流是否正在被沉默
        - 自动清理过期项
        - 返回当前真实的沉默状态
        """
        data = cls._load_data()
        
        if stream_id not in data:
            return False
        
        stream_data = data[stream_id]
        expiration = stream_data.get("expiration")
        
        # 永久沉默
        if expiration is None:
            return True
        
        # 检查是否过期
        current_time = time.time()
        if expiration and expiration >= current_time:
            return True  # 未过期，仍在沉默中
        
        # 已过期，自动清理并恢复组件
        cls._auto_cleanup_expired(stream_id, stream_data)
        return False
    
    @classmethod
    def _auto_cleanup_expired(cls, stream_id: str, stream_data: Dict):
        """自动清理过期的沉默状态"""
        try:
            # 恢复被禁用的组件
            disabled_actions = stream_data.get("disabled_actions", [])
            disabled_commands = stream_data.get("disabled_commands", [])
            cls._enable_components(stream_id, disabled_actions, disabled_commands)
            
            # 从数据中移除
            data = cls._load_data()
            if stream_id in data:
                del data[stream_id]
                cls._save_data(data)
            
            logger.info(f"自动清理了过期的沉默状态: {stream_id}")
        except Exception as e:
            logger.error(f"自动清理过期状态时出错: {str(e)}")
    
    @classmethod
    def add_silence(cls, stream_id: str, duration: Optional[float] = None, 
                   disabled_actions: Optional[List[str]] = None, 
                   disabled_commands: Optional[List[str]] = None) -> bool:
        """
        添加沉默状态
        返回: True=成功添加, False=已经在沉默中
        """
        if cls.is_silenced(stream_id):
            logger.warning(f"聊天流 {stream_id} 已经处于沉默状态")
            return False
        
        # 计算过期时间
        expiration = time.time() + duration if duration else None
        
        # 保存数据
        stream_data = {
            "expiration": expiration,
            "disabled_actions": disabled_actions or [],
            "disabled_commands": disabled_commands or []
        }
        
        data = cls._load_data()
        data[stream_id] = stream_data
        cls._save_data(data)
        
        # 禁用组件
        cls._disable_components(stream_id, disabled_actions or [], disabled_commands or [])
        
        duration_str = f"{duration}秒" if duration else "永久"
        logger.info(f"已添加聊天流 {stream_id} 到沉默列表，持续时间: {duration_str}")
        return True
    
    @classmethod
    def remove_silence(cls, stream_id: str) -> bool:
        """
        移除沉默状态
        返回: True=成功移除, False=不在沉默中
        """
        if not cls.is_silenced(stream_id):
            logger.warning(f"聊天流 {stream_id} 未处于沉默状态")
            return False
        
        # 获取数据用于恢复组件
        data = cls._load_data()
        stream_data = data.get(stream_id, {})
        
        # 恢复组件
        disabled_actions = stream_data.get("disabled_actions", [])
        disabled_commands = stream_data.get("disabled_commands", [])
        cls._enable_components(stream_id, disabled_actions, disabled_commands)
        
        # 移除数据
        if stream_id in data:
            del data[stream_id]
            cls._save_data(data)
        
        logger.info(f"已移除聊天流 {stream_id} 的沉默状态")
        return True
    
    @classmethod
    def _disable_components(cls, stream_id: str, disabled_actions: List[str], disabled_commands: List[str]):
        """禁用指定组件"""
        try:
            # 禁用Action组件
            for action_name in disabled_actions:
                component_manage_api.locally_disable_component(
                    action_name, ComponentType.ACTION, stream_id
                )
            
            # 禁用Command组件  
            for command_name in disabled_commands:
                component_manage_api.locally_disable_component(
                    command_name, ComponentType.COMMAND, stream_id
                )

            # 启用SilenceStopAction
            component_manage_api.locally_enable_component(
                "silence_stop_action", ComponentType.ACTION, stream_id
            )
            
            logger.info(f"已为聊天流 {stream_id} 禁用 {len(disabled_actions)} 个Action和 {len(disabled_commands)} 个Command")
        except Exception as e:
            logger.error(f"禁用组件时出错: {str(e)}")
    
    @classmethod
    def _enable_components(cls, stream_id: str, disabled_actions: List[str], disabled_commands: List[str]):
        """启用指定组件"""
        try:
            # 启用Action组件
            for action_name in disabled_actions:
                component_manage_api.locally_enable_component(
                    action_name, ComponentType.ACTION, stream_id
                )
            
            # 启用Command组件
            for command_name in disabled_commands:
                component_manage_api.locally_enable_component(
                    command_name, ComponentType.COMMAND, stream_id
                )

            # 禁用SilenceStopAction
            component_manage_api.locally_disable_component(
                "silence_stop_action", ComponentType.ACTION, stream_id
            )
            
            logger.info(f"已为聊天流 {stream_id} 恢复 {len(disabled_actions)} 个Action和 {len(disabled_commands)} 个Command")
        except Exception as e:
            logger.error(f"启用组件时出错: {str(e)}")
    
    @classmethod
    def get_all_silenced_streams(cls) -> Dict[str, Optional[float]]:
        """获取所有沉默中的聊天流（不自动清理，仅供查看）"""
        data = cls._load_data()
        result = {}
        for stream_id, stream_data in data.items():
            result[stream_id] = stream_data.get("expiration")
        return result
    
    @classmethod
    def manual_cleanup_expired(cls) -> int:
        """手动清理所有过期的沉默状态，返回清理数量"""
        count = 0
        current_time = time.time()
        data = cls._load_data()
        
        for stream_id, stream_data in list(data.items()):
            expiration = stream_data.get("expiration")
            if expiration is not None and expiration <= current_time:
                cls._auto_cleanup_expired(stream_id, stream_data)
                count += 1
        
        if count > 0:
            logger.info(f"手动清理了 {count} 个过期的沉默状态")
        return count