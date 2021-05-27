from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')
# main_views.py의 bp : 'main', url_prefix='/'
# question_views.py의 ㅠㅔ : 'question', url_prefix='/question'

# url = '/answer/create/2/'
@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
        # Question과 Answer 모델이 연결되어 있어 backref에 설정한 answer_set.
        # question 테이블로 접근한 위으 하드코딩은 아래의 Answer 테이블에 연결하는 코드와 동일하다
        # answer = Answer(question=question, content=content, create_date=datetime.now())
        # db.session.add(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html',question=question, form=form)