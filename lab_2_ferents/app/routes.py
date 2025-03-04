from fastapi import APIRouter, Request
from marshmallow import ValidationError
from .models import Book


books = [
    {"id":1, "title":"test1", "author":"some one"},
    {"id":2, "title":"test2", "author":"some one"},
    {"id":3, "title":"test3", "author":"some one"}
]

book_schema = Book()
main = APIRouter()


@main.get("/")
async def get_books():
    return {"books": books}

@main.get("/{book_id}")
async def get_books(book_id: int):
    book = next((book for book in books if book["id"] == book_id),None)
    if book is not None:
        return {"book": book}
    else:
        return {"message": "Out of range"}
    
@main.delete("/{book_id}/delet_book")
async def delet_book(book_id: int):
    global books

    book = next((book for book in books if book["id"] == book_id),None)
    if book is None:
        return {"massage": f"book {book_id} Not found"}

    books = [book for book in books if book["id"] != book_id]
    return {"massage": f"book {book_id} Succesful deleted"}

@main.post("/create_book/")
async def create_book(request: Request):
    data = await request.json()
    if not data:
        return {"error": "Empty request"}, 400
    try:
        validated_data = book_schema.load(data)
        return (validated_data)
    except ValidationError as e:
        return {"error": e.errors()},400

# @main.route("/create_book", methods=["POST"])
# def create_book():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Empty request"}), 400 
#     try:
#         validated_data = book_schema.load(data)
#         return jsonify(validated_data), 200
#     except ValidationError as e:
#         return jsonify({"error": e.errors()}), 400

# @main.errorhandler(404)
# def page_not_found(error):
#     return jsonify({"error":"out of range"}),404
    