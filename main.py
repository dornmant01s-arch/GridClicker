import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import pyautogui

class GridClicker(QWidget):
    def __init__(self):
        super().__init__()
        # 화면 전체 크기 가져오기
        self.screen_geometry = QApplication.primaryScreen().geometry()
        self.history = []
        
        self.curr_x = 0
        self.curr_y = 0
        self.curr_w = self.screen_geometry.width()
        self.curr_h = self.screen_geometry.height()

        self.initUI()

    def initUI(self):
        # 배경 투명, 테두리 없음, 항상 위 옵션
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(self.screen_geometry)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 선 스타일 설정 (하늘색)
        pen = QPen(QColor(0, 255, 255, 180))
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
        key = event.key()
        
        # 1~9 사이의 숫자가 입력된 경우
        if Qt.Key.Key_1 <= key <= Qt.Key.Key_9:
            self.history.append((self.curr_x, self.curr_y, self.curr_w, self.curr_h))
            choice = key - 48 
            
            row = (choice - 1) // 3
            col = (choice - 1) % 3
            
            self.curr_w /= 3
            self.curr_h /= 3
            self.curr_x += col * self.curr_w
            self.curr_y += row * self.curr_h
            self.update()

        # Backspace: 뒤로 가기
        elif key == Qt.Key.Key_Backspace:
            if self.history:
                self.curr_x, self.curr_y, self.curr_w, self.curr_h = self.history.pop()
                self.update()

        # Enter 또는 Space: 클릭 실행
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space]:
            target_x = int(self.curr_x + (self.curr_w / 2))
            target_y = int(self.curr_y + (self.curr_h / 2))
            
            self.hide() 
            QApplication.processEvents() 
            time.sleep(0.1) 

            if key == Qt.Key.Key_Space:
                pyautogui.rightClick(target_x, target_y)
            else:
                pyautogui.click(target_x, target_y)
            
            sys.exit()

        # ESC: 종료
        elif key == Qt.Key.Key_Escape:
            sys.exit()

if __name__ == '__main__':
    pyautogui.FAILSAFE = True
    app = QApplication(sys.argv)
    ex = GridClicker()
    sys.exit(app.exec())
