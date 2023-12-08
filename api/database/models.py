from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

now = datetime.now()
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

class Parent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    surname = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(15), nullable=False, unique=False)
    children = relationship('Child', back_populates='parent', cascade='all, delete-orphan')
    
class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    surname = db.Column(db.String(20), nullable=False, unique=False)
    gender = db.Column(db.String(15), nullable=False, unique=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parent = relationship('Parent', back_populates='children')
    tasks = relationship('Task', secondary='child_task')
    inventory = relationship('Inventory', back_populates='child')
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    price = db.Column(db.Float, nullable=True)

class StyleTamagochi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    head = db.Column(db.Integer, db.ForeignKey('item.id'))
    chest = db.Column(db.Integer, db.ForeignKey('item.id'))
    feet = db.Column(db.Integer, db.ForeignKey('item.id'))
    glasses = db.Column(db.Integer, db.ForeignKey('item.id'))
    scenario = db.Column(db.Integer, db.ForeignKey('item.id'))
    head_item = relationship('Item', foreign_keys=[head])
    chest_item = relationship('Item', foreign_keys=[chest])
    feet_item = relationship('Item', foreign_keys=[feet])
    glasses_item = relationship('Item', foreign_keys=[glasses])
    scenario_item = relationship('Item', foreign_keys=[scenario])


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    child = relationship('Child', back_populates='inventory')
    item = relationship('Item')

class Tamagochi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    growth = db.Column(db.Integer, nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    style_tamagochi_id = db.Column(db.Integer, db.ForeignKey('style_tamagochi.id'))
    child = relationship('Child')
    style_tamagochi = relationship('StyleTamagochi')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
    is_repeatable = db.Column(db.Boolean, nullable=False, default=False)
    task_parent_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    version = db.Column(db.Integer, default=1)
    task_parent = db.relationship('Task', remote_side=[id], backref='child_tasks')

class ChildTask(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), unique=True)
    done = db.Column(db.Integer, nullable=False, default=0)
    version = db.Column(db.Integer, default=1)
    child = relationship('Child')
    task = relationship('Task')

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(8), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)

class LogMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    child_task_id = db.Column(db.Integer, db.ForeignKey('child_task.id'))
    timestamp = db.Column(db.String(20), nullable=False)
    mood = relationship('Mood')
    child = relationship('Child')
    child_task = relationship('ChildTask')

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class LogReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    timestamp = db.Column(db.String(20), nullable=False)
    reward = relationship('Reward')
    child = relationship('Child')

class TaskReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    reward = relationship('Reward')
    task = relationship('Task')