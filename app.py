from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click
WIN = sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=prefix+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例



@app.cli.command() # 注册为命令
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done!')
@app.route('/') # 装饰器
@app.route('/index') # 装饰器
@app.route('/home') # 装饰器
def main():
    user = User.query.first()
    movies= Movie.query.all()
    return render_template('index.html',user=user,movies=movies)
@app.route('/test')
def test():
    return  '<h1>哈哈</h1><img src="http://helloflask.com/totoro.gif">'
@app.route('/user/<name>')
def userName(name):
    return  'User Page: %s' % name
@app.route('/hello') # 装饰器
def hello():
    print(url_for('test'))
    print(url_for('userName',name='xixi'))
    return 'Welcome to my watchlist!!'
@app.route('/img') # 装饰器
def img():
    return ''

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    title = db.Column(db.String(60)) # 标题
    year = db.Column(db.String(4)) # 年份

