# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(301, 234)
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        Dialog.setWindowIcon(icon)
        self.saveSettingspushButton = QPushButton(Dialog)
        self.saveSettingspushButton.setObjectName(u"saveSettingspushButton")
        self.saveSettingspushButton.setGeometry(QRect(210, 180, 81, 23))
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.saveSettingspushButton.setFont(font)
        self.saveSettingspushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveSettingspushButton.setStyleSheet(u"background-color: rgb(57, 136, 220);\n"
"color: rgb(255, 255, 255);")
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(110, 10, 181, 156))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.serverLineEdit = QLineEdit(self.layoutWidget)
        self.serverLineEdit.setObjectName(u"serverLineEdit")
        font1 = QFont()
        font1.setPointSize(11)
        self.serverLineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.serverLineEdit)

        self.portLineEdit = QLineEdit(self.layoutWidget)
        self.portLineEdit.setObjectName(u"portLineEdit")
        self.portLineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.portLineEdit)

        self.databaseLineEdit = QLineEdit(self.layoutWidget)
        self.databaseLineEdit.setObjectName(u"databaseLineEdit")
        self.databaseLineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.databaseLineEdit)

        self.userLineEdit = QLineEdit(self.layoutWidget)
        self.userLineEdit.setObjectName(u"userLineEdit")
        self.userLineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.userLineEdit)

        self.paswordLineEdit = QLineEdit(self.layoutWidget)
        self.paswordLineEdit.setObjectName(u"paswordLineEdit")
        self.paswordLineEdit.setFont(font1)
        self.paswordLineEdit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.verticalLayout.addWidget(self.paswordLineEdit)

        self.layoutWidget_2 = QWidget(Dialog)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 10, 86, 141))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ServerLabel = QLabel(self.layoutWidget_2)
        self.ServerLabel.setObjectName(u"ServerLabel")
        font2 = QFont()
        font2.setPointSize(10)
        self.ServerLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.ServerLabel)

        self.portLabel = QLabel(self.layoutWidget_2)
        self.portLabel.setObjectName(u"portLabel")
        self.portLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.portLabel)

        self.databaseLabel = QLabel(self.layoutWidget_2)
        self.databaseLabel.setObjectName(u"databaseLabel")
        self.databaseLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.databaseLabel)

        self.userLabel = QLabel(self.layoutWidget_2)
        self.userLabel.setObjectName(u"userLabel")
        self.userLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.userLabel)

        self.passwordLabel = QLabel(self.layoutWidget_2)
        self.passwordLabel.setObjectName(u"passwordLabel")
        self.passwordLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.passwordLabel)

        self.closePushButton = QPushButton(Dialog)
        self.closePushButton.setObjectName(u"closePushButton")
        self.closePushButton.setGeometry(QRect(110, 180, 75, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.saveSettingspushButton.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Tallentaa asetukset tiedostoon</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.saveSettingspushButton.setText(QCoreApplication.translate("Dialog", u"Tallenna", None))
#if QT_CONFIG(tooltip)
        self.serverLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Palvelimen nimi tai IP-osoite</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.portLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Palvelimen porttinumero</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.databaseLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Tietokannan nimi</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.userLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Sovelluksen k\u00e4ytt\u00e4j\u00e4tunnus</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.paswordLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Salasana</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ServerLabel.setText(QCoreApplication.translate("Dialog", u"Palvelin", None))
        self.portLabel.setText(QCoreApplication.translate("Dialog", u"Portti", None))
        self.databaseLabel.setText(QCoreApplication.translate("Dialog", u"Tietokanta", None))
        self.userLabel.setText(QCoreApplication.translate("Dialog", u"K\u00e4ytt\u00e4j\u00e4tunnus", None))
        self.passwordLabel.setText(QCoreApplication.translate("Dialog", u"Salasana", None))
        self.closePushButton.setText(QCoreApplication.translate("Dialog", u"Sulje", None))
    # retranslateUi

