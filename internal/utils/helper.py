import hashlib


def generate_text_hash(text: str) -> str:
    """生成文本哈希值"""
    text = str(text) + "None"
    return hashlib.sha3_256(text.encode()).hexdigest()
