from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from flask import Flask


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
    
