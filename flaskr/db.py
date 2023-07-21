import sqlite3

import click
from flask import current_app, g


# 获取数据库连接
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# 初始化数据库，创建表
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

# 定义命令行工具
@click.command('init-db')        
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("完成数据库初始化")


#关闭数据库连接
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
# 注册函数        
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)