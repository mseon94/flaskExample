# 사전 설치 : pip install flask pymysql requests
from flask import Flask
from config import Config
from backend.models.db import Database
from backend.routes.main_routes import main_bp, init_db
import atexit   # 애플리케이션 종료시 실행을 요청 (ex. DB연결 종료)

def create_app():
    """ 애플리케이션 팩토리 함수 """
    # 팩토리내에서 Flask 앱 초기화
    # app.py가 루트 폴더에 있으므로 탬플릿과 정적 파일 경로가 기본값으로 적용됨
    app = Flask(__name__)  
    
    # config.py 및 .env 활용
    app.config.from_object(Config)
    
    # DB 초기화 및 관리
    db = Database() 
    
    # 애플리케이션 종료 시 DB 연결 종료 예약
    atexit.register(db.close)   
    
    # Blueprint 등록 및 DB 인스턴스 주입
    init_db(db)
    app.register_blueprint(main_bp)
    
    return app

# 애플리케이션 생성
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)