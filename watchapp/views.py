from flask import Flask,url_for,render_template,redirect,flash,request
from watchapp import app, db
from flask_login import LoginManager,login_user,UserMixin,current_user,login_required,logout_user
from watchapp.models import User, Movie
from werkzeug.security import generate_password_hash,check_password_hash
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
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


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success!')
            return redirect(url_for('index'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')


# 修改记录
@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item is detele!')
    return redirect(url_for('index'))


@app.route('/testhash')
def hashtest():
    pw_hash = generate_password_hash('dog')
    print('____________?????????_______')
    print(check_password_hash(pw_hash, 'dog'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user();  # 登出用户
    flash('Goodbye')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['username']
        if not name or len(name) > 20:
            flash('Invalid Input!')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Setting updated')
        return redirect(url_for('index'))
    return render_template('settings.html')