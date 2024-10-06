from PyQt5 import QtCore, QtGui, QtWidgets
from DrowsyDetection import drowsy_detection
from eyes_trainmodel import eyes_cnnmodel
from yawning_trainmodel import yawning_cnnmodel

class Ui_modules(object):

    def build_model(self):

        eyes_cnnmodel()

        yawning_cnnmodel()

        self.showMessageBox("Information", "Model files are generated successfully..!")



    def detection(self):


        drowsy_detection()



    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(950, 550)
        Dialog.setStyleSheet("QDialog{background-image: url(../DrowsyDetection_CNN/uiimg/detect.jpg);}")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(310, 20, 291, 391))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:1 rgba(199, 199, 199, 182));")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName("frame")

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 163, 230, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(200, 80, 112);\n"
"font: 87 12pt \"Arial Black\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 300, 230, 51))

        self.pushButton_3.setStyleSheet("background-color: rgb(200, 80, 112);\n"
                                        "font: 87 12pt \"Arial Black\";")

        self.pushButton_3.setObjectName("pushButton_3")

        #self.label = QtWidgets.QLabel(self.frame)
        #self.label.setGeometry(QtCore.QRect(100, 30, 100, 100))
        #self.label.setStyleSheet("background-image: url(../DrowsyDetection_CNN/uiimg/sd.png);")
        #self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        #self.label.setLineWidth(2)
        #self.label.setText("")
        #self.label.setIndent(-4)
        #self.label.setObjectName("label")



        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton_2.clicked.connect(self.build_model)
        self.pushButton_3.clicked.connect(self.detection)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Modules"))

        self.pushButton_2.setText(_translate("Dialog", "Training CNN Models"))
        self.pushButton_3.setText(_translate("Dialog", "Drowsy Detection"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_modules()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
