# donnee= []
with open ( 'input.txt', 'r') as f: 
    donnee=f.readline().split(',')
# print (donnee)

 
 
table= [ ] #creation d'une liste de tuple, qui contient mes borne id. 
for don in donnee : 
    table.append( (int(don.split('-')[0]),int(don.split('-')[1])))
# print (table)



# =========================
# PART ONE 
# =========================
print ("="*40+"PART ONE"+"="*40)


def ver_similitude(chaine):
    long= len(chaine)//2
    part1=chaine[:long] 
    part2=chaine[long:] 
    # print("1", part1)
    # print("2", part2 )
    return True if part1==part2 else False
    # for i in range

# print(ver_similitude('567890'))


# un id est invalide s'il est paire cet id divisé en deux donne deux chiffre egaux. 

invalid_id=[] # not les id nvalides
for don in table :
    for i in range(don[0],don[1]+1): 
        id=str(i)
        if len(id)%2==0: 
            if ver_similitude(id)==True: 
                invalid_id.append(i) #on prend la valeur int 
                # print( 'invalide ', id)

print("les id invalide:",invalid_id)
print("leurs sommes:",sum(invalid_id))

print("\n"*2)

# =========================
# PART TWO
# =========================

print ("="*40+"PART TWO"+"="*40)
def ver_similitude2(chaine):
    long= int(len(chaine))
    tabdiv=[i for i in range(1,long) if long%i==0]
    # print("tab de div:",tabdiv)
    verdiv=[]
    for div in tabdiv: 
        motifs=[]
        for i in range(0,long,div): 
            motifs.append(chaine[i:(i+div)]) 
        # print ( "motifs",div,"=>",motifs)
        vermotif=[]
        for i in range(1,len(motifs)): 
            if motifs[i]!=motifs[0]:
                vermotif.append(False)
            else: 
                vermotif.append(True)
        # print('vermotif:',vermotif)
        verdiv.append(False if False in vermotif else True)
        # print ( "motifs et verdiv",div,"=>",verdiv)
    
    return True if True in verdiv else False

# print(ver_similitude2('998')) 
# ver_similitude2('454545')


invalid_id2=[] # not les id nvalides
for don in table :
    for i in range(don[0],don[1]+1): 
        id=str(i)
        if ver_similitude2(id)==True: 
            invalid_id2.append(i) #on prend la valeur int 
            # print( 'invalide ', id)
print("les id invalide:",invalid_id2)
print("leurs sommes:",sum(invalid_id2))