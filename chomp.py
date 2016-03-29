from tkinter import *
from random import *
import threading
#import argparse - kasneje bova rabili
import logging
import pickle

SIRINA=7
VISINA=5
IGRALEC_1 = "1"
IGRALEC_2 = "2"
NI_KONEC = "ni konec"

MINIMAX_GLOBINA = 3

#premaknila sem jo v razred Igra
##def nasprotnik(igralec):
##    if igralec == IGRALEC_1:
##        return IGRALEC_2
##    elif igralec == IGRALEC_2:
##        return IGRALEC_1
##    else:
##        assert False, "neveljaven nasprotnik"

#Premaknila sem jo v razred Igra
##def polepsaj(zap, i, j):
##    # Funkcija vrne zaporedje, kakor izgleda po tem ko potegnemo
##    # potezo (okrajša stolpce na višino i oz. jih pusti enake, če
##    # je i > trenutne višine). Pobriše tudi ničle s konca.
##    if (i,j) == (0,0):
##        return [0]
##    else:
##        novo = [x for x in zap]
##        for indeks in range(i, len(novo)):
##            stara_vr = novo[indeks]
##            #print(indeks)
##            novo[indeks] = min(stara_vr, j)
##        novo = [x for x in novo if x != 0]
##        #print ("Izpisujem zaporedje po potezi ({0}, {1}): {2}".format(i,j,novo))
##        return novo

######################################################################
## Razred Igra

class Igra():
    
    def __init__(self):
        self.zaporedje=[VISINA for i in range(SIRINA)]
        self.koscki=[[None for i in range(SIRINA)] for j in range(VISINA)] #tega tudi verjetno več ne rabiva
        # Ustvarimo si matriko z enakimi dimenzijami kot čokolada, v kateri
        # si bomo zapomnili, katere koščke sta igralca že pojedla.
        
        self.na_potezi = IGRALEC_1 # Vedno igro odpre človek.
        
        self.zgodovina = []
        # Zgodovina igre je prazna, ko igro začnemo (ne glede na to, ali
        # smo prej že kaj igrali).

    def shrani_pozicijo(self):
        zap=self.zaporedje
        self.zgodovina.append((zap, self.na_potezi))
        #print("Izpisujem zgodovino:")
        #print(self.zgodovina)

    def kopija(self):
        k=Igra()
        k.zaporedje = self.zaporedje
        k.na_potezi = self.na_potezi
        return k

    def veljavne_poteze(self):
        #print(self.zaporedje)
        poteze=[]
        for j in range(len(self.zaporedje)):
            for i in range(self.zaporedje[j]):
                poteze.append((j,i))
        #print(poteze)
        return poteze

    def stanje_igre(self):
        """
        Ugotovi, kakšno je stanje igre. Vrne:
            - IGRALEC_1, če je igre konec in je zmagal IGRALEC_1 (uporabik)
            - IGRALEC_2, če je igre konec in je zmagal IGRALEC_2 (človek/računalnik)
            - NI_KONEC, če igre še ni konec
        """
        if self.zaporedje[0]>0:
            # Nihče še ni pojedel t.i. zastrupljenega koščka.
            return NI_KONEC
        else:
            return self.na_potezi
            # Mogoče bo treba popravit v nasprotnika, če bo metoda
            # povleci_potezo spremenila igralca, po tem ko bo potegnila
            # potezo.
            
    def povleci_potezo(self, i, j):
        """Povleče potezo (i,j) oz. ne naredi nič, če ni veljavna.
           Vrne stanje_igre po potezi ali None, če je poteza neveljavna."""
        
        if (i,j) not in self.veljavne_poteze():
            """ta poteza ni veljavna, zato jo lahko označimo kot None, ker bo to razred
            Gui zaznal kot neveljavno potezo"""
            assert False, "To je neveljavna poteza"
            return None
###############################        
##to je bilo prej        
##        if (len(self.zaporedje)<=i) or (self.zaporedje[i]<j) :
##            #povleči hočemo neveljavno potezo
##            assert False, "To je neveljavna poteza"
##            #return None
###############################
        else:
            # Pozicijo zapišemo v zgodovino:
            self.shrani_pozicijo()
            # Spremenimo self.zaporedje, ker povlečemo potezo in se pozicija
            # spremeni:
            novi=self.polepsaj(self.zaporedje, i, j)
            print(novi)
            self.zaporedje = novi
            stanje=self.stanje_igre()
            # Če še ni konec igre, moramo zamenjati igralca, ki je na vrsti,
            # v vsakem primeru pa nato vrniti stanje igre
            if stanje == NI_KONEC:
                self.na_potezi = self.nasprotnik(self.na_potezi)
            else:
                self.na_potezi = None
                # Igre je konec, nihče ne sme več narediti poteze.
            return stanje

    def razveljavi(self):
        (self.zaporedje, self.na_potezi)=self.zgodovina.pop()

    def polepsaj(self,zap, i, j):
    # Funkcija vrne zaporedje, kakor izgleda po tem ko potegnemo
    # potezo (okrajša stolpce na višino i oz. jih pusti enake, če
    # je i > trenutne višine). Pobriše tudi ničle s konca.
        if (i,j) == (0,0):
            return [0]
        else:
            novo = [x for x in zap]
            for indeks in range(i, len(novo)):
                stara_vr = novo[indeks]
                #print(indeks)
                novo[indeks] = min(stara_vr, j)
            novo = [x for x in novo if x != 0]
            #print ("Izpisujem zaporedje po potezi ({0}, {1}): {2}".format(i,j,novo))
            return novo

    def nasprotnik(self,igralec):
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
#        print(algoritem)

    def igraj(self):
        self.mislec = threading.Thread(
            target = lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        self.mislec.start()

        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        if self.algoritem.poteza is not None:
            i, j = self.algoritem.poteza
            self.gui.povleci_potezo(i,j)
            self.mislec = None
            #ustavi razmišljanje - "ubije" thread
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        if self.mislec:
            logging.debug("Prekinjam {0}".format(self.mislec))
            self.algoritem.prekini()
            self.mislec.join() # Počakamo, da se vlakno ustavi
            self.mislec = None

    def klik(self, i, j):
        pass
        # povleci_potezo je tu metoda v razredu Gui(), ki kliče metodo
        # povleci_potezo v razredu Igra()
        

#######################################################################
## Naključje:
class Nakljucje():
    def __init__(self, gui):
        self.gui = gui
        self.igra = None
        self.poteza = None # tuple!!
        self.prekinitev = False

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.prekinitev = False
        self.poteza = None
        (poteza, vrednost) = self.nakljucje()
        self.igra = None
        if not self.prekinitev:
            logging.debug("Nakljucje: poteza{0}".format(poteza))
            self.poteza = poteza
        #else:
            #print("Klicana je bila prekinitev")
            

    def nakljucje(self):
        if self.prekinitev:
            logging.debug("Nakljucje prekinja")
            return (None, 0) # Pri nakljucju vrednost poteze ni pomembna.
        stanje = self.igra.stanje_igre()
        if stanje in (IGRALEC_1, IGRALEC_2):
            """ Igre je konec. """
            if stanje == IGRALEC_2:
                return (None, 0)#Nakljucje.ZMAGA)
            else:
                return (None, 0)#-Nakljucje.ZMAGA)
        elif stanje == NI_KONEC:
            return (self.zrebaj(), 0)
        else:
            assert False, "Nakljucje: nedefinirano stanje igre"

    def zrebaj(self):
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
class Medium():
    def __init__(self, gui):
        self.gui = gui
        self.igra = None
        self.poteza = None # tuple!!
        self.prekinitev = False

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.prekinitev = False
        self.poteza = None
        (poteza, vrednost) = self.medium()
        self.igra = None
        if not self.prekinitev:
            logging.debug("Medium: poteza{0}".format(poteza))
            self.poteza = poteza
        #else:
            #print("Klicana je bila prekinitev")
            

    def medium(self):
        if self.prekinitev:
            logging.debug("Medium prekinja")
            return (None, 0) # Pri nakljucju vrednost poteze ni pomembna.
        stanje = self.igra.stanje_igre()
        if stanje in (IGRALEC_1, IGRALEC_2):
            """ Igre je konec. """
            if stanje == IGRALEC_2:
                return (None, 0)#Nakljucje.ZMAGA)
            else:
                return (None, 0)#-Nakljucje.ZMAGA)
        elif stanje == NI_KONEC:
            return (self.zrebaj(), 0)
        else:
            assert False, "Medium: nedefinirano stanje igre"

    def zrebaj(self):
        seznam=self.gui.igra.veljavne_poteze()
        if len(seznam)>1:
            novseznam=seznam[1:]
            return choice(novseznam)
        else:
            return seznam[0]

    def prekini(self):
        self.prekinitev = True

#######################################################################
## Minimax:
class Minimax():
    def __init__(self, globina): # ne sme operirati z gui-em
        self.globina = globina # do katere globine iščemo
        self.prekinitev = False # ali je bila klicana funkcija prekini?
        self.igra = None # objekt, ki opisuje igro
        # Verjetno ne bova potrebovali: self.jaz = IGRALEC_2
        self.poteza = None # sem shrani izračunano potezo


    ZMAGA = 10000
    NESKONCNO = ZMAGA + 1

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
##        self.igra = igra
##        self.prekinitev = False
##        self.poteza = None
##        (poteza, vrednost) = self.minimax()
##        self.igra = None
##        if not self.prekinitev:
##            logging.debug("Nakljucje: poteza{0}".format(poteza))
##            self.poteza = poteza
        pass

    def vrednost_pozicije(self):
        ### Ne moreš dat seznama za ključ v slovarju!!!!
        pass
    
    def minimax(self, globina, maksimiziramo):
        if self.prekinitev:
            logging.debug("Minimax prekinja")
            return (None, 0)
        stanje = self.igra.stanje_igre()
        if stanje in (IGRALEC_1, IGRALEC_2):
            """ Igre je konec. """
            if stanje == IGRALEC_2:
                return (None, -Minimax.ZMAGA)
            else:
                return (None, Minimax.ZMAGA)
        elif stanje == NI_KONEC:
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                poteze = self.igra.veljavne_poteze()
                if maksimiziramo:
                    najvecja_vrednost = -Minimax.NESKONCNO
                    najboljsa_poteza = None
                    for p in poteze:
                        # Računamo, kaj se zgodi če potezo povlečemo
                        self.igra.povleci_potezo(p)
                        # Kakšna je največja možna vrednost poteze pri vseh možnih nadaljevanjih,
                        # nam pove minimax, ki vrača (poteza, vrednost) - zato gledamo le 2.
                        # element v tuple-u.
                        vrednost=self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > najvecja_vrednost:
                            najboljsa_poteza = p
                            najvecja_vrednost = vrednost
                else:
                    najmanjsa_vrednost = Minimax.NESKONCNO
                    najboljsa_poteza = None
                    for p in poteze:
                        # Računamo, kaj se zgodi če potezo povlečemo
                        self.igra.povleci_potezo(p)
                        # Kakšna je največja možna vrednost poteze pri vseh možnih nadaljevanjih,
                        # nam pove minimax, ki vrača (poteza, vrednost) - zato gledamo le 2.
                        # element v tuple-u.
                        vrednost=self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < najvecja_vrednost:
                            najboljsa_poteza = p
                            najmanjsa_vrednost = vrednost
                        
                    
        else:
            assert False, "Nakljucje: nedefinirano stanje igre"
        
        pass

#####################################################################################################################################
## GUI:
class Gui():
    
    def __init__(self,master):
        self.koscki=[[None for i in range(SIRINA)] for j in range(VISINA)]
        #Glavni menu:
        menu = Menu(master)
        master.config(menu=menu)

##        #nastavitev atributov
##        self.pomoc=None  # Okno za pomoč pri igranju igre, ko ni odprto je None.
        self.ime_1="ig 1"
        self.ime_2="ig 2"

        #Podmenu za izbiro igre
        igra_menu = Menu(master)
        menu.add_cascade(label="Igra", menu=igra_menu)

        #Podmenu Nastavitve
        pomoc_menu = Menu(master)
        menu.add_cascade(label="Nastavitve", menu=pomoc_menu)
        pomoc_menu.add_command(label="Igralno polje", command=self.spremeni_visino_in_sirino)

        #Podmenu Pomoč
        pomoc_menu = Menu(master)
        menu.add_cascade(label="Pomoč", menu=pomoc_menu)
        pomoc_menu.add_command(label="Navodila igre", command=self.pomoc)

        igra_menu.add_command(label="2 igralca",command=lambda: self.nova_igra(Clovek(self)))
        # command mora bit funkcija
        igra_menu.add_command(label="Proti racunalniku (easy)",command=lambda: self.nova_igra(Racunalnik(self, Nakljucje(self))))
        igra_menu.add_command(label="Proti racunalniku (medium)", command=lambda: self.nova_igra(Racunalnik(self, Medium(self))))
        igra_menu.add_command(label="Proti racunalniku (hard)")#, command=lambda: self.nova_igra(Racunalnik(self, Minimax(self))))
        igra_menu.add_command(label="Izhod",                      command=master.destroy)

        #Naredimo polje z opisom stanja/pozicije:
        self.napis = StringVar(master, value="Kasneje bo tu pisalo, kateri igralec je na vrsti/kaj je bila zadnja poteza/kdo je zmagal")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        self.plosca = Canvas(master, width=SIRINA*100 + 20, height=VISINA*100 + 60)
#        self.plosca(master,fill=BOTH, expand=YES)
        self.plosca.grid(row=1, column=0)

        #Naredimo polje za čokolado:
##        self.plosca = Canvas(master, width=SIRINA*100 + 20, height=VISINA*100 + 60)
##        self.plosca.grid(row=1, column=0)
        
        self.nova_igra(Racunalnik(self, Nakljucje(self)))#Clovek(self))
        
        #Klik na polje
        self.plosca.bind("<Button-1>", self.plosca_klik)

    def spremeni_visino_in_sirino(self):
        """pomozna funkcija, ki spremeni visino in sirino igralnega polja oz. cokolade"""
        print("spreminjam visino in sirino")
        global VISINA
        global SIRINA

        # Ustvari novo okno za izbiro visine in sirine
        spremeni=Toplevel()
        spremeni.grab_set()                                   # Postavi fokus na okno in ga obdrži
        spremeni.title("Nastavitve igralnega polja")                # Naslov okna
        spremeni.resizable(width=False, height=False)         # Velikosti okna ni mogoče spreminjati

        spremeni.grid_columnconfigure(0, minsize=40)         # Nastavitev minimalne širine ničtega stolpca
        spremeni.grid_columnconfigure(5, minsize=40)         # Nastavitev minimalne širine drugega stolpca
        spremeni.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        spremeni.grid_rowconfigure(6, minsize=10)             # Nastavitev minimalne višine šeste vrstice

        Label(spremeni, text="Nastavitve igralnega polja", font=("Helvetica", 20)).grid(row=0, column=1, columnspan=4)

        Label(spremeni, text="Visina:").grid(row=2, column=1, sticky="E")
        Label(spremeni, text="Sirina:").grid(row=3, column=1, sticky="E")

        visina = Entry(spremeni, font="Helvetica 12", width=10)  # Vnosno polje za visino
        visina.grid(row=2, column=2)
        visina.insert(0, VISINA)                                     # Privzeta visina
        sirina = Entry(spremeni, font="Helvetica 12", width=10)  # Vnosno polje za sirino
        sirina.grid(row=3, column=2)
        sirina.insert(0, SIRINA)                                     # Privzeta sirina
        # ---------------------------------------------------------

        # Gumba za začetek nove igre in preklic
        Button(spremeni, text="Prekliči", width=8, height=2,command= lambda: spremeni.destroy()).grid(row=4, column=1)
        Button(spremeni, text="Začni igro", width=8, height=2,command= lambda: visina_sirina()).grid(row=4, column=2)

        def visina_sirina():
            global VISINA
            global SIRINA
            vi=visina.get()
            si=sirina.get()
            visi=uredi_vnos(vi)
            siri=uredi_vnos(si)
            if visi is not None:
                visin=visi
            else:
                visin=VISINA
            if siri is not None:
                sirin=siri
            else:
                sirin=SIRINA
            VISINA=visin
            SIRINA=sirin
            self.nova_igra(Racunalnik(self, Nakljucje(self)))
            spremeni.destroy()
            
            print(visin,sirin)

        def uredi_vnos(stringa):
            for i in stringa:
                if i not in "0123456789":
                    return None
            return int(stringa)

    def pomoc(self):

        def preklici():
            """Pomožna funkcija, ki zapre okno in nastavi atribut self.help na None."""
            self.pomoc.destroy()
            self.pomoc = None

        # Preveri, če je okno že ustvarjeno, če je ga da na vrh in se vrne.
##        if self.pomoc is not None:
##            pass
##            self.pomoc.lift()
##            pass

        # Ustvari okno z informacijami o igri.
        self.pomoc = Toplevel()
        self.pomoc.title("Navodila igre")
        self.pomoc.resizable(width=False, height=False)
        self.pomoc.protocol("WM_DELETE_WINDOW", preklici)

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
##############################
#je ta del res potreben? v tem primeru je namreč self.igralec_2.klik(i,j) vedno none.
            elif self.igra.na_potezi == IGRALEC_2:
                self.igralec_2.klik(i,j)
            else:
 #                nihce ni na potezi 
                pass
    
        else:
            self.napis.set('neveljavna poteza')

    def koscek(self,i,j,barva):
        """narise koscek čokolade na (i,j)-tem polju izbrane barve"""
        return self.plosca.create_rectangle(15 + j*100, 55 + i*100, 105 + j*100, 145 + i*100, fill=barva)

    def nova_igra(self, Igralec_2):
        print('zaganjam novo igro')
#        print(Igralec_2)
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
        #print(Igralec_2)
        #print(self.igralec_2)
        #print(type (self.igralec_2))
        
        #Narišemo polje:
        for i in range(VISINA):
            for j in range(SIRINA):
                if i==0 and j==0:
                    self.koscek(0,0,'red')
                else:
                    self.koscki[i][j]=self.koscek(i,j,'sienna4')
        
        #Prvi je na potezi človek
        self.napis.set("Ti si na potezi.")
        pass

    def povleci_potezo(self, i, j):
        #Povlečemo potezo v razredu Igra. Le-ta spremeni, kdo naredi potezo, zato si moramo to zapomniti na začetku.
        igralec = self.igra.na_potezi
        stanje = self.igra.povleci_potezo(i,j) # Ta metoda vrača stanje igre po potezi oz. None, če je neveljavna.
        if stanje is None:
            self.napis.set("Ta poteza ni veljavna.")
        else:
            # Poteza je veljavna. V igri smo jo že potegnili, zdaj moramo spremeniti še prikaz.
            self.pobrisi(i,j)
            if stanje == NI_KONEC:
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
    ##povleci_potezo preveri ali je veljavna in kliče pobrisi le ce je.
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
        igralec=nasprotnik(self.igra.zgodovina[-1][1])
        print(igralec)
        if igralec == "1":
            print("čestitam, zmagal/a si!")
            self.koncno_okno(igralec)
        else:
            print("nope")
            self.koncno_okno(igralec)
        self.napis.set("Igre je konec. Zmagal je {0}. igralec".format(nasprotnik(self.igra.zgodovina[-1][1])))
        #pass

    def koncno_okno(self,igralec):
        #print(igralec)
        #print("uspelo mi je")
        napis= "Čestitam, zmagal/a si :)" if igralec == "1" else "Izgubil/a si. Več sreče prihodnjič"
        
        def combine_funcs(*funcs):
            def combined_func(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combined_func
        
        self.konec = Toplevel()
        self.konec.title("Konec igre")
        self.konec.resizable(width=False, height=False)
        self.konec.protocol("WM_DELETE_WINDOW", self.konec.destroy)

        self.konec.grid_columnconfigure(0, minsize=45)
        self.konec.grid_columnconfigure(3, minsize=45)
        self.konec.grid_rowconfigure(0, minsize=60)             # Nastavitev minimalne višine ničte vrstice
        self.konec.grid_rowconfigure(3, minsize=45)             # Nastavitev minimalne višine druge vrstice

        Label(self.konec, text=napis, font=("Helvetica", 20),justify='center').grid(row=0, column=1, columnspan =2,sticky=E+W+N+S)

        Label(self.konec, text= "Želiš igrati ponovno?",
                 justify="center").grid(row=1, column=1, columnspan =2,sticky=E+W+N+S)
    
        gumb_da=Button(self.konec, text="da",width=8, height=2,command=combine_funcs(lambda: self.nova_igra(Racunalnik(self, Nakljucje(self))),self.konec.destroy))
        gumb_da.grid(row=3,column=1)
        
        gumb_ne=Button(self.konec, text="ne",width=8, height=2, command=self.konec.destroy)
        gumb_ne.grid(row=3,column=2)
        

#####################################################
## Glavni program
if __name__ == "__main__":
    root = Tk()
    root.title("Chomp")
    aplikacija = Gui(root)
    root.mainloop()
