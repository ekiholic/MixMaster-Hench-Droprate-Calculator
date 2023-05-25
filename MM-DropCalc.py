import sys
import re
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon

class my_window(QMainWindow):
    def __init__(self):
        super(my_window, self).__init__()
        self.setGeometry(600, 200, 450, 410)
        self.setWindowTitle("Hench Droprate Calculator")
        self.setWindowIcon(QIcon("MM-icon.png"))
        self.droppercentage = ""
        self.droprate = 0
        self.kill_list = []
        self.initUI()

    def initUI(self):
        self.missing_fields = QtWidgets.QErrorMessage()

        self.label_playerlvl = QLabel(self)
        self.label_playerlvl.setText("Player Level :")
        self.label_playerlvl.move(22, 20)
        self.input_playerlvl = QLineEdit(self)
        self.input_playerlvl.setText("100")
        self.input_playerlvl.move(90, 20)
        
        self.label_mob = QLabel(self)
        self.label_mob.setText("Hench Rate :")
        self.label_mob.move(20, 70)
        self.mob = QLineEdit(self)
        self.mob.move(90, 70)

        self.label_moblvl = QLabel(self)
        self.label_moblvl.setText("Hench Base Level :")
        self.label_moblvl.move(220, 70)
        self.moblvl = QLineEdit(self)
        self.moblvl.move(320, 70)

        self.label_server = QLabel(self)
        self.label_server.setText("Server Rate :")
        self.label_server.move(20, 120)
        self.server = QLineEdit(self)
        self.server.setText("7")
        self.server.move(90, 120)

        self.label_mark = QLabel(self)
        self.label_mark.setText("Mark Bonus :")
        self.label_mark.move(220, 120)
        self.mark = QLineEdit(self)
        self.mark.setText("1")
        self.mark.move(290, 120)
        
        self.btn_calc = QtWidgets.QPushButton(self)
        self.btn_calc.setText("Calculate")
        self.btn_calc.clicked.connect(self.CalculateDropRate)
        self.btn_calc.move(170, 190)

        self.label_droprate = QLabel(self)
        self.label_droprate.setText("Droprate :\nExpected kills to drop : ")
        self.label_droprate.move(20, 260)
        self.label_droprate.resize(200, 40)

        self.btn_sim = QtWidgets.QPushButton(self)
        self.btn_sim.setText("Simulate Drop")
        self.btn_sim.clicked.connect(self.SimulateDrop)
        self.btn_sim.move(18, 305)

        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setText("Clear Data")
        self.btn_reset.clicked.connect(self.ClearKills)
        self.btn_reset.move(130, 305)

        self.label_sim_drop = QLabel(self)
        self.label_sim_drop.setText("Dropped after kills\nAverage\nLeast\nMost")
        self.label_sim_drop.move(20, 340)
        self.label_sim_drop.resize(200, 60)
    
    def CalculateDropRate(self):
        list_int = [self.input_playerlvl.text(), self.mob.text(), self.moblvl.text(), self.server.text(), self.mark.text()]

        if self.mob.text() == "" or self.server.text() == "" or self.mark.text() == "":
            self.missing_fields.showMessage("Fill empty fields !")
            return
        for rate in list_int:
            if re.search("[0-9]", rate):
                if int(rate) == 0:
                    self.missing_fields.showMessage("Can't calculate with 0 !")
                    return
                continue
            else:
                self.missing_fields.showMessage("Write number in fields !")
                return

        diff = int(self.input_playerlvl.text()) - int(self.moblvl.text())
        MobRate = int(self.mob.text())
        ServerRate = int(self.server.text())
        MarkRate = int(self.mark.text())
        BaseRate = float(MobRate * ServerRate * MarkRate)

        if diff >= 10 and diff < 19:
            BaseRate = BaseRate * 0.9
        elif diff >= 20 and diff < 29:
            BaseRate = BaseRate * 0.8
        elif diff >= 30 and diff < 39:
            BaseRate = BaseRate * 0.7
        elif diff >= 40 and diff < 49:
            BaseRate = BaseRate * 0.6
        elif diff > 50:
            BaseRate = BaseRate * 0.5

        self.droprate = BaseRate
        self.droppercentage = (BaseRate / 10000000) * 100
        kills = int(10000000/BaseRate)
        self.label_droprate.setText(f"Droprate : {self.droppercentage:.10f}%\nExpected kills to drop : {kills}")
        return

    def SimulateDrop(self):
        if self.droprate == 0:
            self.missing_fields.showMessage("Calculate droprate first !")
            return
        roll = random.randrange(0, 10000000)
        kills = 1
        while roll > self.droprate:
            roll = random.randrange(0, 10000000)
            kills += 1
        self.kill_list.append(kills)
        self.kill_list.sort()
        mean = int(sum(self.kill_list) / len(self.kill_list))
        self.label_sim_drop.setText(f"Dropped after {kills} kills\nAverage kills to drop : {mean}\nLeast kills to drop : {self.kill_list[0]}\nMost kills to drop : {self.kill_list[-1]}")
        return
    
    def ClearKills(self):
        self.kill_list.clear()
        return


def app():
    app = QApplication(sys.argv)
    win = my_window()
    win.show()
    sys.exit(app.exec_())

app()
