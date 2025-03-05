from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import src.functions as fn
import src.schemas as sc

app = FastAPI()

# 🔹 เปิดใช้งาน CORS เพื่อให้ frontend ติดต่อ API ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# response webpages index.html for the frontend
@app.get("/")
async def index():
    print("index.html")
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: sc.ChatRequest):
    return StreamingResponse(fn.llama32(request.prompt), media_type="text/plain")

@app.post("/chat_with_pdf")
async def chat_with_pdf(request: sc.ChatPdfRequest):
    prompt = fn.chat_pdf(request)
    return StreamingResponse(fn.llama32(prompt), media_type="text/plain")
