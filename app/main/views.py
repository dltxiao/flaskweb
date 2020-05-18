from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app
# 导入本层目录中的某个文件
from . import main
# 导入本层目录中的某个文件中的对象
from ..email import send_email
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        user = User.query.filter_by(username=form.name.data).first()
        if user == None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # 增加蓝本后，邮件功能无法使用，
            if current_app.config['FLASKZ_ADMIN']:
                print('1111111111111111111111111111111111111111')
                send_email(current_app.config['FLASKZ_ADMIN'], 'New User',
                        'mail/new_user', user=user)
        else:
            session['known'] = True
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changeed your name! ') #在模板中使用get_flashed_messages()
        # 赋值name为上一次提交的name
        session['name'] = form.name.data
        # 同一蓝本中的重定向可以简写为.xxx，不同蓝本中应写全blurprint_name.path_name
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),current_time=datetime.utcnow())
