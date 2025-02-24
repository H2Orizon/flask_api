from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from .models import Book


books = [
    {"id":1, "title":"test1", "author":"some one"},
    {"id":2, "title":"test2", "author":"some one"},
    {"id":3, "title":"test3", "author":"some one"}
]

book_schema = Book()

main = Blueprint("lab_1", __name__)

@main.route("/all_books", methods=["GET"])
def get_books():
    return jsonify(books), 200

@main.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id),None)
    if book is not None:
        return jsonify(book),200
    else:
        abort(404)

@main.route("/create_book", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}), 400 
    try:
        validated_data = book_schema.load(data)
        return jsonify(validated_data), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@main.route("/delete_book/<int:book_id>", methods=["delete"])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"massage":"Book successful deleted"}),200

@main.errorhandler(404)
def page_not_found(error):
    return jsonify({"error":"out of range"}),404
    