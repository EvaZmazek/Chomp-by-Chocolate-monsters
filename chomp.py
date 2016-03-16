from tkinter import *
from random import *
SIRINA=7
VISINA=5
IGRALEC_1 = "1"
IGRALEC_2 = "2"
NI_KONEC = "ni konec"

def nasprotnik(igralec):
    if igralec == IGRALEC_1:
        return IGRALEC_2
    else:
        return IGRALEC_1

    

######################################################################
## Razred Igra

class Igra():
    
    def __init__(self):
        self.koscki=[[None for i in range(SIRINA)] for j in range(VISINA)]
        # Ustvarimo si matriko z enakimi dimenzijami kot čokolada, v kateri
        # si bomo zapomnili, katere koščke sta igralca že pojedla.
        
        self.na_potezi = IGRALEC_1 # Vedno igro odpre človek.
        
        self.zgodovina = []
        # Zgodovina igre je prazna, ko igro začnemo (ne glede na to, ali
        # smo prej že kaj igrali).

    def shrani_pozicijo(self):
        p = [self.koscki[i][:] for i in range(VISINA)]
        self.zgodovina.append((p, self.na_potezi))
        #print("Izpisujem zgodovino:")
        #print(self.zgodovina)

    def veljavne_poteze(self):
        poteze=[]
        for j in range(VISINA):
            for i in range(SIRINA):
                if self.koscki[j][i] is None:
                    poteze.append((i,j))
        return poteze

    def stanje_igre(self):
        """
        Ugotovi, kakšno je stanje igre. Vrne:
            - IGRALEC_1, če je igre konec in je zmagal IGRALEC_1 (uporabik)
            - IGRALEC_2, če je igre konec in je zmagal IGRALEC_2 (človek/računalnik)
            - NI_KONEC, če igre še ni konec
        """
        if self.koscki[0][0] is None:
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
        if self.koscki[j][i] is not None:
            #povleči hočemo neveljavno potezo
            return None
        else:
            self.shrani_pozicijo()
            polnilo=self.na_potezi
            for b in range(i,SIRINA):
                for a in range(j,VISINA):
                    self.koscki[a][b] = polnilo
                    # Na mesta v matriki plosca, ki jih poje igralec 1 (ali 2),
                    # vpišemo 1-ke (oz. 2-ke)
            stanje=self.stanje_igre()
            # Če še ni konec igre, moramo zamenjati igralca, ki je na vrsti,
            # v vsakem primeru pa nato vrniti stanje igre
            if stanje == NI_KONEC:
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                self.na_potezi = None
                # Igre je konec, nihče ne sme več narediti poteze.
            return stanje                

#######################################################################
## Človek:

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        #Čakamo na to, da igralec klikne na ploščo
        pass

    def klik(self, i, j):
        self.gui.povleci_potezo(i, j)
        # povleci_potezo je tu metoda v razredu Gui(), ki kliče metodo povleci_potezo v razredu Igra()         

#######################################################################
## Naključje:
class Nakljucje():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        i,j=self.zrebaj()
        self.gui.povleci_potezo(i,j)

    def zrebaj(self):
        seznam=self.gui.igra.veljavne_poteze()
        if len(seznam)>1:
            novseznam=seznam[1:]
            return choice(novseznam)
        else:
            return seznam[0]

    def klik(self, i, j):
        pass
        # povleci_potezo je tu metoda v razredu Gui(), ki kliče metodo povleci_potezo v razredu Igra()

#######################################################################
## Minimax:
class Minimax():
    def __init__(self,gui):
        self.gui = gui

    def igraj(self):
        pass

    def vrednost_pozicije(self):
        pass

    def klik(self, i, j):
        pass
        # povleci_potezo je tu metoda v razredu Gui(), ki kliče metodo povleci_potezo v razredu Igra()

#######################################################################

class Gui():
    
    def __init__(self,master):
        self.koscki=[[None for i in range(SIRINA)] for j in range(VISINA)]
        #Glavni menu:
        menu = Menu(master)
        master.config(menu=menu)

        #Podmenu za izbiro igre
        igra_menu = Menu(master)
        menu.add_cascade(label="Igra", menu=igra_menu)

        igra_menu.add_command(label="2 igralca",command=lambda: self.nova_igra(Clovek))
        # command mora bit funkcija
        igra_menu.add_command(label="Proti racunalniku (easy)",command=lambda: self.nova_igra(Nakljucje))
        igra_menu.add_command(label="Proti racunalniku (medium)")#, command=lambda: self.nova_igra(Minimax))
        igra_menu.add_command(label="Proti racunalniku (hard)")#,   command=#lambda: self.nova_igra(AlfaBeta))
        igra_menu.add_command(label="Izhod",                      command=master.destroy)

        #Naredimo polje z opisom stanja/pozicije:
        self.napis = StringVar(master, value="Kasneje bo tu pisalo, kateri igralec je na vrsti/kaj je bila zadnja poteza/kdo je zmagal")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        #Naredimo polje za čokolado:
        self.plosca = Canvas(master, width=SIRINA*100 + 20, height=VISINA*100 + 60)
        self.plosca.grid(row=1, column=0)
        
        self.nova_igra(Clovek)
        
        #Klik na polje
        self.plosca.bind("<Button-1>", self.plosca_klik)

    def plosca_klik(self, event):
        if event.x >= 10 and event.x<=SIRINA*100 + 10 and event.y >= 50 and event.y <= VISINA*100 + 50:
            i= (event.x -10)//100
            j= (event.y - 50)//100
            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_1.klik(i,j)
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
        self.igralec_2 = Igralec_2(self)
        
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
            #print("Klical sem pobrisi({0},{1})".format(i,j))
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
        if i==0 and j==0:
            self.napis.set('raje pojej nezastrupljen košček čokolade')
            #print("Ne brišem.")
        elif self.igra.koscki[j][i] is None:
            self.napis.set('ups, ta košček čokolade je nekdo že pojedel')
            #print("Ne brišem, ker me je baje nekdo prehitel.")
        else:
            for k in range(VISINA-j):
                for l in range(SIRINA-i):
                    if self.koscki[j][i+l]!=None:
                            self.plosca.delete(self.koscki[j+k][i+l])
                    """nariše drobtine"""
            self.plosca.create_oval(i*100+20,j*100+60,i*100+25,j*100+65, fill='sienna4')
            self.plosca.create_oval(i*100+30,j*100+70,i*100+35,j*100+75, fill='sienna4')
            self.plosca.create_oval(i*100+20,j*100+70,i*100+25,j*100+75, fill='sienna4')
            self.plosca.create_oval(i*100+20,j*100+80,i*100+25,j*100+85, fill='sienna4')
            self.plosca.create_oval(i*100+30,j*100+60,i*100+35,j*100+65, fill='sienna4')
            self.plosca.create_oval(i*100+40,j*100+60,i*100+45,j*100+65, fill='sienna4')

    def koncaj_igro(self):
        self.napis.set("Igre je konec. Zmagal je {0}. igralec".format(nasprotnik(self.igra.zgodovina[-1][1])))
        #pass



#####################################################
## Glavni program
if __name__ == "__main__":
    root = Tk()
    root.title("Chomp")
    aplikacija = Gui(root)
    root.mainloop()
