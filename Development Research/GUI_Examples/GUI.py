import cv2
import dlib
import numpy as np
import csv
from pymongo import MongoClient
import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
#from gaze_tracking import GazeTracking

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')
db=client.clients

# baseline collection
# colBaseline = db.baseline
colBaseline = db.ai_training

# injury_test collection
colInjuryTests = db.injury_tests

# global variables
right_x = 0
right_y = 0

left_x = 0 
left_y = 0 

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(727, 600)
        MainWindow.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxForLabels = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxForLabels.setGeometry(QtCore.QRect(10, 10, 521, 401))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxForLabels.setFont(font)
        self.groupBoxForLabels.setAutoFillBackground(False)
        self.groupBoxForLabels.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.groupBoxForLabels.setTitle("")
        self.groupBoxForLabels.setObjectName("groupBoxForLabels")
        self.frame_leftMenu = QtWidgets.QFrame(self.groupBoxForLabels)
        self.frame_leftMenu.setGeometry(QtCore.QRect(0, 30, 121, 371))
        self.frame_leftMenu.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_leftMenu.setAutoFillBackground(False)
        self.frame_leftMenu.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_leftMenu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_leftMenu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_leftMenu.setObjectName("frame_leftMenu")
        
        # baseline button on menu
        self.btn_baseline = QtWidgets.QPushButton(self.frame_leftMenu)
        self.btn_baseline.setGeometry(QtCore.QRect(-10, 20, 131, 41))
        self.btn_baseline.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_baseline.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_baseline.setStyleSheet("QPushButton {\n"
                "    color: rgb(255, 255, 255);\n"
                "    background-color: rgb(35, 35, 35);\n"
                "    border: 0px solid;\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "}")
        self.btn_baseline.setObjectName("btn_baseline")
        
        # injury test button on menu  
        self.btn_InjuryTest = QtWidgets.QPushButton(self.frame_leftMenu)
        self.btn_InjuryTest.setGeometry(QtCore.QRect(0, 50, 121, 40))
        self.btn_InjuryTest.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_InjuryTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_InjuryTest.setStyleSheet("QPushButton {\n"
                "    color: rgb(255, 255, 255);\n"
                "    background-color: rgb(35, 35, 35);\n"
                "    border: 0px solid;\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "}")
        self.btn_InjuryTest.setObjectName("btn_InjuryTest")
        
        self.btn_read_baseline = QtWidgets.QPushButton(self.frame_leftMenu)
        self.btn_read_baseline.setGeometry(QtCore.QRect(0, 80, 121, 41))
        self.btn_read_baseline.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_read_baseline.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_read_baseline.setStyleSheet("QPushButton {\n"
                "    color: rgb(255, 255, 255);\n"
                "    background-color: rgb(35, 35, 35);\n"
                "    border: 0px solid;\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "}")
        self.btn_read_baseline.setObjectName("btn_read_baseline")
        self.btn_read_injurytest = QtWidgets.QPushButton(self.frame_leftMenu)
        self.btn_read_injurytest.setGeometry(QtCore.QRect(0, 110, 121, 41))
        self.btn_read_injurytest.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_read_injurytest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_read_injurytest.setStyleSheet("QPushButton {\n"
                "    color: rgb(255, 255, 255);\n"
                "    background-color: rgb(35, 35, 35);\n"
                "    border: 0px solid;\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "}")
        self.btn_read_injurytest.setObjectName("btn_read_injurytest")
        self.frame = QtWidgets.QFrame(self.groupBoxForLabels)
        self.frame.setGeometry(QtCore.QRect(119, 29, 401, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 10, 391, 361))
        self.stackedWidget.setObjectName("stackedWidget")
        self.BaselineTest = QtWidgets.QWidget()
        self.BaselineTest.setObjectName("BaselineTest")
        self.labelBaselineID = QtWidgets.QLabel(self.BaselineTest)
        self.labelBaselineID.setGeometry(QtCore.QRect(50, 70, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelBaselineID.setFont(font)
        self.labelBaselineID.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.labelBaselineID.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBaselineID.setObjectName("labelBaselineID")
        self.labelBaselineName = QtWidgets.QLabel(self.BaselineTest)
        self.labelBaselineName.setGeometry(QtCore.QRect(50, 120, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelBaselineName.setFont(font)
        self.labelBaselineName.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.labelBaselineName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBaselineName.setObjectName("labelBaselineName")
        self.label2 = QtWidgets.QLabel(self.BaselineTest)
        self.label2.setGeometry(QtCore.QRect(50, 10, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label2.setFont(font)
        self.label2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setObjectName("label2")
        
        # input box for ID on the baseline page 
        self.input_ID_baseline_2 = QtWidgets.QLineEdit(self.BaselineTest)
        self.input_ID_baseline_2.setGeometry(QtCore.QRect(240, 70, 113, 31))
        self.input_ID_baseline_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_ID_baseline_2.setObjectName("input_ID_baseline_2")
        
        # input box for name on the baseline page   
        self.input_name_baseline_2 = QtWidgets.QLineEdit(self.BaselineTest)
        self.input_name_baseline_2.setGeometry(QtCore.QRect(240, 120, 113, 31))
        self.input_name_baseline_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_name_baseline_2.setObjectName("input_name_baseline_2")

        # submit button on baseline page 
        self.btn_Submit_Baseline_2 = QtWidgets.QPushButton(self.BaselineTest)
        self.btn_Submit_Baseline_2.setGeometry(QtCore.QRect(130, 170, 151, 31))
        self.btn_Submit_Baseline_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btn_Submit_Baseline_2.setObjectName("btn_Submit_Baseline_2")
        self.btn_Submit_Baseline_2.clicked.connect(self.clickedSubmitBaseline)       
        
        # quit button on baseline page  
        self.btn_Quit_Baseline_3 = QtWidgets.QPushButton(self.BaselineTest)
        self.btn_Quit_Baseline_3.setGeometry(QtCore.QRect(130, 210, 151, 31))
        self.btn_Quit_Baseline_3.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btn_Quit_Baseline_3.setObjectName("btn_Quit_Baseline_3")
        self.btn_Quit_Baseline_3.clicked.connect(self.QuitApplication)
        
        self.stackedWidget.addWidget(self.BaselineTest)
        self.Injury_test = QtWidgets.QWidget()
        self.Injury_test.setObjectName("Injury_test")
        self.label_name = QtWidgets.QLabel(self.Injury_test)
        self.label_name.setGeometry(QtCore.QRect(50, 120, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setObjectName("label_name")
        self.label_ID = QtWidgets.QLabel(self.Injury_test)
        self.label_ID.setGeometry(QtCore.QRect(50, 70, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_ID.setFont(font)
        self.label_ID.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_ID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ID.setObjectName("label_ID")
        self.label1 = QtWidgets.QLabel(self.Injury_test)
        self.label1.setGeometry(QtCore.QRect(50, 10, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label1.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label1.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label1.setObjectName("label1")
        self.label_activity = QtWidgets.QLabel(self.Injury_test)
        self.label_activity.setGeometry(QtCore.QRect(50, 170, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_activity.setFont(font)
        self.label_activity.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_activity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_activity.setObjectName("label_activity")
        self.label_description = QtWidgets.QLabel(self.Injury_test)
        self.label_description.setGeometry(QtCore.QRect(50, 220, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")

        # input box for ID on the injury type page  
        self.input_ID_Injurytest_2 = QtWidgets.QLineEdit(self.Injury_test)
        self.input_ID_Injurytest_2.setGeometry(QtCore.QRect(240, 70, 113, 31))
        self.input_ID_Injurytest_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_ID_Injurytest_2.setObjectName("input_ID_Injurytest_2")
        
        # input box for name on the injury type page
        self.input_name_Injurytest_2 = QtWidgets.QLineEdit(self.Injury_test)
        self.input_name_Injurytest_2.setGeometry(QtCore.QRect(240, 120, 113, 31))
        self.input_name_Injurytest_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_name_Injurytest_2.setObjectName("input_name_Injurytest_2")
        
        # input box for activity on the injury type page
        self.input_activity_Injurytest_2 = QtWidgets.QLineEdit(self.Injury_test)
        self.input_activity_Injurytest_2.setGeometry(QtCore.QRect(240, 170, 113, 31))
        self.input_activity_Injurytest_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_activity_Injurytest_2.setObjectName("input_activity_Injurytest_2")
        
        # input box for description on the injury type page
        self.input_description_Injurytest_2 = QtWidgets.QLineEdit(self.Injury_test)
        self.input_description_Injurytest_2.setGeometry(QtCore.QRect(240, 220, 113, 31))
        self.input_description_Injurytest_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.input_description_Injurytest_2.setObjectName("input_description_Injurytest_2")
        
        # submit button on injury type page 
        self.btn_Submit_InjuryTest = QtWidgets.QPushButton(self.Injury_test)
        self.btn_Submit_InjuryTest.setGeometry(QtCore.QRect(130, 270, 151, 31))
        self.btn_Submit_InjuryTest.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btn_Submit_InjuryTest.setObjectName("btn_Submit_InjuryTest")
        self.btn_Submit_InjuryTest.clicked.connect(self.clickedSubmitInjuryTest)
        
        # quit button on injury type page 
        self.btn_Quit_InjuryTest = QtWidgets.QPushButton(self.Injury_test)
        self.btn_Quit_InjuryTest.setGeometry(QtCore.QRect(130, 310, 151, 31))
        self.btn_Quit_InjuryTest.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btn_Quit_InjuryTest.setObjectName("btn_Quit_InjuryTest")
        self.btn_Quit_InjuryTest.clicked.connect(self.QuitApplication)
        
        self.stackedWidget.addWidget(self.Injury_test)
        self.Read_Baseline = QtWidgets.QWidget()
        self.Read_Baseline.setStyleSheet("")
        self.Read_Baseline.setObjectName("Read_Baseline")
        self.label_header = QtWidgets.QLabel(self.Read_Baseline)
        self.label_header.setGeometry(QtCore.QRect(50, 10, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_header.setFont(font)
        self.label_header.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)
        self.label_header.setObjectName("label_header")
        self.label_file = QtWidgets.QLabel(self.Read_Baseline)
        self.label_file.setGeometry(QtCore.QRect(50, 90, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_file.setFont(font)
        self.label_file.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file.setObjectName("label_file")
        self.lineEdit_file1 = QtWidgets.QLineEdit(self.Read_Baseline)
        self.lineEdit_file1.setGeometry(QtCore.QRect(240, 90, 101, 31))
        self.lineEdit_file1.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.lineEdit_file1.setObjectName("lineEdit_file1")

        # submit button on read baseline page 
        self.btnRB_submit = QtWidgets.QPushButton(self.Read_Baseline)
        self.btnRB_submit.setGeometry(QtCore.QRect(130, 150, 151, 31))
        self.btnRB_submit.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btnRB_submit.setObjectName("btnRB_submit")
        self.btnRB_submit.clicked.connect(self.clickedReadBaseline)

        # quit button on read baseline page 
        self.btnRB_quit = QtWidgets.QPushButton(self.Read_Baseline)
        self.btnRB_quit.setGeometry(QtCore.QRect(130, 210, 151, 31))
        self.btnRB_quit.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btnRB_quit.setObjectName("btnRB_quit")
        self.btnRB_quit.clicked.connect(self.QuitApplication)

        self.stackedWidget.addWidget(self.Read_Baseline)
        self.Read_InjuryTest = QtWidgets.QWidget()
        self.Read_InjuryTest.setObjectName("Read_InjuryTest")
        self.label_header_2 = QtWidgets.QLabel(self.Read_InjuryTest)
        self.label_header_2.setGeometry(QtCore.QRect(50, 10, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_header_2.setFont(font)
        self.label_header_2.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label_header_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_header_2.setObjectName("label_header_2")
        self.label = QtWidgets.QLabel(self.Read_InjuryTest)
        self.label.setGeometry(QtCore.QRect(50, 90, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.Read_InjuryTest)
        self.lineEdit.setGeometry(QtCore.QRect(240, 90, 101, 31))
        self.lineEdit.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.lineEdit.setObjectName("lineEdit")

        # submit button on read injurt test page        
        self.btnRIT_submit = QtWidgets.QPushButton(self.Read_InjuryTest)
        self.btnRIT_submit.setGeometry(QtCore.QRect(130, 150, 151, 31))
        self.btnRIT_submit.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btnRIT_submit.setObjectName("btnRIT_submit")
        self.btnRIT_submit.clicked.connect(self.clickedReadInjuryTest)

        # quit button on read injurt test page 
        self.btnRIT_quit = QtWidgets.QPushButton(self.Read_InjuryTest)
        self.btnRIT_quit.setGeometry(QtCore.QRect(130, 210, 151, 31))
        self.btnRIT_quit.setStyleSheet("color: rgb(238, 238, 236);\n"
                "background-color: rgb(35, 35, 35);")
        self.btnRIT_quit.setObjectName("btnRIT_quit")
        self.btnRIT_quit.clicked.connect(self.QuitApplication)

        self.stackedWidget.addWidget(self.Read_InjuryTest)
        self.frame_2 = QtWidgets.QFrame(self.groupBoxForLabels)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 531, 41))
        self.frame_2.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 727, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Baseline Test Button
        self.btn_baseline.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.BaselineTest))

        # Injury Test Button
        self.btn_InjuryTest.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Injury_test))

        # Read Baseline Button
        self.btn_read_baseline.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Read_Baseline))

        # Read Injury Test Button
        self.btn_read_injurytest.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Read_InjuryTest))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_baseline.setText(_translate("MainWindow", "Baseline"))
        self.btn_InjuryTest.setText(_translate("MainWindow", " Injury Test"))
        self.btn_read_baseline.setText(_translate("MainWindow", "Read Baseline"))
        self.btn_read_injurytest.setText(_translate("MainWindow", "Read Injury Test"))
        self.labelBaselineID.setText(_translate("MainWindow", "Enter ID"))
        self.labelBaselineName.setText(_translate("MainWindow", "Enter Name"))
        self.label2.setText(_translate("MainWindow", "Baseline Test"))
        self.btn_Submit_Baseline_2.setText(_translate("MainWindow", "Submit"))
        self.btn_Quit_Baseline_3.setText(_translate("MainWindow", "Quit"))
        self.label_name.setText(_translate("MainWindow", "Enter Name"))
        self.label_ID.setText(_translate("MainWindow", "Enter ID"))
        self.label1.setText(_translate("MainWindow", "Injury Test"))
        self.label_activity.setText(_translate("MainWindow", "Enter Activity"))
        self.label_description.setText(_translate("MainWindow", "Enter Description"))
        self.btn_Submit_InjuryTest.setText(_translate("MainWindow", "Submit"))
        self.btn_Quit_InjuryTest.setText(_translate("MainWindow", "Quit"))
        self.label_header.setText(_translate("MainWindow", "Read Baseline"))
        self.label_file.setText(_translate("MainWindow", "Enter File Name"))
        self.btnRB_submit.setText(_translate("MainWindow", "Submit"))
        self.btnRB_quit.setText(_translate("MainWindow", "Quit"))
        self.label_header_2.setText(_translate("MainWindow", "Read Injury Test"))
        self.label.setText(_translate("MainWindow", "Enter File Name"))
        self.btnRIT_submit.setText(_translate("MainWindow", "Submit"))
        self.btnRIT_quit.setText(_translate("MainWindow", "Quit"))

    def clickedSubmitBaseline(self, text):
        test = 1
        baselineID = self.input_ID_baseline_2.text()
        todays_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        baselineName = self.input_name_baseline_2.text()
        self.EyeTrackerOpenCV(baselineID, todays_date, baselineName, "", "", test)

    def clickedSubmitInjuryTest(self, text):
        test = 2
        injurytestID = self.input_ID_Injurytest_2.text()
        todays_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        injurytestName = self.input_name_Injurytest_2.text()
        injurytestActivity = self.input_activity_Injurytest_2.text()
        injurytestDescription = self.input_description_Injurytest_2.text()
        self.EyeTrackerOpenCV(injurytestID, todays_date, injurytestName, injurytestActivity, injurytestDescription, test)

    def clickedReadBaseline(self, text):
        print("Read Baseline")

    def clickedReadInjuryTest(self, text):
        print("Read Injury Test")

    def QuitApplication(self):
        app.exit()

    def save_to_file(self,lx, ly, rx, ry, file1, file2):
        # write Left and Right eye x,y coords to .txt & .csv   
        file1.write(str(lx) + " " + str(ly) + " " + str(rx) + " " + str(ry) + "\n")
        file2.write(str(lx) + ", " + str(ly) + ", " + str(rx) + ", " + str(ry) + "\n")

    def shape_to_np(self, shape, dtype="int"): 
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        # return the list of (x, y)-coordinates
        return coords

    def eye_on_mask(self, mask, side):
        points = [shape[i] for i in side]
        points = np.array(points, dtype=np.int32)
        mask = cv2.fillConvexPoly(mask, points, 255)
        return mask

    def contouring(self, thresh, mid, img, right=False):
        _ , cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        try:
            cnt = max(cnts, key = cv2.contourArea)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print('MID VALUE: ' ,mid)
            if right:
                cx += mid
                # Save right x,y
                global right_x 
                right_x = cx
                global right_y
                right_y = cy
                #print("Right x,y: ", cx, cy)
                #print('RIGHT MID VALUE: ' ,mid)
            else:
                # save left x,y
                global left_x
                left_x = cx
                global left_y
                left_y = cy
                #print("Left x,y: ", cx, cy)
                #print('LEFT MID VALUE: ' ,mid)
            # draw circle on eyes
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
            #cv2.putText(img, "Left pupil:  " + str(left_x + " ," + left_y), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            #cv2.putText(img, "Right pupil: " + str(right_x + " ," + right_y), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            #print('')
        except:
            pass
  
    def nothing(self, x):
        pass

    def EyeTrackerOpenCV(self, ID, todays_date, clientName, injurytestActivity, injurytestDescription, testType):
        
        # open .txt & .csv for writing
        writeToFile = open("eye-coordinates.txt", "w")
        writeToFileCSV = open("eye-coordinatesCSV.csv", "w")
        
        # When record is True, x,y coords are saved to file
        record = False
        prompt1 = "Press 'R' to Start Recording Data: "
        prompt2 = "Press 'ESC' to Exit: "

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_68.dat')

        left = [36, 37, 38, 39, 40, 41]
        right = [42, 43, 44, 45, 46, 47]

        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        thresh = img.copy()

        cv2.namedWindow('image')
        kernel = np.ones((9, 9), np.uint8)

        # initialise threshold slider
        cv2.createTrackbar('threshold', 'image', 0, 255, self.nothing)

        ## Red Dot
        # height and width of web cam frame
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        offset = 25
        # Red Dot center point
        dot_cx = round(width / 2)
        dot_cy = round(height / 2)
        # direction
        dx = 1
        dy = 0
        # speed
        speed = 10

        # start dot in center of screen
        x = dot_cx
        y = dot_cy
        counter = 0
        global shape

        while(True):
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)

            for rect in rects:

                shape = predictor(gray, rect)
                shape = self.shape_to_np(shape)
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                mask = self.eye_on_mask(mask, left)
                mask = self.eye_on_mask(mask, right)
                mask = cv2.dilate(mask, kernel, 5)
                eyes = cv2.bitwise_and(img, img, mask=mask)
                mask = (eyes == [0, 0, 0]).all(axis=2)
                eyes[mask] = [255, 255, 255]
                mid = (shape[42][0] + shape[39][0]) // 2
                eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
                threshold = cv2.getTrackbarPos('threshold', 'image')
                _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
                thresh = cv2.erode(thresh, None, iterations=2) #1
                thresh = cv2.dilate(thresh, None, iterations=4) #2
                thresh = cv2.medianBlur(thresh, 3) #3
                thresh = cv2.bitwise_not(thresh)
                self.contouring(thresh[:, 0:mid], mid, img)
                self.contouring(thresh[:, mid:], mid, img, True)

            # only save when 'R' is pressed, to avoid picking up 0,0,0,0
            if(record == False):
                cv2.putText(img, prompt1, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            else:
                cv2.putText(img, prompt2, (90, 195), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                # save stuff
                self.save_to_file(left_x, left_y, right_x, right_y, writeToFile, writeToFileCSV)

            #for (x, y) in shape[36:48]:
            #   cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

            # draw red dot in center of screen
            cv2.circle(img, (x, y), 10, (0, 0, 255), -1)

            # putText() is used to draw the text string onto the screen.
            cv2.putText(img, "Left pupil:  " + str(left_x) + " ," + str(left_y), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(img, "Right pupil: " + str(right_x) + " ," + str(right_y), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # move the dot if recording
            if(record):
                # apply formula to make it move
                x += dx * speed
                y += dy * speed

                # change x-axis direction when at boundry
                if(x > (width - offset)):
                    dx = -1
                elif(x < offset):
                    dx = 1

                # change y-axis direction when at boundry
                if(y > (height - offset)):
                    dy = -1
                elif(y < offset):
                    dy = 1
            
                # change direction if at center point
                if(x == dot_cx and y == dot_cy):
                    if(counter == 0):
                        print("counter 0 passed")
                        counter += 1
                        dx = 0
                        dy = -1
                    elif(counter == 1):
                        print("counter 1 passed")
                        counter += 1
                        dx = -1
                        dy = 0
                    elif(counter == 2):
                        print("counter 2 passed")
                        counter += 1
                        dx = 0
                        dy = 1
                    elif(counter == 3):
                        print("counter 3 passed")
                        counter += 1
                        dx = 1
                        dy = 0

            # show the image with the face detections + facial landmarks
            # Show vidoe capture in window
            cv2.imshow('eyes', img) #("image", thresh)

            
            k = cv2.waitKey(1)

            # press R to record, ESC to exit
            if k == 114:
                record = True
            elif k == 27 or counter == 4:
                break

        # close file and webcam
        writeToFile.close()  
        writeToFileCSV.close() 
        cap.release()
        cv2.destroyAllWindows()

        # open a file
        f = open('eye-coordinatesCSV.csv')

        # read the entire contents
        text = f.read()

        if(testType == 1):
            # build a document to be inserted    
            text_file_doc = {"client_id": ID, "Date": todays_date, "name": clientName, "contents" : text}

            # insert the contents into the "file" collection
            colBaseline.insert(text_file_doc)
        elif(testType == 2):
            # build a document to be inserted   
            text_file_doc = {"client_id": ID, "Date": todays_date, "name": clientName, "activity": injurytestActivity, "description": injurytestDescription, "contents" : text}

            # insert the contents into the "file" collection
            colInjuryTests.insert(text_file_doc)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())