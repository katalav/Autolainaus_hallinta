# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'administrative.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1107, 634)
        icon = QIcon(QIcon.fromTheme(u"preferences-desktop-accessibility"))
        MainWindow.setWindowIcon(icon)
        self.actionMuokkaa = QAction(MainWindow)
        self.actionMuokkaa.setObjectName(u"actionMuokkaa")
        self.actionTietoja_ohjelmasta = QAction(MainWindow)
        self.actionTietoja_ohjelmasta.setObjectName(u"actionTietoja_ohjelmasta")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 941, 561))
        font = QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lenderTab = QWidget()
        self.lenderTab.setObjectName(u"lenderTab")
        self.lenderTab.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.registeredPersonsTableWidget = QTableWidget(self.lenderTab)
        if (self.registeredPersonsTableWidget.columnCount() < 6):
            self.registeredPersonsTableWidget.setColumnCount(6)
        if (self.registeredPersonsTableWidget.rowCount() < 10):
            self.registeredPersonsTableWidget.setRowCount(10)
        self.registeredPersonsTableWidget.setObjectName(u"registeredPersonsTableWidget")
        self.registeredPersonsTableWidget.setGeometry(QRect(20, 240, 641, 241))
        self.registeredPersonsTableWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.registeredPersonsTableWidget.setRowCount(10)
        self.registeredPersonsTableWidget.setColumnCount(6)
        self.registeredPersonsLabel = QLabel(self.lenderTab)
        self.registeredPersonsLabel.setObjectName(u"registeredPersonsLabel")
        self.registeredPersonsLabel.setGeometry(QRect(20, 220, 131, 16))
        self.savePersonPushButton = QPushButton(self.lenderTab)
        self.savePersonPushButton.setObjectName(u"savePersonPushButton")
        self.savePersonPushButton.setGeometry(QRect(310, 180, 71, 23))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.savePersonPushButton.setFont(font1)
        self.savePersonPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.savePersonPushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"color: rgb(255, 255, 255);")
        self.layoutWidget = QWidget(self.lenderTab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(130, 10, 171, 191))
        self.studentInputsVerticalLayout = QVBoxLayout(self.layoutWidget)
        self.studentInputsVerticalLayout.setObjectName(u"studentInputsVerticalLayout")
        self.studentInputsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ssnLineEdit = QLineEdit(self.layoutWidget)
        self.ssnLineEdit.setObjectName(u"ssnLineEdit")
        font2 = QFont()
        font2.setPointSize(11)
        self.ssnLineEdit.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.ssnLineEdit)

        self.firstNameLineEdit = QLineEdit(self.layoutWidget)
        self.firstNameLineEdit.setObjectName(u"firstNameLineEdit")
        self.firstNameLineEdit.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.firstNameLineEdit)

        self.lastNameLineEdit = QLineEdit(self.layoutWidget)
        self.lastNameLineEdit.setObjectName(u"lastNameLineEdit")
        self.lastNameLineEdit.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.lastNameLineEdit)

        self.groupComboBox = QComboBox(self.layoutWidget)
        self.groupComboBox.setObjectName(u"groupComboBox")
        self.groupComboBox.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.groupComboBox)

        self.vehicleClassLineEdit = QLineEdit(self.layoutWidget)
        self.vehicleClassLineEdit.setObjectName(u"vehicleClassLineEdit")
        self.vehicleClassLineEdit.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.vehicleClassLineEdit)

        self.emailLineEdit = QLineEdit(self.layoutWidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")
        self.emailLineEdit.setFont(font2)

        self.studentInputsVerticalLayout.addWidget(self.emailLineEdit)

        self.layoutWidget1 = QWidget(self.lenderTab)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 10, 101, 191))
        self.studentLabelsVerticalLayout = QVBoxLayout(self.layoutWidget1)
        self.studentLabelsVerticalLayout.setObjectName(u"studentLabelsVerticalLayout")
        self.studentLabelsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ssnLabel = QLabel(self.layoutWidget1)
        self.ssnLabel.setObjectName(u"ssnLabel")
        self.ssnLabel.setFont(font)

        self.studentLabelsVerticalLayout.addWidget(self.ssnLabel)

        self.firstNameLabel = QLabel(self.layoutWidget1)
        self.firstNameLabel.setObjectName(u"firstNameLabel")
        self.firstNameLabel.setFont(font)

        self.studentLabelsVerticalLayout.addWidget(self.firstNameLabel)

        self.lastNameLabel = QLabel(self.layoutWidget1)
        self.lastNameLabel.setObjectName(u"lastNameLabel")
        self.lastNameLabel.setFont(font)

        self.studentLabelsVerticalLayout.addWidget(self.lastNameLabel)

        self.groupLabel = QLabel(self.layoutWidget1)
        self.groupLabel.setObjectName(u"groupLabel")
        self.groupLabel.setFont(font)

        self.studentLabelsVerticalLayout.addWidget(self.groupLabel)

        self.vehicleClassLabel = QLabel(self.layoutWidget1)
        self.vehicleClassLabel.setObjectName(u"vehicleClassLabel")
        self.vehicleClassLabel.setFont(font)

        self.studentLabelsVerticalLayout.addWidget(self.vehicleClassLabel)

        self.emailLabel = QLabel(self.layoutWidget1)
        self.emailLabel.setObjectName(u"emailLabel")

        self.studentLabelsVerticalLayout.addWidget(self.emailLabel)

        self.deletePersonPushButton = QPushButton(self.lenderTab)
        self.deletePersonPushButton.setObjectName(u"deletePersonPushButton")
        self.deletePersonPushButton.setGeometry(QRect(310, 110, 71, 23))
        self.deletePersonPushButton.setFont(font1)
        self.deletePersonPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.deletePersonPushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"background-color: rgb(255, 1, 5);")
        self.tabWidget.addTab(self.lenderTab, "")
        self.vehicleTab = QWidget()
        self.vehicleTab.setObjectName(u"vehicleTab")
        self.vehicleTab.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.layoutWidget2 = QWidget(self.vehicleTab)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 0, 101, 231))
        self.vehicleLabelsVerticalLayout = QVBoxLayout(self.layoutWidget2)
        self.vehicleLabelsVerticalLayout.setObjectName(u"vehicleLabelsVerticalLayout")
        self.vehicleLabelsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.numberPlateLabel = QLabel(self.layoutWidget2)
        self.numberPlateLabel.setObjectName(u"numberPlateLabel")
        self.numberPlateLabel.setFont(font)

        self.vehicleLabelsVerticalLayout.addWidget(self.numberPlateLabel)

        self.manufacturerLabel = QLabel(self.layoutWidget2)
        self.manufacturerLabel.setObjectName(u"manufacturerLabel")
        self.manufacturerLabel.setFont(font)

        self.vehicleLabelsVerticalLayout.addWidget(self.manufacturerLabel)

        self.modelLabel = QLabel(self.layoutWidget2)
        self.modelLabel.setObjectName(u"modelLabel")
        self.modelLabel.setFont(font)

        self.vehicleLabelsVerticalLayout.addWidget(self.modelLabel)

        self.modelYearLabel = QLabel(self.layoutWidget2)
        self.modelYearLabel.setObjectName(u"modelYearLabel")
        self.modelYearLabel.setFont(font)

        self.vehicleLabelsVerticalLayout.addWidget(self.modelYearLabel)

        self.capacityLabel = QLabel(self.layoutWidget2)
        self.capacityLabel.setObjectName(u"capacityLabel")
        self.capacityLabel.setFont(font)

        self.vehicleLabelsVerticalLayout.addWidget(self.capacityLabel)

        self.vehicleTypeLabel = QLabel(self.layoutWidget2)
        self.vehicleTypeLabel.setObjectName(u"vehicleTypeLabel")

        self.vehicleLabelsVerticalLayout.addWidget(self.vehicleTypeLabel)

        self.vehicleOwnerLabol = QLabel(self.layoutWidget2)
        self.vehicleOwnerLabol.setObjectName(u"vehicleOwnerLabol")

        self.vehicleLabelsVerticalLayout.addWidget(self.vehicleOwnerLabol)

        self.layoutWidget_2 = QWidget(self.vehicleTab)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(120, 0, 169, 238))
        self.vehicleInputsVerticalLayout = QVBoxLayout(self.layoutWidget_2)
        self.vehicleInputsVerticalLayout.setObjectName(u"vehicleInputsVerticalLayout")
        self.vehicleInputsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.numberPlateLineEdit = QLineEdit(self.layoutWidget_2)
        self.numberPlateLineEdit.setObjectName(u"numberPlateLineEdit")
        self.numberPlateLineEdit.setFont(font2)
        self.numberPlateLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.numberPlateLineEdit)

        self.manufacturerLineEdit = QLineEdit(self.layoutWidget_2)
        self.manufacturerLineEdit.setObjectName(u"manufacturerLineEdit")
        self.manufacturerLineEdit.setFont(font2)
        self.manufacturerLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.manufacturerLineEdit)

        self.modelLineEdit = QLineEdit(self.layoutWidget_2)
        self.modelLineEdit.setObjectName(u"modelLineEdit")
        self.modelLineEdit.setFont(font2)
        self.modelLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.modelLineEdit)

        self.modelYearLineEdit = QLineEdit(self.layoutWidget_2)
        self.modelYearLineEdit.setObjectName(u"modelYearLineEdit")
        self.modelYearLineEdit.setFont(font2)
        self.modelYearLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.modelYearLineEdit)

        self.capacityLineEdit = QLineEdit(self.layoutWidget_2)
        self.capacityLineEdit.setObjectName(u"capacityLineEdit")
        self.capacityLineEdit.setFont(font2)
        self.capacityLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.capacityLineEdit)

        self.vehicleTypecomboBox = QComboBox(self.layoutWidget_2)
        self.vehicleTypecomboBox.setObjectName(u"vehicleTypecomboBox")
        self.vehicleTypecomboBox.setFont(font2)

        self.vehicleInputsVerticalLayout.addWidget(self.vehicleTypecomboBox)

        self.vehicleOwnerLineEdit = QLineEdit(self.layoutWidget_2)
        self.vehicleOwnerLineEdit.setObjectName(u"vehicleOwnerLineEdit")
        self.vehicleOwnerLineEdit.setClearButtonEnabled(True)

        self.vehicleInputsVerticalLayout.addWidget(self.vehicleOwnerLineEdit)

        self.saveVehiclePushButton = QPushButton(self.vehicleTab)
        self.saveVehiclePushButton.setObjectName(u"saveVehiclePushButton")
        self.saveVehiclePushButton.setGeometry(QRect(300, 180, 91, 23))
        self.saveVehiclePushButton.setFont(font1)
        self.saveVehiclePushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveVehiclePushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"color: rgb(255, 255, 255);")
        self.printBarcodePushButton = QPushButton(self.vehicleTab)
        self.printBarcodePushButton.setObjectName(u"printBarcodePushButton")
        self.printBarcodePushButton.setGeometry(QRect(300, 40, 91, 23))
        self.printBarcodePushButton.setFont(font1)
        self.printBarcodePushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.printBarcodePushButton.setStyleSheet(u"background-color: rgb(220, 162, 25);\n"
"color: rgb(255, 255, 255);")
        self.vehicleCatalogTableWidget = QTableWidget(self.vehicleTab)
        if (self.vehicleCatalogTableWidget.columnCount() < 8):
            self.vehicleCatalogTableWidget.setColumnCount(8)
        if (self.vehicleCatalogTableWidget.rowCount() < 99):
            self.vehicleCatalogTableWidget.setRowCount(99)
        self.vehicleCatalogTableWidget.setObjectName(u"vehicleCatalogTableWidget")
        self.vehicleCatalogTableWidget.setGeometry(QRect(20, 240, 721, 271))
        self.vehicleCatalogTableWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.vehicleCatalogTableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.vehicleCatalogTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vehicleCatalogTableWidget.setRowCount(99)
        self.vehicleCatalogTableWidget.setColumnCount(8)
        self.vehicleListLabel = QLabel(self.vehicleTab)
        self.vehicleListLabel.setObjectName(u"vehicleListLabel")
        self.vehicleListLabel.setGeometry(QRect(630, 220, 101, 16))
        self.openPicturesPushButton = QPushButton(self.vehicleTab)
        self.openPicturesPushButton.setObjectName(u"openPicturesPushButton")
        self.openPicturesPushButton.setGeometry(QRect(300, 120, 91, 51))
        self.openPicturesPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.openPicturesPushButton.setStyleSheet(u"background-color: rgb(85, 170, 127);")
        icon1 = QIcon(QIcon.fromTheme(u"camera-photo"))
        self.openPicturesPushButton.setIcon(icon1)
        self.openPicturesPushButton.setIconSize(QSize(24, 24))
        self.carPhotoLabel = QLabel(self.vehicleTab)
        self.carPhotoLabel.setObjectName(u"carPhotoLabel")
        self.carPhotoLabel.setGeometry(QRect(450, 30, 261, 181))
        self.carPhotoLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.carPhotoLabel.setPixmap(QPixmap(u"uiPictures/noPicture.png"))
        self.carPhotoLabel.setScaledContents(True)
        self.carPhotoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.removeVehiclePushButton = QPushButton(self.vehicleTab)
        self.removeVehiclePushButton.setObjectName(u"removeVehiclePushButton")
        self.removeVehiclePushButton.setGeometry(QRect(300, 80, 91, 23))
        self.removeVehiclePushButton.setFont(font1)
        self.removeVehiclePushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.removeVehiclePushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"background-color: rgb(255, 1, 5);")
        self.tabWidget.addTab(self.vehicleTab, "")
        self.groupsTab = QWidget()
        self.groupsTab.setObjectName(u"groupsTab")
        self.saveGroupPushButton = QPushButton(self.groupsTab)
        self.saveGroupPushButton.setObjectName(u"saveGroupPushButton")
        self.saveGroupPushButton.setGeometry(QRect(300, 60, 81, 23))
        self.saveGroupPushButton.setFont(font1)
        self.saveGroupPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveGroupPushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"color: rgb(255, 255, 255);")
        self.savedGroupsTableWidget = QTableWidget(self.groupsTab)
        if (self.savedGroupsTableWidget.columnCount() < 2):
            self.savedGroupsTableWidget.setColumnCount(2)
        if (self.savedGroupsTableWidget.rowCount() < 10):
            self.savedGroupsTableWidget.setRowCount(10)
        self.savedGroupsTableWidget.setObjectName(u"savedGroupsTableWidget")
        self.savedGroupsTableWidget.setGeometry(QRect(30, 120, 351, 331))
        self.savedGroupsTableWidget.setFont(font2)
        self.savedGroupsTableWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.savedGroupsTableWidget.setRowCount(10)
        self.savedGroupsTableWidget.setColumnCount(2)
        self.savedGroupsLabel = QLabel(self.groupsTab)
        self.savedGroupsLabel.setObjectName(u"savedGroupsLabel")
        self.savedGroupsLabel.setGeometry(QRect(30, 100, 101, 16))
        self.layoutWidget3 = QWidget(self.groupsTab)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(120, 20, 169, 60))
        self.verticalLayout = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupNameLineEdit = QLineEdit(self.layoutWidget3)
        self.groupNameLineEdit.setObjectName(u"groupNameLineEdit")
        self.groupNameLineEdit.setFont(font2)

        self.verticalLayout.addWidget(self.groupNameLineEdit)

        self.responsiblePLineEdit = QLineEdit(self.layoutWidget3)
        self.responsiblePLineEdit.setObjectName(u"responsiblePLineEdit")
        self.responsiblePLineEdit.setFont(font2)

        self.verticalLayout.addWidget(self.responsiblePLineEdit)

        self.layoutWidget4 = QWidget(self.groupsTab)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(30, 20, 84, 51))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupNameLabel = QLabel(self.layoutWidget4)
        self.groupNameLabel.setObjectName(u"groupNameLabel")
        self.groupNameLabel.setFont(font)

        self.verticalLayout_2.addWidget(self.groupNameLabel)

        self.responsiblePLabel_2 = QLabel(self.layoutWidget4)
        self.responsiblePLabel_2.setObjectName(u"responsiblePLabel_2")
        self.responsiblePLabel_2.setFont(font)

        self.verticalLayout_2.addWidget(self.responsiblePLabel_2)

        self.deleteGroupPushButton = QPushButton(self.groupsTab)
        self.deleteGroupPushButton.setObjectName(u"deleteGroupPushButton")
        self.deleteGroupPushButton.setGeometry(QRect(300, 30, 81, 21))
        self.deleteGroupPushButton.setFont(font1)
        self.deleteGroupPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.deleteGroupPushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"background-color: rgb(255, 1, 5);")
        self.tabWidget.addTab(self.groupsTab, "")
        self.reportsTab = QWidget()
        self.reportsTab.setObjectName(u"reportsTab")
        self.reportsTab.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.reportTypecomboBox = QComboBox(self.reportsTab)
        self.reportTypecomboBox.setObjectName(u"reportTypecomboBox")
        self.reportTypecomboBox.setGeometry(QRect(20, 30, 231, 22))
        self.reportTypecomboBox.setFont(font2)
        self.reportTypeLabel = QLabel(self.reportsTab)
        self.reportTypeLabel.setObjectName(u"reportTypeLabel")
        self.reportTypeLabel.setGeometry(QRect(20, 10, 47, 13))
        self.reportTypeLabel.setFont(font)
        self.beginingDateEdit = QDateEdit(self.reportsTab)
        self.beginingDateEdit.setObjectName(u"beginingDateEdit")
        self.beginingDateEdit.setGeometry(QRect(20, 80, 110, 22))
        self.beginingDateEdit.setFont(font2)
        self.beginingDateEdit.setCalendarPopup(True)
        self.beginingDateEdit.setDate(QDate(2025, 1, 1))
        self.beginingLabel = QLabel(self.reportsTab)
        self.beginingLabel.setObjectName(u"beginingLabel")
        self.beginingLabel.setGeometry(QRect(20, 60, 47, 13))
        self.beginingLabel.setFont(font)
        self.endingLabel = QLabel(self.reportsTab)
        self.endingLabel.setObjectName(u"endingLabel")
        self.endingLabel.setGeometry(QRect(140, 60, 47, 13))
        self.endingLabel.setFont(font)
        self.endingDateEdit = QDateEdit(self.reportsTab)
        self.endingDateEdit.setObjectName(u"endingDateEdit")
        self.endingDateEdit.setGeometry(QRect(140, 80, 110, 22))
        self.endingDateEdit.setFont(font2)
        self.endingDateEdit.setCalendarPopup(True)
        self.endingDateEdit.setDate(QDate(2025, 1, 1))
        self.printReportPushButton = QPushButton(self.reportsTab)
        self.printReportPushButton.setObjectName(u"printReportPushButton")
        self.printReportPushButton.setGeometry(QRect(260, 80, 61, 23))
        self.printReportPushButton.setFont(font1)
        self.printReportPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.printReportPushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"color: rgb(255, 255, 255);")
        self.diaryTableWidget = QTableWidget(self.reportsTab)
        if (self.diaryTableWidget.columnCount() < 8):
            self.diaryTableWidget.setColumnCount(8)
        if (self.diaryTableWidget.rowCount() < 10000):
            self.diaryTableWidget.setRowCount(10000)
        self.diaryTableWidget.setObjectName(u"diaryTableWidget")
        self.diaryTableWidget.setGeometry(QRect(20, 160, 861, 321))
        self.diaryTableWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ForbiddenCursor))
        self.diaryTableWidget.setRowCount(10000)
        self.diaryTableWidget.setColumnCount(8)
        self.previewLabel = QLabel(self.reportsTab)
        self.previewLabel.setObjectName(u"previewLabel")
        self.previewLabel.setGeometry(QRect(20, 140, 61, 16))
        self.tabWidget.addTab(self.reportsTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1107, 33))
        self.menuAsetukset = QMenu(self.menubar)
        self.menuAsetukset.setObjectName(u"menuAsetukset")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAsetukset.menuAction())
        self.menuAsetukset.addAction(self.actionMuokkaa)
        self.menuAsetukset.addAction(self.actionTietoja_ohjelmasta)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionMuokkaa.setText(QCoreApplication.translate("MainWindow", u"Muokkaa...", None))
        self.actionTietoja_ohjelmasta.setText(QCoreApplication.translate("MainWindow", u"Tietoja ohjelmasta...", None))
        self.registeredPersonsLabel.setText(QCoreApplication.translate("MainWindow", u"Rekister\u00f6idyt lainaajat", None))
        self.savePersonPushButton.setText(QCoreApplication.translate("MainWindow", u"Tallenna", None))
        self.groupComboBox.setCurrentText("")
        self.ssnLabel.setText(QCoreApplication.translate("MainWindow", u"Henkil\u00f6tunnus", None))
        self.firstNameLabel.setText(QCoreApplication.translate("MainWindow", u"Etunimi", None))
        self.lastNameLabel.setText(QCoreApplication.translate("MainWindow", u"Sukunimi", None))
        self.groupLabel.setText(QCoreApplication.translate("MainWindow", u"Ryhm\u00e4", None))
        self.vehicleClassLabel.setText(QCoreApplication.translate("MainWindow", u"Ajokorttiluokka", None))
        self.emailLabel.setText(QCoreApplication.translate("MainWindow", u"S\u00e4hk\u00f6posti", None))
        self.deletePersonPushButton.setText(QCoreApplication.translate("MainWindow", u"Poista", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lenderTab), QCoreApplication.translate("MainWindow", u"Lainaajat", None))
        self.numberPlateLabel.setText(QCoreApplication.translate("MainWindow", u"Rekisterinumero", None))
        self.manufacturerLabel.setText(QCoreApplication.translate("MainWindow", u"Merkki", None))
        self.modelLabel.setText(QCoreApplication.translate("MainWindow", u"Malli", None))
        self.modelYearLabel.setText(QCoreApplication.translate("MainWindow", u"Vuosimalli", None))
        self.capacityLabel.setText(QCoreApplication.translate("MainWindow", u"Henkil\u00f6m\u00e4\u00e4r\u00e4", None))
        self.vehicleTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Ajoneuvotyyppi", None))
        self.vehicleOwnerLabol.setText(QCoreApplication.translate("MainWindow", u"Vastuuhenkil\u00f6", None))
        self.saveVehiclePushButton.setText(QCoreApplication.translate("MainWindow", u"Tallenna", None))
        self.printBarcodePushButton.setText(QCoreApplication.translate("MainWindow", u"Viivakoodi", None))
        self.vehicleListLabel.setText(QCoreApplication.translate("MainWindow", u"Autoluettelo", None))
        self.openPicturesPushButton.setText("")
        self.carPhotoLabel.setText("")
        self.removeVehiclePushButton.setText(QCoreApplication.translate("MainWindow", u"Poista", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vehicleTab), QCoreApplication.translate("MainWindow", u"Autot", None))
        self.saveGroupPushButton.setText(QCoreApplication.translate("MainWindow", u"Tallenna", None))
        self.savedGroupsLabel.setText(QCoreApplication.translate("MainWindow", u"Tallennetut ryhm\u00e4t", None))
        self.groupNameLabel.setText(QCoreApplication.translate("MainWindow", u"Ryhm\u00e4n nimi", None))
        self.responsiblePLabel_2.setText(QCoreApplication.translate("MainWindow", u"Vastuuhenkil\u00f6", None))
        self.deleteGroupPushButton.setText(QCoreApplication.translate("MainWindow", u"Poista", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.groupsTab), QCoreApplication.translate("MainWindow", u"Ryhm\u00e4t", None))
        self.reportTypecomboBox.setCurrentText("")
        self.reportTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Raportti", None))
        self.beginingLabel.setText(QCoreApplication.translate("MainWindow", u"Alkaa", None))
        self.endingLabel.setText(QCoreApplication.translate("MainWindow", u"P\u00e4\u00e4ttyy", None))
        self.printReportPushButton.setText(QCoreApplication.translate("MainWindow", u"Tulosta", None))
        self.previewLabel.setText(QCoreApplication.translate("MainWindow", u"Esikatselu", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reportsTab), QCoreApplication.translate("MainWindow", u"Raportit", None))
        self.menuAsetukset.setTitle(QCoreApplication.translate("MainWindow", u"Asetukset", None))
    # retranslateUi

