from app.database import db
from app.models import Author
from app.models import User
from flask import Blueprint,request,jsonify,abort
import datetime

authors_bp = Blueprint('authors_v1',__name__)

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

# Create Author
@authors_bp.route('/',methods = ['POST'])
def add_Author() :
    user,error,status = get_user_From_token()
    if error:
      return jsonify(error),status
    if user.Role != 'admin':
      return jsonify({"msg":"you don't have access!"})
    rate_limit_eror,status= rate_limit_check(user)
    if rate_limit_eror:
     return jsonify(rate_limit_eror),status

    data=request.get_json()
    new_Author=Author(name=data['name'],bio=data['bio'])
    db.session.add(new_Author)
    db.session.commit()
 
    return jsonify(new_Author.to_dict())

# Get Author by id
@authors_bp.route('/<int:author_id>',methods = ['GET'])
def get_Author(author_id) :
  user,error,status = get_user_From_token()
  if error:
   return jsonify(error),status
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status

  author = Author.query.get_or_404(author_id)
  return jsonify(author.to_dict())

# Update Author
@authors_bp.route('/<int:author_id>',methods = ['PUT'])
def Update_Author(author_id) :
  user,error,status = get_user_From_token()
  if error:
     return jsonify(error),status
  if user.Role != 'admin':
   return jsonify({"msg":"you don't have access!"})
  
  rate_limit_eror,status= rate_limit_check(user)
  if rate_limit_eror:
   return jsonify(rate_limit_eror),status
  
  author = Author.query.get_or_404(author_id)
  data = request.get_json()
  author.name = data.get('name',author.name)
  author.bio = data.get('bio',author.bio)
  db.session.commit()
  return jsonify(author.to_dict())

# Delete Author
@authors_bp.route('/<int:author_id>',methods = ['DELETE'])
def Delete_Student(author_id) :
 user,error,status = get_user_From_token()
 if error:
   return jsonify(error),status
 if user.Role != 'admin':
   return jsonify({"msg":"you don't have access!"})

 rate_limit_eror,status= rate_limit_check(user)
 if rate_limit_eror:
   return jsonify(rate_limit_eror),status
  
 
 author = Author.query.get_or_404(author_id)
 db.session.delete(author)
 db.session.commit()
 return jsonify({'result':True})
