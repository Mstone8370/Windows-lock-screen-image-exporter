import enum
import os
import sys
import shutil
import cv2
import math
from resource.ui_main import Ui_MainWindow
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# pyside2-uic resource/ui_main.ui -o resource/ui_main.py     --> .ui to .py

COL_CHECK_WIDTH = 35
COL_IMG_WIDTH = 245
ROW_HEIGHT = math.floor(COL_IMG_WIDTH / 16 * 9)

class MessageBoxType(enum.Enum):
    ABOUTQT = 0
    ABOUT = 1
    INFORMATION = 2
    QUESTION = 3
    WARNING = 4
    CRITICAL = 5


# https://stackoverflow.com/a/51061279
def get_resource_path(relative_path=""):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # base_path = os.path.abspath(".")
        base_path = os.getcwd()

    return os.path.join(base_path, relative_path)


def copy_files(files, dst):
    copied_file_dir = []
    try:
        for file in files:
            shutil.copy(file, dst)
            copied_file_dir.append(os.path.join(dst, os.path.split(file)[-1]))
        print(copied_file_dir)
        return copied_file_dir
    except Exception as e:
        print(e)
        for file in copied_file_dir:
            if os.path.isfile(file):
                os.remove(file)
        return None



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowIcon(ICON_PATH)
        self.setWindowTitle("Windows lock screen image exporter")

        self.init_variables()
        self.init_widgets()
        self.load_image()
    

    def closeEvent(self, event):
        self.remove_tmp_image()
    

    def init_variables(self):
        self.resource_dir = get_resource_path()
        self.src_abs_dir = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.join(
                        os.path.expandvars('%LOCALAPPDATA%'),
                        "Packages"
                    ),
                    "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy"
                ),
                "LocalState"
            ),
            "Assets"
        )
        self.dst_abs_dir = os.getcwd()
        self.save_dir = os.getcwd()
        self.checkBoxes = []
        self.tmp_images = []
    

    def init_widgets(self):
        self.ui.refresh_pushButton.clicked.connect(self.refresh)
        self.ui.save_pushButton.clicked.connect(self.save_image)
        self.ui.check_all_pushButton.clicked.connect(self.check_all)
        self.ui.uncheck_all_pushButton.clicked.connect(self.uncheck_all)


    def show_messageBox(self, messageBox_type=MessageBoxType.ABOUT, text="", title=""):
        """Show Message Box"""
        if messageBox_type == MessageBoxType.ABOUTQT:
            QMessageBox.aboutQt(self)
        if messageBox_type == MessageBoxType.ABOUT:
            QMessageBox.about(self, title, text)
        if messageBox_type == MessageBoxType.INFORMATION:
            QMessageBox.information(self, title, text, QMessageBox.Ok)
        if messageBox_type == MessageBoxType.QUESTION:
            QMessageBox.question(self, title, text, QMessageBox.Ok, QMessageBox.Cancel)
        if messageBox_type == MessageBoxType.WARNING:
            QMessageBox.warning(self, title, text, QMessageBox.Ok)
        if messageBox_type == MessageBoxType.CRITICAL:
            QMessageBox.critical(self, title, text, QMessageBox.Ok)


    def load_image(self):
        """이미지 가져와서 ui에 띄움"""
        file_list = []
        if os.path.isdir(self.src_abs_dir):
            file_list = os.listdir(self.src_abs_dir)
        file_list = [os.path.join(self.src_abs_dir, x) for x in file_list]
        copied_files = copy_files(file_list, self.resource_dir)
        if copied_files == None:
            return
        self.tmp_images = self.to_image(copied_files)
        
        # Update widget
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(math.ceil(len(self.tmp_images) / 2))
        self.ui.tableWidget.setColumnWidth(0, COL_CHECK_WIDTH)
        self.ui.tableWidget.setColumnWidth(1, COL_IMG_WIDTH)
        self.ui.tableWidget.setColumnWidth(2, COL_CHECK_WIDTH)
        self.ui.tableWidget.setColumnWidth(3, COL_IMG_WIDTH)
        for i in range(len(self.tmp_images)):
            row = math.floor(i / 2)
            col_checkBox = (i % 2) * 2
            col_img = col_checkBox + 1
            # Create check box widget
            checkbox = ImageCheckBox("", self, self.tmp_images[i])
            self.checkBoxes.append(checkbox)
            checkbox_cell_widget = ClickableWidget(checkbox)
            checkbox_layout = QHBoxLayout(checkbox_cell_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_cell_widget.setLayout(checkbox_layout)
            # Create image label widget
            img = QPixmap(self.tmp_images[i])
            img = img.scaledToHeight(ROW_HEIGHT)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label_cell_widget = ClickableWidget(checkbox)
            img_label_layout = QHBoxLayout(img_label_cell_widget)
            img_label_layout.addWidget(img_label)
            img_label_layout.setAlignment(Qt.AlignCenter)
            img_label_layout.setContentsMargins(0, 0, 0, 0)
            img_label_cell_widget.setLayout(img_label_layout)
            # Set item
            self.ui.tableWidget.setCellWidget(row, col_checkBox, checkbox_cell_widget)
            self.ui.tableWidget.setCellWidget(row, col_img, img_label_cell_widget)
            self.ui.tableWidget.setRowHeight(row, ROW_HEIGHT)
            # Check image size
            img_cv = cv2.imread(self.tmp_images[i])
            img_cv_height, img_cv_width, _ = img_cv.shape
            if img_cv_width > img_cv_height:
                checkbox.setChecked(True)
            QApplication.processEvents()
    

    def to_image(self, files):
        ext = ".jpg"
        for file in files:
            try:
                os.rename(file, file + ext)
            except Exception as e:
                os.remove(file)
        return [x + ext for x in files]


    def refresh(self):
        self.remove_tmp_image()
        self.checkBoxes = []
        # Remove all rows from tableWidget
        while self.ui.tableWidget.rowCount() > 0:
            self.ui.tableWidget.removeRow(0);
        QApplication.processEvents()
        self.load_image()
    

    def remove_tmp_image(self):
        for tmp in self.tmp_images:
            try:
                os.remove(tmp)
            except Exception as e:
                print(e)
                continue
        self.tmp_images = []
        print("temp image removed.")
    

    def save_image(self):
        img_to_save = []
        for checkBox in self.checkBoxes:
            if checkBox.isChecked():
                img_to_save.append(checkBox.image_dir)
        if len(img_to_save) < 1:
            return

        selected_dir = QFileDialog.getExistingDirectory(self, dir=self.save_dir)
        if not os.path.isdir(selected_dir):
            return
        self.save_dir = selected_dir

        for img in img_to_save:
            try:
                shutil.copy(img, self.save_dir)
            except Exception as e:
                continue
        self.show_messageBox(MessageBoxType.INFORMATION, text="Image saved.", title=" ")
    

    def check_all(self):
        for checkbox in self.checkBoxes:
            checkbox.setChecked(True)


    def uncheck_all(self):
        for checkbox in self.checkBoxes:
            checkbox.setChecked(False)



class ImageCheckBox(QCheckBox):
    def __init__(self, text, parent=None, image_dir=""):
        super().__init__(text, parent)
        self.image_dir = image_dir



class ClickableWidget(QWidget):
    def __init__(self, checkBox=None):
        super().__init__()
        self.linked_checkBox = checkBox
        self.mousePressEvent = self.toggle_checkBox


    def toggle_checkBox(self, event):
        if self.linked_checkBox == None:
            return
        self.linked_checkBox.setChecked(not self.linked_checkBox.isChecked())



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
