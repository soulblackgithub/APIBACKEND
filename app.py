from flask import Flask,request,jsonify
from flask_restplus import Api,Resource,fields
from flask_sqlalchemy import SQLAlchemy
import traceback
app = Flask(__name__)
api = Api(app,
version='0.1',
title='the perfect api',
decription='endpoins for class project at ial',
endpoint='api')
app.config['SQLALCHEMYDATABASE_URI']= 'sqlite://test.db'
db = SQLAlchemy(app)
users = api.namespace('users', description = 'CRUD operation for users') 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def asDict(self):
        return{

            'id' : self.id,
            'username'  : self.username,
            'email'  : self.email
        }

db.create_all()   
userModel = users.model('userModel', {
'username' : fields.String(),
'email' : fields.String()

}

)
resp = {200:'success', 400:'user already in db', 406:'content not allowed', 413:'payload too large', 500:'server error'}

@users.route('/users')
class Users(Resource):
    def get(self):

        return 'ciao'

    @users.expect(userModel)       
    def post(self):
        
        '''create new user MODIFIED'''
        try:

            data=request.get_json()
            app.logger.info(data)
            username_request = data.get("username")
            email_request = data.get("email")
            u=User.query.filter_by(username=username_request).first()
            if(u is not None):
                return 'user already in db', 400
            u=User.query.filter_by(email=email_request).first()
            if(u is not None):
                return 'user already in db', 400

            u = User(username=username_request, email=email_request)
            app.logger.info(type(u))
            db.session.add(u)
            db.session.commit()
        except:
            app.logger.error(traceback,format_exc())
            return 'ERROR SERVER SIDE', 500
            

        return jsonify(u.asDict())



@app.route("/")
def main():
    return "Welcome!"
if __name__ == "__main__":
    app.run(debug=True)