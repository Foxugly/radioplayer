import os
import threading
import constantes
from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow, QTableWidget, QMessageBox, \
    QVBoxLayout, QAbstractItemView, QTableWidgetItem, QShortcut
import pyautogui
from time import sleep
from random import randint

pyautogui.FAILSAFE = False


class RadioPlayerWidget(QMainWindow):
    def __init__(self, app, mp):
        super().__init__()
        self.question_menu = None
        self.thread = None
        self.dict_config = {}
        self.app = app
        self.m = False
        self.my_player = mp
        self._create_actions()
        self._create_menubar()
        self._create_toolbar()
        self._create_playlist()
        self.setWindowTitle(constantes.TITLE_APP)
        self.resize(300, 600)
        if self.my_player.current_channel is not None:
            self.tw.item(self.my_player.current_channel, 0).setFont(self.fontselect)
            # play pushed
            self.play_action.setChecked(True)
        else:
            # pause pushed
            self.pause_action.setChecked(True)
        if self.my_player.player.isMuted():
            self.volume_mute_action.setChecked(True)
        self.msg = QShortcut(QKeySequence('Ctrl+M'), self)
        self.msg.activated.connect(self.mm)

    def play(self):
        self.pause_action.setChecked(False)
        self.my_player.current_channel = self.tw.currentIndex().row()
        self.my_player.player.playlist().setCurrentIndex(self.my_player.current_channel)
        self.my_player.player.play()
        for i in range(0, self.nbrow):
            self.tw.item(i, 0).setFont(self.font)
        self.tw.item(self.my_player.current_channel, 0).setFont(self.fontselect)

    def pause(self):
        self.play_action.setChecked(False)
        for i in range(0, self.nbrow):
            self.tw.item(i, 0).setFont(self.font)
        self.my_player.player.pause()

    def volume_up(self):
        current_volume = self.my_player.player.volume()
        self.my_player.player.setVolume(current_volume + 5)

    def volume_down(self):
        current_volume = self.my_player.player.volume()
        self.my_player.player.setVolume(current_volume - 5)

    def volume_mute(self):
        self.my_player.player.setMuted(not self.my_player.player.isMuted())

    def mm(self):
        self.m = not self.m
        if self.m:
            self.question_menu.deleteLater()
            self.thread = threading.Thread(target=self.thread_funct, daemon=True)
            self.thread.start()
        else:
            self.question_menu = QMenu("?", self)
            self.menubar.addMenu(self.question_menu)
            self.question_menu.addAction(self.about_action)

    def thread_funct(self):
        while self.m:
            x = 0
            sleep(randint(5, 10))
            x, y = pyautogui.position()
            x_max, y_max = pyautogui.size()
            if self.m:
                offset = randint(10, 30)
                if x + offset < x_max:
                    for i in range(randint(10, 30)):
                        if self.m:
                            pyautogui.moveTo(x + offset, y)
                            sleep(randint(1, 3))
                            pyautogui.moveTo(x, y)
                else:
                    for i in range(randint(10, 30)):
                        if self.m:
                            pyautogui.moveTo(x - offset, y)
                            sleep(randint(1, 3))
                            pyautogui.moveTo(x, y)
                if self.m:
                    for i in range(randint(1, 10)):
                        pyautogui.press("shift")
            pyautogui.press("escape")

    def about(self):
        QMessageBox.about(None,
                          "RadioPlayer - About",
                          "RadioPlayer v. 1.0.0\n by Foxugly 2022")
    def exit(self):
        self.app.quit()

    def _create_actions(self):
        # File actions
        self.play_action = QAction(QIcon(constantes.ICON_PLAY), "&Play", self)
        self.play_action.setCheckable(True)
        self.play_action.triggered.connect(self.play)
        self.pause_action = QAction(QIcon(constantes.ICON_PAUSE), "&Pause", self)
        self.pause_action.setCheckable(True)
        self.pause_action.triggered.connect(self.pause)
        self.volume_up_action = QAction(QIcon(constantes.ICON_VOLUME_PLUS), "&Volume Up", self)
        self.volume_up_action.triggered.connect(self.volume_up)
        self.volume_down_action = QAction(QIcon(constantes.ICON_VOLUME_MINUS), "&Volume Down", self)
        self.volume_down_action.triggered.connect(self.volume_down)
        self.volume_mute_action = QAction(QIcon(constantes.ICON_MUTE), "&Mute", self)
        self.volume_mute_action.setCheckable(True)
        self.volume_mute_action.triggered.connect(self.volume_mute)
        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self.about)
        self.exit_action = QAction(QIcon(constantes.ICON_EXIT), "&Exit", self)
        self.exit_action.triggered.connect(self.exit)

    def _create_menubar(self):
        self.menubar = self.menuBar()
        self.file_menu = QMenu("&File", self)
        self.menubar.addMenu(self.file_menu)
        self.file_menu.addAction(self.exit_action)
        self.sound_menu = self.menubar.addMenu("&Sounds")
        self.sound_menu.addAction(self.play_action)
        self.sound_menu.addAction(self.pause_action)
        self.sound_menu.addAction(self.volume_up_action)
        self.sound_menu.addAction(self.volume_down_action)
        self.sound_menu.addAction(self.volume_mute_action)
        #self.help_menu = self.menubar.addMenu("&Help")
        #self.help_menu.addAction(self.aboutAction)
        self.question_menu = QMenu("?", self)
        self.menubar.addMenu(self.question_menu)
        self.question_menu.addAction(self.about_action)
        # self.menuBar.addAction(self.questionAction)
        # self.question_action = QAction("?", self)
        # self.question_action.triggered.connect(self.question)
        # self.question_menu = QMenu("?", self)
        # self.menuBar.addMenu(self.question_action)

    def _create_toolbar(self):
        # File toolbar
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.addAction(self.play_action)
        self.file_toolbar.addAction(self.pause_action)
        self.file_toolbar.addAction(self.volume_up_action)
        self.file_toolbar.addAction(self.volume_down_action)
        self.file_toolbar.addAction(self.volume_mute_action)
        self.file_toolbar.addSeparator()
        self.file_toolbar.addAction(self.exit_action)

    def _create_playlist(self):
        famille = "DejaVu Sans"
        taille = 9
        self.font = QFont()
        self.font.setFamily(famille)
        self.font.setPointSize(taille)

        # police avec gras et italique pour la radio sélectionnée
        self.fontselect = QFont()
        self.fontselect.setFamily(famille)
        self.fontselect.setPointSize(taille)
        self.fontselect.setBold(True)
        self.fontselect.setItalic(True)

        # Crée un QTableWidget pour afficher les radios disponibles
        self.tw = QTableWidget(self)
        self.tw.setFont(self.font)
        self.nbrow, self.nbcol = len(self.my_player.radios), 1
        self.tw.setRowCount(self.nbrow)
        self.tw.setColumnCount(self.nbcol)
        layout = QVBoxLayout()
        layout.addWidget(self.tw)

        self.setCentralWidget(self.tw)
        self.tw.cellDoubleClicked.connect(self.selection)
        for row in range(0, self.nbrow):
            item = QTableWidgetItem(self.my_player.radios[row][0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw.setItem(row, 0, item)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem("Radios"))
        h = self.tw.horizontalHeader()
        h.setStretchLastSection(True)
        self.tw.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tw.setFocusPolicy(Qt.StrongFocus)
        self.tw.setFocus()
        cell = self.my_player.current_channel if self.my_player.current_channel else 0
        self.tw.setCurrentCell(cell, 0)

    @pyqtSlot(int, int)
    def selection(self, row, _):
        self.my_player.player.playlist().setCurrentIndex(row)
        self.play()
        self.my_player.current_channel = row


class RadioMenu(QMenu):
    def __init__(self, app):
        super().__init__()
        self.option_open = QAction("Open")
        self.addAction(self.option_open)
        self.quit = QAction("Exit")
        self.quit.triggered.connect(app.quit)
        self.addAction(self.quit)


class MyPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.current_channel = None
        self._chargeradios()
        self.playlist = QMediaPlaylist()
        for _, urlradio in self.radios:
            if os.path.exists(urlradio):
                qurlradio = QUrl.fromLocalFile(urlradio.replace('\\', '/'))
            else:
                qurlradio = QUrl(urlradio)
            self.playlist.addMedia(QMediaContent(qurlradio))
        self.player.setPlaylist(self.playlist)

    def _chargeradios(self):
        try:
            if not os.path.exists(constantes.LIST_RADIO):
                raise ValueError("Le fichier 'radioweb.txt' n'est pas trouvé")
            self.radios = []
            with open(constantes.LIST_RADIO, "r", encoding="utf-8") as fs:
                for ligne in fs:
                    ligne = ligne.strip()
                    if ligne == "":
                        continue
                    if ligne.startswith('#'):
                        continue
                    nom, url = ligne.split('|')
                    self.radios.append([nom.rstrip(), url.lstrip()])
        except ValueError:
            QMessageBox.critical(None,
                                 "RadioPlayer - Error",
                                 "Le fichier 'radioweb.txt' n'est pas trouvé")


class RadioPlayer:
    def __init__(self):
        self.menu = None
        self.tray = None
        self.icon = None
        self.myplayer = MyPlayer()
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.show_widget()
        self.rpw.exit_action.triggered.connect(self.app.quit)
        self.create_tray()
        self.app.exec_()

    def create_tray(self):
        self.icon = QIcon(constantes.ICON_APP)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.menu = RadioMenu(self.app)
        self.menu.option_open.triggered.connect(self.show_widget)
        self.tray.setContextMenu(self.menu)

    def show_widget(self):
        self.rpw = RadioPlayerWidget(self.app, self.myplayer)
        self.rpw.show()


rp = RadioPlayer()
