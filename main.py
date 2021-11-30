from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from Randomizers import Encounters, Evolutions, Trainers, UndergroundEncounters, Levels, Shop, TM, Starters
from Randomizers.dialog import Ui_MainWindow
from Utilities import GlobalGameManager
import sys

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnRandomize.clicked.connect(self.buttonClicked)
    
    def buttonClicked(self):
        #setup directory where romFS To modify is. 
        dialog = QFileDialog()
        global romFSPath
        romFSPath = dialog.getExistingDirectory(self, 'Select ROMFS path')
        self.ui.tbLog.append("RomFS Directory set to " + romFSPath)
        
        if self.ui.cbStarters.isChecked():
            Starters.RandomizeStarters(self.ui.tbLog)
    
        if self.ui.cbPokemon.isChecked():
            self.ui.tbLog.append('Randomizing Pokemon!')
            generations = []
            if self.ui.cbGen1.isChecked():
                generations.append(1)
            if self.ui.cbGen2.isChecked():
                generations.append(2)
            if self.ui.cbGen3.isChecked():
                generations.append(3)
            if self.ui.cbGen4.isChecked():
                generations.append(4)
            #Fixed added safari -- sangawku
            Encounters.RandomizeEncounters(self.ui.tbLog,self.ui.cbLegends.isChecked(), generations, self.ui.cbSafari.isChecked(), romFSPath)
            
        if self.ui.cbTrainers.isChecked():
            self.ui.tbLog.append('Randomizing Trainers!')
            Trainers.RandomizeTrainers(self.ui.tbLog, romFSPath)
            
        if self.ui.cbTimeSkip.isChecked() or self.ui.cb60FPS.isChecked():
            self.ui.tbLog.append('Applying Utilities!')
            GlobalGameManager.ApplyUtilities(self.ui.cb60FPS.isChecked(), self.ui.sbTimeStep.value(), self.ui.tbLog, romFSPath)
        
        if self.ui.cbUnderground.isChecked():
            self.ui.tbLog.append('Randomizing Underground Pokemon!')
            UndergroundEncounters.RandomizeUG(self.ui.tbLog, romFSPath)
            
        if self.ui.cbEvolutions.isChecked():
            self.ui.tbLog.append('Randomizing Evolutions!')
            Evolutions.RandomizeEvolutions(self.ui.tbLog, romFSPath)
        
        if self.ui.cbTM.isChecked():
            self.ui.tbLog.append('Randomizing TMs!')
            TM.RandomizeTMs(self.ui.tbLog, romFSPath)
        
        if self.ui.cbShops.isChecked():
            self.ui.tbLog.append('Randomizing Shops!')
            Shop.RandomizeShops(self.ui.tbLog, romFSPath)
        #if self.ui.cbLevels.isChecked():
        #    self.ui.tbLog.append('Randomizing Levels!')
        #    if self.ui.rbFlat.isChecked():
        #        Levels.RandomizeLevels(self.ui.tbLog,1, self.ui.sbMin.value(), self.ui.sbMax.value())
        #    else:
        #        Levels.RandomizeLevels(self.ui.tbLog,0, self.ui.sbMin.value(), self.ui.sbMax.value())

app = QApplication(sys.argv)

# Set our style, We don't want mismatched themes 
app.setStyle("Fusion")

# Now make them bitches dark as night:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
app.setApplicationName("BDSP Randomizer")

w = AppWindow()
w.show()
sys.exit(app.exec_())

w = AppWindow()
w.show()
app.exec_()

