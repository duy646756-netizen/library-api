from fastapi import FastAPI
from app.routers import books

app = FastAPI(title="Library API – Khoa CNTT", version="1.0.0",
              description="API quản lý sách của Thư viện số Khoa CNTT")

app.include_router(books.router)

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}