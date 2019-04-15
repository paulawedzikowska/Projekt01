import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initInterface()
        self.initWidgets()

    def initInterface(self):
        self.setGeometry(100,100,600,500)
        self.setWindowTitle("Projekt 1")
        self.show()

    def initWidgets(self):
        # Tworzenie etykiet
        etykieta0 = QLabel("Wprowadz dane:", self)
        etykieta1 = QLabel("aX:", self)
        etykieta2 = QLabel("aY:", self)
        etykieta3 = QLabel("bX", self)
        etykieta4 = QLabel("bY", self)
        etykieta5 = QLabel("cX", self)
        etykieta6 = QLabel("cY", self)
        etykieta7 = QLabel("dX", self)
        etykieta8 = QLabel("dY", self)
        etykietaX = QLabel("pX", self)
        etykietaY = QLabel("pY", self)
        przerwa = QLabel("       ", self)
        # Tworzenie przycisków
        przycisk1 = QPushButton("Oblicz punkt przecięcia", self)
        przycisk2 = QPushButton("Rysuj", self)
        self.przycisk3 = QPushButton("Zmień kolor odcinka AB i CD", self)
        self.przycisk3.setEnabled(False)
        przycisk4 = QPushButton("Wyczyść", self)
        przycisk5 = QPushButton("Wczytaj z pliku", self)
        przycisk6 = QPushButton("Zapisz wynik do pliku", self)

        # Tworzenie pól z wartosciami
        self.aXEdit = QLineEdit()
        self.aYEdit = QLineEdit()
        self.bXEdit = QLineEdit()
        self.bYEdit = QLineEdit()
        self.cXEdit = QLineEdit()
        self.cYEdit = QLineEdit()
        self.dXEdit = QLineEdit()
        self.dYEdit = QLineEdit()
        self.przedluzenie = QLineEdit() #Zmienna pomocnicza do narysowania przedłużenia
        self.zmiana = QLineEdit() #Zmienna pomocnicza do funkcji rysuj
        self.wynikXEdit = QLineEdit()
        self.wynikYEdit = QLineEdit()
        self.wynikXEdit.readonly = True
        self.wynikYEdit.readonly = True

        self.komunikatEdit = QTextEdit()
        self.komunikatEdit.readonly = True

        # Tworzenie miejsca pod wykres
        self.figure = plt.figure()
        self.figure = plt.figure(figsize=(10, 10), dpi=60)
        self.canvas = FigureCanvas(self.figure)

        # Przypisanie widgetów do okna programu
        grid = QGridLayout()
        grid.addWidget(etykieta0, 0, 0, 1, 0)

        grid.addWidget(etykieta1, 1, 0)
        grid.addWidget(self.aXEdit, 1, 1)
        grid.addWidget(etykieta2, 1, 2)
        grid.addWidget(self.aYEdit, 1, 3)

        grid.addWidget(etykieta3, 2, 0)
        grid.addWidget(self.bXEdit, 2, 1)
        grid.addWidget(etykieta4, 2, 2)
        grid.addWidget(self.bYEdit, 2, 3)

        grid.addWidget(etykieta5, 3, 0)
        grid.addWidget(self.cXEdit, 3, 1)
        grid.addWidget(etykieta6, 3, 2)
        grid.addWidget(self.cYEdit, 3, 3)

        grid.addWidget(etykieta7, 4, 0)
        grid.addWidget(self.dXEdit, 4, 1)
        grid.addWidget(etykieta8, 4, 2)
        grid.addWidget(self.dYEdit, 4, 3)

        grid.addWidget(przycisk5, 0, 2, 1, 2)
        grid.addWidget(przycisk4, 5, 1, 1, 3)
        grid.addWidget(przycisk6, 9, 0, 1, 6)

        grid.addWidget(przerwa, 0, 5)
        grid.addWidget(przycisk1, 0, 7, 1, 3)
        grid.addWidget(etykietaX, 1, 6)
        grid.addWidget(self.wynikXEdit, 1, 7)
        grid.addWidget(etykietaY, 1, 8)
        grid.addWidget(self.wynikYEdit, 1, 9)

        grid.addWidget(self.komunikatEdit, 2, 7, 3, 3)
        grid.addWidget(przycisk2, 5, 7)
        grid.addWidget(self.przycisk3, 5, 8,1,2)
        grid.addWidget(self.canvas, 6, 7,4,3)

        # Wywołanie okna programu
        self.setLayout(grid)
        # Pyzpisanie funkcji do przycisków
        przycisk1.clicked.connect(self.oblicz)
        przycisk2.clicked.connect(self.rysuj)
        self.przycisk3.clicked.connect(self.zmienKolor)
        przycisk4.clicked.connect(self.wyczysc)
        przycisk5.clicked.connect(self.wczytaj)
        przycisk6.clicked.connect(self.zapisz)

    #Funkcje
    def wczytaj(self):
        wartosci = [] #Zmienna do przechowywania wartości z pliku
        plik = open('dane.txt', 'r') #Otwieranie pliku
        linie = plik.readlines() #Zmienna przechowująca wszystkie linie z pliku

        for linia in linie[0:]:
            linia = linia.strip('\n').split(' ') #Pobranie jednej linii i rozdzielenie jej "spacjami"
            wartosci.append(linia[0])
            wartosci.append(linia[1])
        # Przypisanie do zmiennych poszczególnych wartości
        ax = wartosci[0]
        ay = wartosci[1]
        bx = wartosci[2]
        by = wartosci[3]
        cx = wartosci[4]
        cy = wartosci[5]
        dx = wartosci[6]
        dy = wartosci[7]
        # Wstawienie do pola z wartością wczytanych wartości
        self.aXEdit.setText(ax)
        self.aYEdit.setText(ay)
        self.bXEdit.setText(bx)
        self.bYEdit.setText(by)
        self.cXEdit.setText(cx)
        self.cYEdit.setText(cy)
        self.dXEdit.setText(dx)
        self.dYEdit.setText(dy)

        plik.close() #zamknięcie pliku

    def zapisz(self):
        #Przypisanie do zmiennych wartości liczbowych
        x = self.sprawdzWartosc(self.wynikXEdit)
        y = self.sprawdzWartosc(self.wynikYEdit)

        if x != None and y != None:  #sprawdzenie czy wartość x i y istnieją
            plik = open('wynik.txt', 'a')
            #Wpisanie do pliku wartości x i y
            plik.write("pX = ")
            plik.write("{:.3f}".format(x))
            plik.write("\tpY = ")
            plik.write("{:.3f}".format(y))
            plik.write('\n')
            plik.close()

    def oblicz(self):
        #sprawdzenie czy wpisane wartości w polach są liczbą
        ax = self.sprawdzWartosc(self.aXEdit)
        ay = self.sprawdzWartosc(self.aYEdit)
        bx = self.sprawdzWartosc(self.bXEdit)
        by = self.sprawdzWartosc(self.bYEdit)
        cx = self.sprawdzWartosc(self.cXEdit)
        cy = self.sprawdzWartosc(self.cYEdit)
        dx = self.sprawdzWartosc(self.dXEdit)
        dy = self.sprawdzWartosc(self.dYEdit)

        #Sprawdzenie czy każda wartość spełnia warunek
        if(ax != None and ay != None and bx != None and by != None and cx != None and cy != None and dx != None and dy != None):
            if (((bx - ax) * (dy - cy)) - ((by - ay) * (dx - cx))) == 0: #Sprawdzenie czy proste są równoległe
                self.komunikatEdit.setText("Proste są równoległe")
            else:
                #Obliczenia na podstawie wzorów
                t1 = (((cx - ax) * (dy - cy)) - ((cy - ay) * (dx - cx))) / (((bx - ax) * (dy - cy)) - ((by - ay) * (dx - cx)))
                t2 = (((cx - ax) * (by - ay)) - ((cy - ay) * (bx - ax))) / (((bx - ax) * (dy - cy)) - ((by - ay) * (dx - cx)))

                px = ax + t1 * (bx - ax)
                py = ay + t1 * (by - ay)
                px = round(px, 3)
                py = round(py, 3)
                #Wpisanie w pola wyników powyższych obliczeń
                self.wynikXEdit.setText("{:.3f}".format(px))
                self.wynikYEdit.setText("{:.3f}".format(py))

                #Sprawdzenie warunków położenia wyliczonego punktu względem odcinków
                if 0 <= t1 <= 1 and 0 <= t2 <= 1:
                    self.komunikatEdit.setText("Punkt przecięcia leży wewnątrz obu odcinków")
                elif (0 <= t1 <= 1) and (t2 < 0 or t2 > 1):
                    self.komunikatEdit.setText("Punkt przecięcia leży wewnątrz odcinka AB i na przedłużeniu odcinka CD")
                    self.przedluzenie.setText('1')
                elif (0 <= t2 <= 1) and (t1 < 0 or t1 > 1):
                    self.komunikatEdit.setText("Punkt przecięcia leży wewnątrz odcinka CD i na przedłużeniu odcinka AB")
                    self.przedluzenie.setText('2')
                elif (t2 < 0 or t2 > 1) and (t1 < 0 or t1 > 1):
                    self.komunikatEdit.setText("Punkt przecięcia leży na przedłużeniu obu odcinków")
                    self.przedluzenie.setText('3')

        else:
            self.komunikatEdit.setText("Błędne dane. Podaj brakujące wartości.")
    #Utworzenie funkcji sprawdzającej czy podana wartość jest liczbą
    def sprawdzWartosc(self, element):
        if element.text().lstrip('-').replace('.', '', 1).isdigit():
            return float(element.text())
        else:
            element.setFocus()
            #Jeśli podana wartość nie jest liczbą wyczyść dane pole
            element.setText("")
            return None

    def wyczysc(self):
        #Wstawianie do pól z wartościami pustego napisu
        self.aXEdit.setText("")
        self.aYEdit.setText("")
        self.bXEdit.setText("")
        self.bYEdit.setText("")
        self.cXEdit.setText("")
        self.cYEdit.setText("")
        self.dXEdit.setText("")
        self.dYEdit.setText("")
        self.wynikXEdit.setText("")
        self.wynikYEdit.setText("")
        self.komunikatEdit.setText("")
        #Wyczyszczenie pola figury
        self.figure.clear()
        self.canvas.draw()
        # Zablokowanie przycisku
        self.przycisk3.setEnabled(False)

    def rysuj(self):
        ax = self.sprawdzWartosc(self.aXEdit)
        ay = self.sprawdzWartosc(self.aYEdit)
        bx = self.sprawdzWartosc(self.bXEdit)
        by = self.sprawdzWartosc(self.bYEdit)
        cx = self.sprawdzWartosc(self.cXEdit)
        cy = self.sprawdzWartosc(self.cYEdit)
        dx = self.sprawdzWartosc(self.dXEdit)
        dy = self.sprawdzWartosc(self.dYEdit)
        px = self.sprawdzWartosc(self.wynikXEdit)
        py = self.sprawdzWartosc(self.wynikYEdit)

        #Sprawdzenie warunku
        if(ax != None and ay != None and bx != None and by != None and cx != None and cy != None and dx != None and dy != None and px != None and py != None):
            self.figure.clear()
            plt.title('Wykres punktu P')
            plt.xlabel('X')
            plt.ylabel('Y')

            if self.sprawdzWartosc(self.zmiana) == 1: #Jeśli zmiana=1 to zmiana koloru
                self.kolor = QColorDialog.getColor() #Pobranie koloru
                self.kolor = self.kolor.name() #Pobranie nazwy koloru
                plt.plot([ax, bx], [ay, by], self.kolor) #Narysowanie linii wybranym kolorem
                self.kolor2 = QColorDialog.getColor()
                self.kolor2 = self.kolor2.name()
                plt.plot([cx, dx], [cy, dy], self.kolor2)
            else:
                #Rysowanie linii
                plt.plot([ax, bx], [ay, by], 'b')
                plt.plot([cx, dx], [cy, dy], 'r')
                #Odblokowanie przycisku po narysowaniu wykresu
                self.przycisk3.setEnabled(True)
            #Rysowanie punktów końców odcinków i punktu P na wykresie
            plt.scatter(ax, ay, s=150, c='#FF0000')
            plt.scatter(bx, by, s=150, c='#33FF00')
            plt.scatter(cx, cy, s=150, c='#0066FF')
            plt.scatter(dx, dy, s=150, c='#FFFF00')
            plt.scatter(px, py, s=150, c='k')
            #Tworzenie legendy
            plt.legend(('AB', 'CD', 'a', 'b', 'c', 'd', 'p'))

            # Rysowanie przedluzen
            przedlz = self.sprawdzWartosc(self.przedluzenie)
            #Jeśli zmiana=1 to przedłużenie rysowane zmienionym kolorem
            if self.sprawdzWartosc(self.zmiana) == 1:
                if przedlz == 1:
                    plt.plot([cx, px], [cy, py], self.kolor, linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, dx], [py, dy], 'r', linewidth=0.3)
                elif przedlz == 2:
                    plt.plot([ax, px], [ay, py], self.kolor2, linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, bx], [py, by], 'b-', linewidth=0.3)
                elif przedlz == 3:
                    plt.plot([ax, px], [ay, py], self.kolor, linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, bx], [py, by], 'b-', linewidth=0.3)
                    plt.plot([cx, px], [cy, py], self.kolor2, linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, dx], [py, dy], 'r-', linewidth=0.3)
                self.zmiana.setText("0")
            else:
                if przedlz == 1:
                    plt.plot([cx, px], [cy, py], 'r', linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, dx], [py, dy], 'r', linewidth=0.3)
                elif przedlz == 2:
                    plt.plot([ax, px], [ay, py], 'b', linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, bx], [py, by], 'b-', linewidth=0.3)
                elif przedlz == 3:
                    plt.plot([ax, px], [ay, py], 'b', linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, bx], [py, by], 'b-', linewidth=0.3)
                    plt.plot([cx, px], [cy, py], 'r', linestyle='dashed', linewidth=0.5)
                    #plt.plot([px, dx], [py, dy], 'r-', linewidth=0.3)
            self.canvas.draw()

    def zmienKolor(self):
        #Jeżeli zostanie kliknęty przycisk ZmianaKoloru to zmienna pomocnicza "zmiana"  dostaje wartość 1
        self.zmiana.setText("1")
        #Wywołanie funkcji rysuj
        self.rysuj()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = AppWindow() #Stworzenie obiektu klasy
    sys.exit(app.exec_())
