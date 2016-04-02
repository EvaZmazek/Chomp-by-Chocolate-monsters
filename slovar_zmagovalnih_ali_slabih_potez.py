import pickle

MAX=16
#pickle.dump({'[0]': 1},  open( "poznane_vrednosti.p", "wb" ))
print("printam obstojec_slovar")
obstojec_slovar = pickle.load( open( "poznane_vrednosti.p", "rb" ) )
print(obstojec_slovar)
print("evo ga")

def preuredi(nizek):
    seznam=nizek.split(",")
    seznam[0]=preuredi1(seznam[0])
    seznam[-1]=preuredi1(seznam[-1])
    sez=[]
    for i in seznam:
        sez.append(int(i))
    return [MAX]+sez+[0]

def preuredi1(nizek):
    novi=[]
    for i in nizek:
        if i not in ["[","]"," "]:
            novi.append(i)
    return novi[0]

def prepisi(seznam):
    sez=[]
    for s in seznam:
        sez.append(s)
    return sez

def preveri(seznam):
    """ta funkcija preveri če je seznam prieren za dodajanje v slovar: torej,
    če nima treh zaporedno enako velikih stolpcev in če ne obstaja preskok, večji ali enak 3"""
    sez=seznam+[0]
    l=len(sez)
    i=0
    while i<l-2:
        if sez[i]==sez[i+1]==sez[i+2] or sez[i]>sez[i+1]+2:
            return False
        i+=1
    if sez[l-2]>sez[l-1]+2: #more še preveriti skok med predzadnjim in zadnjim
        return False
    return True

def poberi_prave(seznam):
    koncni=[]
    for i in seznam:
        if preveri(i) and len(i)<MAX and i[0]<MAX:
            koncni.append(i)
    return koncni

def zapisi_seznam_iz_slovarja(slovar):
    seznam=[]
    for i in slovar:
        j=preuredi(i)
        seznam.append(j)
    return seznam

def najdi_nove(seznam):
    seznamcek=[]
    for i in seznam:
##        print(i)
##        print(i[0])
        m=0
        dolzina=len(i)
        while m+1<dolzina:
            if i[m]>i[m+1]:
                novi=prepisi(i)
                novi[m+1]=novi[m+1]+1
                if novi[-1]==0:
                    novinovi=novi[1:-1]
                else:
                    novinovi=novi[1:]
##                print(novinovi)
                if i[-1]==0:
                    ii=i[1:-1]
                else: ii=i[1:]
                if preveri(novinovi):
                    seznamcek.append((str(novinovi),str(ii)))
##                print(novi[1:])
##                print(novi)
##                print("iscem vse nove in jih shranim v seznam") #poisci vse nove
            m+=1
##    print ("vse vrednosti v tem seznamu so (-1) * vrednost i v slovarju")
    return seznamcek

def zapisi_v_slovar(seznamcek,slovar):
    for i,j in seznamcek:
        if i in slovar:
            if slovar[i]!=slovar[j]*(-1):
                del slovar[i]
    ##        pickle.dump({i: max(slovar[j]*(-1),slovar[i])},  open( "poznane_vrednosti.p", "wb" ))
        else:
            slovar[i]=slovar[j]*(-1)
    return slovar

seznam_pravi=zapisi_seznam_iz_slovarja(obstojec_slovar)
##print("pretvarjam iz slovarja v seznam:")
##print(seznam_pravi)
seznamcek_pravi=najdi_nove(seznam_pravi)
##print("poiscem nove vrednosti za v slovar:")
##print(seznamcek_pravi)
zapisi=zapisi_v_slovar(seznamcek_pravi,obstojec_slovar)
##print("tako bi moral izgledati nov slovar")
##print(zapisi)

print("zapisujem v datoteko 'poznane_vrednosti.p'...")
pickle.dump(zapisi ,open( "poznane_vrednosti.p", "wb" ))

novi=pickle.load( open( "poznane_vrednosti.p", "rb" ) )
##print("tako zdaj izgleda datoteka 'poznane_vrednosti.p':")
##print(novi)
print("novi slovar ima dolžino:")
print(len(novi))

print("to pa je izmišljen slovar:")
slovar=dict()

slovar["[0]"]=1
slovar["[1]"]=-1
slovar["[2]"]=1
slovar["[1, 1]"]=1
    
sez=zapisi_seznam_iz_slovarja(slovar)
seznamcek=najdi_nove(sez)
print(seznamcek)

print(zapisi_v_slovar(seznamcek,slovar))



