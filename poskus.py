from tkinter import *
SIRINA=6
VISINA=5
neveljavne_poteze=set()
kliki=set()
class Gui():
    
    def __init__(self,master):
        #Glavni menu:
        menu = Menu(master)
        master.config(menu=menu)

        #Podmenu za izbiro igre
        igra_menu = Menu(master)
        menu.add_cascade(label="Igra", menu=igra_menu)

        igra_menu.add_command(label="2 igralca", command=self.nova_igra)#mora bit funkcija
        #Popravi, da bo za razlicne stile igre
        igra_menu.add_command(label="Proti racunalniku (easy)",   command=self.nova_igra)
        igra_menu.add_command(label="Proti racunalniku (medium)", command=self.nova_igra)
        igra_menu.add_command(label="Proti racunalniku (hard)",   command=self.nova_igra)
        igra_menu.add_command(label="Izhod",                      command=master.destroy)

        #Naredimo polje z opisom stanja/pozicije:
        self.napis = StringVar(master, value="Kasneje bo tu pisalo, kateri igralec je na vrsti/kaj je bila zadnja poteza/kdo je zmagal")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        #Naredimo polje za čokolado:
        self.plosca = Canvas(master, width=SIRINA*100 + 20, height=VISINA*100 + 60)
        self.plosca.grid(row=1, column=0)
        
        for i in range(VISINA+1):
            self.plosca.create_line(10, i*100 + 50, SIRINA*100 + 10, i*100 + 50)
        for i in range(SIRINA+1):
            self.plosca.create_line(i*100+10, 50, i*100+10, VISINA*100 + 50)

        self.nova_igra()
        
        #Klik na polje
        self.plosca.bind("<Button-1>", self.plosca_klik)

    def ime_koscka(self,i,j):
        return 'koscek('+str(i)+','+str(j)+')'

    def plosca_klik(self, event):
        if event.x >= 10 and event.x<=SIRINA*100 + 10 and event.y >= 50 and event.y <= VISINA*100 + 50:
            i= (event.x -10)//100
            j= (event.y - 50)//100
            if i==0 and j==0:
                self.napis.set('raje pojej nezastrupljen košček čokolade')
            elif (i,j) in neveljavne_poteze:
                self.napis.set('ups, ta košček čokolade je nekdo že pojedel')
            else:
                for k in range(VISINA-j):
                    for l in range(SIRINA-i):
#                       ime=self.ime_koscka(j+k,i+l)
#                       print(ime)
#                       self.plosca.itemconfig(ime, fill="blue")
                        self.koscek(j+k,i+l,'white')
                        neveljavne_poteze.add((i+k,j+l))
                        self.plosca.create_oval(i*100+20,j*100+60,i*100+25,j*100+65, fill='sienna4')
                        self.plosca.create_oval(i*100+30,j*100+70,i*100+35,j*100+75, fill='sienna4')
                        self.plosca.create_oval(i*100+20,j*100+70,i*100+25,j*100+75, fill='sienna4')
                        self.plosca.create_oval(i*100+20,j*100+80,i*100+25,j*100+85, fill='sienna4')
                        self.plosca.create_oval(i*100+30,j*100+60,i*100+35,j*100+65, fill='sienna4')
                        self.plosca.create_oval(i*100+40,j*100+60,i*100+45,j*100+65, fill='sienna4')
                kliki.add((i,j))
            return kliki
    
        else:
            self.napis.set('neveljavna poteza')

    def koscek(self,i,j,barva):
        """narise koscek čokolade na (i,j)-tem polju izbrane barve"""
        return self.plosca.create_rectangle(15 + j*100, 55 + i*100, 105 + j*100, 145 + i*100, fill=barva)

    def nova_igra(self):
        """Vzpostavi zaèetno stanje."""
        #Pobrišemo vse s canvasa:
        self.plosca.delete(ALL)
        
        """"je res treba vse še enrat napisat?"""
        for i in range(VISINA+1):
            self.plosca.create_line(10, i*100 + 50, SIRINA*100 + 10, i*100 + 50) 
        for i in range(SIRINA+1):
            self.plosca.create_line(i*100+10, 50, i*100+10, VISINA*100 + 50)

        #Ustvarimo novo igro
        #self.igra = Igra()
        #Narišemo polje:
        for i in range(VISINA):
            for j in range(SIRINA):
                if i==0 and j==0:
                    self.plosca.create_rectangle(15, 55 , 105, 145, fill='red')
                else:
                    self.koscek(i,j,'sienna4')
        
        #Manjka še mnogo košèkov in tudi njigovi TAG-i
        #Prvi je na potezi človek
        self.napis.set("Ti si na potezi.")
        pass



#####################################################
## Glavni program
if __name__ == "__main__":
    root = Tk()
    root.title("Chomp")
    aplikacija = Gui(root)
    root.mainloop()
