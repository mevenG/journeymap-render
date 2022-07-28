from ast import For
import os
from PIL import Image
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

#dir_path = r'C:\Users\XPS15\AppData\Roaming\.lk\instances\LostKingdoms-1.12.2\journeymap\data\mp\LostKingdoms\DIM-28\day'
#dir_path = r'C:\Users\XPS15\Documents\python\journeymap\test'

res = []
pox = []
poy = []
midx = 0
midy = 0
def calcpos(posox,posoy,midx,midy):
    n = 0
    posax = midx*512 + posox*512
    posay = midy*512 + posoy*512
    #print(posox, posoy, posax, posay)
    return posax,posay

def render(dir_path,dimrend,typ,wayp):
    logtobox("Rendu en cours ...")
    print(dir_path+'\\'+dimrend+'\\'+typ)
    for path in os.listdir(dir_path+'\\'+dimrend+'\\'+typ):
        if os.path.isfile(os.path.join(dir_path+'\\'+dimrend+'\\'+typ, path)):
            res.append(path)
            pox.append(float(path.split(",")[0]))
            poy.append(float(path.split(",")[1].split(".")[0]))

    lenx = int(512*abs(min(pox) - max(pox))+512)
    leny = int(512*abs(min(poy) - max(poy))+512)
    midx = 0 - min(pox)
    midy = 0 - min(poy)

    print("IMAGE SIZE :")
    print(lenx,leny)
    logtobox("Taille de l'image :")
    logtobox(str(lenx)+"px, "+str(leny)+"px")
    

    bg = Image.new('RGB', (lenx, leny),'black')

    for path in res:
        posx = path.split(",")[0]
        posy = path.split(",")[1].split(".")[0]
        if os.path.isfile(dir_path+'\\'+dimrend+'\\'+typ+'\\'+path):
            if path.endswith('.png'):
                im = Image.open(dir_path+'\\'+dimrend+'\\'+typ+'\\'+path)
                print(posx,posy)
                logtobox(str(posx)+", "+str(posy))
                px,py = calcpos(float(posx),float(posy),midx,midy)
                bg.paste(im, (int(px), int(py)))

    if wayp:
        logtobox('créations des waypoints')


    
    
    logtobox('Rendu fini !')
    file , check = QFileDialog.getSaveFileName(None, "Enregistrer sous", "", "Image Files (*.png)")
    if check:
        print(file)
        logtobox("Enregistrement de l'image ...")
        bg.save(file)
        logtobox('oké !')
    #rendered = Image.open('DEBUG.png')
    #rendered.show()

dims = []
def init():
    for path in os.listdir(os.getenv('APPDATA')+'\.lk\instances\LostKingdoms-1.12.2\journeymap\data\mp\LostKingdoms'):
        print(path)
        dims.append(convdim(path))
    print(dims)

def convdim(dim):
    match dim:
        case 'DIM-28':
            return 'Lune'
        case 'b':
            return 'toto'
        case 'DIM1':
            return 'BigEnd'
        case 'DIM-1':
            return False
        case 'DIM2':
            return 'Terre'
        case 'DIM305':
            return 'Minage'
        case 'DIM338':
            return 'Event'
        case 'waypoints':
            return False
        case _:
            return False

def dimconv(dim):
    match dim:
        case 'Lune':
            return 'DIM-28'
        case 'BigEnd':
            return 'DIM1'
        case 'Nether':
            return 'DIM-1'
        case 'Terre':
            return 'DIM2'
        case 'Minage':
            return 'DIM305'
        case 'Event':
            return 'DIM338'
        case _:
            return False

app = QApplication([])
window = QWidget()
layout = QGridLayout()
init()

dimlist = QComboBox()
for dim in dims:
    if dim:
        dimval = dimconv(dim)
        dimlist.addItem(dim)
dimlist.move(100,100)
layout.addWidget(dimlist, 0, 0)

waypcb = QCheckBox("Waypoints")
waypcb.setChecked(False)
layout.addWidget(waypcb, 0, 2)

dayb = QRadioButton("Jour")
dayb.setChecked(True)
layout.addWidget(dayb, 1, 0)

nightb = QRadioButton("Nuit")
layout.addWidget(nightb, 1, 1)

topob = QRadioButton("Topo")
layout.addWidget(topob, 1, 2)

renbut = QPushButton('Render')
renbut.move(300,300)
layout.addWidget(renbut, 3, 3)

logbox = QPlainTextEdit("")
#logbox.setEnabled(False)
layout.addWidget(logbox, 4, 3)


def logtobox(contents):
    logbox.insertPlainText(str(contents)+"\r\n")
    logbox.verticalScrollBar().setValue(logbox.verticalScrollBar().maximum())
    app.processEvents()

def on_render():
    print('rendering')
    ways = False
    if waypcb.isChecked():
        ways = True

    if dayb.isChecked():
        rendtyp = 'day'
    elif nightb.isChecked():
        rendtyp = 'night'
    elif topob.isChecked():
        rendtyp = 'topo'

    render(os.getenv('APPDATA')+'\.lk\instances\LostKingdoms-1.12.2\journeymap\data\mp\LostKingdoms',dimconv(dimlist.currentText()), rendtyp, ways)

    



renbut.clicked.connect(on_render)

window.setLayout(layout)
window.setWindowTitle("Xel' Collage de map")
window.setWindowIcon(QtGui.QIcon('icon.png'))
#window.setFixedWidth(500)
#window.setFixedHeight(500)
window.show()
app.exec()