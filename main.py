from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import os, sys, json, webbrowser



# requirements : pyQt6


class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.setFixedSize(800,700)
        self.move(50,50)
        self.show()
        self.setWindowTitle('EncrpytPassword')
        self.json='encrypt.json'
        self.string = ''
        self.encryptField.textChanged.connect(lambda : self.encryptString())
        self.encryptString()
        self.encryptField.setFocus()
        self.tabWidget.currentChanged.connect(lambda : self.updateJson())
        
        
    def encryptString(self):
        with open(self.json, encoding='utf-8') as jsonFile:
            self.stringTable = json.load(jsonFile)
            result = ""
            for char in self.encryptField.text():
                try:
                    result+=self.stringTable[char]
                except:
                    result+= " "
            print(result)
            self.resultLabel.setText(result)
            
            
    def updateJson(self):
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet("margin:0 0 0 0")
        scrollLayout = QVBoxLayout(scrollWidget)
        with open(self.json, encoding='utf-8') as jsonFile:
            self.stringTable = json.load(jsonFile)
            for char in self.stringTable:
                tableLayout = QVBoxLayout()
                label = QLabel("{} : {}\n".format(char, self.stringTable[char]))
                tableLayout.addWidget(label)
                tableWidget = QWidget()
                tableWidget.setLayout(tableLayout)
                scrollLayout.addWidget(tableWidget)
        self.TableScrollArea.setWidget(scrollWidget)
                
            
            
    
        
    def delFileCourse(self, list, property):
        courseName = self.listCoursesByCat.selectedItems()[0].text()
        cat=self.categoriesList.selectedItems()[0].text()

        listItems=list.selectedItems()
        if not listItems: return
        for item in listItems:
            list.takeItem(list.row(item))
        
        files=[]
        for courseIndex in self.globalCourses[cat]:
            if courseName==courseIndex['nom']:
                for file in courseIndex[property]:
                    if listItems[0].text()!=file['name']:
                        files.append(file)
                courseIndex[property]=files

        with open(self.json, 'w', encoding='utf8') as json_file:
            json.dump(self.globalCourses,json_file, ensure_ascii=False, indent=2)
            

        
    def restart(self):
        os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
        exit()

    def loadCourses(self, jsonFile, scrollArea, type):
        
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet("margin:0 0 50 0")
        scrollLayout = QVBoxLayout(scrollWidget)
        with open(jsonFile, encoding='utf-8') as jsonFile:
            self.globalCourses = json.load(jsonFile)
            for categoriesIndex in self.globalCourses:
                categoryLayout = QVBoxLayout()
                categoryLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                if type == "DWWM":
                    self.categoriesList.addItem(categoriesIndex)
                    self.categoriesList.setCurrentRow(0)
                    self.showCatCourses()
                    try:
                        self.listCoursesByCat.setCurrentRow(0)
                    except:
                        False

                #display category name
                label = QLabel("\n{}".format(categoriesIndex))
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("font-size:24px;color:#153754;font-weight:600;font-family: 'Comic Sans';")
                categoryLayout.addWidget(label)
                category = self.globalCourses[categoriesIndex]
                coursesLayout = QGridLayout()
                count = 0
                try:
                    for course in category:
                        #add Btn for each course*
                        if (type in course['type'] or ("OPT"+type) in course['type']):
                            courseBtn = QPushButton(text=course["nom"],parent=self)
                            if ("OPT"+type) in course['type']:
                                courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #A47500, stop: 1 #8C5000); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                            else:
                                courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #206a95, stop: 1 #153754); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                            courseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                            courseBtn.setFixedHeight(60)

                            # trigger copy to clipboard on click
                            courseBtn.clicked.connect(lambda : self.copyBuffer())
                            courseBtn.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
                            # coursesLayout.addWidget(courseBtn,  count, 0)
                            coursesLayout.addWidget(courseBtn,  count//3, count%3)
                            count+=1
                except:
                    False
                coursesWidget = QWidget()
                coursesWidget.setLayout(coursesLayout)
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryLayout.addWidget(coursesWidget)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 10 10")
                categoryWidget.setContentsMargins(0, 0, 0, 30)
                if count > 0:
                    scrollLayout.addWidget(categoryWidget)
        scrollArea.setWidget(scrollWidget)
   
def main():
    try :
        # Add ffmpeg to the PATH
        ffmpegPath= os.path.dirname(os.path.realpath(__file__))+"\\ffmpeg\\bin"
        os.environ['PATH'] = ffmpegPath
    except Exception as error:
        print("An exception occurred:"+ str(error))
    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec()


if __name__ == '__main__':
    main() 