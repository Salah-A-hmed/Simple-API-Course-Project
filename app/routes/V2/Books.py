from app.database import db
from app.models import Book
from app.models import User
from flask_cors import cross_origin
from flask import Blueprint,request,jsonify
import datetime

books_bp = Blueprint('books_v2',__name__)

# Get User from token
def get_user_From_token() :
 token = request.headers.get('Authorization')
 if not token:
     return None, {'msg': 'Token is missing!'}, 401
 user = User.query.filter_by(token=token).first()
 if not user:
     return None, {'msg': 'Invalid token!'}, 401
 return user, None, None

# Rate limit check
def rate_limit_check(user):
  current_time = datetime.datetime.utcnow()
  time_diff = current_time - user.last_request_time
  if time_diff.total_seconds() >= 60*60*24:
    user.reset_rate_limit()
  if user.request_count >= 100:
    return {'msg': 'Rate limit exceeded!'}, 429
  user.request_count +=1
  user.last_request_time= current_time
  return None,None

# Create Book
@books_bp.route('/',methods = ['post'])
@cross_origin()
def add_Book() :
   
  user,error,status = get_user_From_token()
  if error:
    return jsonify(error),status
  if user.Role != 'admin':
    return jsonify({"msg":"you don't have access!"})
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status

  data=request.get_json()
  new_Book = Book(title=data['title'],author_id=data['author_id'],published_date=data['published_date'],isbn=data.get('isbn',''))
  db.session.add(new_Book)
  db.session.commit()
 
  return jsonify(new_Book.to_dict())


# Get Book by id
@books_bp.route('/<int:Book_id>',methods = ['GET'])
@cross_origin()
def get_Course(Book_id) :
  user,error,status = get_user_From_token()
  if error:
   return jsonify(error),status
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status

  book = Book.query.get_or_404(Book_id)
  return jsonify(book.to_dict())


# Update Book
@books_bp.route('/<int:Book_id>',methods = ['PUT'])
@cross_origin()
def Update_Book(Course_id) :
    
  user,error,status = get_user_From_token()
  if error:
    return jsonify(error),status
  if user.Role != 'admin':
    return jsonify({"msg":"you don't have access!"})
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status

  book = Book.query.get_or_404(Course_id)
  data = request.get_json()
  book.title = data.get('title',book.title)
  book.author_id = data.get('author_id',book.author_id)
  book.published_date = data.get('published_date',book.published_date)
  book.isbn = data.get('isbn',book.isbn)
  db.session.commit()
  return jsonify(book.to_dict())


# Delete Book
@books_bp.route('/<int:Book_id>',methods = ['DELETE'])
@cross_origin()
def Delete_Book(Book_id) :
     
  user,error,status = get_user_From_token()
  if error:
    return jsonify(error),status
  if user.Role != 'admin':
    return jsonify({"msg":"you don't have access!"})
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status


  book = Book.query.get_or_404(Book_id)
  db.session.delete(book)
  db.session.commit()
  return jsonify({'result':True})
