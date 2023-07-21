import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # 用户POST提交了表单
        username = request.form['username']
        password = request.form['password']
        # 获取数据库连接
        db = get_db()
        error = None
        #进行基础的数据检查
        if not username:
            error = '必须设置用户名.'
        elif not password:
            error = '必须设置密码.'
        #如果没有错误写入数据库
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # 我们在创建数据库的时候加了唯一性检测，因此报出此异常
                error = f"用户 {username} 已经注册了."
            else:
                #跳转到登录页
                return redirect(url_for("auth.login"))
        #如果有错误则展示错误
        flash(error)
    # 如果是GET方式则渲染表单给用户
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        #查询用户
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = '无效的用户名或者密码.'
        elif not check_password_hash(user['password'], password):
            error = '密码错误.'

        if error is None:
            # 设置Session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')
        
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        

        return view(**kwargs)

    return wrapped_view