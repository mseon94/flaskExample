from flask import Blueprint, render_template, request
from backend.services.bmi import BMICalculator

# Blueprint 생성
main_bp = Blueprint('main', __name__)

# DB 인스턴스는 앱 초기화 시 주입받거나 전역으로 관리
db = None

"""
database = Database()
init_db(database)
처럼 DB 객체를 받는 곳 -> app.py에서 호출
// DB 인스턴스를 설정하는 헬퍼 함수
"""
def init_db(database_instance):
    global db
    db = database_instance
    
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        # 입력값 유효성 검사
        if weight <= 0 or height <= 0:
            return render_template('index.html', error="체중과 신장은 양수여야 합니다.")
        
        # BMI 계산
        calculator = BMICalculator(weight, height)
        result = calculator.get_result()
        
        # 데이터베이스에 저장
        db.save_bmi_record(weight, height, result["bmi"], result["category"])
        
        return render_template('result.html', 
                              bmi=result["bmi"], 
                              category=result["category"],
                              weight=weight,
                              height=height)
    except ValueError:
        return render_template('index.html', error="유효한 숫자를 입력해주세요.")
    
@main_bp.route('/history')
def history():
    # 최근 BMI 기록 10개 가져오기
    # db가 있을 경우에만 실행하도록 리팩토링
    records = []
    if db:
        records = db.get_bmi_records(10)
    return render_template('history.html', records=records)