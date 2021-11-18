from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, Regexp         # проверяет наличие данных в форме


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Имя',
                       validators=[DataRequired(message='Поле не должно быть пустым'),
                                   Length(min=4,
                                          message='Слишком короткое имя. Оно должно быть больше 4 символов'),
                                   Regexp(r'^[a-zA-Zа-яА-Я]+$',
                                          message="Некорректное имя! "
                                                  "Используйте только символы латинского алфавита "
                                                  "и/или кириллицу")],
                       render_kw={"class": "form-control"})

    email = StringField('E-mail',
                        validators=[DataRequired(message='Поле не должно быть пустым'),
                                    Length(min=6,
                                           message='Слишком короткий e-mail. Он должен быть больше 6 символов'),
                                    Regexp(r'[a-zA-Z]+',
                                           message="Некорректный e-mail!")],
                        render_kw={"class": "form-control"})

    password = PasswordField('Пароль',
                             validators=[DataRequired(message='Поле не должно быть пустым'),
                                         Length(min=6,
                                                max=64,
                                                message='Некорректная длина пароля'),
                                         Regexp(r'[a-zA-Z0-9/+!#$%^&*()`~]+',
                                                message='Недопустимые символы в пароле, возможно, у вас '
                                                        'включена кириллица')],
                             render_kw={"class": "form-control"})

    valid_password = PasswordField('Повторите пароль',
                                   validators=[validators.DataRequired(),
                                               Length(min=6,
                                                      max=64,
                                                      message='Некорректная длина пароля'),
                                               Regexp(r'[a-zA-Z0-9/+!#$%^&*()`~]+',
                                                      message='Недопустимые символы в пароле, возможно, у вас '
                                                              'включена кириллица')],
                                   render_kw={"class": "form-control"})

    register = SubmitField('Зарегестрироваться', render_kw={"class": "btn btn-primary"})


class SigningInForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('E-mail',
                        validators=[Length(min=4, max=64, message="Слишком короткий e-mail"),
                                    DataRequired(message="Поле не должно быть пустым"),
                                    Regexp(r'[a-zA-Z0-9]+',
                                           message=r"Некорректный e-mail!")],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired(message="Поле не должно быть пустым"),
                                         Length(min=6,
                                                max=64,
                                                message='Некорректная длина пароля'),
                                         Regexp(r'[a-zA-Z0-9/+!@#$%^&*:~]+',
                                                message="Недопустимые символы в пароле, возможно, у вас "
                                                        "включена кириллица")],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Подтвердить', render_kw={"class": "btn btn-primary"})