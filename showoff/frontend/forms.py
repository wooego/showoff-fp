#coding:utf-8
# Imports {{{
from wtforms import StringField, PasswordField, validators
from flask_wtf import FlaskForm

# }}}


class LoginForm(FlaskForm):
    username = StringField(
        u'用户名',
        validators=[validators.DataRequired(message=u'请输入用户名.')])
    password = PasswordField(
        u'密　码',
        validators=[validators.DataRequired(message=u'请输入密码.')])
