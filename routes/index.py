from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from models.topic import Topic
from models.reply import Reply
from bson import ObjectId
import os
import uuid

from routes import current_user
from utils import log

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/setting/<string:id>", methods=['POST'])
def setting(id):
    form = request.form
    # 用类函数来判断
    User.update(id,form)
    return redirect(url_for('index.user_detail', id=id))


@main.route("/setting_password/<string:id>", methods=['POST'])
def setting_password(id):
    form = request.form
    u = User.validate_password(form)
    if u is None:
        abort(404)
    else:
        # del form['old_pass']
        User.update_password(id,form)
        return redirect(url_for('index.user_detail', id=id))





@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login u', u)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login', session)
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        topic = Topic.all()
        reply = Reply.all()
        t = sorted(topic, key=lambda l: l.updated_time, reverse=True)
        r = sorted(reply, key=lambda s: s.updated_time, reverse=True)
        return render_template('profile.html', user=u, topic=t, reply=r)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    u = current_user()

    # file 是一个上传的文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        # filename = secure_filename(file.filename)
        # 2017/6/14/19/56/yiasduifhy289389f.png
        # import time
        # filename = str(time.time()) + filename
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        User.update(u.id, dict(
            user_image='/uploads/' + filename
        ))

    return redirect(url_for(".profile"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)


@main.route('/user/<string:id>')
def user_detail(id):
    u = User.find(id)
    if u is None:
        abort(404)
    else:
        topic = Topic.all()
        reply = Reply.all()
        t = sorted(topic, key=lambda l: l.updated_time, reverse=True)
        r = sorted(reply, key=lambda s: s.updated_time, reverse=True)
        return render_template('profile.html', user=u, topic=t, reply=r)


@main.route('/user_setting/<string:id>')
def user_setting(id):
    u = User.find(id)
    return render_template('setting.html', user=u)
