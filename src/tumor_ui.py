from PyQt5 import QtCore, QtGui, QtWidgets
import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(743, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("Start")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setObjectName("End")
        self.horizontalLayout.addWidget(self.pushButton1)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setMaximum(255)
        self.slider.setMinimum(0)
        self.slider.setProperty("value", 100)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.slider.valueChanged.connect(self.changed_slider)
        self.label = QtWidgets.QLabel("label")
        self.label.setText("Red: 100")

        self.horizontalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.slider1 = QtWidgets.QSlider(self.centralwidget)
        self.slider1.setMaximum(255)
        self.slider1.setMinimum(0)
        self.slider1.setProperty("value", 100)
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setObjectName("slider")
        self.slider1.valueChanged.connect(self.changed_slider1)
        self.label1 = QtWidgets.QLabel("label")
        self.label1.setText("Green: 100")

        self.horizontalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.slider2 = QtWidgets.QSlider(self.centralwidget)
        self.slider2.setMaximum(255)
        self.slider2.setMinimum(0)
        self.slider2.setProperty("value", 0)
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setObjectName("slider")
        self.slider2.valueChanged.connect(self.changed_slider2)
        self.label2 = QtWidgets.QLabel("label")
        self.label2.setText("Blue: 0")

        self.horizontalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.label)

        self.horizontalLayout.addWidget(self.slider1)
        self.horizontalLayout.addWidget(self.label1)

        self.horizontalLayout.addWidget(self.slider2)
        self.horizontalLayout.addWidget(self.label2)

        MainWindow.setCentralWidget(self.centralwidget)
        # Set the stretch factors for both the pushButton & the frame
        self.horizontalLayout.setStretchFactor(self.frame, 1)
        self.horizontalLayout.setStretchFactor(self.pushButton, 1)
        self.horizontalLayout.setStretchFactor(self.slider, 1)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def checker(self, current_value):
        """responsible to decide if the sliding of slider has stopped.
        IDEA is that each time the slider is changed this guy is called. it will keep track of last 3 slider values and
        time, so if the slider is changed in a short period of time(maybe 3 second), it will not be considered as a sliding of slider.
        """
        REFRESH = False

        for key, val in current_value.items():
            if val != self.slider_data[key]['value']:
                print("slider changed")
                print(time.time() - self.slider_data[key]['timestamp'])
                if time.time() - self.slider_data[key][
                    'timestamp'] > self.delay_time:  # if more time has passed than the delay time since the last change
                    REFRESH = True
                    break
        # if REFRESH:
        #     self.end()
        #     time.sleep(5)
        #     self.setup()


    def changed_slider(self):
        value = self.slider.value()
        # print(f'changing Red to {value}')
        self.label.setText("Red: " + str(value))

        curr_values = {
            'slider': value,
            'slider1': self.slider_data['slider1']['value'],
            'slider2': self.slider_data['slider2']['value']
        }
        self.checker(curr_values)
        # update time after check
        self.slider_data['slider']['timestamp'] = time.time()

    def changed_slider1(self):
        value = self.slider1.value()
        # print(f'changing Green to {value}')
        self.label1.setText("Green: " + str(value))
        curr_values = {
            'slider': self.slider_data['slider']['value'],
            'slider1': value,
            'slider2': self.slider_data['slider2']['value']
        }
        self.checker(curr_values)
        # update time after check
        self.slider_data['slider']['timestamp'] = time.time()

    def changed_slider2(self):
        value = self.slider2.value()
        # print(f'changing Blue to {value}')
        self.label2.setText("Blue: " + str(value))
        curr_values = {
            'slider': self.slider_data['slider']['value'],
            'slider1': self.slider_data['slider1']['value'],
            'slider2': value,
        }
        self.checker(curr_values)
        # update time after check
        self.slider_data['slider']['timestamp'] = time.time()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton1.setText(_translate("MainWindow", "End"))
