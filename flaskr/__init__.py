import os

from flask import Flask


def create_app(test_config=None):
    # 创建Flask对象，设置加载
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # 加载配置文件
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 加载测试配置
        app.config.from_mapping(test_config)

    # 创建必要的目录
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #初始化数据库
    from . import db
    db.init_app(app)
    
    # 注册蓝图
    from . import auth
    from . import blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    # 注册一个简单的路由
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app