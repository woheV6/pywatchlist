
from watchapp import  db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# 用户表
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    def set_password(self,password):
        self.password_hash= generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

# 电影表
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    title = db.Column(db.String(60)) # 标题
    year = db.Column(db.String(4)) # 年份


# 留言表

class MessageBoard(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    content = db.Column(db.String(200)) #留言内容
from watchapp.models import User, Movie
