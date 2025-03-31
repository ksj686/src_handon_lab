import sys
import os
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel

class FileCommands(QObject):
    @pyqtSlot(str)
    def add_to_cart(self, item_name, item_price):
        print(f"장바구니에 {item_name} ({item_price}원)이 추가되었습니다.")

    @pyqtSlot(str)
    def confirm_order(self):
        print("주문이 완료되었습니다.")

class KioskApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("음식점 키오스크")
        self.setGeometry(100, 100, 800, 600)

        # HTML 로드
        self.browser = QWebEngineView(self)
        # 현재 스크립트와 동일한 디렉터리에서 index.html 파일 경로를 생성
        html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kiosk.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_file_path))
        self.setCentralWidget(self.browser)

        # WebChannel 설정
        self.channel = QWebChannel(self)
        self.browser.page().setWebChannel(self.channel)

        # JavaScript에서 호출할 Python 객체 등록
        self.commands = FileCommands()
        self.channel.registerObject('pyqtApp', self.commands)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KioskApp()
    sys.exit(app.exec_())
