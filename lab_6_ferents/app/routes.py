from flask import Blueprint, jsonify, abort, request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from .models import BookShema, Book
from app import db

book_schema = BookShema()

main = Blueprint("lab_3", __name__)

class BookListResource(Resource):
    def get(self):
        """
        Get all books
        ---
        responses:
          200:
            description: Returns a list of books
        """
        last_id = request.args.get("last_id", 0, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        books = Book.query.filter(Book.id > last_id).order_by(Book.id).limit(per_page).all()

        books_list=[{"id": book.id, "book_name":book.book_name, "author":book.author} for book in books]
        next_id = books[-1].id if books else None

        return {
            "books": books_list,
            "next_id": next_id
        }, 200
    def post(self):
        """
        Create a new book
        ---
        parameters:
          - in: body
            name: book
            schema:
              type: object
              properties:
                title:
                  type: string
                author:
                  type: string
              required: [title, author]
        responses:
          201:
            description: Book created
        """
        data = request.get_json()
        if not data:
            return {"error": "Empty request"}, 400 
        try:
            validated_data = book_schema.load(data)

            new_book = Book(
                            book_name=validated_data["title"], 
                            author=validated_data["author"]
                            )

            db.session.add(new_book)
            db.session.commit()

            return {
                    "message": "Book created successfully", 
                    "book": {"id": new_book.id, "book_name": new_book.book_name, "author": new_book.author}
                }, 201
        except ValidationError as e:
            return {"error": e.errors()}, 400

class BookResource(Resource):
    def get(self, book_id):
        """
        Get a book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: A book object
        """
        book = Book.query.get_or_404(book_id)
        book_json = [{"id": book.id, "book_name":book.book_name, "author":book.author}]
        if book is not None:
            return book_json ,200
        else:
            abort(404)
    def delete(self, book_id):
        """
        Delete a book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book successfully deleted
        """
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message":"Book successful deleted"}, 200

@main.errorhandler(404)
def page_not_found(error):
    return {"error":"out of range"}, 404