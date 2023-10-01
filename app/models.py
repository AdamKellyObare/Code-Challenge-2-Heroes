from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from flask import Flask, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError, DataError


db = SQLAlchemy()
app = Flask(__name__)

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    powers = relationship("HeroPowers", back_populates="hero")


class Powers(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    Powers = relationship("HeroPowers", back_populates="power")

    @validates('description')
    def validate_description(self, key, description):
        assert len(description)>= 20
        return description


class HeroPowers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    hero = relationship("Hero", back_populates="powers")
    power = relationship("Powers", back_populates="heroes")

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average']
        return strength
    
# for the routes add the following

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    output = []
    for hero in heroes:
        output.append({'id' : hero.id, 
                       'name' : hero.name, 
                       'super_name' : hero.super_name})
    return jsonify(output)

@app.route('/heroes/<id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(jsonify({'error': 'Hero not found'}), 404)
    powers = [{'id': power.id, 
               'name': power.name, 
               'description': power.description} for power in hero.powers]
    return jsonify({'id' : hero.id, 
                    'name' : hero.name, 
                    'super_name' : hero.super_name, 
                    'powers': powers})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Powers.query.all()
    output = []
    for power in powers:
        output.append({'id' : power.id, 
                       'name' : power.name, 
                       'description' : power.description})
    return jsonify(output)

@app.route('/powers/<id>', methods=['GET'])
def get_power(id):
    power = Powers.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)
    return jsonify({'id' : power.id, 
                    'name' : power.name, 
                    'description' : power.description})

@app.route('/powers/<id>', methods=['PATCH'])
def update_power(id):
    power = Powers.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)
    try:
        power.description = request.json['description']
        db.session.commit()
    except (IntegrityError, DataError):
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    return jsonify({'id' : power.id, 
                    'name' : power.name, 
                    'description' : power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    power_id = request.json['power_id']
    hero_id = request.json['hero_id']
    strength = request.json['strength']
    try:
        new_hero_power = HeroPowers(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(new_hero_power)
        db.session.commit()
        hero = Hero.query.get(hero_id)
        powers = [{'id': power.id, 
                   'name': power.name, 
                   'description': power.description} for power in hero.powers]
        return jsonify({'id' : hero.id, 
                        'name' : hero.name, 
                        'super_name' : hero.super_name, 
                        'powers': powers}), 201
    except (IntegrityError, DataError):
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    
if __name__ == "__main__":
    app.run(debug=True)