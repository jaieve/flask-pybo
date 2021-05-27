from flask import Blueprint, url_for
from werkzeug.utils import redirect
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')
#Blueprint 클래스로 객체 생성시 이름, 모듈명, URL프리픽스값을 전달해야 함.
# 블루프린트 객체 이름 'main'은 나중에 url_for로 함수명을 찾을 때 사용된다.
# url_for('main')

#@bp.route에서 bp는 Blueprint 클래스로 생성한 객체를 의미
@bp.route('/hello')
def hello_pybo():
    return "Hello, Pybo!"

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
    # url_for 메서드에서 전달되는 인수는 controller에 존재하는 각 함수 이다.
    # 만약 다른 controller.py(_views.py)에 존재하는 함수라면 임포트하지 않고
    # 'blueprint_name.method_name' 형식으로 인수를 전달해준다.
