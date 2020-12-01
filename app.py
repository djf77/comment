# app.py
from flask import Flask, request, session, jsonify
from mysql.connector import connect
from werkzeug.security import generate_password_hash, check_password_hash


config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'board'
}


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


# 自定义错误
class HttpError(Exception):
    def __init__(self, status_code, message):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            'status': self.status_code,
            'msg': self.message
        }


# 注册一个错误处理器
@app.errorhandler(HttpError)
def handle_http_error(error):
    response = jsonify(error.to_dict())  # 创建一个Response实例
    response.status_code = error.status_code  # 修改HTTP状态码
    return response


def get_connection():
    conn = connect(user=config.get('user'), password=config.get('password'),
                   database=config.get('database'))
    cursor = conn.cursor()

    return conn, cursor


# 注册接口
@app.route('/add', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    sex = data.get('sex')
    age = data.get('age')
    address = data.get('address')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 判断用户名是否存在
    cursor.execute('select count(*) from `users` where `username`=%s', (username,))
    count = cursor.fetchone()
    # 如果用户名已存在则返回409错误
    if count[0] >= 1:
        raise HttpError(409, '用户名已存在')

    # 插入数据库与加密
    cursor.execute('insert into `users`(`username`, `password`, `sex`, `age`, `address`,) values (%s, %s, %s, %s, %s)',
                   (username, generate_password_hash(password), sex, age, address))
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return '创建成功'


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 获取传入的用户的密码和id
    cursor.execute('select `id`, `password` from `users` where `username`=%s', (username, ))
    values = cursor.fetchone()

    # 如果数据库中没有这个用户，则fetchone函数会返回None
    if values is None:
        raise HttpError(400, '用户名或密码错误')

    user_id = values[0]  # 用户的id
    pwd = values[1]  # 数据库中的密码

    # 判断
    if not check_password_hash(pwd, password):  # 如果密码不同
        raise HttpError(400, '用户名或密码错误')
    session['username'] = username
    session['user_id'] = user_id

    return '登录成功'


# 个人信息界面
@app.route('/me', methods=['GET'])
def get_information():
    # 获取数据库连接
    conn, cursor = get_connection()
    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')
    # 数据库操作
    cursor.execute('select count() from `users` where `username`=%s', (session.get('user_id')))
    data = cursor.fetchone()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    return data


# 修改用户名
@app.route('/username', methods=['PUT'])
def change_username():
    data = request.get_json(force=True)
    username = data.get('username')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')

    # 判断用户名是否存在
    cursor.execute('select count(*) from `users` where id=%s', (username,))
    count = cursor.fetchone()[0]
    # 如果用户名已存在则返回409错误
    if count >= 1:
        raise HttpError(409, '用户名已存在')

    # 根据登录时储存的user_id在where子句中定位到具体的用户并更新他的用户名
    cursor.execute('update `users` set `username`=%s where id=%s', (username, session.get('user_id')))

    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return '修改用户名成功'


# 修改密码
@app.route('/password', methods=['PUT'])
def change_password():
    data = request.get_json(force=True)
    password = data.get('password')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')

    # 根据登录时储存的user_id在where子句中定位到具体的用户并更新他的密码
    cursor.execute('update `users` set `password`=%s where id=%s',
                   (generate_password_hash(password), session.get('user_id')))

    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return '修改密码成功'


@app.route('/information', methods=['PUT'])
def change_information():
    data = request.get_json(force=True)
    sex = data.get('sex')
    age = data.get('age')
    address = data.get('address')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')

    # 数据库操作
    cursor.execute('update `users` set `sex`, `age`, `address`,=%s where id=%s', (sex, age, address,
                   session.get('user_id')))

    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return '修改个人信息成功'


if __name__ == '__main__':
    app.run()
