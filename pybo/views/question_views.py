from flask import Blueprint, render_template, request, url_for

from pybo.models import Question
from ..forms import QuestionForm

from datetime import datetime
from werkzeug.utils import redirect
from .. import db
from ..forms import QuestionForm, AnswerForm


bp = Blueprint('question', __name__, url_prefix='/question')
# main_views.py의 bp와 구분하기 위해 url_prefix를 '/'에서 '/question'으로 수정
# main_views.py의 bp : 'main', url_prefix='/'

# main_views.py의 index()에서 기능 분리하면서 가져온 기능의 메서드 _list()로 변경
# list는 파이썬으 예약어이기때문에 함수명에 쓸수 없음
# 라우트도 '/' 에서 "/list'로 변경
@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

# 질문목록에서 링크를 누르면 다음의 url을 요청
# url = '/question/detail/2/'
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # 존재하지 않는 question_id를 요청할 경우 404오류페이지를 표시해주는 메서드
    #질문내용을 Question(클래스, pybo.db)에서 꺼내 렌더링html로 전송
    return render_template('question/question_detail.html', question=question, form=form)

# url = '/question/create/'
@bp.route('/create/', methods=('POST', 'GET'))
def create():
    form = QuestionForm()
    if request.method =='POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date = datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

