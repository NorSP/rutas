"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorite  
#from models import Person
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None) #Formas de recibir el front
    password = request.json.get("password", None) #Formas de recibir el front
    login_user = User.query.filter_by(email=email).first()
    if login_user is None:
        return jsonify({"msg": "User don't exist"}), 404
    elif email != login_user.email or password != login_user.password:
        return jsonify({"msg": "Bad email or password"}), 401
#crea el acceso y devuelve un token a las personas al loguearse
    access_token = create_access_token(identity=email)
    response_body={
        "access_token":access_token,
        "user":login_user.serialize()
        
    }
    return jsonify(response_body)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required() #portero de la ruta 
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    login_user = User.query.filter_by(email=current_user).first()
    if login_user is None:
        return jsonify({"msg": "User don't exist"}), 404
    response_body={
        
        "user":login_user.serialize()
        
    }
    return jsonify(response_body), 200




# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def users():

    all_users = User.query.all()
    results = list(map(lambda item: item.serialize(), all_users))
    return jsonify(results), 200

@app.route('/users', methods=['POST'])
def usersPost():
    body = json.loads(request.data)
    query_user = User.query.filter_by(email=body["email"]).first()
    favorites_user = Favorite.query.first()
    if query_user is None:
        new_user = User(email=body["email"], password=body["password"], name=body["name"], is_active=bool(body["is_active"]), id=len(User.query.all())+1)
        db.session.add(new_user)
        db.session.commit()
        new_table_favorite = Favorite(favorite_lista="",id=len(Favorite.query.all())+1)
        db.session.add(new_table_favorite)
        db.session.commit()

        response_body = {
            "msg" : "created user"
        }
        return jsonify(response_body), 200
    

    
    return jsonify("usuario existente")



@app.route('/users/<int:users_id>', methods=['GET'])
def usersId(users_id):
    
    usuario = User.query.filter_by(id = users_id).first()
      #no se mapea en este caso
    return jsonify(usuario.serialize()), 200


@app.route('/planets', methods=['GET'])
def planets():
    
    planetas = Planets.query.all()
    print(planetas)
    results = list(map(lambda item: item.serialize(), planetas))
    return jsonify(results), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def planetsId(planets_id):
    
    planetasId = Planets.query.filter_by(id = planets_id).first()
      #no se mapea en este caso
    return jsonify(planetasId.serialize()), 200

@app.route('/users/<int:users_id>/favorite', methods=['GET'])
def favoritesId(users_id):
    favoritesUser = Favorite.query.filter_by(id = users_id).first()
    if favoritesUser is None:
        obj = {
            "msg": "error; the user does not exist"
        }
        return jsonify(obj), 404
    obj = {
        "favorite_lista": dict(favoritesUser.serialize())["favorite_lista"].split("$$")
    }

    
    return jsonify(obj), 200

@app.route('/users/<int:users_id>/favorite', methods=['PUT'])
def favoritePost(users_id):

    body = json.loads(request.data)
    favorites_user = Favorite.query.filter_by(id = users_id).first()
    
    
    if body["favorite"] in dict(favorites_user.serialize())["favorite_lista"]:
        
       
        aux = dict(favorites_user.serialize())["favorite_lista"]
        aux = aux.split("$$"+body["favorite"])
        aux = ''.join(aux)
        favorites_user.favorite_lista = aux 
        db.session.commit()

        return jsonify({"msg": "the favorite has been deleted successfully" }), 200
        
    elif favorites_user is None and body is None:
        return jsonify({"msg": "There is no list for this user"}), 404
    favorites_user.favorite_lista = dict(favorites_user.serialize())["favorite_lista"]+"$$"+body["favorite"]
    db.session.commit()
    return jsonify({"msg": "The favorite has been added successfully"}), 404


    
    

   










    



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
