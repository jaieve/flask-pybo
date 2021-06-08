# Flask-WTF를 사용하기 위해 필요한 Flask 환경변수 'SECRET_KEY'
# 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지를 판단해주는 역할을하는 CSRF 토큰
# CSRF토근은 SECRET_KEY를 기반으로 해서 생성된다.
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# 두 form은 Flas-WTF 모듈의 FlaskForm 클래스를 상속받음
# FlaskForm 클래스에는 subject와 content 속성이 있음.
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
# 플라스크 폼에는 여러 필드가 있다. (글자수 제한 있는 Stringfield, 글자수 제한 없는 TextAreaField)
# 모든 필드의 첫 인자는 form의 label로 사용
# 필드의 두번째 인자는 필드값을 검증할 때 사용
    # DataRequired : 필수 항목인지 점검
    # Email : 이메일인지 점검
    # Length : 길이를 점검

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])