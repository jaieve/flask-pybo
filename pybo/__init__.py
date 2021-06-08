from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import config
# config.py에서 설정해준 다음, 생성한 app에 적용하기 위해 임포트한 config 적용

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# create_app()로 app 만들어질때 마다 생성되지 않게 밖에서 선언
# create_app() 될때 마다 초기화(init_app())
# db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 불러올 수 없다

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #ORM(SQLAlchemy)
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    #생성된 모델(models.py의 Question, Answer 클래스)를 migrate기능에 인식시키기
    from . import models
    # Terminal에서 flask db migrate, flask db upgrade 명령 입력하면
    # pybo.db 리비전 파일이 생성되고(SQLite의 데이터베이스파일)
    # question와 answer 데이블이 만들어진다.

    #블루프린트
    # 상대경로인 views 폴더에서 3가지 view.py 임포트
    # 플라스트 어플인 app이 생성될 때 각 블루프린트 적용
    from .views import main_views,question_views, answer_views, auth_views, comment_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)


    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app