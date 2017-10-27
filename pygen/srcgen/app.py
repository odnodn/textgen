from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref='books')

class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author
    books = ma.List(ma.HyperlinkRelated('book_detail'))


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
    author = ma.HyperlinkRelated('author_detail')

from sqlalchemy import orm
Session = orm.scoped_session(orm.sessionmaker())


@app.route('/api/authors/')
def authors():
    authors = Author.query.all()
    print (authors)
    data=  AuthorSchema().dump(authors, many=True).data
    print (data)
    return data

@app.route('/api/authors/<id>')
def author_detail():
    return AuthorSchema().jsonify(Author.get(id))


@app.route('/api/books')
def books():
    return BookSchema().jsonify(Book.query.all())

@app.route('/api/books/<id>')
def book_detail(id):
    return BookSchema().jsonify(Book.get(id))


def createRecords():
    a = Author(name='eckhart tolle')
    b = Book(title='power of now', author = a)
    bc = Book(title='new Earth', author = a)
    db.session.add(b)
    db.session.add(bc)
    db.session.flush()

db.create_all()
createRecords()
app.run()



