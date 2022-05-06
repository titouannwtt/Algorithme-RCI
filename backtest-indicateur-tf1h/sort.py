################################################################

import subprocess
import pandas as pd
import sys, getopt
import sys
import telegram_send

##########################
#   VALEUR PAR DEFAUT
##########################

csv="/home/moutonneux/bots/backtest/backtest-indicateur/sorted_1h.csv"
argumentList = sys.argv[1:]
bestValue=0.0
try :
    ancienClassement = pd.read_csv(csv)
    bestValue=float(ancienClassement['finalBalance'].iloc[0])
    print(f"BestValue={bestValue}")
except :
    print(f"Le fichier {csv} n'a pas été trouvé, il va être créé")
    pass
classement = pd.DataFrame([])
for arg in argumentList:
    dataframe=pd.read_csv(arg)
    classement = classement.append(dataframe, ignore_index=True)

classement=classement.sort_values(by=['finalBalance'], ascending=False)
print(classement)
classement.to_csv(csv)
print(f"BestValue={bestValue}")
print(f"{classement['finalBalance'].iloc[0]}")
if bestValue<float(classement['finalBalance'].iloc[0]):
    telegram_send.send(messages=[f"Nouvelle meilleure performance pour l'algo multiples indicators {bestValue}"])
    print("Nouvelle meilleure performance pour l'algo multiples indicators!")
    