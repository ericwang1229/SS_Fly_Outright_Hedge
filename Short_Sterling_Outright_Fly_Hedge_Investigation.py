import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
         
    
class trades:
    trades = []
    position = 0
    def __init__(self):
        pass
    def add(self, datetime, price, lots):
        self.position += lots
        self.trades.append([datetime, price, lots])
    def pnl(self):
        temp = 0
        pnl = 0
        for trade in self.trades:
            temp += trade[2]
            pnl -= trade[1] * trade[2]
        return pnl
    
path = "L_History.xlsx"
xls = pd.ExcelFile(path)
data = {}
for sheet_name in xls.sheet_names:
    data[sheet_name] = xls.parse(sheet_name)
    data[sheet_name].columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
outrights = xls.sheet_names[0:12]
flies = xls.sheet_names[12:]

h5h6 = data['BL-H5H6 Comdty']
u5 = data['L U5 Comdty']

rolling_window = 20
trade_recorder = {}
m = pd.merge(u5, h5h6, on = "DateTime", suffixes = ('_u5', '_h5h6'))
for i in range(2, 11):
    index = 'hr_'+i.__str__()
    trade_recorder[index] = trades()
    m[index] = -i*m['Close_u5'] + m['Close_h5h6']
    m[index+'_mean'] = pd.rolling_mean(m[index], rolling_window)
    m[index+'_std']  = pd.rolling_var (m[index], rolling_window)
    for rn in range(1,len(m)):
        if (m.iloc[rn-1][index] > m.iloc[rn][index+'_mean'] + 2*m.iloc[rn][index+'_std']) and\
           (m.iloc[rn][index] < m.iloc[rn][index+'_mean'] + 2*m.iloc[rn][index+'_std']) and\
           (trade_recorder[index].position == 0):
            trade_recorder[index].add(m.iloc[rn]['DateTime'],
                              m.iloc[rn][index],
                              -1)
        if m.iloc[rn-1][index] < m.iloc[rn][index+'_mean'] - 2*m.iloc[rn][index+'_std'] and\
           m.iloc[rn][index] > m.iloc[rn][index+'_mean'] - 2*m.iloc[rn][index+'_std'] and\
           trade_recorder[index].position == 0:
            trade_recorder[index].add(m.iloc[rn]['DateTime'],
                              m.iloc[rn][index],
                              1)
        if trade_recorder[index].position > 0 and\
           m.iloc[rn][index] > m.iloc[rn][index+'_mean'] + m.iloc[rn][index+'_std']:
            trade_recorder[index].add(m.iloc[rn]['DateTime'],
                              m.iloc[rn][index],
                              -1)
        if trade_recorder[index].position < 0 and\
           m.iloc[rn][index] < m.iloc[rn][index+'_mean'] - m.iloc[rn][index+'_std']:
            trade_recorder[index].add(m.iloc[rn]['DateTime'],
                              m.iloc[rn][index],
                              1)
    if trade_recorder[index].position <> 0:
            trade_recorder[index].add(m.iloc[len(m)-1]['DateTime'],
                              m.iloc[len(m)-1][index],
                              -trade_recorder[index].position)
    print index + ", " + trade_recorder[index].pnl().__str__()
        
            
def plot(outright_index, fly_index, hedged_index):
    date = m["DateTime"].tolist()
    outright_prices = m[outright_index].values.tolist()
    fly_prices = m[fly_index].values.tolist()
    hedged_prices = m[hedged_index].values.tolist()
    upper_band = (m[hedged_index+"_mean"]+2*m[hedged_index+"_std"]).values.tolist()
    lower_band = (m[hedged_index+"_mean"]-2*m[hedged_index+"_std"]).values.tolist()
    buy_dates = [x[0] for x in trade_recorder[hedged_index].trades if x[2]>0]
    buy_prices = [x[1] for x in trade_recorder[hedged_index].trades if x[2]>0]
    sell_dates = [x[0] for x in trade_recorder[hedged_index].trades if x[2]<0]
    sell_prices = [x[1] for x in trade_recorder[hedged_index].trades if x[2]<0]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex = True)
    mondays = WeekdayLocator(MONDAY)
    mondays.MAXTICKS = 2000
    alldays = DayLocator()              # minor ticks on the days
    alldays.MAXTICKS = 2000
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_minor_locator(alldays)
    ax1.xaxis.set_major_formatter(weekFormatter)
    
    ax1.plot(date, outright_prices)
    ax2.plot(date, fly_prices)
    ax3.plot(date, hedged_prices)
    ax3.plot(date, upper_band, color='k')
    ax3.plot(date, lower_band, color='k')
##    ax3.plot(buy_dates, buy_prices, "^", markersize = 5, color='m')
##    ax3.plot(sell_dates, sell_prices, "v", markersize = 5, color='k')
    
    ax1.xaxis_date()
    ax1.autoscale_view()

plot("Close_u5", "Close_h5h6", "hr_7")
plt.show()
