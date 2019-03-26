from watchapp import app
from flask import render_template
# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404