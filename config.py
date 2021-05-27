# config.py 는 설정파일!

import os
BASE_DIR = os.path.dirname(__file__)
# SQLAlchemy
# 파이썬 모델을 이용해 테이블을 생성하고 컬럼을 추가하는 등의
# 작업을 할 수 있게 해주는 Flask-Migrate 라이브러리
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소
# pybo.db를 프로젝트의 base_dir에 저장하려는 것.
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Modification은 SQLalchemy의 이벤트를 처리하는 옵션. 파이보에서 안필요해서 비활성화(flase)

SECRET_KEY = "dev"