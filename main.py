import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag_pipeline import RAG_Pipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

rag = RAG_Pipeline()


class QueryRequest(BaseModel):
    question: str


@app.on_event("startup")
def startup():
    rag.run()
    print("RAG Ready ✅")


@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join("pdf", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = rag.add_pdf(file_path)

    return {
        "message": f"{file.filename} uploaded",
        "chunks": chunks
    }


@app.post("/ask")
def ask(req: QueryRequest):
    answer = rag.query(req.question)
    return {"answer": answer}