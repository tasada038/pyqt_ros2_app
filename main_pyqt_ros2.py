import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QAction, QStyle, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from ui_pyqt_ros2 import Ui_MainWindow

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.float_topic_name = '/micro_ros_arduino_node_publisher'
        self.icon_path = "image/qt_ros_logo.png"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(self.icon_path))
        self.create_menubars()
        self.show()

        self.ui.checkBox_float_01.stateChanged.connect(self.connect_ros_float)
        self.ui.checkBox_float_02.stateChanged.connect(self.update_ros_float)
        self.ui.label_topic_setting_float.setText(self.float_topic_name)
        self.ui.lineEdit_topic_float.editingFinished.connect(self.change_float_topic)

    def connect_ros_float(self, state):
        if (Qt.Checked == state):
            try:
                # ROS2 init
                rclpy.init(args=None)
                self.node = Node('Qt_view_node')
                self.pub = self.node.create_subscription(
                    Float64,
                    self.float_topic_name,
                    self.sub_float_callback,
                    10,
                )
                # spin once, timeout_sec 5[s]
                timeout_sec_rclpy = 5
                timeout_init = time.time()
                rclpy.spin_once(self.node, timeout_sec=timeout_sec_rclpy)
                timeout_end = time.time()
                ros_connect_time = timeout_end - timeout_init

                # Error Handle for rclpy timeout
                if ros_connect_time >= timeout_sec_rclpy:
                    self.ui.label_ros2_state_float.setText("Couldn't Connect")
                    self.ui.label_ros2_state_float.setStyleSheet(
                        "color: rgb(255,255,255);"
                        "background-color: rgb(255,0,51);"
                        "border-radius:5px;"
                    )
                else:
                    self.ui.label_ros2_state_float.setText("Connected")
                    self.ui.label_ros2_state_float.setStyleSheet(
                        "color: rgb(255,255,255);"
                        "background-color: rgb(18,230,95);"
                        "border-radius:5px;"
                    )
            except:
                pass
        else:
            self.node.destroy_node()
            rclpy.shutdown()

    def update_ros_float(self, state):
        if (Qt.Checked == state):
            # create timer
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.timer_float_update)
            self.timer.start(10)
        else:
            self.timer.stop()        

    def change_float_topic(self):
        self.float_topic_name = self.ui.lineEdit_topic_float.text()
        self.ui.label_topic_setting_float.setText(self.float_topic_name)

    ### ROS2 Data Updater
    def sub_float_callback(self, msg):
        self.number = round(msg.data, 2)
        # print(self.number)
        self.update_float_data_label()

    def update_float_data_label(self):
        self.ui.label_data_num_float.setText(str(self.number))
        self.show()

    def timer_float_update(self):
        rclpy.spin_once(self.node)
        self.update_float_data_label()
        self.show()
        self.timer.start(10)

    ### QMenu
    def create_menubars(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.exit_action())
        fileMenu.addMenu(self.prefer_action())

        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addMenu("Undo")
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addMenu("Get Started")

    def prefer_action(self):
        preferMenu = QMenu('Preferences', self)
        preferAct = QAction(QIcon('image/setting.jpg'),'Setting', self)
        preferMenu.addAction(preferAct)

        return preferMenu

    def exit_action(self):
       # Exit Action, connect
        exitAction = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton),
                             '&Exit', self)       
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        self.statusBar()
        return exitAction


if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())