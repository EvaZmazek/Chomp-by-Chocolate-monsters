from tkinter import *
from random import *
import threading
import logging
import pickle

#Konstante:
SIRINA=7
VISINA=5
IGRALEC_1 = "1"
IGRALEC_2 = "2"
NI_KONEC = "ni konec"
KONEC = "konec"

MINIMAX_GLOBINA = 3

POZNANE_VREDNOSTI = pickle.load( open( "poznane_vrednosti.p", "rb" ) )

######################################################################
## Razred Igra

class Igra():
    
    def __init__(self):
        """ Konstruktor objektov razreda Igra"""
        self.zaporedje=[VISINA for i in range(SIRINA)]
        #ustvarimo zaporedje, s pomočjo katerega vidimo, kateri koščki čokolade so še v igri
        self.na_potezi = IGRALEC_1      # Vedno igro odpre človek.
        self.zgodovina = []
        # Zgodovina igre je prazna, ko igro začnemo (ne glede na to, ali smo prej že kaj igrali).

    def shrani_pozicijo(self):
        '''Funkcija zapiše trenutno pozicijo in igralca v zgodovino'''
        zap=self.zaporedje
        self.zgodovina.append((zap, self.na_potezi))

    def kopija(self):
        '''Za potrebe vzporednega izvajanja v več threadih potrebujemo kopijo igre'''
        k=Igra()
        k.zaporedje = self.zaporedje
        k.na_potezi = self.na_potezi
        return k

    def veljavne_poteze(self):
        """Preveri, katere poteze igralec sploh lahko potegne."""
        poteze=[]
        for j in range(len(self.zaporedje)):
            for i in range(self.zaporedje[j]):
                poteze.append((j,i))
        return poteze

    def stanje_igre(self):
        """
        Ugotovi, kakšno je stanje igre. Vrne:
            - IGRALEC_1, če je igre konec in je zmagal IGRALEC_1 (uporabik)
            - IGRALEC_2, če je igre konec in je zmagal IGRALEC_2 (človek/računalnik)
            - NI_KONEC, če igre še ni konec
            - KONEC - to potrebujemo za druge funkcije. Ta funkcija tega ne vrne.
        """
        if self.zaporedje[0]>0:
            # Nihče še ni pojedel t.i. zastrupljenega koščka.
            return NI_KONEC 
        else:
            return self.na_potezi
            
    def povleci_potezo(self, i, j):
        """Povleče potezo (i,j) oz. ne naredi nič, če ni veljavna.
           Vrne stanje_igre po potezi ali None, če je poteza neveljavna."""
        
        if (i,j) not in self.veljavne_poteze():
            """Ta poteza ni veljavna, zato jo lahko označimo kot None, ker bo to razred
            Gui zaznal kot neveljavno potezo"""
            return None
        else:
            # Pozicijo zapišemo v zgodovino:
            self.shrani_pozicijo()
            # Spremenimo self.zaporedje, ker povlečemo potezo in se pozicija
            # spremeni. Funkcija polepsaj zapiše pozicijo v ustrezni obliki.
            novi=self.polepsaj(i,j)#self.zaporedje, i, j)
            self.zaporedje = novi
            stanje=self.stanje_igre()
            # Če še ni konec igre, moramo zamenjati igralca, ki je na vrsti,
            # v vsakem primeru pa nato vrniti stanje igre
            if stanje == NI_KONEC:
                self.na_potezi = self.nasprotnik(self.na_potezi)
            else:
                self.na_potezi = KONEC
                # Igre je konec, nihče ne sme več narediti poteze.
            return stanje
 
    def razveljavi(self):
        """Funkcija razveljavi potezo. Potrebuje jo minimax."""
        (self.zaporedje, self.na_potezi)=self.zgodovina.pop()

    def polepsaj(self, i, j):#,zap, i, j):
        """ Funkcija vrne zaporedje, kakor izgleda po tem ko potegnemo potezo
(okrajša stolpce na višino i oz. jih pusti enake, če je i > trenutne višine).
Pobriše tudi ničle s konca. """
        if (i,j) == (0,0):
            return [0]
        else:
            novo = [x for x in self.zaporedje]
            for indeks in range(i, len(novo)):
                stara_vr = novo[indeks]
                novo[indeks] = min(stara_vr, j)
            novo = [x for x in novo if x != 0]
            return novo
       

    def nasprotnik(self,igralec):
        """Funkcija vrne nasprotnika igralca "igralec" """
        if igralec == IGRALEC_1:
            return IGRALEC_2
        elif igralec == IGRALEC_2:
            return IGRALEC_1
        else:
            assert False, "neveljaven nasprotnik"


#######################################################################
## Človek:

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        #Čakamo na to, da igralec klikne na ploščo
        pass

    def prekini(self):
        pass

    def klik(self, i, j):
        self.gui.povleci_potezo(i, j)
        # povleci_potezo je tu metoda v razredu Gui(), ki kliče metodo povleci_potezo v razredu Igra()         


#######################################################################
## Razred Racunalnik:
class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None

    def igraj(self):
        """ Ko računalniku povemo, naj igra, mora zagnati vzporedni thread, da
        v njem razmišlja, med tem ko originalni vodi igro. Podati moramo kopijo igre,
        saj med razmišljanjem računalnik vleče poteze, a le 'v glavi' """
        self.mislec = threading.Thread(
            target = lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
        self.mislec.start()

        self.gui.plosca.after(100, self.preveri_potezo)
        #Gui konstantno preverja, ali je računalnik že izračunal potezo.

    def preveri_potezo(self):
        """Pogleda, ali je že našel potezo. Če je, jo potegne, sicer preverja
        na vsakih 100 ms."""
        if self.algoritem.poteza is not None:
            i, j = self.algoritem.poteza
            self.gui.povleci_potezo(i,j)
            self.mislec = None      #ustavi razmišljanje - "ubije" thread
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        """Če recimo igralec želi začeti novo igro, moramo prekiniti
        razmišljanje v drugem threadu."""
        if self.mislec:
            logging.debug("Prekinjam {0}".format(self.mislec))
            self.algoritem.prekini()
            self.mislec.join()      # Počakamo, da se vlakno ustavi
            self.mislec = None

    def klik(self, i, j):
        """Če človek ni na potezi, klike na ploščo ignoriramo."""
        pass
        

#######################################################################
## Naključje:
class Nakljucje():
    def __init__(self, gui):
        self.gui = gui
        self.igra = None
        self.poteza = None # tuple!!
        self.prekinitev = False

    def izracunaj_potezo(self, igra):
        """Funkcija ne vrača ničesar. Pripravi in nadzira nadaljevanje."""
        self.igra = igra
        self.prekinitev = False
        self.poteza = None
        (poteza, vrednost) = self.nakljucje()
        self.igra = None
        if not self.prekinitev:
            logging.debug("Nakljucje: poteza{0}".format(poteza))
            self.poteza = poteza
          
    def nakljucje(self):
        """Glavna funkcija, vrača tuple (poteza, vrednost)"""
        if self.prekinitev:
            logging.debug("Nakljucje prekinja")
            return (None, 0) # Pri nakljucju vrednost poteze ni pomembna.
        stanje = self.igra.stanje_igre()
        if stanje in (IGRALEC_1, IGRALEC_2):
            """ Igre je konec. """
            if stanje == IGRALEC_2:
                return (None, 0)
            else:
                return (None, 0)
        elif stanje == NI_KONEC:
            return (self.zrebaj(), 0)
        else:
            assert False, "Nakljucje: nedefinirano stanje igre"

    def zrebaj(self):
        """Izmed veljavnih potez izbere naključno."""
        seznam=self.gui.igra.veljavne_poteze()
        if len(seznam)>1:
            novseznam=seznam[1:]
            return choice(novseznam)
        else:
            return seznam[0]

    def prekini(self):
        self.prekinitev = True

#######################################################################
## Medium:
class Rekurzija():
    def __init__(self, gui):
        self.gui = gui
        self.igra = None
        self.poteza = None # tuple!!
        self.prekinitev = False

    def izracunaj_potezo(self, igra):
        """Funkcija ne vrača ničesar. Pripravi in nadzira nadaljevanje."""
        self.igra = igra
        self.prekinitev = False
        self.poteza = None
        (poteza, vrednost) = self.rekurzija()
        self.igra = None
        if not self.prekinitev:
            logging.debug("Medium: poteza{0}".format(poteza))
            self.poteza = poteza
            
    def rekurzija(self):
        """glavna funkcija, ki kliče funkcija izračunaj, če igre ni konec in vrne potezo, ki naj jo odigra računalnik"""
        if self.prekinitev:
            logging.debug("Medium prekinja")
            return (None, 0) # Pri nakljucju vrednost poteze ni pomembna.
        stanje = self.igra.stanje_igre()
        if stanje in (IGRALEC_1, IGRALEC_2):
            """ Igre je konec. """
            if stanje == IGRALEC_2:
                return (None, 0)
            else:
                return (None, 0)
        elif stanje == NI_KONEC:
            return (self.izracunaj(), 0)
        else:
            assert False, "Rekurzija: nedefinirano stanje igre"

    def izracunaj(self):
        """funkcija izračunaj se kliče, ko igre ni konec in rekurzivno izračuna potezo, ki jo računalnik naj odigra"""
        veljavne=self.gui.igra.veljavne_poteze() #seznam veljavnih potez, ki jih izračuna igra
        zaporedje=self.gui.igra.zaporedje   #igralno polje, predstavljeno v obliki zaporedja
        povej=self.izracunaj_rekurzivno(veljavne,zaporedje)
        return(povej)
        
    def izracunaj_rekurzivno(self, veljavne,zaporedje):
        """"funkcija izračunaj1 preveri, če je polje 'L' oblike. Če je, igra 'simetrično', sicer se rekurzivno pokliče
        na polju brez prve vrstice in prvega stolpce"""
        if len(veljavne)>1:
            novseznam=veljavne[1:]
            if (1,1) not in novseznam:
                if zaporedje[0]==1 and zaporedje[1]>0:
                    return (1,0)
                elif len(zaporedje)==1 and zaporedje[0]>1:
                    return (0,1)
                else:
                    a=len(zaporedje)
                    b=zaporedje[0]
                    if a==b:
                        return (a-1,0)
                    elif a<b:
                        return (0,a)
                    else:
                        return (b,0)
            else:
                veljavne1=self.L_seznam(novseznam) #veljavne poteze brez polj v prvi vrstici in prvem stoplcu
                zaporedje1=self.L_zaporedje(zaporedje) #preurejeno zaporedje, zaporedje brez prve vrstice in prvega stolpa
                resitev=self.izracunaj_rekurzivno(veljavne1,zaporedje1)
                if resitev==(0,1):
                    return (1,2)
                elif resitev==(1,0):
                    return (2,1)
                else:
                    x=resitev[0]
                    y=resitev[1]
                    return (x+1,y+1) #(x,y) košček na polju brez prve vrstice in prvega stolpca,
                                     #je (x+1,y+1) košček na originalnem polju
        else:
            return veljavne[0]
        
    def L_zaporedje(self,zaporedje):
        """preuredi zaporedje v zaporedje brez prve vrstice in prvega stolpca"""
        novo=[]
        for i in zaporedje:
            if i>1:
                novo.append(i-1)
        return novo[1:]
        
    def L_seznam(self,seznam):
        """preuredi seznam vrednosti v senam vrednosti brez prve vrstice in prvega stolpca"""
        novi=[]
        for i,j in seznam:
            if i!=0 and j!=0:
                novi.append((i-1,j-1))
        return novi

    def prekini(self):
        self.prekinitev = True
        
######################################################################################
## Minimax:
class Minimax():
    def __init__(self, globina): # ne sme operirati z gui-em
        self.globina = globina # do katere globine iščemo
        self.prekinitev = False # ali je bila klicana funkcija prekini?
        self.igra = None # objekt, ki opisuje igro
        self.poteza = None # sem shrani izračunano potezo

    # Konstanti:
    ZMAGA = 1
    NESKONCNO = 2

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.prekinitev = False
        self.poteza = None
        (poteza, vrednost) = self.minimax(MINIMAX_GLOBINA,False)
        self.igra = None
        if not self.prekinitev:
            logging.debug("Minimax: poteza{0}".format(poteza))
            self.poteza = poteza

    def vrednost_pozicije(self):
    # Ocena pozicije
        if str(self.igra.zaporedje) in POZNANE_VREDNOSTI:
            return POZNANE_VREDNOSTI.get(str(self.igra.zaporedje))
        else:
            return 0
    
    def minimax(self, globina, maksimiziramo):
        """Glavna funkcija, vrača tuple (poteza, vrednost). Kličemo jo
rekurzivno, po algoritmu minimax."""
        if self.prekinitev:
            logging.debug("Minimax prekinja")
            return (None, 0)
        stanje = self.igra.stanje_igre()

# Igre je konec. Gledamo le, kdo je zmagal.
        if stanje in (IGRALEC_1,IGRALEC_2,KONEC):
            if (stanje == IGRALEC_1) or (self.igra.zgodovina[-1][1] == IGRALEC_1):
                return (None, -Minimax.ZMAGA)
            elif stanje == IGRALEC_2 or (self.igra.zgodovina[-1][1] == IGRALEC_2):
                return (None, Minimax.ZMAGA)
            else:
                pass

# Igre ni konec, iščemo potezo.
        elif stanje == NI_KONEC:
            if globina == 0:
                # Prišli smo do konca rekurzije in moramo oceniti pozicijo.
                return (None, self.vrednost_pozicije())
            else:
                # Nismo še na koncu rekurzije.
                poteze=self.igra.veljavne_poteze()
                shuffle(poteze)

                #MAKSIMIZIRAMO----------------------------------------------
                if maksimiziramo:
                    najvecja_vrednost = -Minimax.NESKONCNO
                    najmanjsa_vrednost = Minimax.NESKONCNO
                    najboljsa_poteza = None
                    for (i,j) in poteze:
                        self.igra.povleci_potezo(i,j)
                        if str(self.igra.zaporedje) in POZNANE_VREDNOSTI:
                            vrednost = -POZNANE_VREDNOSTI.get(str(self.igra.zaporedje))
                        else:
                            # Rekurzivni klic:
                            vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        if vrednost > najvecja_vrednost:
                            najvecja_vrednost=vrednost
                            najboljsa_poteza=(i,j)
                        if vrednost < najmanjsa_vrednost:
                            najmanjsa_vrednost=vrednost
                        self.igra.razveljavi()
                    if najmanjsa_vrednost == 1:
                        # Pozicija je zmagovalna
                        POZNANE_VREDNOSTI[str(self.igra.zaporedje)]=1
                    if najvecja_vrednost == -1:
                        # Pozicija je slaba
                        POZNANE_VREDNOSTI[str(self.igra.zaporedje)]=-1
                    # Sproti novo ugotovljene vrednosti zapisujemo v slovar v datoteko
                    # izven programa:
                    pickle.dump(POZNANE_VREDNOSTI, open("poznane_vrednosti.p", "wb"))
                    return (najboljsa_poteza, najvecja_vrednost)
                
                #MINIMIZIRAMO-------------------------------------------------
                else:
                    najmanjsa_vrednost = Minimax.NESKONCNO
                    najboljsa_poteza = None
                    for (i,j) in poteze:
                        self.igra.povleci_potezo(i,j)
                        if str(self.igra.zaporedje) in POZNANE_VREDNOSTI:
                            vrednost = POZNANE_VREDNOSTI.get(str(self.igra.zaporedje))
                        else:
                            # Rekurzivni klic:
                            vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        if vrednost < najmanjsa_vrednost:
                            najmanjsa_vrednost=vrednost
                            najboljsa_poteza=(i,j)
                        self.igra.razveljavi()
                    return (najboljsa_poteza, najmanjsa_vrednost)

#Imamo napačno stanje:
        else:
            pass
                

#####################################################################################################################################
## GUI:
class Gui():
    
    def __init__(self,master):
        self.koscki=[[None for i in range(20)] for j in range(20)] #polje(cokolado) predstavimo v obliki matrike (maksimum)
        #Glavni menu:
        menu = Menu(master)
        master.config(menu=menu)

        #nastavitev atributov
        self.tezavnost=None     #pomaga nam ob koncu igre, da ponovimo igro iste težavnosti
        self.clovek="clovek"

        #Podmenu za izbiro igre
        igra_menu = Menu(master)
        menu.add_cascade(label="Igra", menu=igra_menu)
        igra_menu.add_command(label="2 igralca",command=lambda: self.doloci_igralce(self.clovek)) # command mora bit funkcija
        igra_menu.add_command(label="Proti racunalniku (easy)",command=lambda: self.doloci_igralce(Nakljucje))
        igra_menu.add_command(label="Proti racunalniku (medium)", command=lambda: self.doloci_igralce(Rekurzija))
        igra_menu.add_command(label="Proti racunalniku (hard)", command=lambda: self.doloci_igralce(Minimax))
        igra_menu.add_command(label="Izhod",                      command=master.destroy)
        
        #Podmenu Nastavitve
        pomoc_menu = Menu(master)
        menu.add_cascade(label="Nastavitve", menu=pomoc_menu)
        pomoc_menu.add_command(label="Velikost čokolade", command=lambda: self.spremeni_visino_in_sirino(master))
        
        #Podmenu Pomoč
        pomoc_menu = Menu(master)
        menu.add_cascade(label="Pomoč", menu=pomoc_menu)
        pomoc_menu.add_command(label="Navodila igre", command=self.pomoc)

        #Naredimo polje z opisom stanja/pozicije:
        self.napis = StringVar(master, value="Kasneje bo tu pisalo, kateri igralec je na vrsti/kaj je bila zadnja poteza/kdo je zmagal")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        #pokličemo funkcijo, ki nam nariše polje
        self.pripravi_plosco(master)
        self.nova_igra(Racunalnik(self, Nakljucje(self)))   #na začetku nastavimo na algoritem Nakljucje
        
    def pripravi_plosco(self,master):
        #Naredimo polje za čokolado:
        self.plosca = Canvas(master, width=SIRINA*100 + 20, height=VISINA*100 + 60)
        self.plosca.grid(row=1, column=0)
        master.resizable(0,0)   # Onemogoči resize.
        self.plosca.bind("<Button-1>", self.plosca_klik)    #Klik na polje

#----------------------------------------------------------------------------------------------------------
#SPREMINJANJE VIŠINE IN ŠIRINE
    def spremeni_visino_in_sirino(self,master):
        """pomozna funkcija, ki spremeni visino in sirino igralnega polja oz. cokolade"""
        global VISINA
        global SIRINA

        # Ustvari novo okno za izbiro visine in sirine
        spremeni=Toplevel()
        spremeni.grab_set()                                   # Postavi fokus na okno in ga obdrži
        spremeni.title("Velikost čokolade")                   # Naslov okna
        spremeni.resizable(width=False, height=False)         # Velikosti okna ni mogoče spreminjati

        spremeni.grid_columnconfigure(0, minsize=40)          # Nastavitev minimalne širine ničtega stolpca
        spremeni.grid_columnconfigure(5, minsize=40)          # Nastavitev minimalne širine drugega stolpca
        spremeni.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        spremeni.grid_rowconfigure(6, minsize=10)             # Nastavitev minimalne višine šeste vrstice

        Label(spremeni, text="Velikost čokolade", font=("Helvetica", 20)).grid(row=0, column=1, columnspan=4)

        Label(spremeni, text="Visina:").grid(row=2, column=1, sticky="E")
        Label(spremeni, text="Sirina:").grid(row=3, column=1, sticky="E")

        visina = Entry(spremeni, font="Helvetica 12", width=10)  # Vnosno polje za visino
        visina.grid(row=2, column=2)                             # Pozicija polja za visino
        visina.insert(0, VISINA)                                 # Privzeta visina
        sirina = Entry(spremeni, font="Helvetica 12", width=10)  # Vnosno polje za sirino
        sirina.grid(row=3, column=2)                             # Pozicija polja za sirino
        sirina.insert(0, SIRINA)                                 # Privzeta sirina

        Label(spremeni, text= "vneseš lahko vrednosti med 1 in 15", 
        justify="left").grid(row=4, column=1, columnspan=4)

        # Gumba za začetek nove igre in preklic
        Button(spremeni, text="Prekliči", width=8, height=2,command= lambda: spremeni.destroy()).grid(row=5, column=1)
        Button(spremeni, text="Začni igro", width=8, height=2,command= lambda: visina_sirina(master)).grid(row=5, column=2)


        def visina_sirina(master):
            """funkcija, ki spremeni višino in širine tako, da zapre prejšnjo okno in odpre novo
na isti težavnosti kot prej"""
            global VISINA
            global SIRINA
            visi=uredi_vnos(visina.get())
            siri=uredi_vnos(sirina.get())
            if visi is not None:
                VISINA=visi
            if siri is not None:
                SIRINA=siri
            self.plosca.destroy()
            self.pripravi_plosco(master)
            self.preveri(self.tezavnost)
            spremeni.destroy()

        def uredi_vnos(stringa):
            """funkcija, ki preveri kaj smo napisali v polje in upošteva vnos le,
če je to število med 1 in 15"""
            for i in stringa:
                if i not in "0123456789":
                    return None
            if int(stringa) > 15:
                return None
            return int(stringa)

#-----------------------------------------------------------------------------------------------------------
#NAVODILA IGRE
        
    def pomoc(self):

        """ Ustvari okno z informacijami o igri. """
        self.pomoc = Toplevel()
        self.pomoc.title("Navodila igre")
        self.pomoc.resizable(width=False, height=False)

        self.pomoc.grid_columnconfigure(0, minsize=600)
        self.pomoc.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        self.pomoc.grid_rowconfigure(2, minsize=20)             # Nastavitev minimalne višine druge vrstice

        Label(self.pomoc, text="Navodila za igranje igre Chomp", font=("Helvetica", 20)).grid(row=0, column=0)

        Label(self.pomoc, text= "Igra se igra na pravokotni plošči dimenzije nxm (tablici čokolade), ki je\n"
                                "razdeljena na kvadratke. Igralca izmenično izbirata po en košček čokolade,\n"
                                "pri čemer morata nato pojesti izbran kvadratek in vse kvardratke, ki so \n"
                                "desno in pod njim. Kvadratek na zgornjem levem robu je zastrupljen. \n"
                                "Igralec, ki poje ta košček čokolade, izgubi.\n",
                 justify="left").grid(row=1, column=0)

    def plosca_klik(self, event):
        if event.x >= 10 and event.x<=SIRINA*100 + 10 and event.y >= 50 and event.y <= VISINA*100 + 50:
            i= (event.x -10)//100
            j= (event.y - 50)//100
            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_1.klik(i,j)
            elif self.igra.na_potezi == IGRALEC_2:
                self.igralec_2.klik(i,j)
            else:
                #nihce ni na potezi 
                pass
        else:
            self.napis.set('neveljavna poteza')

    def koscek(self,i,j,barva):
        """narise koscek čokolade na (i,j)-tem polju izbrane barve"""
        return self.plosca.create_rectangle(15 + j*100, 55 + i*100, 105 + j*100, 145 + i*100, fill=barva)

    def doloci_igralce(self,Igralec2):
        """funkcija, ki sprejme način igranja in v tem načinu požene igro"""
        if Igralec2==Nakljucje:
            igra=Racunalnik(self, Nakljucje(self))
        elif Igralec2==Rekurzija:
            igra=Racunalnik(self, Rekurzija(self))
        elif Igralec2==Minimax:
            igra=Racunalnik(self, Minimax(self))
        else:
            igra=Clovek(self)
        self.tezavnost=Igralec2
        self.nova_igra(igra)
        
    def nova_igra(self, Igralec_2,barva='sienna4'):
        """Vzpostavi zaèetno stanje. Igralec_1 je vedno človek."""
        
        #Pobrišemo vse s canvasa:
        self.plosca.delete(ALL)
        for i in range(VISINA+1):
            self.plosca.create_line(10, i*100 + 50, SIRINA*100 + 10, i*100 + 50) 
        for i in range(SIRINA+1):
            self.plosca.create_line(i*100+10, 50, i*100+10, VISINA*100 + 50)

        #Ustvarimo novo igro
        self.igra = Igra()

        #Določimo igralce
        self.igralec_1 = Clovek(self)
        self.igralec_2 = Igralec_2
        
        #Narišemo polje:
        for i in range(VISINA):
            for j in range(SIRINA):
                if i==0 and j==0:
                    self.koscek(0,0,'red')
                else:
                    self.koscki[i][j]=self.koscek(i,j,barva)
        
        #Prvi je na potezi človek
        self.napis.set("Ti si na potezi.")
        pass

    def povleci_potezo(self, i, j):
        """ Povlečemo potezo v razredu Igra. Le-ta spremeni, kdo naredi potezo, zato si moramo to zapomniti na začetku."""
        igralec = self.igra.na_potezi
        stanje = self.igra.povleci_potezo(i,j) # Ta metoda vrača stanje igre po potezi oz. None, če je neveljavna.
        if stanje is None:
            self.napis.set("Ta poteza ni veljavna.")
        else:
            # Poteza je veljavna. V igri smo jo že potegnili, zdaj moramo spremeniti še prikaz.
            self.pobrisi(i,j)
            if stanje == NI_KONEC: #tu ga še uporabiva
                # Potezo ima naslednji igralec. To moramo povedati na zaslonu in klicati metodo, da bo igral.
                if self.igra.na_potezi == IGRALEC_1:
                    self.napis.set("Na potezi je 1. igralec.")
                    self.igralec_1.igraj()
                elif self.igra.na_potezi == IGRALEC_2:
                    self.napis.set("Na potezi je 2. igralec.")
                    self.igralec_2.igraj()
            else:
                # stanje != NI_KONEC -> Igre je konec
                self.koncaj_igro()

    def pobrisi(self,i,j):
        """povleci_potezo preveri ali je veljavna in kliče pobrisi le ce je."""
        for k in range(j, VISINA):
            for l in range(i, SIRINA):
                if self.koscki[k][l]!=None:
                    self.plosca.delete(self.koscki[k][l])
        self.plosca.create_oval(i*100+20,j*100+60,i*100+25,j*100+65, fill='sienna4')
        self.plosca.create_oval(i*100+30,j*100+70,i*100+35,j*100+75, fill='sienna4')
        self.plosca.create_oval(i*100+20,j*100+70,i*100+25,j*100+75, fill='sienna4')
        self.plosca.create_oval(i*100+20,j*100+80,i*100+25,j*100+85, fill='sienna4')
        self.plosca.create_oval(i*100+30,j*100+60,i*100+35,j*100+65, fill='sienna4')
        self.plosca.create_oval(i*100+40,j*100+60,i*100+45,j*100+65, fill='sienna4')

    def koncaj_igro(self):
        """funkcija, ki preveri kdo je zmagovalec igre ter odpre končno okno o končani igri"""
        igralec=self.igra.nasprotnik(self.igra.zgodovina[-1][1])
        self.napis.set("Igre je konec. Zmagal je {0}. igralec".format(igralec))
        if igralec == IGRALEC_1:
            self.koncno_okno(igralec)
        else:
            self.koncno_okno(igralec)

    def koncno_okno(self,igralec):
        """funkcija, ki odpre končno okno, v katerem so podatki o uspešnosti v igri"""
        if self.tezavnost==None or str(self.tezavnost)=="<class '__main__.Nakljucje'>" or str(self.tezavnost)=="<class '__main__.Rekurzija'>" or str(self.tezavnost)=="<class '__main__.Minimax'>":
            napis= "Čestitam, zmagal/a si :)" if igralec == IGRALEC_1 else "Izgubil/a si. Več sreče prihodnjič"
        else:
            napis="zmagal je igralec " + str(igralec)
        
        self.konec = Toplevel()
        self.konec.title("Konec igre")
        self.konec.resizable(width=False, height=False)

        self.konec.grid_columnconfigure(0, minsize=45)
        self.konec.grid_columnconfigure(3, minsize=45)
        self.konec.grid_rowconfigure(0, minsize=60)             # Nastavitev minimalne višine ničte vrstice
        self.konec.grid_rowconfigure(3, minsize=45)             # Nastavitev minimalne višine druge vrstice

        Label(self.konec, text=napis, font=("Helvetica", 20),justify='center').grid(row=0, column=1, columnspan =2,sticky=E+W+N+S)

        Label(self.konec, text= "Želiš igrati ponovno?",
                 justify="center").grid(row=1, column=1, columnspan =2,sticky=E+W+N+S)        
    
        gumb_da=Button(self.konec, text="da",width=8, height=2,command=self.combine_funcs(lambda: self.preveri(self.tezavnost),self.konec.destroy))
        gumb_da.grid(row=3,column=1)
        
        gumb_ne=Button(self.konec, text="ne",width=8, height=2, command=self.konec.destroy)
        gumb_ne.grid(row=3,column=2)
        
    def combine_funcs(self,*funcs):
        """ funkcija, zduži dve ali več funkcij v eno """
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def preveri(self,tezavnost):
        """preveri na kateri težavnosti igramo, da ob ponovitvi
igre ali spremembi velikosti polja težavnost ostane enaka"""
        if self.tezavnost == None:
            self.nova_igra(Racunalnik(self,Nakljucje(self)))
        elif str(self.tezavnost) == "<class '__main__.Nakljucje'>":
            self.nova_igra(Racunalnik(self,Nakljucje(self)))
        elif str(self.tezavnost) == "<class '__main__.Rekurzija'>":
            self.nova_igra(Racunalnik(self,Rekurzija(self)))
        elif str(self.tezavnost) == "<class '__main__.Minimax'>":
            self.nova_igra(Racunalnik(self,Minimax(self)))
        else:
            self.nova_igra(Clovek(self))

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Vlaknom, ki tečejo vzporedno, je treba sporočiti, da morajo
        # končati, sicer se bo okno zaprlo, aplikacija pa bo še vedno
        # delovala.
        if self.Igralec_2:
            self.Igralec_2.prekini()
        # Dejansko zapremo okno.
        master.destroy()

#####################################################
## Glavni program
if __name__ == "__main__":
    root = Tk()
    root.title("Chomp")
    aplikacija = Gui(root)
    root.mainloop()
