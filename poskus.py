from tkinter import *
SIRINA=7
VISINA=4
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
        self.plosca = Canvas(master, width=750, height=455)
        self.plosca.grid(row=1, column=0)

        for i in range(VISINA+1):
            self.plosca.create_line(10, i*100 + 50, 710, i*100 + 50)
        for i in range(SIRINA+1):
            self.plosca.create_line(i*100+10, 50, i*100+10, 450)
        
 #       self.nova_igra()

    def nova_igra(self):
        """Vzpostavi zaèetno stanje."""
        #Pobrišemo vse s canvasa:
        self.plosca.delete(ALL)
        #Ustvarimo novo igro
        #self.igra = Igra()
        #Narišemo polje:
        self.plosca.create_oval(10, 10, 50, 50, fill='red')
        #Manjka še mnogo košèkov in tudi njigovi TAG-i
        #Prvi je na potezi èlovek
        self.napis.set("Ti si na potezi.")
        pass



#####################################################
## Glavni program
if __name__ == "__main__":
    root = Tk()
    root.title("Chomp")
    aplikacija = Gui(root)
    root.mainloop()
