from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from app.data import BOOKS
from app.models import BookCreate, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])

BookId = Annotated[int, Path(gt=0, description="Mã sách")]

def find_book(book_id: int) -> dict:
    for b in BOOKS:
        if b["id"] == book_id:
            return b
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        f"Không tìm thấy sách id={book_id}")

def check_isbn(isbn: str, exclude_id: int | None = None) -> None:
    if any(b["isbn"] == isbn and b["id"] != exclude_id for b in BOOKS):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"ISBN {isbn} đã tồn tại")

@router.get("", response_model=list[BookOut], summary="Danh sách sách")
def list_books(
    q: Annotated[str | None, Query(max_length=50)] = None,
    author: str | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    data = BOOKS
    if q:
        data = [b for b in data if q.lower() in b["title"].lower()]
    if author:
        data = [b for b in data if author.lower() in b["author"].lower()]
    return data[skip : skip + limit]

@router.get("/{book_id}", response_model=BookOut, summary="Chi tiết sách")
def get_book(book_id: BookId):
    return find_book(book_id)

@router.post("", response_model=BookOut,
             status_code=status.HTTP_201_CREATED, summary="Thêm sách")
def create_book(book: BookCreate):
    check_isbn(book.isbn)
    new_id = max((b["id"] for b in BOOKS), default=0) + 1
    new = {"id": new_id, **book.model_dump()}
    BOOKS.append(new)
    return new

@router.put("/{book_id}", response_model=BookOut, summary="Cập nhật toàn bộ")
def replace_book(book_id: BookId, book: BookCreate):
    current = find_book(book_id)
    check_isbn(book.isbn, exclude_id=book_id)
    current.update(book.model_dump())
    return current

@router.patch("/{book_id}", response_model=BookOut, summary="Cập nhật một phần")
def update_book(book_id: BookId, book: BookUpdate):
    current = find_book(book_id)
    current.update(book.model_dump(exclude_unset=True))
    return current

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Xóa sách")
def delete_book(book_id: BookId):
    BOOKS.remove(find_book(book_id))