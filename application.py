#api
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///date.db'
db = SQLAlchemy(app)
app.app_context().push()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(12))
    publisher = db.Column(db.String(20))

    def __repr__(self):
        return f"{self.bookName} - {self.author} - {self.publisher}"






@app.route('/')
def index():
   return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'id': book.id, 'name': book.bookName, 'author': book.author, "publisher": book.publisher}
       
        output.append(book_data)
    return{'books': output}

@app.route('/books/<id>')
def get_books_id(id):
    book = Book.query.get_or_404(id)
    return {'name': book.bookName, 'author': book.author, "publisher": book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    book = Book(id=request.json['id'], bookName=request.json['bookName'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message": "deleted"}
    
