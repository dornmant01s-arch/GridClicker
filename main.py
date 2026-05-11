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
        key = event.key()
        
        # 1~9: 영역 좁히기
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

        # Backspace: 한 단계 취소
        elif key == Qt.Key.Key_Backspace:
            if self.history:
                self.curr_x, self.curr_y, self.curr_w, self.curr_h = self.history.pop()
                self.update()

        # [수정됨] Enter 또는 Space: 클릭 실행
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space]:
            # 1. 정수 좌표 계산 (PyAutoGUI는 정수만 받음)
            target_x = int(self.curr_x + (self.curr_w / 2))
            target_y = int(self.curr_y + (self.curr_h / 2))
            
            # 2. 아주 중요: 투명 UI를 완전히 숨기고 시스템에 포커스를 넘김
            self.hide()
            QApplication.processEvents() # UI가 숨겨지는 걸 시스템이 인식하게 함
            import time
            time.sleep(0.1) # 0.1초 대기 (OS가 포커스를 돌려받는 시간)

            # 3. 클릭 실행
            if key == Qt.Key.Key_Space:
                pyautogui.rightClick(target_x, target_y)
                print(f"우클릭: {target_x}, {target_y}")
            else:
                pyautogui.click(target_x, target_y)
                print(f"좌클릭: {target_x}, {target_y}")
            
            # 4. 클릭 후 프로그램 종료 (원치 않으면 주석 처리)
            QApplication.quit()

        # ESC: 종료
        elif key == Qt.Key.Key_Escape:
            QApplication.quit()

     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridClicker()
    sys.exit(app.exec())
