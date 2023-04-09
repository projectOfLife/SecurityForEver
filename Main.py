import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QMessageBox, QLineEdit, \
    QRadioButton, QCheckBox
import logo_rc
from Recon.recon import *


class Thread(QThread):
    finished = pyqtSignal()

    def __init__(self, domain=None, is_live=None, is_end=None, is_par=None, is_JS=None, is_screen=None):
        super().__init__()
        self.is_screen = is_screen
        self.is_par = is_par
        self.is_JS = is_JS
        self.domain = domain
        self.is_live = is_live
        self.is_end = is_end
        self.is_running = True

    def run(self) -> None:
        # super().sleep(1)
        print("Im in thread")
        if not self.is_running:
            return
        subfinder_for_single_windows(self.domain)
        if self.is_live:
            httprobe_w()
        if self.is_end:
            wwayback()
        if self.is_JS:
            Js_file()
        if self.is_par:
            Parameter()
        if self.is_screen:
            screenwin()
        self.finished.emit()
    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    path: str = None
    thread = None
    selected_directory: str = None
    is_live_subdomain: bool = None
    is_endpoints: bool = None
    is_JS_files: bool = None
    is_parameter: bool = None
    is_screenshot: bool = None


    def __init__(self):
        super().__init__()
        loadUi("design.ui", self)
        # ----------- Home ------------ #
        self.chooseProject.hide()
        self.widget_list_domain.hide()
        self.widget_single_domain.hide()
        self.WAFbtn.clicked.connect(self.do_work)
        self.BackHomebtn.clicked.connect(self.back_home)
        self.BackHomebtn_2.clicked.connect(self.back_home)
        self.filebtn.clicked.connect(self.open_file_dialog)

        # ------------- Recon ---------- #
        # self.Screenshot
        # self.Parameter
        # self.Js_files
        # self.Endpoint
        # self.Live_subdomain
        # self.stopbtn
        self.stopbtn.hide()

        self.reconbtn.clicked.connect(self.start_single_list_task)

    def start_single_list_task(self):
        target: str = self.target_line.text()
        is_live: QCheckBox = self.Live_subdomain
        is_endpoint: QCheckBox = self.Endpoint
        is_JS: QCheckBox = self.Js_files
        is_screen: QCheckBox = self.Screenshot
        is_parameter: QCheckBox = self.Parameter

        if self.singleRadio.isChecked():
            if target.strip() == '':
                self.stopbtn.hide()
                QMessageBox.information(self, 'Information', f'Enter Right Target Plz')
            else:
                # Subdomain Checkbox
                if is_live.isChecked():
                    self.is_live_subdomain = True
                    is_live.setEnabled(False)

                if is_endpoint.isChecked():
                    self.is_endpoints = True
                    is_endpoint.setEnabled(False)

                if is_JS.isChecked():
                    self.is_JS_files = True
                    is_JS.setEnabled(False)

                if is_screen.isChecked():
                    self.is_screenshot = True
                    is_screen.setEnabled(False)

                if is_parameter.isChecked():
                    self.is_parameter = True
                    is_parameter.setEnabled(False)

                self.reconbtn.setEnabled(False)
                thread = Thread(target.strip(),
                                     is_live=self.is_live_subdomain,
                                     is_end=self.is_endpoints,
                                     is_par=self.is_parameter,
                                     is_screen=self.is_screenshot,
                                     is_JS=self.is_JS_files)

                self.thread.finished.connect(self.on_finished)
                # self.stopbtn.pressed.connect(self.thread.stop)
                self.thread.start()

        elif self.listRadio.isChecked():
            pass
        else:
            self.stopbtn.hide()
            QMessageBox.information(self, 'Information', f'Choosing Single or List Domain')

    def on_finished(self):
        self.reconbtn.setEnabled(True)
        self.Live_subdomain.setEnabled(True)
        self.is_parameter.setEnabled(True)
        self.is_screenshot.setEnabled(True)
        self.is_endpoints.setEnabled(True)
        self.is_JS_files.setEnabled(True)

    def open_file_dialog(self):
        project_name: QLineEdit = self.projectName.text()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if project_name.strip() != '':
            if file_dialog.exec_() == file_dialog.Accepted:
                self.selected_directory = file_dialog.selectedFiles()[0]
                self.path = self.selected_directory + r'/' + project_name

            else:
                QMessageBox.warning(self, 'Warning', 'No directory selected.')
        else:
            QMessageBox.information(self, 'Information', f'write project name correct.')

    def do_work(self):
        project_name: QLineEdit = self.projectName
        stack_widget: QStackedWidget = self.stackedWidget
        waf_widget: QRadioButton = self.WafRadio
        frame_widget: QRadioButton = self.FrameRadio
        if waf_widget.isChecked():
            stack_widget.setCurrentIndex(1)
        elif frame_widget.isChecked():
            # print(f"What's happen {self.path}")
            if self.selected_directory is None:
                QMessageBox.information(self, 'Information', f'Select Path.')
            elif os.path.exists(self.path):
                QMessageBox.information(self, 'Warning', f'Project is already in this {self.path} change project name')
            else:
                os.mkdir(self.path)
                stack_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Warning', 'Choose Option')

    def back_home(self):
        # waf_widget: QtWidgets.QRadioButton = self.WafRadio
        # frame_widget: QtWidgets.QRadioButton = self.FrameRadio
        self.stackedWidget.setCurrentIndex(0)
        self.chooseProject.hide()
        # waf_widget.setChecked(False)
        # frame_widget.setChecked(False)


def main():
    app = QApplication([])  # Start App
    main_app = MainWindow()
    main_app.show()
    try:
        sys.exit(app.exec_())  # Exit app when Press X
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
