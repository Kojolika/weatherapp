print(f'Loading {__name__}')
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



app = Flask(__name__)
CORS(app, origins='http://localhost:3000',supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_EXPIRATION_DELTA'] = 10

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
jwt = JWTManager(app)

from auth import resources, models

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token_header, decrypted_token_payload: dict):
    jti = decrypted_token_payload['jti']
    return models.RevokeTokenModel.is_jti_blacklisted(jti)

@app.before_first_request
def create_tables():
    db.create_all()

#adds endpoints (url destinations essentially) to the api
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

if __name__ == "__main__":
    app.run(debug=True)

