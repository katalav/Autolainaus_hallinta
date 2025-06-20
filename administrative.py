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
from PySide6 import QtGui # Pixmap ja web sivujen näyttö
from PySide6.QtCore import QDate, QUrl # Päivämäärät ja URL-osoitteet


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
        
        # Poistettavan tietojen avaimmet
        self.vehicleToModify = ''
        self.personToDelete = ''
        self.vehicleTypeToModify = ''
        self.reasonToModify = ''
        
        # Kuluvan päivän ja vuoden määritys

        self.today = QDate.currentDate()
        self.currentYear = str(self.today.toPython())[0:4]
        self.firstDayOfYear = QDate(int(self.currentYear), 1, 1)


        # OHJELMOIDUT SIGNAALIT
        # ---------------------
        
        # Valikkotoiminnot
        self.ui.actionMuokkaa.triggered.connect(self.openSettingsDialog)
        self.ui.actionOhjesivut.triggered.connect(self.openWebHelp)
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
        self.ui.notLendablePushButton.clicked.connect(self.setNotLendable)
        self.ui.reasonAddPushButton.clicked.connect(self.newReason)
        self.ui.vehicleTypeAddPushButton.clicked.connect(self.newVehicleType)
        self.ui.reasonDeletePushButton.clicked.connect(self.deleteReason)
        self.ui.vehicleTypeDeletePushButton.clicked.connect(self.deleteVehicleType)
        self.ui.updatePicturePushButton.clicked.connect(self.updatePicture)
        
        # Taulukoiden soluvalinnat
        self.ui.vehicleCatalogTableWidget.cellClicked.connect(self.setRegisterNumber)
        self.ui.registeredPersonsTableWidget.cellClicked.connect(self.setSSN)
        self.ui.vehicleTypeTableWidget.clicked.connect(self.setVehicleType)
        self.ui.reasonAddTableWidget.clicked.connect(self.setReason)
        
        #Painikkeiden aktivoinnit syöttökentistä poistuttaessa
        self.ui.capacityLineEdit.textChanged.connect(self.showSaveVehiclePB) # Poistutaan henkilömäärä-kentästä
        self.ui.vehicleClassLineEdit.textChanged.connect(self.showSavePersonPB) #Poistutaan ajokorttiluokka-kentästä
        self.ui.vehicleTypeAddLineEdit.textChanged.connect(self.showVehicleTypeAddPB)
        self.ui.reasonAddLineEdit.textChanged.connect(self.showReasonAddPB)
    
        # Painikkeiden deaktiovoinnit kun aloitetaan ensimmäisen lomakekentän muokkaaminen
        self.ui.ssnLineEdit.textChanged.connect(self.hideDeletePersonPB)
        self.ui.numberPlateLineEdit.textChanged.connect(self.hideVehicleButtons)
        
        # Kenttien tietojen muuntaminen isoiksi kirjaimmiksi tai isoiksialkukirjaimmiksi
        self.ui.ssnLineEdit.editingFinished.connect(self.makeUpperCase)
        self.ui.vehicleClassLineEdit.editingFinished.connect(self.makeUpperCase)
        self.ui.numberPlateLineEdit.editingFinished.connect(self.makeUpperCase)
        self.ui.firstNameLineEdit.editingFinished.connect(self.makeFirstCharUpperCase)
        self.ui.lastNameLineEdit.editingFinished.connect(self.makeFirstCharUpperCase)
        self.ui.manufacturerLineEdit.editingFinished.connect(self.makeFirstCharUpperCase)
        self.ui.modelLineEdit.editingFinished.connect(self.makeFirstCharUpperCase)
        self.ui.vehicleOwnerLineEdit.editingFinished.connect(self.makeFirstCharUpperCase)
        

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
        
    # Tietoja ohjelmasta -sivun avaus (tiviopetus repositorion readme.md)
    def openAboutDialog(self):
        url = QUrl('https://github.com/TiViOpetus/Autolainaus_hallinta')
        QtGui.QDesktopServices.openUrl(url)
        
        
    def openWebHelp(self):
        url = QUrl('https://github.com/katalav/Autolainaus_hallinta/wiki/K%C3%A4ytt%C3%B6ohje')
        QtGui.QDesktopServices.openUrl(url)
        
    # Yleinen käyttöliittymän verestys (refresh)
    def refreshUi(self):
        
        # Auton kuvaksi kameran kuva
        self.vehiclePicture = 'uiPictures\\noPicture.png' # Kuvan poluksi ei kuvaa symboli
        self.ui.carPhotoLabel.setPixmap(QtGui.QPixmap(self.vehiclePicture)) # auton kuvan päivitys
        self.updateChoices() # Ryhmän valinta -yhdistelmäruudun arvot
        self.updateLenderTableWidget() # Lainaajien tiedot
        self.updateVehicleTableWidget() # Autojen tiedot
        self.updateVehicleTypeTableWidget() # Autotyyppien ylläpidon taulukko
        self.updateReasonTableWidget() # Ajon syiden ylläpidon taulukko
        self.ui.diaryTableWidget.clear() # Tyhjentää raporttisivun taulukon
        self.ui.reasonAddLineEdit.clear() # Ajon syyn lisäyskentän tyhjennys
        self.ui.vehicleTypeAddLineEdit.clear() # Ajoneuvotyypin lisäyskentän tyhjennys
        self.ui.removeVehiclePushButton.setHidden(True) # Auton-poisto painike piiloon
        self.ui.deletePersonPushButton.setHidden(True) # Käyttäjän poisto-painike piiloon
        self.ui.notLendablePushButton.setHidden(True) # Käytettävissä painike piiloon
        self.ui.savePersonPushButton.setHidden(True) # Lainaajan tallennapainike piiloon
        self.ui.saveVehiclePushButton.setHidden(True) # Auton tallennapainike piiloon
        self.ui.vehicleTypeAddPushButton.setHidden(True) # Ajoneuvotyypin lisäyspainike piiloon
        self.ui.reasonAddPushButton.setHidden(True) # Ajon syyn lisäyspainike piiloon
        self.ui.reasonDeletePushButton.setHidden(True) # Ajon syyn poistopainike piiloon
        self.ui.vehicleTypeDeletePushButton.setHidden(True) # Ajon tarkoituksen poistopainike piiloon
        self.ui.updatePicturePushButton.setHidden(True) # Auton kuvan päivityspainike piiloon
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
        
        self.ui.vehicleTypeComboBox.clear()
        self.ui.vehicleTypeComboBox.addItems(typeStringList)
        
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
        headerRow = ['Rekisteri', 'Käytettävissä', 'Merkki', 'Malli', 'Vuosimalli', 'Henkilömäärä', 'Tyyppi', 'Automaatti', 'Vastuuhenkilö']
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
        reasonFilter = self.ui.reasonFilterLineEdit.text()
        sqlFilter = ''

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Määritellään aikaväli, jolta raportti tulostetaan
        dateFilterSring = f"otto >= '{dateStart} 00:00:00+2' AND otto <= '{dateEnd} 23:59:59+2'"

        # Määritellään mahdollinen käyttäjäsuodatin
        if userFilter == '':
            userFilterString = ''
        else:
            userFilterString = f"AND hetu = '{userFilter}'"
        
        # Määritellään mahdollinen rekisterinumerosuodatin
        if registerFilter == '':
            registerFilterString = ''
        else:
            registerFilterString = f"AND rekisterinumero = '{registerFilter}'"
        
        # Määritellään mahdollinen ajontarkoitussuodatin   
        if reasonFilter == '':
            reasonFiltterString = ''
        else:
            reasonFiltterString = f"AND tarkoitus = '{reasonFilter}'"

        # Lopullinen SQL-suodatin
        sqlFilter = dateFilterSring + userFilterString + registerFilterString + reasonFiltterString
        print(sqlFilter)
        tableData = dbConnection.filterColumsFromTable(reportName,['*'], sqlFilter)
        
        # Tyhjennetään vanhat tiedot käyttöliittymästä ennen uusien lukemista tietokannasta
        self.ui.diaryTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Rekisteri', 'Merkki', 'Malli', 'Tarkoitus', 'HeTu', 'Sukunimi', 'Etunimi', 'Otettu', 'Palautettu']
        self.ui.diaryTableWidget.setHorizontalHeaderLabels(headerRow)

        # Tulosjoukon rivimäärä
        numberOfRows = len(tableData)
        self.ui.diaryTableWidget.setRowCount(numberOfRows)

        # Asetetaan taulukon solujen arvot
        for row in range(numberOfRows): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.diaryTableWidget.setItem(row, column, data)
    

    # Päivitetään Ajoneuvotyyppitaulukko
    def updateVehicleTypeTableWidget(self):
        
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('ajoneuvotyyppi')
        
 #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.vehicleTypeTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Ajoneuvotyyppi']
        self.ui.vehicleTypeTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.vehicleTypeTableWidget.setItem(row, column, data)
    
    #Päivitetään ajon tarkoitus-taulukko
    def updateReasonTableWidget(self):
        
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Tehdään lista lainaaja-taulun tiedoista
        tableData = dbConnection.readAllColumnsFromTable('tarkoitus')
        
 #Tyhjennetään vanhat tiedot käyttöliittymästä ennen  uusien lukemista tietokannasta
        self.ui.reasonAddTableWidget.clearContents()

        # Määritellään taulukkoelementin otsikot
        headerRow = ['Tarkoitus']
        self.ui.reasonAddTableWidget.setHorizontalHeaderLabels(headerRow)

        # Asetetaan taulukon solujen arvot
        for row in range(len(tableData)): # Luetaan listaa riveittäin
            for column in range(len(tableData[row])): # Luetaan monikkoa sarakkeittain
                
                # Muutetaan merkkijonoksi ja QTableWidgetItem-olioksi
                data = QtWidgets.QTableWidgetItem(str(tableData[row][column])) 
                self.ui.reasonAddTableWidget.setItem(row, column, data)
 
    # Syöttölomaketietojen tyhjennys
    # ------------------------------
    
    #Lainaaja tietojen tyhjennys
    def clearLenderData(self):
        self.ui.ssnLineEdit.clear()
        self.ui.firstNameLineEdit.clear()
        self.ui.lastNameLineEdit.clear()
        self.ui.vehicleClassLineEdit.clear()
        self.ui.agbRestrictionCheckBox.setChecked(False)
        self.ui.emailLineEdit.clear()
    
    # Auto tietojen tyhjennys
    def clearVehicleData(self):
        self.ui.numberPlateLineEdit.clear()
        self.ui.manufacturerLineEdit.clear()
        self.ui.modelLineEdit.clear()
        self.ui.modelLineEdit.clear()
        self.ui.modelYearLineEdit.clear()
        self.ui.capacityLineEdit.clear()
        self.ui.agbCheckBox.setChecked(False)
        self.ui.vehicleOwnerLineEdit.clear()
    
    # Ajopäiväkirjausten tyhjennys 
    def clearDiaryFilters(self):
        self.ui.ssnFilterLineEdit.clear()
        self.ui.registerFilterLineEdit.clear()
        self.ui.reasonFilterLineEdit.clear()
        
    # Lomakkeiden syöttötietojen siistiminen
    def makeUpperCase(self):
        self.ui.ssnLineEdit.setText(self.ui.ssnLineEdit.text().upper())
        self.ui.vehicleClassLineEdit.setText(self.ui.vehicleClassLineEdit.text().upper())
        self.ui.numberPlateLineEdit.setText(self.ui.numberPlateLineEdit.text().upper())
    
    def makeFirstCharUpperCase(self):
        self.ui.firstNameLineEdit.setText(self.ui.firstNameLineEdit.text().title())
        self.ui.lastNameLineEdit.setText(self.ui.lastNameLineEdit.text().title())
        self.ui.manufacturerLineEdit.setText(self.ui.manufacturerLineEdit.text().title())
        self.ui.modelLineEdit.setText(self.ui.modelLineEdit.text().title())
        self.ui.vehicleOwnerLineEdit.setText(self.ui.vehicleOwnerLineEdit.text().title()) 
        
        
    # Painikkeiden slotit
    # -------------------

    #Auton tallennuspainikkeen näkyminen
    def showSaveVehiclePB(self):
        self.ui.saveVehiclePushButton.setHidden(False)
        
    # Lainaajan tallennuspainikkeen näkyminen 
    def showSavePersonPB(self):
        self.ui.savePersonPushButton.setHidden(False)
        

    # Ajoneuvotyypin lisäyspainikkeen näyttäminen
    def showVehicleTypeAddPB(self):
        self.ui.vehicleTypeAddPushButton.setHidden(False)

    # Ajon syyn lisäyspainikkeen näyttäminen
    def showReasonAddPB(self):
        self.ui.reasonAddPushButton.setHidden(False)
        
    # Piilotetaan ajoneuvon Poista- ja Ei käytettävissä -painikkeet
    def hideVehicleButtons(self):
        self.ui.removeVehiclePushButton.setHidden(True)
        self.ui.notLendablePushButton.setHidden(True)
        self.ui.updatePicturePushButton.setHidden(True)
        
        # Päivitetään auton kuvaksi harmaa kamera
        self.vehiclePicture = 'uiPictures\\noPicture.png'
        
    def hideDeletePersonPB(self):
        self.ui.deletePersonPushButton.setHidden(True)
    
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
            self.ui.savePersonPushButton.setHidden(False)
            statusBarMessage = f'Lainaajan {self.ui.lastNameLineEdit.text()} tiedot tallennettiin'
            self.ui.statusbar.showMessage(statusBarMessage, 5000)
            self.clearLenderData()
            
            
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
        vehicleType = self.ui.vehicleTypeComboBox.currentText()
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
                          'automaatti': automaticGearBox,
                          'vastuuhenkilo': responsiblePerson
                          }
        
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.addToTable(tableName, vehicleDictionary)
            self.clearVehicleData()
            self.ui.saveVehiclePushButton.setHidden(True)
            
        except Exception as e:
            self.openWarning('Tallennus ei onnistunut', str(e))

        # Luetaan kuvatiedosto ja päivitetään auto-taulua
        with open(self.vehiclePicture, 'rb') as pictureFile:
            pictureData = pictureFile.read()

        # Luodaan uusi yhteys, koska edellinen suljettiin    
        dbConnection2 = dbOperations.DbConnection(dbSettings)

        try:
            dbConnection2.updateBinaryField('auto', 'kuva', 'rekisterinumero', f"'{numberPlate}'", pictureData)
            self.refreshUi()

        except Exception as e:
            self.openWarning('Kuvan päivitys ei onnistunut', str(e))
    
    
    def setNotLendable(self):
        # Asetetaan auto-taulun käytettävissä sarakkeen arvoksi FALSE
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        
         # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)
        
        #Kutsutaan päivitysmetodia
        try:
            dbConnection.modifyTableData('auto', 'kaytettavissa', False, 'rekisterinumero', f"'{self.vehicleToModify}'")
            self.refreshUi()
        except Exception as e:
            self.openWarning('Auton tilaa ei saatu muutettua',str(e))
            
            
            
    def updatePicture(self):
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan päivitysmetodia
        # Luetaan kuvatiedosto ja päivitetään auto-taulua
        with open(self.vehiclePicture, 'rb') as pictureFile:
            pictureData = pictureFile.read()

        # Luodaan uusi yhteys koska edellinen suljettiin    
        dbConnection = dbOperations.DbConnection(dbSettings)

        try:
            dbConnection.updateBinaryField('auto', 'kuva', 'rekisterinumero', f"'{self.vehicleToModify}'", pictureData)
            self.refreshUi()
            self.ui.updatePicturePushButton.setHidden(True)

        except Exception as e:
            self.openWarning('Kuvan päivitys ei onnistunut', str(e))
            
            

            
            
    def deleteVehicle(self):

         # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        
         # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan poistometodia
        try:
            dbConnection.deleteRowsFromTable('auto', 'rekisterinumero', f"'{self.vehicleToModify}'")
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


    # 
    def newReason(self):
         # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword
        
        # Luetaan syöttöelementtien arvot paikallisiin muuttujiin
        reason = self.ui.reasonAddLineEdit.text()
        
        # Määritellään tallennusmetodin vaatimat parametrit
        tableName = 'tarkoitus'
        reasonDictionary = {'tarkoitus': reason}
        
        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan tallennusmetodia
        try:
            dbConnection.addToTable(tableName, reasonDictionary)
            self.refreshUi() # Päivitetään taulukko lisäyksen jälkeen(lisäsin itse hehe)
            
        except Exception as e:
            self.openWarning('Tallennus ei onnistunut', str(e))
    # 
    def newVehicleType(self):
        
         # Määritellään tietokanta-asetukset
         dbSettings = self.currentSettings
         plainTextPassword = self.plainTextPassword
         dbSettings['password'] = plainTextPassword
 
         # Luetaan syöttöelementtien arvot paikallisiin muuttujiin
         vehicleType = self.ui.vehicleTypeAddLineEdit.text()
 
         # Määritellään tallennusmetodin vaatimat parametrit
         tableName = 'ajoneuvotyyppi'
         typeDictionary = {'tyyppi': vehicleType}
         
         # Luodaan tietokantayhteys-olio
         dbConnection = dbOperations.DbConnection(dbSettings)
 
         # Kutsutaan tallennusmetodia
         try:
             dbConnection.addToTable(tableName, typeDictionary)
             self.refreshUi() # Päivitetään taulukko lisäyksen jälkeen
                    
             
         except Exception as e:
             self.openWarning('Tallennus ei onnistunut', str(e))
    
    # Poistaa ajon tarkoituksen
    def deleteReason(self):
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan poistometodia
        try:
            dbConnection.deleteRowsFromTable('tarkoitus', 'tarkoitus', f"'{self.reasonToModify}'")
            self.refreshUi()
        except Exception as e:
            self.openWarning('Poisto ei onnistunut', str(e))
            
    # Poistaa ajoneuvotyypin
    def deleteVehicleType(self, arg):
        
        # Määritellään tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword

        # Luodaan tietokantayhteys-olio
        dbConnection = dbOperations.DbConnection(dbSettings)

        # Kutsutaan poistometodia
        try:
            dbConnection.deleteRowsFromTable('ajoneuvotyyppi', 'tyyppi', f"'{self.vehicleTypeToModify}'")
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
        self.vehicleToModify = cellValue
        self.ui.statusbar.showMessage(f'valitun auton rekisterinumero on {cellValue}')
        self.ui.removeVehiclePushButton.setHidden(False)
        self.ui.notLendablePushButton.setHidden(False)
        self.ui.updatePicturePushButton.setHidden(False)
        #self.ui.saveVehiclePushButton.setHidden(True)
        
        # Päivitetään kuvakettään valitun auton kuva
        
        # Muodostetaan yhteys tietokantaan
        # TODO Kuvan näyttö 
        
        try:
            # Luodaan tietokantayhteys-olio
            dbSettings = self.currentSettings
            plainTextPassword = self.plainTextPassword
            dbSettings['password'] = plainTextPassword
            dbConnection = dbOperations.DbConnection(dbSettings)
            criteria = f"rekisterinumero = '{self.vehicleToModify}'"
            
            # Haetaan auton kuva auto-taulusta
            resultSet = dbConnection.filterColumsFromTable('auto', ['kuva'], criteria)
            row = resultSet[0]
            picture = row[0] # PNG tai JPG kuva tietokannasta
           
            # Tallennetaan kuva väliaikaisesti levylle pixmap-muotoon muuttamista varten
            with open('currentCar.png', 'wb') as temporaryFile: 
                temporaryFile.write(picture)

            # Luodaan pixmap kuvatiedostosta ja päivitetään valitun auton kuva    
            pixmap = QtGui.QPixmap('currentCar.png')
            self.ui.carPhotoLabel.setPixmap(pixmap)
            
        except Exception as e:
            title = 'Auton kuvan lataaminen ei onnistunut'
            text = 'Jos mitään tietoja ei tullut näkyviin, ota yhteys henkilökuntaan'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)
        
    def setSSN(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''
        
        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.registeredPersonsTableWidget.currentRow()
        cellValue = self.ui.registeredPersonsTableWidget.item(rowIndex, columnIndex).text()
        self.personToDelete = cellValue
        self.ui.statusbar.showMessage(f'valitun käyttäjän henkilötunnus on {cellValue}')
        self.ui.deletePersonPushButton.setHidden(False)
        
    
 
        # Asetetaan poistettavan ajoneuvotyypin arvo
    def setVehicleType(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''

        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.vehicleTypeTableWidget.currentRow()
        cellValue = self.ui.vehicleTypeTableWidget.item(rowIndex, columnIndex).text()
        self.vehicleTypeToModify = cellValue
        self.ui.statusbar.showMessage(f'Poistettava ajoneuvotyyppi on {cellValue}')
        self.ui.vehicleTypeDeletePushButton.setHidden(False)
        self.ui.reasonDeletePushButton.setHidden(True)

    # Asetetaan poistettava ajon syy    
    def setReason(self):
        rowIndex = 0
        columnIndex = 0
        cellValue = ''

        # Haetaan aktiivisen solun rivinumero ja ensimmäisen sarakkeen arvo siltä riviltä
        rowIndex = self.ui.reasonAddTableWidget.currentRow()
        cellValue = self.ui.reasonAddTableWidget.item(rowIndex, columnIndex).text()
        self.reasonToModify = cellValue
        self.ui.statusbar.showMessage(f'Poistettava ajon syy on {cellValue}')
        self.ui.reasonDeletePushButton.setHidden(False)
        self.ui.vehicleTypeDeletePushButton.setHidden(True)


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

    