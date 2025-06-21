# NSIS INSTALLER TEMPLATE WITH MODERN UI
# =======================================================

# Include Modern UI
  # Let's use modern look importing header file  
  !include "MUI2.nsh"

# --- Include end

# General

  # Name and installer file name, do not use plain setup.exe as OutFile
  Name "Autolainaushallinta"
  OutFile "administrativeAppSetup.exe"
  Unicode True

  # Default installation folder: user's application data directory
  InstallDir "$PROGRAMFILES64\Autolainaushallinta"
  
  # Get installation folder from registry if available (reinstall)
  InstallDirRegKey HKCU "Software\Autolainaushallinta" ""

  # Request application privileges for Windows Vista or later: user | admin
  RequestExecutionLevel admin

# --- General end

# Variable declarations

  Var StartMenuFolder

# --- Variable definitions end

# Interface Settings

  # Set icon for installer window
  !define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"

  # Add a bitmap (150 x 57 px) for a logo into the header of the installer page
  !define MUI_HEADERIMAGE
  !define MUI_HEADERIMAGE_BITMAP "RasekoNSIS.bmp"

  # Set left side image for start and end pages
  !define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
  
  # Check if user really wants to abort
  !define MUI_ABORTWARNING

  # Show all languages, despite user's codepage
  !define MUI_LANGDLL_ALLLANGUAGES

# --- end Interface settings

# Language Selection Dialog Settings

  # Remember the installer language -> language not asked when installer restarted
  !define MUI_LANGDLL_REGISTRY_ROOT "HKCU" 
  !define MUI_LANGDLL_REGISTRY_KEY "Software\Autolainaushallinta" 
  !define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"

# --- Language Selection Dialog Settings end

# Pages
  !insertmacro MUI_PAGE_WELCOME

  # License file containing the GNU GPL 3 information
  !insertmacro MUI_PAGE_LICENSE "LICENSE"

  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  
  # Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Autolainaushallinta" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

# --- Pages end

# Languages, 1st is the default
 
  !insertmacro MUI_LANGUAGE "Finnish"
  !insertmacro MUI_LANGUAGE "English"

# --- Languages end

# Installer Sections

# Section for choosing the program 
Section "Autolaiaussovellus hallinta" SecProgram

  SetOutPath "$INSTDIR"
  
  # READ FILES RECURSIVELY FROM DITRIBUTION FOLDER CREATED BY PYINSTALLER
  # Files to put into the installation directory from the distribution folder
  File /r "dist\administrative\"

  # Store installation folder to registry
  WriteRegStr HKCU "Software\Autolainaushallinta" "" $INSTDIR
  
  # Create uninstaller
  WriteUninstaller "$INSTDIR\UninstallAutolainaushallinta.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    # Create shortcuts
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Autolainaushallinta.lnk" "$INSTDIR\autolainaushallinta.exe"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\UninstallApp.lnk" "$INSTDIR\UninstallAutolainaushallinta.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

; # Section for optional files or directories
; Section "NameOfFile" SecAdditions
;     SetOutPath "$INSTDIR\AdditionsFolderName"
  
;   # Files to put into Additional files subdirectory
;   File "*.something"
;   File "*.otherType"
; SectionEnd

# --- # Installer Sections end

# Installer Functions

# A function for asking the installation language at startup
Function .onInit
  
  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd

# --- Installer Functions


# Descriptions

  # Language strings
  LangString DESC_SecProgram ${LANG_FINNISH} "Autojen lainaus- ja palautussovelluksen hallinta"
  LangString DESC_SecProgram ${LANG_ENGLISH} "A program to administer vehicles and users"
  ;LangString DESC_SecAdditions ${LANG_FINNISH} "Additional content explained in finnish"
  ;LangString DESC_SecAdditions ${LANG_ENGLISH} "Additional content explained in english"

  # Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecProgram} $(DESC_SecProgram)
    ;!insertmacro MUI_DESCRIPTION_TEXT ${SecAdditions} $(DESC_SecAdditions)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END
 
# --- Descriptions end

# Uninstaller Section
Section "Uninstall"

  # Remove files and folders from installation directory, if not successfull remove after reboot
  RMDir /r /REBOOTOK $INSTDIR
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

  # Remove start menu items  
  Delete "$SMPROGRAMS\$StartMenuFolder\Autolainaushallinta.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\UninstallApp.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"
  
  # Clean the registry by removing all keys under the Sofware branch of the app
  
  DeleteRegKey HKCU "Software\Autolainaushallinta"

SectionEnd

#--- Uninstaller Section end

# A function for the uninstaller's language
Function un.onInit

  !insertmacro MUI_UNGETLANGUAGE
  
FunctionEnd

# --- Unistaller language function end