from app.database import db
from app.models import Borrow_Record
from app.models import User
from flask import Blueprint,request,jsonify,abort
import datetime

Borrow_Records_bp = Blueprint('borrowrecords_v2',__name__)

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


# Create Borrow_Record
@Borrow_Records_bp.route('/',methods = ['POST'])
def add_Borrow_Record() :
       
 user,error,status = get_user_From_token()
 if error:
   return jsonify(error),status
 if user.Role != 'admin':
  return jsonify({"msg":"you don't have access!"})
 rate_limit_eror,status= rate_limit_check(user)
 if rate_limit_eror:
  return jsonify(rate_limit_eror),status
   
 data=request.get_json()
 new_Borrow_Record=Borrow_Record(book_id=data['book_id'],borrower_name=data['borrower_name'],borrow_date=data['borrow_date'],return_date=data['return_date'])
 db.session.add(new_Borrow_Record)
 db.session.commit()
 
 return jsonify(new_Borrow_Record.to_dict())

# Get Borrow_Record by id
@Borrow_Records_bp.route('/<int:Borrow_Record_id>',methods = ['GET'])
def get_Borrow_Record(Borrow_Record_id) :
 user,error,status = get_user_From_token()
 if error:
  return jsonify(error),status
 rate_limit_eror,status= rate_limit_check(user)
 if rate_limit_eror:
  return jsonify(rate_limit_eror),status

 borrowrecord = Borrow_Record.query.get_or_404(Borrow_Record_id)
 return jsonify(borrowrecord.to_dict())

# Update Borrow_Record
@Borrow_Records_bp.route('/<int:Borrow_Record_id>',methods = ['PUT'])
def Update_Borrow_Record(Borrow_Record_id) :
       
 user,error,status = get_user_From_token()
 if error:
   return jsonify(error),status
 if user.Role != 'admin':
  return jsonify({"msg":"you don't have access!"})
 rate_limit_eror,status= rate_limit_check(user)
 if rate_limit_eror:
  return jsonify(rate_limit_eror),status
  
 borrowrecord = Borrow_Record.query.get_or_404(Borrow_Record_id)
 data = request.get_json()
 borrowrecord.book_id = data.get('book_id',borrowrecord.book_id)
 borrowrecord.borrower_name = data.get('borrower_name',borrowrecord.borrower_name)
 borrowrecord.borrow_date = data.get('borrow_date',borrowrecord.borrow_date)
 #  In Verson 2 I Decided that return_date shouldnot be changed
 #borrowrecord.return_date = data.get('return_date',borrowrecord.return_date)
 db.session.commit()
 return jsonify(borrowrecord.to_dict())

# Delete Borrow_Record
@Borrow_Records_bp.route('/<int:Borrow_Record_id>',methods = ['DELETE'])
def Delete_Borrow_Record(Borrow_Record_id) :
      
 user,error,status = get_user_From_token()
 if error:
   return jsonify(error),status
 if user.Role != 'admin':
  return jsonify({"msg":"you don't have access!"})
 rate_limit_eror,status= rate_limit_check(user)
 if rate_limit_eror:
  return jsonify(rate_limit_eror),status
  
 borrowrecord = Borrow_Record.query.get_or_404(Borrow_Record_id)
 db.session.delete(borrowrecord)
 db.session.commit()
 return jsonify({'result':True})
