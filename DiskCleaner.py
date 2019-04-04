from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QFileDialog,QMenu,QSystemTrayIcon,\
                             QMainWindow,QHBoxLayout,QAction,QTreeView,QTextEdit,QFileSystemModel,QVBoxLayout
import sys
import os
from zipfile import ZipFile
from os.path import basename
import zipfile
from os.path import expanduser
import subprocess
import hashlib
import traceback
import shutil

import DiskCleaner_ui


class main(QMainWindow, DiskCleaner_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.openMenu()

        systray_icon = QIcon("DC.png")
        self.systray = QSystemTrayIcon(systray_icon, self)
        self.systray.setContextMenu(self.menu)
        self.systray.show()
        self.systray.showMessage("DC", "Started...", QSystemTrayIcon.Information)
        self.closeapp.triggered.connect(self.close)

        self.setWindowIcon(systray_icon)


        self.Duplicate()
        self.dormant()
        self.Temp()



    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    
    def scan(self):
        if os.listdir(self.temp_path) or os.listdir(self.dormant_path) == []:
            self.systray.showMessage("DC", "No Temporary files..", QSystemTrayIcon.Information)
        else:
            pass

    def clear_Files(self):
        reply = QMessageBox.question(self, 'Clear Files', "Are you sure you want delete all files?", QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.scan()
                with os.scandir(self.temp_path) or os.scandir(self.dormant_path) as entries:
                    for entry in entries:
                        if entry.is_file() or entry.is_symlink():
                            os.remove(entry.path)
                            self.systray.showMessage("DC", "Temporary files/folders cleared",
                                                     QSystemTrayIcon.Information)
                        elif entry.is_dir():
                            shutil.rmtree(entry.path)
                            self.systray.showMessage("DC", "Temporary files/folders cleared",
                                                     QSystemTrayIcon.Information)
                        else:
                            pass
            except Exception:
                pass




    def openMenu(self):
        self.menu = QMenu()
        self.restore = QAction("Restore", self)
        self.closeapp = QAction("Close", self)

        self.menu.addActions([self.restore, self.closeapp])

    def on_clicked(self, index):
        self.path = self.fileSystemModel.filePath(index)
        print(self.path)


    def zip_file(self):
        try:
            if os.path.exists(self.path):
                try:
                    dask = QFileDialog.getSaveFileName(self, 'Select Folder to store Zip file',
                                                       expanduser("~"), '.zip')
                    dpath = str(dask[0])
                    if os.path.isfile(self.path):
                        with ZipFile(dpath, 'w') as zip:
                            zip.write(self.path, basename(self.path))

                            self.systray.showMessage("DC", "File Zipped succesfully",
                                                     QSystemTrayIcon.Information)
                    else:
                        zf = zipfile.ZipFile(dpath, "w")
                        for dirname, subdirs, files in os.walk(self.path):
                            zf.write(dirname, basename(dirname))
                            for filename in files:
                                zf.write(os.path.join(dirname, filename), basename(os.path.join(dirname, filename)))
                        zf.close()
                        self.systray.showMessage("DC", "Folder Zipped Succesfully", QSystemTrayIcon.Information)
                except Exception:
                    pass
            else:
                pass
        except Exception:
            pass



    def delete_file(self):
        reply = QMessageBox.question(self, 'Delete File', "Are you sure you want to delete file?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if os.path.exists(self.path):
                    try:
                        os.remove(self.path)
                        self.systray.showMessage("DC", "Temporary  file Deleted", QSystemTrayIcon.Information)
                    except Exception:
                        shutil.rmtree(self.path)
                        self.systray.showMessage("DC", "Temporary  folder Deleted", QSystemTrayIcon.Information)
            except Exception:
                self.systray.showMessage("DC", "Error deleting file", QSystemTrayIcon.Critical)
        else:
            pass

    def tabMenu(self,position):

        self.tmenu = QMenu()

        self.open = self.tmenu.addAction('Open')
        self.open_file_location = self.tmenu.addAction('Open File Location')

        self.tmenu.addActions([self.open, self.open_file_location])
        action = self.tmenu.exec_(self.temp_treeView.viewport().mapToGlobal(position))

        if action == self.open:
            os.startfile(self.path, 'open')
        elif action == self.open_file_location:
            try:
                subprocess.Popen(r'explorer /select,' + "{}".format(self.path).replace('/', '\\'))
            except Exception:
                pass

    def Temp(self):
        self.temp_treeView = QTreeView()

        self.temp_treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.temp_treeView.customContextMenuRequested.connect(self.tabMenu)

        self.fileSystemModel = QFileSystemModel(self.temp_treeView)
        self.fileSystemModel.setReadOnly(False)
        self.temp_path = expanduser('~') + '\AppData\Local\Temp'
        root = self.fileSystemModel.setRootPath(self.temp_path)
        self.temp_treeView.setModel(self.fileSystemModel)
        self.temp_treeView.setRootIndex(root)
        self.temp_treeView.setSortingEnabled(True)

        self.temp_treeView.clicked.connect(self.on_clicked)

        self.clearAll_button = QPushButton("Clear all Files")
        self.clearAll_button.setFixedSize(90, 30)

        self.clearAll_button.clicked.connect(self.clear_Files)

        self.temp_delete_button = QPushButton('Delete')
        self.temp_delete_button.setFixedSize(90, 30)

        self.temp_delete_button.clicked.connect(self.delete_file)

        self.temp_zip_button = QPushButton('Zip file')
        self.temp_zip_button.setFixedSize(90, 30)


        self.temp_zip_button.clicked.connect(self.zip_file)

        Layout = QHBoxLayout(self)
        Layout.addWidget(self.clearAll_button)
        Layout.addWidget(self.temp_delete_button)
        Layout.addWidget(self.temp_zip_button)
        Layout.addWidget(self.temp_treeView)

        self.Temp_Tab.setLayout(Layout)

    def Duplicate(self):

        dup_button = QPushButton('Duplicate Finder')
        dup_button.setFixedSize(90, 30)

        Layout = QHBoxLayout(self)
        Layout.addWidget(dup_button)

        dup_button.clicked.connect(self.dup_finder)

        self.Duplicate_Tab.setLayout(Layout)

    def dup_finder(self):

        def chunk_reader(fobj, chunk_size=2048):
            """ Generator that reads a file in chunks of bytes """
            while True:
                chunk = fobj.read(chunk_size)
                if not chunk:
                    return
                yield chunk

        class SignalHelper(QObject):
            error = pyqtSignal(tuple)
            result = pyqtSignal(object)
            finished = pyqtSignal()
            progress = pyqtSignal(str, str)

        class Worker(QRunnable):
            def __init__(self, fn, *args, **kwargs):
                super(Worker, self).__init__()

                self.fn = fn
                self.args = args
                self.kwargs = kwargs
                self.signals = SignalHelper()

                # Add a callback to our kwargs
                kwargs['progress_callback'] = self.signals.progress

            @pyqtSlot()
            def run(self):
                try:
                    result = self.fn(*self.args, **self.kwargs)
                except:
                    traceback.print_exc()
                    exctype, value = sys.exc_info()[:2]
                    self.signals.error.emit((exctype, value,
                                             traceback.format_exc()))
                else:
                    self.signals.result.emit(result)
                finally:
                    self.signals.finished.emit()

        class MainWindow(QMainWindow):
            def __init__(self, *args, **kwargs):
                super(MainWindow, self).__init__(*args, **kwargs)

                self.setWindowTitle('Duplicate Finder')

                systray_icon = QIcon("s.png")
                self.systray = QSystemTrayIcon(systray_icon, self)
                self.systray.show()


                layout = QVBoxLayout()
                self.textEdit = QTextEdit("Display duplicate files :")
                self.textEdit.setReadOnly(True)

                self.b = QPushButton("Scan files")
                self.b.setCheckable(True)
                self.b.pressed.connect(self.watcher)

                self.d = QPushButton('Delete dup files')
                self.d.clicked.connect(self.delete_duplicate_files)

                layout.addWidget(self.textEdit)
                layout.addWidget(self.b)
                layout.addWidget(self.d)

                w = QWidget()
                w.setLayout(layout)
                self.setCentralWidget(w)

                self.threadpool = QThreadPool()

            def delete_duplicate_files(self):

                def remove_duplicates(dir, hashfun=hashlib.sha512):

                    unique = set()
                    for filename in os.listdir(dir):
                        filepath = os.path.join(dir, filename)
                        if os.path.isfile(filepath):
                            hashobj = hashfun()
                            for chunk in chunk_reader(open(filepath, 'rb')):
                                hashobj.update(chunk)
                                # the size of the hashobj is constant
                            hashfile = hashobj.hexdigest()
                            if hashfile not in unique:
                                unique.add(hashfile)
                            else:
                                try:
                                    os.remove(filepath)
                                    print('delete')

                                except Exception:
                                    print(' cant delete')


                try:
                    reply = QMessageBox.question(self, 'Delete File', "Are you sure you want to delete file?",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        hashfun = hashlib.sha256
                        remove_duplicates(self.path)
                        self.systray.showMessage("DC", 'Duplicate files deleted', QSystemTrayIcon.Information)
                    else:
                        pass
                except IndexError:
                    self.systray.showMessage("DC", "Error deleting duplicate files", QSystemTrayIcon.Critical)

            def watcher(self):
                self.path = QFileDialog.getExistingDirectory(self, 'select folder to scan', expanduser('~'))

                worker = Worker(self.check_for_duplicates)
                worker.signals.progress.connect(self.progress_fn)
                self.threadpool.start(worker)

            def progress_fn(self, duplicate, full_path):
                self.textEdit.append(
                    "<font color=red>Duplicate found:</font> %s <b>and</b> %s" % (full_path, duplicate))
                self.textEdit.append("")
                self.textEdit.append("")


            def check_for_duplicates(self, progress_callback, hash=hashlib.sha1):
                # specify your path !!!
                hashes = {}
                for dirpath, dirnames, filenames in os.walk(self.path):
                    for filename in filenames:
                        full_path = os.path.join(dirpath, filename).replace('/', '\\')
                        # print(full_path)
                        hashobj = hash()
                        for chunk in chunk_reader(open(full_path, 'rb')):
                            hashobj.update(chunk)
                        file_id = (hashobj.digest(), os.path.getsize(full_path))
                        self.duplicate = hashes.get(file_id, None)
                        if self.duplicate:
                            progress_callback.emit(self.duplicate, full_path)
                            print("Duplicate found: %s and %s" % (full_path, self.duplicate))
                            try:
                                print(self.duplicate)
                            except Exception:

                                print('could not delete')
                        else:
                            hashes[file_id] = full_path

                # return duplicate



        global w
        w = MainWindow()
        w.setGeometry(700, 200, 550, 300)
        w.show()


    def dormant(self):

        treeView = QTreeView()

        treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        treeView.customContextMenuRequested.connect(self.tabMenu)

        fileSystemModel = QFileSystemModel(treeView)
        fileSystemModel.setReadOnly(False)
        self.dormant_path = expanduser('~') + '\Documents'
        root = fileSystemModel.setRootPath(self.dormant_path)
        treeView.setModel(fileSystemModel)
        treeView.setRootIndex(root)
        treeView.setSortingEnabled(True)

        treeView.clicked.connect(self.on_clicked)

        dormant_clearAll_button = QPushButton("Clear all Files")
        dormant_clearAll_button.setFixedSize(90, 30)
        self.dormant_delete_button = QPushButton('Delete')
        self.dormant_delete_button.setFixedSize(90, 30)

        self.dormant_delete_button.clicked.connect(self.delete_file)

        dormant_zip_button = QPushButton('Zip file')
        dormant_zip_button.setFixedSize(90, 30)

        dormant_zip_button.clicked.connect(self.zip_file)

        Layout = QHBoxLayout(self)
        Layout.addWidget(dormant_clearAll_button)
        Layout.addWidget(self.dormant_delete_button)
        Layout.addWidget(dormant_zip_button)
        Layout.addWidget(treeView)

        #dormant_clearAll_button.clicked.connect(self.clear_Files())

        self.UnUsed_Tab.setLayout(Layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    H = main()
    H.show()
    app.exec_()
