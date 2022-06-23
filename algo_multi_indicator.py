################################################################

import subprocess
import pandas as pd
import sys, getopt
import sys
import telegram_send
import configparser
import time
import statistics

##########################
#   VALEUR PAR DEFAUT
##########################

fichierEnregistrement="backtest-multi-indicator.csv"

argumentList = sys.argv[1:]
try:
    substring = ".csv"

    if substring in sys.argv[1]:
        fichierEnregistrement=sys.argv[1]
        print("Enregistrement des données dans : ", fichierEnregistrement)
        print("Si des données étaient déjà présente dans le fichier, elles ont été supprimées\n")
        classement = pd.DataFrame([])
        try :
            classement = pd.read_csv(fichierEnregistrement)
        except :
            print(f"Le fichier {fichierEnregistrement} n'existe pas, nous allons le créer.")
            classement = classement.append(pd.DataFrame({
                        'dates' : [0], 'finalBalance' : [0], 'perfVSUSD' : [0], 'holdPercentage' : [0], 'vsHoldPercentage' : [0],
                        'bestTrade' : [0], 'worstTrade' : [0], 'drawDown' : [0], 'taxes' : [0], 'totalTrades' : [0], 'totalGoodTrades' : [0],
                        'totalBadTrades' : [0], 'winRateRatio' : [0],  'tradesPerformance' : [0], 'averagePercentagePositivTrades' : [0],
                        'averagePercentageNegativTrades' : [0], 'startingBalance': [0], 'cci': [0], 'pvo': [0], 'willr': [0], 'kama': [0],
                        'ao': [0], 'sp': [0], 'psar': [0], 'atr': [0], 'adx': [0], 'aroon': [0], 'keltner': [0], 'boll': [0], 'stochrsi': [0],
                        'macd': [0], 'kst': [0], 'vol': [0], 'trix': [0], 'emad': [0], 'ema': [0], 'hichi': [0]}), ignore_index=True)
    else:
        print("Vous devez spécifier un fichier .csv\npython3 algorithme.py <nom-du-fichier.csv>")
        exit()
except :
    print("Vous devez specifier un nom de fichier csv :\npython3 algorithme.py <nom-du-fichier.csv>")
    exit()

dateAnnee='2022' #1
dateMois='01' #2
dateJour='01' #3
startingBalance = 1000 #4

# cci
ccidefault = 0
ccimin = 0
ccimax = 1
ccipas = 1
cciuse = 'true'
cci = ccidefault

# pvo
pvodefault = 0
pvomin = 0
pvomax = 1
pvopas = 1
pvouse = 'true'
pvo = pvodefault

# willr
willrdefault = 0
willrmin = 0
willrmax = 1
willrpas = 1
willruse = 'true'
willr = willrdefault

# kama
kamadefault = 0
kamamin = 0
kamamax = 1
kamapas = 1
kamause = 'true'
kama = kamadefault

# ao
aodefault = 0
aomin = 0
aomax = 1
aopas = 1
aouse = 'true'
ao = aodefault

# sp
spdefault = 0
spmin = 0
spmax = 1
sppas = 1
spuse = 'true'
sp = spdefault

# psar
psardefault = 0
psarmin = 0
psarmax = 1
psarpas = 1
psaruse = 'true'
psar = psardefault

# atr
atrdefault = 0
atrmin = 0
atrmax = 1
atrpas = 1
atruse = 'true'
atr = atrdefault

# adx
adxdefault = 0
adxmin = 0
adxmax = 1
adxpas = 1
adxuse = 'true'
adx = adxdefault

# aroon
aroondefault = 0
aroonmin = 0
aroonmax = 1
aroonpas = 1
aroonuse = 'true'
aroon = aroondefault

# keltner
keltnerdefault = 0
keltnermin = 0
keltnermax = 1
keltnerpas = 1
keltneruse = 'true'
keltner = keltnerdefault

# boll
bolldefault = 0
bollmin = 0
bollmax = 1
bollpas = 1
bolluse = 'true'
boll = bolldefault

# stochrsi
stochrsidefault = 0
stochrsimin = 0
stochrsimax = 1
stochrsipas = 1
stochrsiuse = 'true'
stochrsi = stochrsidefault

# macd
macddefault = 0
macdmin = 0
macdmax = 1
macdpas = 1
macduse = 'true'
macd = macddefault

# kst
kstdefault = 0
kstmin = 0
kstmax = 1
kstpas = 1
kstuse = 'true'
kst = kstdefault

# vol
voldefault = 0
volmin = 0
volmax = 1
volpas = 1
voluse = 'true'
vol = voldefault

# trix
trixdefault = 0
trixmin = 0
trixmax = 1
trixpas = 1
trixuse = 'true'
trix = trixdefault

# emad
emaddefault = 0
emadmin = 0
emadmax = 1
emadpas = 1
emaduse = 'true'
emad = emaddefault

# ema
emadefault = 0
emamin = 0
emamax = 1
emapas = 1
emause = 'true'
ema = emadefault

# hichi
hichidefault = 0
hichimin = 0
hichimax = 1
hichipas = 1
hichiuse = 'true'
hichi = hichidefault

# ao
# sp
# psar
# atr
# adx
# aroon
# keltner
# boll
# stochrsi
# macd
# kst
# vol
# trix
# emad
# ema
# hichi

def getNbOfIndicators():
    global cci
    global pvo
    global willr
    global kama
    global ao
    global sp
    global psar
    global atr
    global adx
    global aroon
    global keltner
    global boll
    global stochrsi
    global macd
    global kst
    global vol
    global trix
    global emad
    global ema
    global hichi
    nbOfIndicators = cci + pvo + willr + kama + ao + sp + psar + atr + adx + aroon + keltner + boll + stochrsi + macd + kst + vol + trix + emad + ema + hichi
    return nbOfIndicators

maxIndicators=4
bestFinalBalance = 0
elapsed = 0
measures = []
measures.append(40)

i=0

#=================================================================================================
#   FONCTION QUI LANCE BACKTEST AVEC LES ARGUMENTS ET ENREGISTRE LE RESULTAT DANS UN FICHIER CSV
#=================================================================================================
def launch_backtest():
    print(f"Lancement du backtest avec les paramètres : {cci} {pvo} {willr} {kama} {ao} {sp} {psar} {atr} {adx} {aroon} {keltner} {boll} {stochrsi} {macd} {kst} {vol} {trix} {emad} {ema} {hichi}")
    global i
    global classement
    global elapsed
    global measures
    i=i+1
    pourcent=round(100*i/count,4)
    moyenne=round(statistics.mean(measures),3)
    start = time.time()
    print(f"La dernière execution a durée : {elapsed} secondes")
    print(f"Avancement total d'execution : {i}/{count} ({pourcent}%) (Temps restant estimé par rapport aux dernières executions : {((count-i)*moyenne)} secondes soit {(((count-i)*moyenne)/60)} minutes ou {round((count-i)*moyenne/60/60, 1)} heures ou {round((count-i)*elapsed/60/60/24, 1)} jours)")
    if ((classement['cci'] == cci) & (classement['pvo'] == pvo) & (classement['willr'] == willr) & (classement['kama'] == kama) & (classement['ao'] == ao) & (classement['sp'] == sp) & (classement['psar'] == psar) & (classement['atr'] == atr) & (classement['adx'] == adx) & (classement['aroon'] == aroon) & (classement['keltner'] == keltner) & (classement['boll'] == boll) & (classement['stochrsi'] == stochrsi) & (classement['macd'] == macd) & (classement['kst'] == kst) & (classement['vol'] == vol) & (classement['trix'] == trix) & (classement['emad'] == emad) & (classement['ema'] == ema) & (classement['hichi'] == hichi)).any() :
        print(f"Données {cci} {pvo} {willr} {kama} {ao} {sp} {psar} {atr} {adx} {aroon} {keltner} {boll} {stochrsi} {macd} {kst} {vol} {trix} {emad} {ema} {hichi} déjà présentes dans le classement")
    else :
        cmd = (f"python3 -W ignore backtest_multi_indicator.py {cci} {pvo} {willr} {kama} {ao} {sp} {psar} {atr} {adx} {aroon} {keltner} {boll} {stochrsi} {macd} {kst} {vol} {trix} {emad} {ema} {hichi}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate() 
        end = time.time()
        elapsed = end - start
        measures.append(elapsed)
        result=out.decode('utf-8')
        if result=='':
            result=1000
            dates=str("0")
            finalBalance=float(0)
            perfVSUSD=float(0)
            holdPercentage=float(0)
            vsHoldPercentage=float(0)
            bestTrade=float(0)
            worstTrade=float(0)
            drawDown=float(0)
            taxes=float(0)
            totalTrades=float(0)
            totalGoodTrades=float(0)
            totalBadTrades=float(0)
            winRateRatio=float(0)
            tradesPerformance=float(0)
            averagePercentagePositivTrades=float(0)
            averagePercentageNegativTrades=float(0)
        else:
            separatedResult=result.split('\n')
            y=1
            for line in separatedResult:
                if y==1 :
                    dates=str(line)
                if y==2 :
                    finalBalance=float(line)
                if y==3 :
                    perfVSUSD=float(line)
                if y==4 :
                    holdPercentage=float(line)
                if y==5 :
                    vsHoldPercentage=float(line)
                if y==6 :
                    bestTrade=float(line)
                if y==7 :
                    worstTrade=float(line)
                if y==8 :
                    drawDown=float(line)
                if y==9 :
                    taxes=float(line)
                if y==10 :
                    totalTrades=float(line)
                if y==11 :
                    totalGoodTrades=float(line)
                if y==12 :
                    totalBadTrades=float(line)
                if y==13 :
                    winRateRatio=float(line)
                if y==14 :
                    tradesPerformance=float(line)
                if y==15 :
                    averagePercentagePositivTrades=float(line)
                if y==16 :
                    averagePercentageNegativTrades=float(line)
                y=y+1
        classement = classement.append(pd.DataFrame({
                    'dates' : [dates],
                    'finalBalance' : [finalBalance],
                    'perfVSUSD' : [perfVSUSD],
                    'holdPercentage' : [holdPercentage],
                    'vsHoldPercentage' : [vsHoldPercentage],
                    'bestTrade' : [bestTrade],
                    'worstTrade' : [worstTrade],
                    'drawDown' : [drawDown],
                    'taxes' : [taxes],
                    'totalTrades' : [totalTrades],
                    'totalGoodTrades' : [totalGoodTrades],
                    'totalBadTrades' : [totalBadTrades],
                    'winRateRatio' : [winRateRatio],
                    'tradesPerformance' : [tradesPerformance],
                    'averagePercentagePositivTrades' : [averagePercentagePositivTrades],
                    'averagePercentageNegativTrades' : [averagePercentageNegativTrades],
                    'startingBalance': [startingBalance],
                    'cci': [cci],
                    'pvo': [pvo],
                    'willr': [willr],
                    'kama': [kama],
                    'ao': [ao],
                    'sp': [sp],
                    'psar': [psar],
                    'atr': [atr],
                    'adx': [adx],
                    'aroon': [aroon],
                    'keltner': [keltner],
                    'boll': [boll],
                    'stochrsi': [stochrsi],
                    'macd': [macd],
                    'kst': [kst],
                    'vol': [vol],
                    'trix': [trix],
                    'emad': [emad],
                    'ema': [ema],
                    'hichi': [hichi]}), ignore_index=True)
                    
        classement.dates = classement.dates.astype(str)
        classement.finalBalance = classement.finalBalance.astype(float)
        classement.perfVSUSD = classement.perfVSUSD.astype(float)
        classement.holdPercentage = classement.holdPercentage.astype(float)
        classement.vsHoldPercentage = classement.vsHoldPercentage.astype(float)
        classement.bestTrade = classement.bestTrade.astype(float)
        classement.worstTrade = classement.worstTrade.astype(float)
        classement.drawDown = classement.drawDown.astype(float)
        classement.taxes = classement.taxes.astype(float)
        classement.totalTrades = classement.totalTrades.astype(float)
        classement.totalGoodTrades = classement.totalGoodTrades.astype(float)
        classement.totalBadTrades = classement.totalBadTrades.astype(float)
        classement.winRateRatio = classement.winRateRatio.astype(float)
        classement.tradesPerformance = classement.tradesPerformance.astype(float)
        classement.averagePercentagePositivTrades = classement.averagePercentagePositivTrades.astype(float)
        classement.averagePercentageNegativTrades = classement.averagePercentageNegativTrades.astype(float)
        

        classement.to_csv(fichierEnregistrement)
    return True

#=================================================================
#   SUCCESSION DE BOUCLE QUI VA FAIRE VARIER TOUS NOS PARAMETRES
#=================================================================

count=0
for j in range(2):
    #cci
    if cciuse=='true':
        cci = ccimin
    else:
        cci = ccidefault
        ccimin = cci
        ccimax = cci
    while cci <= ccimax:

        #pvo
        if pvouse=='true':
            pvo = pvomin
        else:
            pvo = pvodefault
            pvomin = pvo
            pvomax = pvo
        while pvo <= pvomax:
        
            #willr
            if willruse=='true':
                willr = willrmin
            else:
                willr = willrdefault
                willrmin = willr
                willrmax = willr
            while willr <= willrmax:
                
                #kama
                if kamause=='true':
                    kama = kamamin
                else:
                    kama = kamadefault
                    kamamin = kama
                    kamamax = kama
                while kama <= kamamax:
                    
                    #ao
                    if aouse=='true':
                        ao = aomin
                    else:
                        ao = aodefault
                        aomin = ao
                        aomax = ao
                    while ao <= aomax:
                        
                        #sp
                        if spuse=='true':
                            sp = spmin
                        else:
                            sp = spdefault
                            spmin = sp
                            spmax = sp
                        while sp <= spmax:
                        
                            #psar
                            if psaruse=='true':
                                psar = psarmin
                            else:
                                psar = psardefault
                                psarmin = psar
                                psarmax = psar
                            while psar <= psarmax:
                            
                                #atr
                                if atruse=='true':
                                    atr = atrmin
                                else:
                                    atr = atrdefault
                                    atrmin = atr
                                    atrmax = atr
                                while atr <= atrmax:
                                    
                                    #adx
                                    if adxuse=='true':
                                        adx = adxmin
                                    else:
                                        adx = adxdefault
                                        adxmin = adx
                                        adxmax = adx
                                    while adx <= adxmax:
                   
                                        #aroon
                                        if aroonuse=='true':
                                            aroon = aroonmin
                                        else:
                                            aroon = aroondefault
                                            aroonmin = aroon
                                            aroonmax = aroon
                                        while aroon <= aroonmax:
                                        
                                            #keltner
                                            if keltneruse=='true':
                                                keltner = keltnermin
                                            else:
                                                keltner = keltnerdefault
                                                keltnermin = keltner
                                                keltnermax = keltner
                                            while keltner <= keltnermax:
                                                
                                                #boll
                                                if bolluse=='true':
                                                    boll = bollmin
                                                else:
                                                    boll = bolldefault
                                                    bollmin = boll
                                                    bollmax = boll
                                                while boll <= bollmax:
                                                        
                                                    #stochrsi
                                                    if stochrsiuse=='true':
                                                        stochrsi = stochrsimin
                                                    else:
                                                        stochrsi = stochrsidefault
                                                        stochrsimin = stochrsi
                                                        stochrsimax = stochrsi
                                                    while stochrsi <= stochrsimax:
                                                        
                                                        #macd
                                                        if macduse=='true':
                                                            macd = macdmin
                                                        else:
                                                            macd = macddefault
                                                            macdmin = macd
                                                            macdmax = macd
                                                        while macd <= macdmax:
                                                            #kst
                                                            if kstuse=='true':
                                                                kst = kstmin
                                                            else:
                                                                kst = kstdefault
                                                                kstmin = kst
                                                                kstmax = kst
                                                            while kst <= kstmax:
                                                                #vol
                                                                if voluse=='true':
                                                                    vol = volmin
                                                                else:
                                                                    vol = voldefault
                                                                    volmin = vol
                                                                    volmax = vol
                                                                while vol <= volmax:
                                                                    #trix
                                                                    if trixuse=='true':
                                                                        trix = trixmin
                                                                    else:
                                                                        trix = trixdefault
                                                                        trixmin = trix
                                                                        trixmax = trix
                                                                    while trix <= trixmax:
                                                                        #emad
                                                                        if emaduse=='true':
                                                                            emad = emadmin
                                                                        else:
                                                                            emad = emaddefault
                                                                            emadmin = emad
                                                                            emadmax = emad
                                                                        while emad <= emadmax:
                                                                            #ema
                                                                            if emause=='true':
                                                                                ema = emamin
                                                                            else:
                                                                                ema = emadefault
                                                                                emamin = ema
                                                                                emamax = ema
                                                                            while ema <= emamax:
                                                                                if getNbOfIndicators()<=maxIndicators :
                                                                                    if j==1:
                                                                                        launch_backtest()
                                                                                    else :
                                                                                        count=count+1
                                                                                ema=ema+emapas
                                                                            emad=emad+emadpas
                                                                        trix=trix+trixpas
                                                                    vol=vol+volpas
                                                                kst=kst+kstpas
                                                            macd=macd+macdpas
                                                        stochrsi=stochrsi+stochrsipas
                                                    boll=boll+bollpas
                                                keltner=keltner+keltnerpas
                                            aroon=aroon+aroonpas
                                        adx=adx+adxpas
                                    atr=atr+atrpas
                                psar=psar+psarpas
                            sp=sp+sppas
                        ao=ao+aopas
                    kama=kama+kamapas
                willr=willr+willrpas
            pvo=pvo+pvopas
        cci=cci+ccipas
    
#==================================================================================
#   ENREGISTREMENT FINALE (AU CAS OU MAIS NORMALEMENT LE FICHIER SERA DEJA REMPLI
#==================================================================================

print(classement.head())
classement.to_csv(fichierEnregistrement)
telegram_send.send(messages=[f"Votre algorithme de combinaison d'indicateurs a enregistré toutes les données dans {fichierEnregistrement}"])