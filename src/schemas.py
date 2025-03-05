from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    file: str = None  # รับไฟล์ PDF ในรูปแบบ Base64 (เป็น string)

class ChatPdfRequest(BaseModel):
    prompt: str
    file: str = None  # รับไฟล์ PDF ในรูปแบบ Base64 (เป็น string)