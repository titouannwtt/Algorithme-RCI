<div id="top"></div>

Pour suivre mes autres projets :

[![LinkedIn][linkedin-shield]][linkedin-url]

# Algorithme RCI : Algorithme de Recherche de Combinaisons d'Indicateurs performantes en timeframe 5 minutes

Dépôt GitHub dédié à la recherche de combinaisons d'indicateurs intéressantes dans l'optique de déterminer de bonnes stratégies à appliquer à des bots de trading en timeframe 5 minutes.

Le backtest suivant ("backtest_multi_indicator.py") est sur une timeframe de 5 minutes avec un solde de départ de 1000$. Il permet, mélangé à un algorithme ("algo_multi_indicator.py"), de tester des combinaisons d'indicateurs possibles (jusqu'à 4 simultanément d'après les configurations par défaut). La stratégie fait uniquement des LONG et le backtest a été réalisé sur une période de baisse (entre janvier 2022 et mars 2022).
Les résultats des combinaisons sont enregistrés dans un fichier csv ("algo_multi_indicator.csv"), il est ensuite possible d'executer "sort.py" qui va trier les résultats dans un nouveau csv : "all_result.csv". On enregistrera également tous les résultats dont le solde final est supérieur à 1050.0$ dans le fichier "best_results.csv".
Une fois l'exécution totalement achevée, on sera en mesure de déterminer des bonnes combinaisons d'indicateurs performantes sur cette période en timeframe 5 minutes dans l'objectif de créer une stratégie rentable. 
On pourra ensuite tenter de faire varier les paramètres de ces indicateurs pour essayer d'améliorer les performances, en utilisant https://github.com/titouannwtt/Analyseur-PBM par exemple.

# Remerciement :
Certains bout de code du fichier "backtest_multi_indicator.py" sont issues des codes proposés par https://github.com/CryptoRobotFr/

Ce code vous est partagé gratuitement, vous pouvez me remercier en utilisant un de mes liens d'affiliations :

- FTX : https://ftx.com/eu/profile#a=titouannwtt

- Binance : https://www.binance.me/fr/activity/referral/offers/claim?ref=CPA_00C08H2X8E

Ou en me faisant des dons cryptos :

- Adresse BTC : 3GYhBgZMfgzqjYhVhc2w53oMcvZb4jfGfL

- Adresse ETH (Réseau ERC20) : 0x43fC6F9B8b1CfBd83b52a1FD1de510effe0A49a7

- Adresse SOL : 5QKaHfJWxAZ6sbU5QMb2e14yAAZ45iBH91SBgnheK26v

<p align="right">(<a href="#top">back to top</a>)</p>

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/titouan-wtt-78a941162/
