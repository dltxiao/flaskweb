from flask import Flask, render_template, request, make_response, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'someonelikeyou'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    # 增加这个关系声明后，可以使用user.role来获取Role模型对象,可以使用user.role.id, user.role.name来获取对应的值。
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    sexy = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Hello, Flaskz</h1><p>Your browser is {}'.format(user_agent)
    ##
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer','42')
    # return response
    ##
    # return redirect('http://127.0.0.1:5000/user/anonymous')
    ##
    # 初始化name 为空值
    # name=None
    # 生成一个表单
    form=NameForm()
    # 检测表单是否提交过
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user == None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changeed your name! ') #在模板中使用get_flashed_messages()
        # 赋值name为上一次提交的name
        session['name'] = form.name.data 
        # 清空新的表单的name的input区域，避免上一次提交的name残留,使用 POST / 重定向 / GET 方式后不再被需要
        # form.name.data = ''
    # 渲染index.html， 绘制新的表单，显示上一次提交NameForm.name，以及当前时间。

    # return render_template('index.html', form=form, name=name, current_time = datetime.utcnow())
    # POST / redirct / GET 方式,点击提交后，返回下面的重定向，让客户端重新以GET方式获取/，最外层的return则处理GET请求，以session中保存的信息来渲染页面。
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known',False), current_time = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    # return '<h1>hello, {}!</h1>'.format(name)
    return render_template('user.html', name=name)

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h1>Hello, {}</h1>'.format(user.name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
