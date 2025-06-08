import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class RandomNumberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('随机数生成器')
        self.setGeometry(300, 300, 300, 200)

        # 创建一个标签，用于显示随机数
        self.label = QLabel('点击按钮生成随机数', self)
        self.label.setAlignment(Qt.AlignCenter)  # 文本居中
        self.label.setFont(QFont('Arial', 24))  # 设置字体大小为 24

        # 创建一个按钮
        self.button = QPushButton('生成随机数', self)
        self.button.setFont(QFont('Arial', 16))  # 设置按钮字体大小为 16
        self.button.clicked.connect(self.generate_random_number)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def generate_random_number(self):
        # 生成 0 到 720 之间的随机整数
        random_number = random.randint(0, 21)
        self.label.setText(str(random_number))  # 更新标签内容

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RandomNumberApp()
    window.show()
    sys.exit(app.exec_())