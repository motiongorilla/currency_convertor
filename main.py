from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import requests # API KEY l9RnYZvz0ebfFxRg6ZkMSzyBjxdlNCYo

API_TOKEN = "l9RnYZvz0ebfFxRg6ZkMSzyBjxdlNCYo"


class CurrConvert(QWidget):
    def __init__(self):
        super(CurrConvert, self).__init__()

        # window settings
        self.setFixedSize(400, 150)
        self.setWindowTitle("Currency converter")
        self.setStyleSheet("background-color: rgb(50,50,50);")

        ly = QVBoxLayout(self)
        self.curr_ly = QHBoxLayout()

        self.header_lb = QLabel()
        self.header_lb.setText("Currency converter")
        self.header_lb.setAlignment(Qt.AlignCenter)
        self.header_lb.setStyleSheet("font: 600 20pt 'Nunito SemiBold'; color: rgb(230,230,230);")

        ly.addWidget(self.header_lb)
        ly.addLayout(self.curr_ly)

        self.input_le = QLineEdit()
        self.input_le.setPlaceholderText("Amount to change")
        self.input_le.setFrame(False)
        self.input_le.setStyleSheet("background-color: rgb(128,128,128);")
        self.curr_ly.addWidget(self.input_le)

        self.in_curr_cb = QComboBox(self)
        self.in_curr_cb.setStyleSheet("background-color: rgb(130,130,130); font: 800 8pt 'Montserrat';")

        self.out_curr_cb = QComboBox(self)
        self.out_curr_cb.setStyleSheet("background-color: rgb(130,130,130); font: 800 8pt 'Montserrat';")

        self.convert_btn = QPushButton(self)
        self.convert_btn.setText("Convert")
        self.convert_btn.setStyleSheet("background-color: rgb(164, 164, 164);")
    
        self.curr_ly.addWidget(self.in_curr_cb)
        self.curr_ly.addWidget(self.convert_btn)
        self.curr_ly.addWidget(self.out_curr_cb)


        self.result_lb = QLabel(self)
        self.result_lb.setText("Results")
        self.result_lb.setAlignment(Qt.AlignCenter)
        self.result_lb.setStyleSheet("font: 1000 16pt 'Nunito SemiBold'; color: rgb(248,248,248);")

        ly.addWidget(self.result_lb)

        self.setCurrencyList()
        self.convert_btn.clicked.connect(lambda: self.convertMoney(float(self.input_le.text()), self.in_curr_cb.currentText(), self.out_curr_cb.currentText()))

    def setCurrencyList(self):
        url = "https://api.apilayer.com/fixer/symbols"

        payload = {}
        headers= {
        "apikey": API_TOKEN
        }

        response = requests.request("GET", url, headers=headers, data = payload)
        result: dict = response.json()
        self.in_curr_cb.addItems(result["symbols"].keys())
        self.out_curr_cb.addItems(result["symbols"].keys())
            
        

    def convertMoney(self, amount: float, fr: str, to: str):
        url = f"https://api.apilayer.com/fixer/convert?to={to}&from={fr}&amount={amount}"

        payload = {}
        headers= {
        "apikey": API_TOKEN
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        status_code = response.status_code
        result = response.json()
        self.result_lb.setText(str(round(result["result"], 2)) + " " + to)

if __name__ == '__main__':
    app = QApplication([])
    w = CurrConvert()
    w.show()
    app.exec()