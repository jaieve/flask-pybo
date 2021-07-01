from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from sqlalchemy import func
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer, User, question_voter
from ..views.auth_views import login_required
# Flask-WTF (플라스크 폼모듈)로 만든 form을 가져오기위해 상위디렉터리의 forms.py로부터
# QuestionForn(create())과 AnswerForm 임포트


bp = Blueprint('question', __name__, url_prefix='/question')
# main_views.py의 bp와 구분하기 위해 url_prefix를 '/'에서 '/question'으로 수정
# main_views.py의 bp : 'main', url_prefix='/'

# main_views.py의 index()에서 기능 분리하면서 가져온 기능의 메서드 _list()로 변경
# list는 파이썬으 예약어이기때문에 함수명에 쓸수 없음
# 라우트도 '/' 에서 "/list'로 변경
@bp.route('/list/')
def _list():
    #입력파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    # GET 방식으로 요청한 URL에서 page값을 가져올 때 사용한다.
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    #페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)

# 질문목록에서 링크를 누르면 다음의 url을 요청
# url = '/question/detail/2/'
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    # 질문 상세 템플릿에서 답변이 작성될 때 필요한 AnswerForm
    question = Question.query.get_or_404(question_id)
    # 존재하지 않는 question_id를 요청할 경우 404오류페이지를 표시해주는 메서드
    #질문내용을 Question(클래스, pybo.db)에서 꺼내 렌더링html로 전송
    return render_template('question/question_detail.html', question=question, form=form)

# url = '/question/create/'
@bp.route('/create/', methods=('POST', 'GET'))
@login_required
def create():
    form = QuestionForm()
    # method가 POST : 질문등록페이지(/question/create/)에서 폼 제출
    # form값 받아서 db에 commit해야 함.
    if request.method =='POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date = datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # method가 GET이라면 질문게시판페이지에서 '질문등록하기'버튼을 누른 것
    # 질문작성 form을 html로 전달. url은 라우트함수로 지정된다. ('/question/create/
    return render_template('question/question_form.html', form=form)


@bp.route("/modify/<int:question_id>", methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method =='POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))