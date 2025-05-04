from locust import HttpUser, task, between

class BookHendler(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_books(self):
        self.client.get("/books")

    @task
    def get_book(self):
        self.client.get("/books/3")

    @task 
    def create_book(self):
        self.client.post("/books/create_book", json={"id": 10, "title": "New Book", "author": "Author"})

    @task
    def delete_book(self):
        self.client.delete("/books/10/delete_book", json={"message": "Book deleted"})