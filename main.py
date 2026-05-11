import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import pyautogui

class GridClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_geometry = QApplication.primaryScreen().geometry()
        # 이력 저장을 위한 스택 (뒤로 가기용)
        self.history = []
        
        self.curr_x = 0
        self.curr_y = 0
        self.curr_w = self.screen_geometry.width()
        self.curr_h = self.screen_geometry.height()

        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(self.screen_geometry)
        self.setWindowTitle('Recursive Grid Clicker')
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(QColor(0, 255, 255, 180)) # 하늘색 선
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setFont(QFont('Malgun Gothic', 25, QFont.Weight.Bold))

        sub_w = self.curr_w / 3
        sub_h = self.curr_h / 3

        for i in range(3):
            for j in range(3):
                rect = QRect(int(self.curr_x + j * sub_w), 
                             int(self.curr_y + i * sub_h), 
                             int(sub_w), int(sub_h))
                painter.drawRect(rect)
                num = i * 3 + j + 1
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(num))

    def keyPressEvent(self, event):
        # 숫자를 눌렀는지 확인 (숫자패드 및 상단 숫자키 모두 포함)
        key = event.key()
        
        # Qt.Key_1 (0x31) ~ Qt.Key_9 (0x39) 범위 체크
        if Qt.Key.Key_1 <= key <= Qt.Key.Key_9:
            # 현재 상태 저장 (뒤로 가기용)
            self.history.append((self.curr_x, self.curr_y, self.curr_w, self.curr_h))
            
            # 숫자 값 추출 (Key_1은 49이므로 48을 빼면 1이 됨)
            choice = key - 48 
            
            row = (choice - 1) // 3
            col = (choice - 1) % 3
            
            self.curr_w /= 3
            self.curr_h /= 3
            self.curr_x += col * self.curr_w
            self.curr_y += row * self.curr_h
            
            print(f"선택번호: {choice}, 영역: {self.curr_x, self.curr_y}") # 디버깅용 출력
            self.update()

        # 뒤로 가기 (Backspace)
        elif key == Qt.Key.Key_Backspace:
            if self.history:
                self.curr_x, self.curr_y, self.curr_w, self.curr_h = self.history.pop()
                self.update()

        # 클릭 (Enter 또는 Space)
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space]:
            target_x = int(self.curr_x + (self.curr_w / 2))
            target_y = int(self.curr_y + (self.curr_h / 2))
            
            self.hide()
            if key == Qt.Key.Key_Space:
                pyautogui.rightClick(target_x, target_y)
            else:
                pyautogui.click(target_x, target_y)
            sys.exit()

        # 종료 (ESC)
        elif key == Qt.Key.Key_Escape:
            sys.exit()

        # Backspace: 뒤로 가기
        elif event.key() == Qt.Key.Key_Backspace:
            if self.history:
                self.curr_x, self.curr_y, self.curr_w, self.curr_h = self.history.pop()
                self.update()

        # Enter: 왼쪽 클릭 / Space: 오른쪽 클릭
        elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Space]:
            target_x = self.curr_x + (self.curr_w / 2)
            target_y = self.curr_y + (self.curr_h / 2)
            
            self.hide()
            if event.key() == Qt.Key.Key_Return:
                pyautogui.click(target_x, target_y)
            else:
                pyautogui.rightClick(target_x, target_y)
            sys.exit()

        # ESC: 종료
        elif event.key() == Qt.Key.Key_Escape:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridClicker()
    sys.exit(app.exec())
