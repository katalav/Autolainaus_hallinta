# HALLINTASOVELLUKSEN PÄÄIKKUNAN JA DIALOGIEN KOODI
# =================================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------

# Pythonin sisäiset moduulit
import os # Polkumääritykset
import sys # Käynnistysargumentit
import json # JSON-objektien ja tiedostojen käsittely

# Asennuksen vaativat kirjastot

from PySide6 import QtWidgets # Qt-vimpaimet
from PySide6 import QtGui # Pixmap- muunnoksia varten
from PySide6.QtCore import QDate


# Käyttöliittymämoduulien lataukset
from administrative_ui import Ui_MainWindow # Käännetyn käyttöliittymän luokka
from settingsDialog_ui import Ui_Dialog as Settings_Dialog# Asetukset-dialogin luokka
from aboutDialog_ui import Ui_Dialog as About_Dialog


# Omat moduulit
from lendingModules import dbOperations # PostgreSQL-tietokantayhteydet
from lendingModules import cipher # Salakirjoitusmoduuli
from lendingModules import barcode # viivakoodin muodostin


# LUOKKAMÄÄRITYKSET
# -----------------

# Määritellään pääikkunan luokka, joka perii QMainWindow- ja Ui_MainWindow-luokan
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """A class for creating main window for the application"""
    
    # Määritellään olionmuodostin ja kutsutaan yliluokkien muodostimia
    def __init__(self):
        super().__init__()

        # Luodaan käyttöliittymä konvertoidun tiedoston perusteella MainWindow:n ui-ominaisuudeksi. Tämä suojaa lopun MainWindow-olion ylikirjoitukselta, kun ui-tiedostoa päivitetään
        self.ui = Ui_MainWindow()

        # Kutsutaan käyttöliittymän muodostusmetodia setupUi
        self.ui.setupUi(self)

        # Rutiini, joka lukee asetukset, jos ne ovat olemassa
        try:
            # Avataam asetustiedosto ja muutetaan se Python sanakirjaksi
            with open('settings.json', 'rt') as settingsFile: # With sulkee tiedoston automaattisesti
                
                jsonData = settingsFile.read()
                self.currentSettings = json.loads(jsonData)
            
            # Puretaan salasana tietokantaoperaatioita varten  
            self.plainTextPassword = cipher.decryptString(self.currentSettings['password'])
            
            # Huom! Salasana pitää tallentaa JSON-tiedostoon tavallisena merkkijonona,
            # ei byte string muodossa. Salauskirjaston decode ja encode metodit hoitavat asian
            
            # Päivitetään käyttöliittymäelementtien tiedot tietokannasta
            self.refreshUi()
            
            
        except Exception as e:
            self.openSettingsDialog()
        
        # Asetetaan auton oletuskuvaksi harmaa kamera
        self.vehiclePicture = 'uiPictures\\noPicture.png'
        
        # Poistettavan auton rekisterinumero
        self.vehicleToDelete = ''
        self.personToDelete = ''
        
        # Kuluvan päivän ja vuoden määritys
        # TODO : Tee slotti, joka päivittää -> getDates()
        # TODO : Tee sille singnaali kun valitaan Raportit-välilehti
        self.today = QDate.currentDate()
        self.currentYear = str(self.today.toPython())[0:4]
        self.firstDayOfYear = QDate(int(self.currentYear), 1, 1)


        # OHJELMOIDUT SIGNAALIT
        # ---------------------
        
        # Valikkotoiminnot
        self.ui.actionMuokkaa.triggered.connect(self.openSettingsDialog)
        self.ui.actionTietoja_ohjelmasta.triggered.connect(self.openAboutDialog)

        # Välilehtien vaihdon käynnistämät signaalit

        # Kun välilehteä vaihdetaan, päivitetään yhdistelmäruutujen valinnat
        self.ui.tabWidget.currentChanged.connect(self.updateChoices)

        # Painikkeet
        self.ui.savePersonPushButton.clicked.connect(self.savePerson)
        self.ui.saveVehiclePushButton.clicked.connect(self.saveVehicle)
        self.ui.openPicturesPushButton.clicked.connect(self.openPicture)
        self.ui.removeVehiclePushButton.clicked.connect(self.deleteVehicle)
        self.ui.deletePersonPushButton.clicked.connect(self.deletePerson)
        self.ui.getReportPushButton.clicked.connect(self.updateDiaryTableWidget) # Ajopäiväkirjojen haku
        
        # Taulukoiden soluvalinnat
        self.ui.vehicleCatalogTableWidget.cellClicked.connect(self.setRegisterNumber)
        self.ui.registeredPersonsTableWidget.cellClicked.connect(self.setSSN)

        
   
   
    # OHJELMOIDUT SLOTIT
    # ==================

    # DIALOGIEN AVAUSMETODIT
    # ----------------------

    # Valikkotoimintojen slotit
    # -------------------------

    # Asetusdialogin avaus
    def openSettingsDialog(self):
        self.saveSettingsDialog = SaveSettingsDialog() # Luodaan luokasta olio
        self.saveSettingsDialog.setWindowTitle('Palvelinasetukset')
        self.saveSettingsDialog.exec() # Luodaan dialogille oma event loop
        
    # Tietoja ohjelmasta -dialogin avaus
    def openAboutDialog(self):
        self.aboutDialog = AboutDialog()
        self.aboutDialog.setWindowTitle('Tietoja ohjelmasta')
        self.aboutDialog.exec() # Luodaan dialogille event loop

    # Yleinen käyttöliittymän verestys (refresh)
    def refreshUi(self):
        
        # Auton kuvaksi kameran kuva
        self.vehiclePicture = 'uiPictures\\noPicture.png' # Kuvan poluksi ei kuvaa symboli
        self.ui.carPhotoLabel.setPixmap(QtGui.QPixmap(self.vehiclePicture)) # auton kuvan päivitys
        self.updateChoices() # Ryhmän valinta -yhdistelmäruudun arvot
        self.updateLenderTableWidget() # Lainaajien tiedot
        self.updateVehicleTableWidget() # Autojen tiedot
        self.ui.diaryTableWidget.clear() # Tyhjentää raporttisivun taulukon
        self.ui.removeVehiclePushButton.setEnabled(False) # Otetaan auton-poisto painike pois käytöstä
        self.ui.deletePersonPushButton.setEnabled(False) # Otetaan käyttäjän poisto-painike pois käytöstä
        
    # Välilehtien slotit
    # ------------------
    # Ryhmän valinta ja ajoneuvotyyppi ruutujen arvojen päivitys
    def updateChoices(self):
        
        # Päivitetään kuluva päivämäärä ja vuoden ensimmäinen päivä
        self.today = QDate.currentDate()
        self.currentYear = str(self.today.toPython())[0:4]
        self.firstDayOfYear = QDate(int(self.currentYear), 1, 1)


        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Tehdään lista ajoneuvotyypit-yhdistelmäruudun arvoista
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista ajoneuvotyyppi-yhdistelmäruudun arvoista
        typeList = dbConnection.readColumsFromTable('ajoneuvotyyppi', ['tyyppi'])
        typeStringList = []
        for item in typeList:
            stringValue = str(item[0])
            typeStringList.append(stringValue)
        
        self.ui.vehicleTypecomboBox.clear()
        self.ui.vehicleTypecomboBox.addItems(typeStringList)
        
        # Lista ajopäiväkirjoista -> reporttinäkymien nimet
        self.ui.reportTypecomboBox.clear()
        self.ui.reportTypecomboBox.addItems(['ajopaivakirja', 'autoittain'])
        
        #Raporttivälin päivämäärävalitsinten oletuspäivien asetus
        self.ui.beginingDateEdit.setDate(self.firstDayOfYear)
        self.ui.endingDateEdit.setDate(self.today)
        
    # Lainaajat-taulukon päivitys
    def updateLenderTableWidget(self):
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('lainaaja')
        

        #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.registeredPersonsTableWidget.clearContents()
        
        # Määritellään taulukkoelementin otsikot
        headerRow = ['Henkilötunnus', 'Etunimi', 'Sukunimi', 'Ajokorttiluokka', 'Automaatti', 'sähköposti']
        self.ui.registeredPersonsTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.registeredPersonsTableWidget.setItem(row, column, data)


    # Autot-taulukon päivitys
    def updateVehicleTableWidget(self):
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('auto')
        
        #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.vehicleCatalogTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Rekisteri', 'Merkki', 'Malli', 'Vuosimalli', 'Henkilömäärä', 'Tyyppi', 'Automaatti', 'Vastuuhenkilö']
        self.ui.vehicleCatalogTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.vehicleCatalogTableWidget.setItem(row, column, data)


    # Päivitetään ajopäiväkirjan taulukko
    def updateDiaryTableWidget(self):
         # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luetaan raportti-sivun kontrollit paikallisiin muuttujiin
        reportName = self.ui.reportTypecomboBox.currentText()
        dateStart = self.ui.beginingDateEdit.date().toPython()
        dateEnd = self.ui.endingDateEdit.date().toPython()
        userFilter = self.ui.ssnFilterLineEdit.text()
        registerFilter = self.ui.registerFilterLineEdit.text()
        sqlFilter = ''

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Määritellään aikaväli, jolta raportti tulostetaan
        dateFilterSring = f"otto >= '{dateStart} 00:00:00+2' AND otto <= '{dateEnd} 23:59:59+2'"

        if userFilter == '':
            userFilterString = ''
        else:
            userFilterString = f"AND hetu = '{userFilter}'"
            
        if registerFilter == '':
            registerFilterString = ''
        else:
            registerFilterString = f"AND rekisterinumero = '{registerFilter}'"

        sqlFilter = dateFilterSring + userFilterString + registerFilterString
        print(sqlFilter)
        tableData = dbConnection.filterColumsFromTable(reportName,['*'], sqlFilter)
        
        # Tyhjennetään vanhat tiedot käyttöliittymästä ennen uusien lukemista tietokannasta
        self.ui.diaryTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Rekisteri', 'Merkki', 'Malli', 'HeTu', 'Sukunimi', 'Etunimi', 'Otettu', 'Palautettu']
        self.ui.diaryTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.diaryTableWidget.setItem(row, column, data)
    
 
 
    # Painikkeiden slotit
    # -----------------

    # Lainaajien tallennus
    def savePerson(self):
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        

        # Määritellään tallennusmetodin vaatimat parametrit
        tableName = 'lainaaja'
        ssn = self.ui.ssnLineEdit.text()
        email = self.ui.emailLineEdit.text()
        firstName = self.ui.firstNameLineEdit.text()
        lastName = self.ui.lastNameLineEdit.text()
        licenseType = self.ui.vehicleClassLineEdit.text()
        automaticGB = self.ui.agbRestrictionCheckBox.isChecked()
        lenderDictionary = {'hetu': ssn,
                          'etunimi': firstName,
                          'sukunimi': lastName,
                          'ajokorttiluokka': licenseType,
                          'automaatti': automaticGB,
                          'sahkoposti': email
                          }
        
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.addToTable(tableName, lenderDictionary)
            self.updateLenderTableWidget()
        except Exception as e:
            self.openWarning('Tallennus ei onnistunut', str(e)) 
    
    # Ajoneuvojen kuvan lataaminen
    def openPicture(self):
        userPath = os.path.expanduser('~')
        pathToPictureFolder = userPath + '\\Pictures'
        fileName, check =QtWidgets.QFileDialog.getOpenFileName(None, 'Valitse auton kuva', pathToPictureFolder, 'Kuvat (*.png *.jpg)')
        
        # Jos kuvatiedosto on valittu
        if fileName:
            self.vehiclePicture = fileName
            
        vehiclePixmap = QtGui.QPixmap(self.vehiclePicture)
        self.ui.carPhotoLabel.setPixmap(vehiclePixmap)
        
        
    # Ajoneuvon tallennus
    def saveVehicle(self):
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        
        # Luetaan syöttöelementtien arvot paikallisiin muuttujiin
        numberPlate = self.ui.numberPlateLineEdit.text()
        manufacturer = self.ui.manufacturerLineEdit.text()
        model = self.ui.modelLineEdit.text()
        year = self.ui.modelYearLineEdit.text()
        capacity = int(self.ui.capacityLineEdit.text())
        vehicleType = self.ui.vehicleTypecomboBox.currentText()
        automaticGearBox = self.ui.agbCheckBox.isChecked()
        responsiblePerson = self.ui.vehicleOwnerLineEdit.text()
        
        # Määritellään tallennusmetodin vaatimat parametrit
        tableName = 'auto'
        vehicleDictionary = {'rekisterinumero': numberPlate,
                          'merkki': manufacturer,
                          'malli': model,
                          'vuosimalli': year,
                          'henkilomaara': capacity,
                          'tyyppi': vehicleType,
                          'automaatti' : automaticGearBox,
                          'vastuuhenkilo': responsiblePerson
                          }
        
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.addToTable(tableName, vehicleDictionary)
            
        except Exception as e:
            self.openWarning('Tallennus ei onnistunut', str(e))
            
        # Luodaan kuvatiedosto ja päivitetään auto- taulua
        with open(self.vehiclePicture, 'rb') as pictureFile:
            pictureData = pictureFile.read()
            
        # Luodaan uusi yhteys, koska edellinen suljettiin
        dbConnection2 = dbOperations.DbConnection(dbSettings)
        
        try:     
            dbConnection2.updateBinaryField('auto', 'kuva', 'rekisterinumero', f"'{numberPlate}'", pictureData)
            self.refreshUi()
            

        except Exception as e: 
            self.openWarning('Kuvan päivitys ei onnistunut', str(e))
            
    def deleteVehicle(self):

         # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        
         # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.deleteRowsFromTable('auto', 'rekisterinumero', f"'{self.vehicleToDelete}'")
            self.refreshUi()
        except Exception as e:
            self.openWarning('Poisto ei onnistunut', str(e)) 
            
        
    def deletePerson(self):

         # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
         # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.deleteRowsFromTable('lainaaja', 'hetu', f"'{self.personToDelete}'")
            self.refreshUi()
        except Exception as e:
            self.openWarning('Poisto ei onnistunut', str(e)) 


            
    # Taulukoiden soluvalinnat
    #-------------------------
    

    
    # Asetetaan poistettavan henkilön HeTu valitun rivin perusteella
    def setRegisterNumber(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''
        
        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.vehicleCatalogTableWidget.currentRow()
        cellValue = self.ui.vehicleCatalogTableWidget.item(rowIndex, columnIndex).text()
        self.vehicleToDelete = cellValue
        self.ui.statusbar.showMessage(f'valitun auton rekisterinumero on {cellValue}')
        self.ui.removeVehiclePushButton.setEnabled(True)
        
    def setSSN(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''
        
        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.registeredPersonsTableWidget.currentRow()
        cellValue = self.ui.registeredPersonsTableWidget.item(rowIndex, columnIndex).text()
        self.personToDelete = cellValue
        self.ui.statusbar.showMessage(f'valitun käyttäjän henkilötunnus on {cellValue}')
        self.ui.deletePersonPushButton.setEnabled(True)
        
 

    # Virheilmoitukset ja muut Message Box -dialogit
    # ----------------------------------------------

    # Malli mahdollista virheilmoitusta varten
    def openWarning(self, title: str, text:str) -> None: 
        """Opens a message box for errors

        Args:
            title (str): The title of the message box
            text (str): Error message
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setWindowTitle(title)
        msgBox.setText('Tapahtui vakava virhe')
        msgBox.setDetailedText(text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

# Asetusten tallennusikkunan luokka
# ---------------------------------
class SaveSettingsDialog(QtWidgets.QDialog, Settings_Dialog):
    """A class to open settings dialog window"""
    
    # Määritellään olionmuodostin ja kutsutaan yliluokkien muodostimia
    def __init__(self):
        super().__init__()

        # Luodaan käyttöliittymä konvertoidun tiedoston perusteella MainWindow:n ui-ominaisuudeksi. Tämä suojaa lopun MainWindow-olion ylikirjoitukselta, kun ui-tiedostoa päivitetään
        self.ui = Settings_Dialog()

        # Kutsutaan käyttöliittymän muodostusmetodia setupUi
        self.ui.setupUi(self)
        
        # Luetaan asetustiedosto Python-sanakirjaksi
        self.currentSettings = {}

        # Tarkistetaan ensin, että asetustiedosto on olemassa

        try:
            with open('settings.json', 'rt') as settingsFile:
                jsonData = settingsFile.read()
                self.currentSettings = json.loads(jsonData)

            self.ui.serverLineEdit.setText(self.currentSettings['server'])
            self.ui.portLineEdit.setText(self.currentSettings['port'])
            self.ui.databaseLineEdit.setText(self.currentSettings['database'])
            self.ui.userLineEdit.setText(self.currentSettings['userName'])
            plaintextPassword = cipher.decryptString(self.currentSettings['password'])
            self.ui.paswordLineEdit.setText(plaintextPassword)
        except Exception as e:
            self.openInfo()
        

        # OHJELMOIDUT SIGNAALIT
        # ---------------------

        # Kun Tallenna-painiketta on klikattu, kutsutaan saveToJsonFile-metodia
        self.ui.saveSettingspushButton.clicked.connect(self.saveToJsonFile)

        # Suljepainikkeen toiminnot
        self.ui.closePushButton.clicked.connect(self.closeSettingsDialog)
        
        # OHJELMOIDUT SLOTIT (Luokan metodit)
    # -----------------------------------

    # Tallennetaan käyttöliittymään syötetyt asetukset tiedostoon
    def saveToJsonFile(self):

        # Luetaan käyttöliittymästä tiedot paikallisiin muuttujiin
        server = self.ui.serverLineEdit.text()
        port = self.ui.portLineEdit.text()
        database = self.ui.databaseLineEdit.text()
        userName = self.ui.userLineEdit.text()

        # Muutetaan merkkijono tavumuotoon (byte, merkistö UTF-8)
        plainTextPassword = self.ui.paswordLineEdit.text()
       
        # Salataan ja muunnetaan tavalliseksi merkkijonoksi, jotta JSON-tallennus onnistuu
        encryptedPassword = cipher.encryptString(plainTextPassword)

        # Muodostetaan muuttujista Python-sanakirja
        settingsDictionary = {
            'server': server,
            'port': port,
            'database': database,
            'userName': userName,
            'password': encryptedPassword
        }

        # Muunnetaan sanakirja JSON-muotoon

        jsonData = json.dumps(settingsDictionary)
        
        # Avataan asetustiedosto ja kirjoitetaan asetukset
        with open('settings.json', 'wt') as settingsFile:
            settingsFile.write(jsonData)

        # Suljetaan dialogin ikkuna
        self.close()

    def closeSettingsDialog(self):
        self.close()

    # Avataan MessageBox, jossa kerrotaan että tehdää uusi asetustiedosto
    def openInfo(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle('Luodaan uusi asetustiedosto')
        msgBox.setText('Syötä kaikkien kenttien tiedot ja käynnistä sovellus uudelleen!')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec() # Luodaan Msg Box:lle oma event loop

# Tietoja ohjelmasta ikkunan luokka
# ---------------------------------
class AboutDialog(QtWidgets.QDialog, About_Dialog):
    """A class to show About dialog."""
    def __init__(self):
        super().__init__()

        # Luodaan käyttöliittymä konvertoidun tiedoston perusteella MainWindow:n ui-ominaisuudeksi. Tämä suojaa lopun MainWindow-olion ylikirjoitukselta, kun ui-tiedostoa päivitetään
        self.ui =About_Dialog()

        # Kutsutaan käyttöliittymän muodostusmetodia setupUi
        self.ui.setupUi(self)
    


if __name__ == "__main__":
    
    # Luodaan sovellus ja asetetaan tyyliksi Fusion
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    # Luodaan objekti pääikkunalle ja tehdään siitä näkyvä
    window = MainWindow()
    window.setWindowTitle('Autolainauksen hallinta')
    window.show()

    # Käynnistetään sovellus ja tapahtumienkäsittelijä
    app.exec()

    