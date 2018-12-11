import sys
from random import *

import pygame
from pygame.locals import *


def game_over():
    jookseb = False
    return ('Miin!!!')


def maara_miinid():  # koostab randomilt sõnastiku, kus 1 tähistab miini ja 0 miini puudumist.

    valjund = {}
    miinide_list = sample(range(RUUTUDE_VEERGE * RUUTUDE_RIDU - 1), int(RUUTUDE_VEERGE * RUUTUDE_RIDU / 100 * PROTSENT_MIINE))
    for el in range(RUUTUDE_VEERGE * RUUTUDE_RIDU):
        valjund[el] = 0
    for i in miinide_list:
        valjund[i] = 1
    return valjund

def kas_umbritsev(vasakpoolsed_ruudud): # koostab sõnastiku, mida mäng uuendab, et kontrollida kas kõrvalt on midagi avatud
    
    valjund = {}
    for el in range(RUUTUDE_VEERGE * RUUTUDE_RIDU):
        valjund[el] = 0
    for el in vasakpoolsed_ruudud:
        valjund[el] = 1
    return valjund

def jah_umbritsev(sisend, kas_umbritseb):
    
    try:
        kas_umbritseb[sisend - RUUTUDE_VEERGE] = 1
    except:
        pass
    try:
        kas_umbritseb[sisend + RUUTUDE_VEERGE] = 1
    except:
        pass
        
    if sisend not in vasakpoolsed_ruudud:
        kas_umbritseb[sisend - 1] = 1
        try:
            kas_umbritseb[sisend - RUUTUDE_VEERGE - 1] = 1
        except:
            pass
        try:
            kas_umbritseb[sisend + RUUTUDE_VEERGE - 1] = 1
        except:
            pass
            
    if sisend not in parempoolsed_ruudud:
        kas_umbritseb[sisend + 1] = 1
        try:
            kas_umbritseb[sisend - RUUTUDE_VEERGE + 1] = 1
        except:
            pass
        try:
            kas_umbritseb[sisend + RUUTUDE_VEERGE + 1] = 1
        except:
            pass


def miinide_maatriks(sonastik):

    seis = []

    for i in range(RUUTUDE_RIDU):
        rida = []
        for j in range(RUUTUDE_VEERGE):
            rida.append(sonastik[j])
        seis.append(rida)
    
    return seis


def safe_zone():

    for ruut in valjak:
        if ruut in vasakpoolsed_ruudud or ruut in parempoolsed_ruudud:
            valjak[ruut] = 0
    
    # Joonistab rohelised ruudud
    for i in range(len(maatriks)):
        for j in range(0, len(maatriks[i]), RUUTUDE_VEERGE - 1):
            maatriks[i][j] = 23


def miinide_arv(sisend):
    
    miinide_arv = 0
    
    try:
        miinide_arv += valjak[sisend - RUUTUDE_VEERGE]
    except:
        pass
    try:
        miinide_arv += valjak[sisend + RUUTUDE_VEERGE]
    except:
        pass
        
    if sisend not in vasakpoolsed_ruudud:
        miinide_arv += valjak[sisend - 1]
        try:
            miinide_arv += valjak[sisend - RUUTUDE_VEERGE - 1]
        except:
            pass
        try:
            miinide_arv += valjak[sisend + RUUTUDE_VEERGE - 1]
        except:
            pass
            
    if sisend not in parempoolsed_ruudud:
        miinide_arv += valjak[sisend + 1]
        try:
            miinide_arv += valjak[sisend - RUUTUDE_VEERGE + 1]
        except:
            pass
        try:
            miinide_arv += valjak[sisend + RUUTUDE_VEERGE + 1]
        except:
            pass
        
##    if miinide_arv == 0:
##        ava_umbritsevad(sisend)
##
    if miinide_arv == None:
        miinide_arv = 0
    
    return miinide_arv


def klikk(x, y):  # tagastab hulga elemendi, mille peale vajutati

    if x >= SERVA_PAKSUS and x <= (RUUTUDE_VEERGE * RUUDU_KULG + SERVA_PAKSUS):
        x_asukoht = int((x - SERVA_PAKSUS) / RUUDU_KULG)

    elif x < SERVA_PAKSUS or x > (SERVA_PAKSUS + RUUTUDE_VEERGE * RUUDU_KULG):
        return

    if y >= SERVA_PAKSUS and y <= (RUUTUDE_RIDU * RUUDU_KULG + SERVA_PAKSUS):
        y_asukoht = int((y - SERVA_PAKSUS) / RUUDU_KULG)

    elif y < SERVA_PAKSUS or y > (SERVA_PAKSUS + RUUTUDE_VEERGE * RUUDU_KULG):
        return

    valjund = y_asukoht * RUUTUDE_VEERGE + x_asukoht
    
    return valjund


def kliki_tagajarg(sisend, kas_umbritseb):     # klikk avab ühe ruudu, see otsustab, kas ta astus miini otsa või tagastada kuvamiseks ümbritsevate miinide arv

    if kas_umbritseb[sisend] == 1:
        jah_umbritsev((peale_vajutatud_element), kas_umbritseb)
        if valjak[sisend] == 1:
            return game_over()
        else:
            return miinide_arv(sisend)


# Põhifunktsioon
def main():

    global jookseb, valjak, maatriks, vasakpoolsed_ruudud, parempoolsed_ruudud, peale_vajutatud_element

    pygame.init()

    # Teeb akna valmis
    aken = pygame.display.set_mode((akna_laius, akna_korgus))
    pygame.display.set_caption('Minesweeper Vol. 2')

    # Laeb pildid sisse
    ruut = pygame.image.load('ruut.png').convert()
    avatud_ruut = pygame.image.load('avatud_ruut.png').convert()
    safe_ruut = pygame.image.load('safe_ruut.png').convert()
    uks = pygame.image.load('1.png').convert()
    kaks = pygame.image.load('2.png').convert()
    kolm = pygame.image.load('3.png').convert()
    neli = pygame.image.load('4.png').convert()
    viis = pygame.image.load('5.png').convert()
    kuus = pygame.image.load('6.png').convert()
    seitse = pygame.image.load('7.png').convert()
    kaheksa = pygame.image.load('8.png').convert()
    miin = pygame.image.load('miin.png').convert()
    lipp = pygame.image.load('lipp.png').convert()

    # Seab kindla numbri pildiga vastavusse
    pildi_id = {1:ruut, 0:ruut, 11: uks, 12:kaks, 13:kolm,
                14:neli, 15:viis, 16:kuus, 17:seitse, 18:kaheksa,
                10:avatud_ruut, 21:miin, 22:lipp, 23:safe_ruut}

    # Tsükkel, mis täidab akna avamata ruutudega
    for ruudu_y in range(SERVA_PAKSUS, RUUDU_KULG * RUUTUDE_RIDU, RUUDU_KULG):
        for ruudu_x in range(SERVA_PAKSUS, RUUDU_KULG * RUUTUDE_VEERGE, RUUDU_KULG):
            aken.blit(ruut, (ruudu_x, ruudu_y))

    # Mänguvälja loomine
    valjak = maara_miinid()
    
    # Safe zone'i ruutude loomine
    vasakpoolsed_ruudud = []
    for i in range(RUUTUDE_RIDU):
        vasakpoolsed_ruudud.append(i * RUUTUDE_VEERGE)

    parempoolsed_ruudud = []
    for i in range(RUUTUDE_RIDU):
        parempoolsed_ruudud.append(i * RUUTUDE_VEERGE + (RUUTUDE_VEERGE - 1))
        
    # Loob sõnastiku, mis salvestab, milliseid ruute saab
    kas_umbritseb = kas_umbritsev(vasakpoolsed_ruudud)
        
    # Maatriks mille järgi joonistatakse mängu seis
    maatriks = miinide_maatriks(valjak)
    
    # Loob rohelised ruudud
    safe_zone()

    # Põhitsükkel
    jookseb = True
    while jookseb:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    jookseb = False
                    sys.exit()
            elif event.type == pygame.QUIT:
                jookseb = False
                sys.exit()
        
        rida = 0

        # Tsükkel, mis joonistab pildi maatriksi põhjal
        for ruudu_y in range(SERVA_PAKSUS, RUUDU_KULG * RUUTUDE_RIDU, RUUDU_KULG):
            
            id = 0

            for ruudu_x in range(SERVA_PAKSUS, RUUDU_KULG * RUUTUDE_VEERGE, RUUDU_KULG):

                    pilt = pildi_id[maatriks[rida][id]]
                    aken.blit(pilt, (ruudu_x, ruudu_y))
                    # Kui on miini klikitud, siis joonistab selle ja paneb mängu kinni
                    if pilt == miin:
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        jookseb = False
                    id += 1
            
            rida += 1

        # Vasak hiireklõps
        if pygame.mouse.get_pressed()[0] == 1:
            # Hiire koordinaadid
            hiire_pos = pygame.mouse.get_pos()
            peale_vajutatud_element = klikk(hiire_pos[0], hiire_pos[1])
            if peale_vajutatud_element == None:
                continue
            else:
                
                ava_ruut = kliki_tagajarg(peale_vajutatud_element, kas_umbritseb)
                if ava_ruut == 'Miin!!!':
                    print('Mäng läbi!')
                    rea_nr = peale_vajutatud_element // RUUTUDE_VEERGE
                    elemendi_nr = peale_vajutatud_element % RUUTUDE_VEERGE
                    maatriks[rea_nr][elemendi_nr] = 21
                    # TODO avab kõik ruudud
                else:
                    rea_nr = peale_vajutatud_element // RUUTUDE_VEERGE
                    elemendi_nr = peale_vajutatud_element % RUUTUDE_VEERGE
                    try:
                        maatriks[rea_nr][elemendi_nr] = 10 + ava_ruut
                    except:
                        pass
        
        # Parem hiireklõps
        if pygame.mouse.get_pressed()[2] == 1:
            # Hiire koordinaadid
            hiire_pos = pygame.mouse.get_pos()
            peale_vajutatud_element = klikk(hiire_pos[0], hiire_pos[1])
            if peale_vajutatud_element == None:
                continue
            else:
                rea_nr = peale_vajutatud_element // RUUTUDE_VEERGE
                elemendi_nr = peale_vajutatud_element % RUUTUDE_VEERGE
                maatriks[rea_nr][elemendi_nr] = 22
                
        
        # Uuendab pilti
        pygame.display.flip()

        # 60 fps
        kell.tick(FPS)





# Ühe ruudukese suurus pikslites
RUUDU_KULG = 20

# Mitu ruutu väljal on
RUUTUDE_VEERGE = 60
RUUTUDE_RIDU = 15
# TODO muudetav arv ruute

# Akna ääre paksus pikslites
SERVA_PAKSUS = 0

# Arvutab akna suuruse
akna_laius = RUUDU_KULG * RUUTUDE_VEERGE + 2 * SERVA_PAKSUS
akna_korgus = RUUDU_KULG * RUUTUDE_RIDU + 2 * SERVA_PAKSUS

# Mitu protsenti ruutudest on miinid
PROTSENT_MIINE = 20

# Loob kella fps-i jaoks
kell = pygame.time.Clock()

FPS = 60



# valjak = maara_miinid()
# safe_zone()
# print(valjak)
# miine_kokku = 0
# for el in valjak:
#     if valjak[el] == 1:
#         miine_kokku += 1

# # Debugimine kindlatel kliki koordinaatidel
# k = klikk(500, 160)
# print('miine kokku = ' + str(miine_kokku))
# print('elemendi number = ' + str(k))
# print(str(kliki_tagajarg(k)) + ' miini on selle ümber')





main()
