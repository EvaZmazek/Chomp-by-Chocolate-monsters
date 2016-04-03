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
Program je implementiran v Pythonu 3 in sestoji iz dveh delov:  

▶︎ Uporabniški vmesnik: uporablja knjižnico [tkinter](http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html).    
▶︎ Računalniški igralec:  
😃 način easy: računalnik bo izbiral svoje poteze naključno.  
🤔 način medium: računalnik bo izbiral svoje poteze z rekurzijo.
😥 način hard: računalnik bo izbiral svoje poteze z algoritmom [minimax](https://en.wikipedia.org/wiki/Minimax).

###RAZREDI
Vsi razredi so v datoteki chomp.py, ker gre za preprosto aplikacijo.

####Razred GUI(preuredi)
Razred, v katerem je definiran uporabniški vmesnik. Metode:  
🎲 nova_igra(self, Igralec_1, Igralec_2): začni igrati igro z danimi igralci, kjer izbor igralcev pomeni tudi način igre  
🎲 koncaj_igro(self, zmagovalec): končaj igro z danim zmagovalecem  
🎲 povleci_potezo(self, i, j): povleci potezo (i,j)

####Razred Igra
Objekt tega razreda vsebuje trenutno stanje igre, kakor tudi njeno zgodovino. Ima naslednje metode:  
🎲 povleci_potezo(self,i,j): pojej košček čokolade (i,j) in vse spodaj-desno, pri čemer je i vrstica  in j stolpec      
🎲 stanje_igre(self,i,j): ugotovi, kakšno je trenutno stanje igre: ni konec, zmagal je Igralec_1, zmagal je Igralec_2  
🎲razveljavi(self): vrni se v stanje pred zadnjo potezo, metodo lahko pokličemo večkrat, s tem se premikamo navzgor po igralnem drevesu.  
🎲 na_potezi: kdo je na potezi: IGRALEC_1, IGRALEC_2 ali None  
🎲 veljavne_poteze(self): vrne seznam vseh veljavnih potez  

###IGRALCI
Razne vrste igralcev (človek, metoda nakjučje, algoritem minimax, algoritem alfa-beta) predstavimo vsakega s svojim razredom. Objekt, ki predstavlja igralca, mora imeti naslednje metode:  
▶︎ __init__(self, gui): konstruktorju podamo objekt gui, s katerim lahko dostopa do uporabniškega vmesnika in stanja igre  
▶︎ igraj(self): GUI pokliče to metodo, ko je igralec na potezi  
▶︎ klik(self, i, j): GUI pokliče to metodo, če je igralec na potezi in je uporabnik kliknil polje (i,j) na čokoladi  

####Razred Clovek
Igralec je človek, potezo dobi s klikom na miško.

####Razred Nakjucje
Igralec računalnik, ki poteze izbira nakjučno.

####Razred Minimax
Igralec računalnik, ki igra rekurzivno.

####Razred AlfaBeta
Igralec računalnik, ki igra z metodo mini-max.

