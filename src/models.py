from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', lazy=True)

    

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.email,
            "favorites": list(map(lambda x: x.serialize(), self.favorites))
            
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
   
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(250), nullable=False)
    populaton = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    terrain_grasslands = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
           
            "name": self.name,
            "populaton": self.populaton,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain_grasslands": self.terrain_grasslands,
            "surface_water": self.surface_water,
            "climate": self.climate,


            
            # do not serialize the password, its a security breach
        }
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    favorite_lista = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __repr__(self):
        return '<Favorite %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "favorite_lista": self.favorite_lista
            
            
            # do not serialize the password, its a security breach
        }
