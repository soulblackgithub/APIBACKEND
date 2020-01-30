from flask import Flask
from flask_restplus import Api,Resource,fields
from flask_sqlalchemy import SQLAlchemy
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
db.create_all()   
userModel = users.model('userModel', {
'username' : fields.String(),
'email' : fields.String()

}

)

@users.route('/users')
class Users(Resource):
    def get(self):
        return 'ciao'

    @users.expect(userModel)       
    def post(self):
        '''create new user'''
        return'user expect'


@app.route("/")
def main():
    return "Welcome!"
if __name__ == "__main__":
    app.run(debug=True)