from flask import Flask,url_for,render_template,redirect,flash,request
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


app.config['SECRET_KEY'] = '123456'

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

# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# 模版上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 主键
    title = db.Column(db.String(60)) # 标题
    year = db.Column(db.String(4)) # 年份

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        print(title)
        print(year)
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/login')
def login():
     return render_template('login.html')
# 修改记录
@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录
# 删除记录
@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item is detele!')
    return redirect(url_for('index'))