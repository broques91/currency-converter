from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        
    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_currencyFrom = QtWidgets.QComboBox()
        self.spn_amount = QtWidgets.QSpinBox()
        self.cbb_currencyTo = QtWidgets.QComboBox()
        self.spn_convertedAmount = QtWidgets.QSpinBox()
        self.btn_reverse = QtWidgets.QPushButton("Inverser devises")
        
        self.layout.addWidget(self.cbb_currencyFrom)
        self.layout.addWidget(self.spn_amount)
        self.layout.addWidget(self.cbb_currencyTo)
        self.layout.addWidget(self.spn_convertedAmount)
        self.layout.addWidget(self.btn_reverse)
        
    def set_default_values(self):
        self.cbb_currencyFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_currencyTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_currencyFrom.setCurrentText("EUR")
        self.cbb_currencyTo.setCurrentText("EUR")
        
        self.spn_amount.setRange(1, 1000000)
        self.spn_convertedAmount.setRange(1, 1000000)
        
        self.spn_amount.setValue(100)
        self.spn_convertedAmount.setValue(100)

    def setup_connections(self):
        self.cbb_currencyFrom.activated.connect(self.compute)
        self.cbb_currencyTo.activated.connect(self.compute)
        self.spn_amount.valueChanged.connect(self.compute)
        self.btn_reverse.clicked.connect(self.reverse_currency)
    
    def compute(self):
        amount = self.spn_amount.value()
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()
        
        try:
            result = self.c.convert(amount, currency_from, currency_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion a échoué.") 
        else:
            self.spn_convertedAmount.setValue(result)
    
    def reverse_currency(self):
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()
        
        self.cbb_currencyFrom.setCurrentText(currency_to)
        self.cbb_currencyTo.setCurrentText(currency_from)

        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()