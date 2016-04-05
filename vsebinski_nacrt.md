#VSEBINSKI NAČRT

##OPIS APLIKACIJE
Igro Chomp dva igralca(človek ali računalnik) igrata v glavnem oknu, ki je razdeljeno na mxn polj.
Človek igra tako, da s klikom izbira polja v igralnem oknu.

Aplikacija je v enem izmed treh stanj:  

  🍫začetek:  
  izbor igralcev in težavnosti:  
    👥 človek-človek  
    👤 človek-računalnik - 😃 easy   
    👤 človek-računalnik - 🤔 medium  
    👤 človek-računalnik - 😥 hard  
  
  🍫igra:  
  v glavnem oknu so podatki:  
  🎲 trenutna pozicija  
  🎲 kdo je na potezi 
    
  🍫konec:  
  prikaže podatke o zmagovalcu  

Prehodi med stanji:  
▶︎prehod iz začetka v igro: avtomatsko se sproži način igranja človek-računalnik(easy), uporabnik pa lahko v meniju izbere drug način igre.  
▶︎prehod iz igre v konec igre: sproži ga uporabniški vmesnik, ko ugotovi, da je igre konec  
▶︎prehod iz konca igre v začetek igre: uporabnik klikne na gumb "igraj še enkrat"  

##STRUKTURA PROGRAMA
Glavni program je implementiran v Pythonu 3 in sestoji iz dveh delov:  

▶︎ Uporabniški vmesnik: uporablja knjižnico [tkinter](http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html).    
▶︎ Računalniški igralec:  
😃 način easy: računalnik bo izbiral svoje poteze naključno.  
🤔 način medium: računalnik bo izbiral svoje poteze z rekurzijo.  
😥 način hard: računalnik bo izbiral svoje poteze z algoritmom [minimax](https://en.wikipedia.org/wiki/Minimax).  

Druge datoteke: v programu slovar_zmagovalnih_in_slabih_potez.py generiramo nekatera stanja in ocenimo njihove vrednosti.  

###RAZREDI
Vsi razredi so v datoteki chomp.py, ker gre za preprosto aplikacijo.

####Razred GUI
Razred, v katerem je definiran uporabniški vmesnik. Metode:    
🎲 nova_igra(self, Igralec_2, barva): začni igrati igro s človekom in danim drugim igralcem, kjer izbor drugega igralca pomeni tudi način igre (atribut barva potrebujemo pri risanju polja.)  
🎲 koncaj_igro(self): končaj igro  
🎲 povleci_potezo(self, i, j): povleci potezo (i,j)  
🎲 plosca_klik(self, event): kaj se zgodi ob kliku na ploščo  
🎲 koscek(self, i, j, barva): nariše košček čokolade na polju (i,j) izbrane barve  
🎲 doloci_igralce(self, Igralec_2): funkcija, ki sprejme način igranja in v tem načinu požene igro  
🎲 pomoc(self): ustvari okno z informacijami o igri.  
🎲 pobrisi(self, i, j): pobriše košček (i,j)  
🎲 koncno_okno(self,igralec): funkcija, ki odpre končno okno z razpletom igre  
🎲 preveri(self,tezavnost): preveri na kateri težavnosti igramo, da ob ponovitvi  
igre ali spremembi velikosti polja težavnost ostane enaka  
🎲 combine_funcs(self, *funcs): funkcija, zduži dve ali več funkcij v eno  

####Razred Igra
Objekt tega razreda vsebuje trenutno stanje igre, kakor tudi njeno zgodovino. Ima naslednje metode:  
🎲 __init __(self): konstruktor
🎲 povleci_potezo(self,i,j): pojej košček čokolade (i,j) in vse spodaj-desno, pri čemer je i vrstica  in j stolpec      
🎲 stanje_igre(self,i,j): ugotovi, kakšno je trenutno stanje igre: ni konec, je konec, zmagal je Igralec_1, zmagal je Igralec_2
🎲 razveljavi(self): vrni se v stanje pred zadnjo potezo, metodo lahko pokličemo večkrat, s tem se premikamo navzgor po igralnem drevesu.  
🎲 na_potezi: kdo je na potezi: IGRALEC_1, IGRALEC_2 ali None  
🎲 veljavne_poteze(self): vrne seznam vseh veljavnih potez  
🎲 shrani_pozicijo(self): zapiše trenutno pozicijo in trenutnega igralca v zgodovino  
🎲 kopija(self): za potrebe vzporednega izvajanja v več threadih potrebujemo kopijo igre  
🎲 polepsaj(self, zap): vrne zaporedje, ki predstavlja pozicijo po potegnjeni potezi  
🎲 nasprotnik(self, igralec): vrne nasprotnika od danega igralca  

###IGRALCI
Razne vrste igralcev (človek, metoda nakjučje, algoritem minimax, algoritem alfa-beta) predstavimo vsakega s svojim razredom. Objekt, ki predstavlja igralca, mora imeti naslednje metode:  
▶︎  __init __(self, gui): konstruktorju podamo objekt gui, s katerim lahko dostopa do uporabniškega vmesnika in stanja igre  
▶︎ igraj(self): GUI pokliče to metodo, ko je igralec na potezi  
▶︎ klik(self, i, j): GUI pokliče to metodo, če je igralec na potezi in je uporabnik kliknil polje (i,j) na čokoladi  
▶ prekini(self): GUI kliče to metodo, če zapremo okno, začnemo novo igra, ali naredimo kaj takega, da mora prekiniti razmišljanje.

####Razred Clovek
Igralec je človek, potezo dobi s klikom na miško.

####Razred Nakjucje
Igralec računalnik, ki poteze izbira nakjučno.

####Razred Rekurzija
Igralec računalnik, ki igra rekurzivno.

####Razred Minimax
Igralec računalnik, ki igra z metodo mini-max. Zaradi potrebe po oceni vrednosti poteze, program slovar_zmagovalnih_in_slabih_potez.py generira seznam osnovnejših pozicij z znanimi vrednostmi in ga zapiše v datoteko poznane_vrednosti.p. Iz te datoteke nato preberemo slovar in ga tudi širimo s pozicijami, ki jih naš program ne generira, a je njihova vrednost vseeno znana.

