from .database import db
import datetime
import secrets
class Author(db.Model):
  __tablename__='author'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), nullable=False)
  bio = db.Column(db.Text)

  def to_dict(self):
        authors_dict = {
         'id':self.id,
         'name':self.name,
         'bio':self.bio
        }
        return authors_dict

class Book(db.Model):
  __tablename__='book'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(250), nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('Author.id'))
  published_date = db.Column(db.Date)
  isbn = db.Column(db.String(255),unique=True)

  def to_dict(self):
        books_dict = {
        'id':self.id,
        'title':self.title,
        'author_id':self.author_id,
        'published_date':self.published_date,
        'isbn':self.isbn
        }
        return books_dict

class Borrow_Record(db.Model):
  __tablename__='borrowrecord'
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
  borrower_name = db.Column(db.String,nullable=False)
  borrow_date = db.Column(db.Date)
  return_date = db.Column(db.Date)

  def to_dict(self):
    return{
      'id':self.id,
      'book_id':self.book_id,
      'borrower_name':self.borrower_name,
      'borrow_date':self.borrow_date,
      'return_date':self.return_date,
    }
  
class User(db.Model):
  __tablename__='user'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False,unique=True)
  password = db.Column(db.String(255), nullable=False)
  role = db.Column(db.String(50), nullable=False, default='user')
  token = db.Column(db.String(255))
  last_request_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
  request_count = db.Column(db.Integer, default=0)
  def to_dict(self):
    return{
      'id':self.id,
      'username':self.username,
      'password':self.password,
      'role':self.role,
      'token':self.token
    }
  def generate_token(self):
    self.token = secrets.token_urlsafe(24)
  def reset_rate_limit(self):
     self.request_count=0
     self.last_request_time = datetime.datetime.utcnow
     db.session.commit()