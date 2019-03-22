from flask import Flask,url_for,render_template
app = Flask(__name__)
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
@app.route('/') # 装饰器
@app.route('/index') # 装饰器
@app.route('/home') # 装饰器
def main():
    return render_template('index.html',name=name,movies=movies)
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

