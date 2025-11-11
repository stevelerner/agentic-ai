"""Short-term memory for conversation context."""
from typing import List, Dict, Any
from collections import deque


class ShortTermMemory:
    """Manages short-term conversation memory with sliding window."""
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: deque = deque(maxlen=max_messages)
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a message to memory."""
        message = {
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.messages.append(message)
    
    def get_messages(self, last_n: int = None) -> List[Dict[str, Any]]:
        """Get recent messages."""
        if last_n:
            return list(self.messages)[-last_n:]
        return list(self.messages)
    
    def clear(self):
        """Clear all messages."""
        self.messages.clear()
    
    def get_context_string(self, last_n: int = 5) -> str:
        """Get recent conversation as a string."""
        messages = self.get_messages(last_n)
        context = []
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            context.append(f"{role}: {content}")
        return "\n".join(context)
    
    def set_metadata(self, key: str, value: Any):
        """Store metadata about the conversation."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """Retrieve metadata."""
        return self.metadata.get(key)

