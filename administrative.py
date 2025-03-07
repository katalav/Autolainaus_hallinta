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
        self.vehicleToDelete = ''
        self.personToDelete = ''
        self.groupToDelete = ''

        # OHJELMOIDUT SIGNAALIT
        # ---------------------
        
        # Valikkotoiminnot
        self.ui.actionMuokkaa.triggered.connect(self.openSettingsDialog)
        self.ui.actionTietoja_ohjelmasta.triggered.connect(self.openAboutDialog)

        # Välilehtien vaihdon käynnistämät signaalit

        # Kun välilehteä vaihdetaan, päivitetään yhdistelmäruutujen valinnat
        self.ui.tabWidget.currentChanged.connect(self.updateCombos)

        # Painikkeet
        self.ui.saveGroupPushButton.clicked.connect(self.saveGroup)
        self.ui.savePersonPushButton.clicked.connect(self.savePerson)
        self.ui.saveVehiclePushButton.clicked.connect(self.saveVehicle)
        self.ui.openPicturesPushButton.clicked.connect(self.openPicture)
        self.ui.removeVehiclePushButton.clicked.connect(self.deleteVehicle)
        self.ui.deletePersonPushButton.clicked.connect(self.deletePerson)
        self.ui.deleteGroupPushButton.clicked.connect(self.deleteGroup)
        
        # Taulukoiden soluvalinnat
        self.ui.vehicleCatalogTableWidget.cellClicked.connect(self.setRegisterNumber)
        self.ui.registeredPersonsTableWidget.cellClicked.connect(self.setSSN)
        self.ui.savedGroupsTableWidget.cellClicked.connect(self.setGroup)
        
   
   
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
        self.updateCombos() # Ryhmän valinta -yhdistelmäruudun arvot
        self.updateLenderTableWidget() # Lainaajien tiedot
        self.updateVehicleTableWidget() # Autojen tiedot
        self.updateGroupTableWidget() # Ryhmien tiedot
        self.updateDiaryTableWidget() # Ajopäiväkirja
        self.ui.removeVehiclePushButton.setEnabled(False) # Otetaan auton-poisto painike pois käytöstä
        self.ui.deletePersonPushButton.setEnabled(False) # Otetaan lainaajan poisto-painike pois käytöstä
        self.ui.deleteGroupPushButton.setEnabled(False) # Otetaan ryhmän poisto-painike pois käytöstä
        
    # Välilehtien slotit
    # ------------------
    # Ryhmän valinta ja ajoneuvotyyppi ruutujen arvojen päivitys
    def updateCombos(self):

        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista ryhmät-yhdistelmäruudun arvoista
        groupList = dbConnection.readColumsFromTable('ryhma',['ryhma'])
        groupStringList = []
        for item in groupList:
            stringValue = str(item[0])
            groupStringList.append(stringValue)
        
        self.ui.groupComboBox.clear()
        self.ui.groupComboBox.addItems(groupStringList)
        
        # Tehdään lista ajoneuvotyypit-yhdistelmäruudun arvoista

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista ryhmät-yhdistelmäruudun arvoista
        typeList = dbConnection.readColumsFromTable('ajoneuvotyyppi', ['tyyppi'])

        
        typeStringList = []
        for item in typeList:
            stringValue = str(item[0])
            typeStringList.append(stringValue)
        
        self.ui.vehicleTypecomboBox.clear()
        self.ui.vehicleTypecomboBox.addItems(typeStringList)
        
        # Lista ajopäiväkirjoista -> reporttinäkymien nimet
        self.ui.reportTypecomboBox.addItem('Ajopäiväkirja -kaikki')
        
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
        headerRow = ['Henkilötunnus', 'Etunimi', 'Sukunimi', 'Ryhmä', 'Ajokortti', 'sähköposti']
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
        headerRow = ['Rekisteri', 'Merkki', 'Malli', 'Vuosimalli', 'Henkilömäärä', 'Vastuuhenkilö', 'Tyyppi']
        self.ui.vehicleCatalogTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.vehicleCatalogTableWidget.setItem(row, column, data)


    # Ryhmät-taulukon päivitys
    def updateGroupTableWidget(self):
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('ryhma')
        
        #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.savedGroupsTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Ryhmä', 'Vastuuhenkilö']
        self.ui.savedGroupsTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.savedGroupsTableWidget.setItem(row, column, data)

    
    # Päivitetään ajopäiväkirjan taulukko
    def updateDiaryTableWidget(self):
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('ajopaivakirja')
        
        #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.diaryTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Rekisteri', 'Merkki', 'HeTu', 'Sukunimi', 'Etunimi','Ryhmä', 'Otettu', 'Palautettu']
        self.ui.diaryTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.diaryTableWidget.setItem(row, column, data)
    # Painikkeiden slotit
    # -----------------

    # Ryhmän tallennus
    def saveGroup(self):
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaihdetaan salasana selväkieliseksi
        
        

        # Määritellään tallennusmetodin vaatimat parametrit
        tableName = 'ryhma'
        group = self.ui.groupNameLineEdit.text()
        responsiblePerson = self.ui.responsiblePLineEdit.text()
        groupDictionary = {'ryhma': group,
                          'vastuuhenkilo': responsiblePerson }
        
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.addToTable(tableName, groupDictionary)
            self.updateGroupTableWidget()
        except Exception as e:

            self.openWarning('Tallennus ei onnistunut', str(e))

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
        group = self.ui.groupComboBox.currentText()
        licenseType = self.ui.vehicleClassLineEdit.text()
        lenderDictionary = {'hetu': ssn,
                          'sahkoposti': email,
                          'etunimi': firstName,
                          'sukunimi': lastName,
                          'ryhma': group,
                          'ajokorttiluokka': licenseType }
        
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
        numberPlate = self.ui.numberPlateLineEdit.text()
        manufacturer = self.ui.manufacturerLineEdit.text()
        model = self.ui.modelLineEdit.text()
        year = self.ui.modelYearLineEdit.text()
        capacity = int(self.ui.capacityLineEdit.text())
        vehicleType = self.ui.vehicleTypecomboBox.currentText()
        responsiblePerson = self.ui.vehicleOwnerLineEdit.text()
        
        # Määritellään tallennusmetodin vaatimat parametrit
        tableName = 'auto'
        
        vehicleDictionary = {'rekisterinumero': numberPlate,
                          'merkki': manufacturer,
                          'malli': model,
                          'vuosimalli': year,
                          'henkilomaara': capacity,
                          'tyyppi': vehicleType,
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
            
            # Tätä voisi muokata siten, että tallennetaan tietokanta pixmap
            #jollin user.py:ssä voitaisiin suoraan päivittää auton kuva 
            #tallentamatta sitä ensin levylle.
            
        # Luodaan uusi yhteys, koska edellinen suljettiin
        dbConnection2 = dbOperations.DbConnection(dbSettings)
        
        try:     
            dbConnection2.updateBinaryField('auto','kuva', 'rekisterinumero', f"'{numberPlate}'", pictureData)
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


    def deleteGroup(self):

         # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
         # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.deleteRowsFromTable('ryhma', 'ryhma', f"'{self.groupToDelete}'")
            self.refreshUi()
        except Exception as e:
            self.openWarning('Poisto ei onnistunut', str(e)) 
            
    # Taulukoiden soluvalinnat
    #-------------------------
    
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
        
    def setGroup(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''
        
        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.savedGroupsTableWidget.currentRow()
        cellValue = self.ui.savedGroupsTableWidget.item(rowIndex, columnIndex).text()
        self.groupToDelete = cellValue
        self.ui.statusbar.showMessage(f'valitun ryhmän nimi on {cellValue}')
        self.ui.deleteGroupPushButton.setEnabled(True)
    

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
        msgBox.setText('Syötä kaikkien kenttien tiedot!')
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

    