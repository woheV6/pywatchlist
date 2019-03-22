from flask import Flask,url_for
app = Flask(__name__)
@app.route('/') # 装饰器
@app.route('/index') # 装饰器
@app.route('/home') # 装饰器
def main():
    return 'Welcome to my watchlist!!'
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

