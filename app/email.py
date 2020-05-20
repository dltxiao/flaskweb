from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    # 被线程调用时，激活app上下文
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    # 引用app.config的方法
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKZ_MAIL_SUBJECT_PREFIX'] + subject,
            sender = app.config['FLASKZ_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 开辟一个新的线程来发送邮件，但新线程默认没有app上下文，所以把app作为参数传给这个函数，用于创建上下文。
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

