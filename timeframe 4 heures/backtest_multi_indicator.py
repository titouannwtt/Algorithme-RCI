################################################################
import sys, getopt
import sys
sys.path.append( '../utilities' )
from data_engine import DataEngine
from backtesting import Backtesting
from backtesting import Backtesting
import pandas as pd
import pandas_ta as pda
import ta
import others as o1
import ccxt
import json
f = open('../database/pair_list.json',)
pairJson = json.load(f)
f.close()
#import pandas_ta as pda
from custom_indicators import CustomIndocators as ci
import numpy as np
from datetime import datetime, timedelta

################################################################
##################
#HYPERPARAMÈTRE
##################

dateAnnee='2022'
dateMois='05'
dateJour='01'

# -- Starting value --
startingBalance = 1000
makerFee = 0.0002
takerFee = 0.0007

# -- Rules --
showLog = False

# -- Hyper parameters --
SlPct = 0.007
TpPct = 0.007
maxPositions = 3


################################################################
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
try:
    test=sys.argv[20]
    if(sys.argv[1]=='1'):
        useCCI=True
    else :
        useCCI=False

    if(sys.argv[2]=='1'):
        usePVO=True
    else :
        usePVO=False
        
    if(sys.argv[3]=='1'):
        useWillr=True
    else :
        useWillr=False
     
    if(sys.argv[4]=='1'):
        useKama=True
    else :
        useKama=False
     
    if(sys.argv[5]=='1'):
        useAO=True
    else :
        useAO=False
     
    if(sys.argv[6]=='1'):
        useSP=True
    else :
        useSP=False
     
    if(sys.argv[7]=='1'):
        usePsar=True
    else :
        usePsar=False
     
    if(sys.argv[8]=='1'):
        useAtr=True
    else :
        useAtr=False
     
    if(sys.argv[9]=='1'):
        useAdx=True
    else :
        useAdx=False
     
    if(sys.argv[10]=='1'):
        useAroon=True
    else :
        useAroon=False
     
    if(sys.argv[11]=='1'):
        useKeltner=True
    else :
        useKeltner=False
     
    if(sys.argv[12]=='1'):
        useBoll=True
    else :
        useBoll=False
     
    if(sys.argv[13]=='1'):
        useStochrsi=True
    else :
        useStochrsi=False
     
    if(sys.argv[14]=='1'):
        useMacd=True
    else :
        useMacd=False
     
    if(sys.argv[15]=='1'):
        useKst=True
    else :
        useKst=False
     
    if(sys.argv[16]=='1'):
        useVol=True
    else :
        useVol=False
     
    if(sys.argv[17]=='1'):
        useTrix=True
    else :
        useTrix=False
     
    if(sys.argv[18]=='1'):
        useEmad=True
    else :
        useEmad=False
     
    if(sys.argv[19]=='1'):
        useEma=True
    else :
        useEma=False
     
    if(sys.argv[20]=='1'):
        useHichi=True
    else :
        useHichi=False
except :
    print( "Use :"
            "\nuseCCI=",   #5
            "\nusePVO=",     #6 
            "\nuseWillr=",   #7
            "\nuseKama=", #8
            "\nuseAO=",    #9
            "\nuseSP=", #10
            "\nusePsar=",
            "\nuseAtr=",    #12
            "\nuseAdx=",  #13
            "\nuseAroon=",   #14
            "\nuseKeltner=",   #15
            "\nuseBoll=",   #16
            "\nuseStochrsi=", #17
            "\nuseMacd=",   #18
            "\nuseKst=",  #19
            "\nuseVol=", #20
            "\nuseTrix=",   #21
            "\nuseEmad=",  #22
            "\nuseEma=", #23
            "\nuseHichi=",  #24
            )

################################################################
pairList = pairJson['all']
timeframe = '4h'
startDate = '2022-05-01T00:00:00'

dfList = []
if 1==1 :
    #On précise sur quel exchange on se base :
    if 1==1 :
        try :
            #print("Récupération des données FTX...")
            dataEngine = DataEngine(session=ccxt.ftx(), path_to_data='../database/')
        except :
            print("Une erreur est survenue en tentant de récupérer les données, on attend 10 secondes...")
            time.sleep(10)
            try :
                dataEngine = DataEngine(session=ccxt.ftx(), path_to_data='../database/')
            except Exception as error :
                interrompre=True
                print(f"Error : {error}")
        
        if 1==1 :
            for pair in pairList:
                df = dataEngine.get_historical_from_db(pair, timeframe, startDate)
                if df is None or (df.empty==True) :
                    #print(f"Données introuvables ou corrompues pour {pair} en timeframe {timeframe}, tentative de récupération sur l'API...")
                    # -- Download data from data variable --
                    timeframes = [f'{timeframe}']
                    pair_symbol = [f'{pair}']
                    dataEngine.download_data(pair_symbol, timeframes, startDate)
                    df = dataEngine.get_historical_from_db(pair, timeframe, startDate)
                    if df is not None :
                        pass
                        #print(f"Les données de {pair} en timeframe {timeframe} ont bien été récupérées sur l'API\n")
                    elif df is None :
                        #print(f"Echec, on reessaye, peut être que l'API n'était pas joignable.")
                        dataEngine.download_data(pair_symbol, timeframes, startDate)
                        df = dataEngine.get_historical_from_db(pair, timeframe, startDate)
                        if df is not None :
                            pass
                            #print(f"Les données de {pair} en timeframe {timeframe} ont bien été récupérées sur l'API\n")
                        elif df is None :
                            pass
                            #print(f"Les données de {pair} en timeframe {timeframe} n'ont pas été récupérées correctement sur l'API\n")
                try :
                    dfList.append(df.loc[startDate:])
                except :
                    pass
                    #print(f"Impossible de prendre en compte la paire : {pair}")




useBolh=True

################################################
# -- Drop all columns we do not need --
for df in dfList:
    # -- Drop all columns we do not need --
    df.drop(columns=df.columns.difference(['open','high','low','close','volume']), inplace=True)
    # -- Indicators, you can edit every value --

    if useHichi == True:
        df['base'] = ta.trend.ichimoku_base_line(df['high'], df['low'], window1=9, window2=26)
        df['spanb'] = ta.trend.ichimoku_b(df['high'], df['low'], window2=25, window3=52, visual=True)
    
    if useEma == True:
        df['ema10']=ta.trend.ema_indicator(close=df['close'], window=10)
        df['ema50']=ta.trend.ema_indicator(close=df['close'], window=50)

    if useEmad == True:
        df['ema9d']=ta.trend.ema_indicator(close=df['close'], window=216)
        df['ema13d']=ta.trend.ema_indicator(close=df['close'], window=312)

    if useTrix == True:
        trixLength = 8
        trixSignal = 21
        df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trixLength), window=trixLength), window=trixLength)
        df['TRIX_PCT'] = df["TRIX"].pct_change()*100
        df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trixSignal)
        df['trix'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']
    
    if useVol == True:    
        vol = ta.volume.MFIIndicator(df['high'], df['low'], df['close'], df['volume'], window = 14)
        df['vol'] = vol.money_flow_index()
    
    if useKst == True:
        kst = ta.trend.KSTIndicator(close=df['close'], roc1 = 10, roc2= 15, roc3 = 20, roc4 = 30, window1 = 10, window2 = 10, window3 = 10, window4 = 15, nsig = 9) 
        df['kst'] = kst.kst_diff()
    
    if useMacd == True:
        MACD = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=10)
        df['macd'] = MACD.macd_diff()

    if useStochrsi == True:
        df['stochrsi'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3)

    if useBolh == True:
        BOL_BAND = ta.volatility.BollingerBands(close=df['close'], window=44, window_dev=2) 
        df['bolh'] = BOL_BAND.bollinger_hband_indicator()

    if useBoll == True:
        BOL_BAND = ta.volatility.BollingerBands(close=df['close'], window=44, window_dev=2)     
        df['boll'] = BOL_BAND.bollinger_lband_indicator()
    
    if useKeltner == True:
        keltner = ta.volatility.KeltnerChannel(df['high'], df['low'], df['close'], window = 10, window_atr = 10)
        df['keltnerl'] = keltner.keltner_channel_lband_indicator()
        df['keltnerh'] = keltner.keltner_channel_hband_indicator()


    if useAroon == True:
        Aroon = ta.trend.AroonIndicator(close=df['close'], window = 25)
        df['aroon'] = Aroon.aroon_indicator()
    
    if useAdx == True:
        ADX = ta.trend.ADXIndicator(df['high'], df['low'], df['close'], window=20)
        df['ADX'] = ADX.adx()
        df['ADX_NEG'] = ADX.adx_neg()
        df['ADX_POS'] = ADX.adx_pos()
        df['adx'] = df['ADX_POS'] - df['ADX_NEG']

    if useAtr == True:
        df['atr'] = ta.volatility.average_true_range(high=df['high'], low=df['low'], close=df['close'], window=14)

    if usePsar == True:
        PSAR = ta.trend.PSARIndicator(df['high'], df['low'], df['close'], step = 0.2, max_step = 0.2)
        df['psar'] = PSAR.psar()

    
 #   if sp == True:
 #       ST_length = 10
 #       ST_multiplier = 3
 #       superTrend = pda.supertrend(high=df['high'], low=df['low'], close=df['close'], length=ST_length, multiplier=ST_multiplier)
 #       df['SUPER_TREND'] = superTrend['SUPER_TREND'+str(ST_length)+"_"+str(ST_multiplier)] 
 #       df['sp'] = superTrend['SUPER_TREND_DIRECTION'+str(ST_length)+"_"+str(ST_multiplier)] 
    
    if useAO == True:
        df['ao'] = ta.momentum.awesome_oscillator(high=df['high'], low=df['low'], window1=5, window2=34)

    if useKama == True:
        df['kama'] = ta.momentum.kama(close=df['close'], window=10, pow1=2, pow2=30)

    if useWillr == True:
        df['willr'] = ta.momentum.williams_r(high=df['high'], low=df['low'], close=df['close'], lbp=10)

    if usePVO == True:
        pvo = ta.momentum.PercentageVolumeOscillator(df['volume'], window_slow = 26, window_fast = 12, window_sign = 15)
        df['pvo'] = pvo.pvo_hist()

    if useCCI == True:
        CCI = ta.trend.CCIIndicator(df['high'], df['low'], df['close'], window = 20, constant = 0.015)
        df['cci'] = CCI.cci()

dfTestList = []
for df in dfList:
    dfTestList.append(df.loc['2022-05-01':'2022-06-30'])

# -- Trade Functions --
# -- Condition to BUY market --
    
def buyCondition(row, previousRow=None):
    if (    ((useCCI==True and row['cci'] <= -100) or useCCI==False)
        and ((usePVO==True and row['pvo'] > 0) or usePVO==False)
        and ((useWillr==True and row['willr'] < -85) or useWillr==False)
        and ((useKama==True and row['close'] > row['kama']) or useKama==False)
        and ((useAO==True and row['ao'] > 0) or useAO==False)
        and ((useSP==True and row['sp'] == 1) or useSP==False)
        and ((usePsar==True and row['psar'] < row['close']) or usePsar==False)
        and ((useAtr==True and row['atr'] > previousRow['atr']) or useAtr==False)
        and ((useAdx==True and row['adx'] > 0) or useAdx==False)
        and ((useAroon==True and row['aroon'] > 0) or useAroon==False)
        and ((useKeltner==True and row['keltnerl'] > row['close']) or useKeltner==False)
        and ((useBoll==True and row['boll'] > row['close']) or useBoll==False)
        and ((useStochrsi==True and row['stochrsi'] < 0.85) or useStochrsi==False)
        and ((useMacd==True and row['macd'] > 0) or useMacd==False)
        and ((useKst==True and row['kst'] > 0) or useKst==False)
        and ((useVol==True and row['vol'] < 20) or useVol==False)
        and ((useTrix==True and row['trix'] > 0) or useTrix==False)
        and ((useEmad==True and row['ema9d'] > row['ema13d']) or useEmad==False)
        and ((useEma==True and row['ema10'] > row['ema50']) or useEma==False)
        and ((useHichi==True and row['base'] > row['spanb']) or useHichi==False)
    ):
        return True
    else:
        return False

# -- Condition to SELL market --
def sellCondition(row, previousRow=None):
    if (    ((useCCI==True and row['cci'] >= 100) or useCCI==False)
        and ((usePVO==True and row['pvo'] < 0) or usePVO==False)
        and ((useWillr==True and row['willr'] > -10) or useWillr==False)
        and ((useKama==True and row['close'] < row['kama']) or useKama==False)
        and ((useAO==True and row['ao'] < 0) or useAO==False)
        and ((useSP==True and row['sp'] == -1) or useSP==False)
        and ((usePsar==True and row['psar'] > row['close']) or usePsar==False)
        and ((useAtr==True and row['atr'] < previousRow['atr']) or useAtr==False)
        and ((useAdx==True and row['adx'] < 0) or useAdx==False)
        and ((useAroon==True and row['aroon'] < 0) or useAroon==False)
        and ((useKeltner==True and row['keltnerl'] < row['close']) or useKeltner==False)
        and ((useBoll==True and row['boll'] > row['close']) or useBoll==False)
        and ((useStochrsi==True and row['stochrsi'] > 0.23) or useStochrsi==False)
        and ((useMacd==True and row['macd'] < 0) or useMacd==False)
        and ((useKst==True and row['kst'] < 0) or useKst==False)
        and ((useVol==True and row['vol'] > 80) or useVol==False)
        and ((useTrix==True and row['trix'] < 0) or useTrix==False)
        and ((useEmad==True and row['ema9d'] < row['ema13d']) or useEmad==False)
        and ((useEma==True and row['ema10'] < row['ema50']) or useEma==False)
        and ((useHichi==True and row['base'] < row['spanb']) or useHichi==False)
    ):
        return True
    else:
        return False

# -- Value initialisation --
usd = startingBalance
wallet = startingBalance
stopLoss = [0] * len(pairList)
takeProfit = [5000000] * len(pairList)
walletCoinArray = [0] * len(pairList)
walletUsdArray = [0] * len(pairList)
activePositions = 0
try :
	lastIndex = dfTestList[0].index.values[1]
except :
	lastIndex = 0
Max = []

# -- Definition of dfTrades, that will be the dataset to do your trades analyses --
dfTrades = None
dfTrades = pd.DataFrame(columns=['date', 'symbol','position', 'reason', 'price', 'frais', 'fiat', 'coins', 'wallet'])

# # -- Iteration on all your price dataset (df) --
for index, row in dfTestList[0].iterrows():
    # -- Check if you have one coin in your wallet --
    if (walletCoinArray.count(0) == len(walletCoinArray)) == False:
        # -- Iteration on all coin (upgrade possible: only check coin in your wallet) --
        for i in range(0,len(dfTestList)):
            # -- Check if you have more than 0 coin --
            if walletCoinArray[i] != 0:
                try:
                    actualRow = dfTestList[i].loc[index]
                    previousRow = dfTestList[i].loc[lastIndex]
                    #-- Sell Market --
                    if sellCondition(actualRow, previousRow):
                        sellPrice = actualRow['close']
                        usd = usd + walletCoinArray[i] * sellPrice
                        fee = makerFee * walletCoinArray[i] * sellPrice
                        usd = usd - fee
                        #-- Set coin and equivalent usd to 0 after sold position --
                        walletCoinArray[i] = 0
                        walletUsdArray[i] = 0
                        activePositions -= 1
                        #-- LOG --
                        if showLog:
                            print("Sell", pairList[i],"at", sellPrice, '$ the', index)
                        #-- Add the trade to DfTrades to analyse it later --
                        myrow = {
                            'date': index,
                            'symbol': pairList[i],
                            'position': "Sell",
                            'reason': 'Sell Market Order',
                            'price': sellPrice,
                            'frais': fee,
                            'fiat': usd,
                            'coins': 0,
                            'wallet': sum(walletUsdArray) + usd}
                        dfTrades = dfTrades.append(myrow, ignore_index=True)
                except:
                    pass
    # -- Buy market order --
    # -- Check if you can open a new position --
    if activePositions < maxPositions:
        for i in range(0,len(dfTestList)):
            try:
                actualRow = dfTestList[i].loc[index]
                previousRow = dfTestList[i].loc[lastIndex]
            # -- Buy condition --
                if buyCondition(actualRow, previousRow) and activePositions < maxPositions and walletCoinArray[i]==0:
                    buyPrice = actualRow['close']
                    # -- Define size of the position --
                    usdMultiplier = 1/(maxPositions-activePositions)
                    fee = takerFee * usd * usdMultiplier
                    usd = usd - fee
                    coin = (usd * usdMultiplier) / buyPrice
                    usd = usd - (usd * usdMultiplier)
                    # -- Set coin and equivalent usd to size of position after open position --
                    walletCoinArray[i] = coin
                    walletUsdArray[i] = coin * actualRow['close']
                    activePositions += 1
                    # -- LOG --
                    if showLog:
                        print("Buy", pairList[i],"at", buyPrice, '$ the', index)
                    # -- Add the trade to dfTrades to analyse it later --
                    myrow = {'date': index,'symbol': pairList[i],'position': "Buy",'reason': 'Buy Market Order','price': buyPrice,'frais': fee,'fiat': usd,'coins': coin,'wallet': sum(walletUsdArray) + usd}
                    dfTrades = dfTrades.append(myrow, ignore_index=True) 
            except:
                pass
    else:
        Max.append(1)
    # -- Keep last index to define last row --            
    lastIndex = index

BTobject = Backtesting()
if (sum(walletUsdArray) + usd) != startingBalance :
    BTobject.multi_spot_backtest_print(dfTrades=dfTrades, dfTest=dfTestList[0], pairList=pairList, timeframe=timeframe)

#newDf = BTobject.multi_spot_backtest_analys(dfTrades=dfTrades, dfTest=dfTestList[0], pairList=pairList, timeframe=timeframe)
