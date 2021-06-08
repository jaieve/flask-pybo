from pybo import db
#  두 클래스는 모든 모델의 기본클래스인 db.Model을 상속
# init.py에서 creat_app()하기전에 만든 SQLAlchemy 객체


# 질문모델 속성
# id  :질문 데이터 고유 번호
# subject : 질문 제목
# content : 질문 내용
# create_date : 질문작성 일시
# 외래키로 가진 Answer에서 만든 answer_set (db.backref로 설정)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

# 답변모델 속성
# id : 답변데이터의 고유 번호
# question_id : 질문데이터의 고유번호
# 외래키 설정 : question(Question 클래스)
# content : 답변 내용
# create_date : 답변 작성 일시
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    #ondelete : 연결된 테이블에서 해당 데이터가 삭제되면 답변 테이블의 데이터도 함께 삭제
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # db.Column이 아닌 db.relationship을 사용했기 때문에
    # 답변 모델 객체에서 질문 모델 객체의 제목을 참조하려면
    # answer.question.subject처럼 할 수 있다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))
