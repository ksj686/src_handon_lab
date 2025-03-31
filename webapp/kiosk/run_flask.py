# app.py
from flask import Flask, request
from flask_cors import CORS
import logging

app = Flask(__name__)
# CORS(app) # 됨
CORS(app, resources={r"/*": {"origins": "*"}}) # 됨
# CORS(app, origins="172.16.10.248")
# CORS(app, resources={r'*':{'origins':['http://localhost']}})
# CORS(app, resources={r'/*':{'origins':['http://172.16.10.248']}})
# 포트번호 계속 바뀜
# CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:55667", "http://localhost:55667"], "allow_headers": "*"}}) 
# CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "Content-Type"}}) # 됨





app.logger.setLevel(logging.DEBUG)

# 기본 핸들러 제거 
#if app.logger.hasHandlers(): 
#    app.logger.handlers.clear()


# 콘솔 핸들러 추가 (필요할 경우 파일 핸들러도 추가할 수 있음)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.json.get('item_name')
    item_price = request.json.get('item_price')
    # 받은 데이터 처리
    app.logger.debug(f"장바구니에 {item_name} ({item_price}원)이 추가되었습니다.")
    app.logger.info('info')
    client_ip = request.remote_addr  # 클라이언트의 IP 주소
    client_port = request.environ.get('REMOTE_PORT')  # 클라이언트의 포트 번호
    app.logger.info(f'ip: {client_ip}, port: {client_port}')
    # print(f"장바구니에 {item_name} ({item_price}원)이 추가되었습니다.")
    return {'status': 'success'}

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    # 주문 처리 로직
    app.logger.debug("주문이 완료되었습니다.")
    app.logger.info('confirm_order')
    client_ip = request.remote_addr  # 클라이언트의 IP 주소
    client_port = request.environ.get('REMOTE_PORT')  # 클라이언트의 포트 번호
    app.logger.info(f'ip: {client_ip}, port: {client_port}')
    # print("주문이 완료되었습니다.")
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)
