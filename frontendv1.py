import sys
from PyQt5.QtWidgets import (QPushButton,QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout,QApplication)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class TweetNormalizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def analyze(self,tweet):
        ##SYNC the backend code here
        result = tweet
        return result

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.white)
        self.setPalette(p)

        hint_label = QLabel("Please enter the tweet:")
        label_font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        hint_label.setFont(label_font)

        input_review = QLineEdit()
        btn1 = QPushButton("Normalize", self)
        btn2 = QPushButton("Clear", self)
        button_font = QtGui.QFont("Times", 13, QtGui.QFont.Bold)
        btn1.setFont(button_font)
        btn2.setFont(button_font)

        analyze_result = QTextEdit()
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(hint_label, 1, 0)
        grid.addWidget(input_review, 2, 0)
        grid.addWidget(btn1, 3, 0)
        grid.addWidget(btn2, 3, 1)
        grid.addWidget(analyze_result, 4, 0, 5, 0)
        self.setLayout(grid)

        def analysing():
            normalizedtweet = self.analyze(input_review.text())
            analyze_result.setText(normalizedtweet)
        btn1.clicked.connect(analysing)

        def clear():
            analyze_result.setText("")
            input_review.setText("")
        btn2.clicked.connect(clear)

        self.setGeometry(400, 150, 600, 500)
        self.setWindowTitle("Tweet Normalizer")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    analyzer = TweetNormalizer()
    analyzer.show()
    sys.exit(app.exec_())