import numpy as np
import fitz
import base64
import asyncio
import ollama
from src.initConfig import embedder
import src.schemas as sc

def text_to_embedding(text):
    return embedder.encode(text).tolist()

def similarity_score(text1, text2):
    v1 = text_to_embedding(text1)
    v2 = text_to_embedding(text2)
    return np.dot(v1, v2)

def query_similarity(query, candidates):
    query_embedding = text_to_embedding(query)
    candidate_embeddings = [text_to_embedding(candidate) for candidate in candidates]
    return np.asarray([np.dot(query_embedding, candidate_embedding) for candidate_embedding in candidate_embeddings])

def pdf_to_text(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

def base64_pdf_to_text(base64_pdf):
    # แปลง Base64 เป็น PDF bytes
    pdf_bytes = base64.b64decode(base64_pdf)
    
    # อ่านเนื้อหาจากไฟล์ PDF
    text_from_pdf = ""
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in pdf_doc:
        text_from_pdf += page.get_text("text") + "\n"

    return text_from_pdf

def split_lines(text):
    return text.split("\n")

async def llama32(prompt: str):
    stream = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}], stream=True)
    print("prompt",prompt)
    print("\n",10*"-","start",10*"-")
    for chunk in stream:
        yield chunk["message"]["content"]
        await asyncio.sleep(0)  # ป้องกันการ block event loop
        print(chunk["message"]["content"], end="", flush=True)  # แสดงผลทันทีโดยไม่ต้องรอทั้งหมด
    print("\n",10*"-","end",10*"-")

def chat_pdf(request: sc.ChatPdfRequest):
    text_from_pdf = ""

    if request.file:
        text_from_pdf = base64_pdf_to_text(request.file)

    # รวม prompt กับข้อมูลจาก PDF
    final_prompt = f"Prompt: {request.prompt}\n\nPDF Content:\n{text_from_pdf}"

    return final_prompt