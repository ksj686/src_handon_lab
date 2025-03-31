import sys
import shutil
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from PyQt5.QtWebChannel import QWebChannel

class FileManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()

        # 현재 스크립트와 동일한 디렉터리에서 index.html 파일 경로를 생성
        html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_screen.html')
        
        # QUrl을 통해 HTML 파일 로드
        self.browser.setUrl(QUrl.fromLocalFile(html_file_path))

        self.browser.setGeometry(0, 0, 800, 600)
        self.setCentralWidget(self.browser)
        self.setWindowTitle('파일 관리 앱')
        self.setGeometry(100, 100, 800, 600)

        # WebChannel 설정
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)

        self.commands = FileCommands()
        self.channel.registerObject('pyqtApp', self.commands)

        # 파일 경로를 저장할 변수
        self.src_path = ""
        self.dst_path = ""

        # UI 요소 설정 (파일 경로 선택 버튼과 레이블 추가)
        self.init_ui()

    def init_ui(self):
        # 위젯을 위한 레이아웃 설정
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        # src 경로 선택 버튼
        self.src_button = QPushButton('소스 파일/폴더 선택', self)
        self.src_button.clicked.connect(self.select_src)
        layout.addWidget(self.src_button)

        # dst 경로 선택 버튼
        self.dst_button = QPushButton('대상 파일/폴더 선택', self)
        self.dst_button.clicked.connect(self.select_dst)
        layout.addWidget(self.dst_button)

        # 경로를 표시할 레이블
        self.src_label = QLabel('소스 경로: 선택되지 않음', self)
        self.dst_label = QLabel('대상 경로: 선택되지 않음', self)
        layout.addWidget(self.src_label)
        layout.addWidget(self.dst_label)

        # 작업 버튼 (복사/이동/삭제 수행)
        self.execute_button = QPushButton('작업 실행', self)
        self.execute_button.clicked.connect(self.execute_command)
        layout.addWidget(self.execute_button)

        self.setCentralWidget(widget)

    def select_src(self):
        # 소스 경로 선택
        options = QFileDialog.Options()
        src_file, _ = QFileDialog.getOpenFileName(self, "소스 파일 선택", "", "모든 파일 (*)", options=options)

        if src_file:
            self.src_path = src_file
            self.src_label.setText(f"소스 경로: {src_file}")

    def select_dst(self):
        # 대상 경로 선택
        options = QFileDialog.Options()
        dst_folder = QFileDialog.getExistingDirectory(self, "대상 폴더 선택", options=options)

        if dst_folder:
            self.dst_path = dst_folder
            self.dst_label.setText(f"대상 경로: {dst_folder}")

    def execute_command(self):
        # 경로가 모두 선택되었는지 확인
        if not self.src_path or not self.dst_path:
            self.src_label.setText("소스 경로와 대상 경로를 모두 선택해야 합니다.")
            return

        # 작업을 수행하기 위한 명령어 준비
        command = f"copy {self.src_path} {self.dst_path}"

        # 명령어 실행 (파일 복사)
        result = self.commands.execute(command)
        self.src_label.setText(result)


class FileCommands(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str, result=str)
    def execute(self, command):
        try:
            result = self._execute_command(command)
            return result
        except Exception as e:
            return str(e)

    def _execute_command(self, command):
        parts = command.split()
        if len(parts) < 2:
            return "명령어가 불완전합니다."

        cmd = parts[0].lower()
        src = parts[1]
        dest = parts[2] if len(parts) > 2 else None

        if cmd == 'copy' and dest:
            return self.copy_file(src, dest)
        elif cmd == 'move' and dest:
            return self.move_file(src, dest)
        elif cmd == 'delete':
            return self.delete_file(src)
        else:
            return "알 수 없는 명령어 또는 잘못된 인수입니다."

    def copy_file(self, src, dest):
        if not os.path.exists(src):
            return "소스 파일이 존재하지 않습니다."
        try:
            shutil.copy(src, dest)
            return f"{src} 파일이 {dest}로 복사되었습니다."
        except Exception as e:
            return f"복사 중 오류 발생: {e}"

    def move_file(self, src, dest):
        if not os.path.exists(src):
            return "소스 파일이 존재하지 않습니다."
        try:
            shutil.move(src, dest)
            return f"{src} 파일이 {dest}로 이동되었습니다."
        except Exception as e:
            return f"이동 중 오류 발생: {e}"

    def delete_file(self, src):
        if not os.path.exists(src):
            return "파일이 존재하지 않습니다."
        try:
            os.remove(src)
            return f"{src} 파일이 삭제되었습니다."
        except Exception as e:
            return f"삭제 중 오류 발생: {e}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileManagerApp()
    window.show()
    sys.exit(app.exec_())
