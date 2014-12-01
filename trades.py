class trades:
    def __init__(self):
        self.trades = []
        self.position = 0
    def add(self, datetime, price, lots, note):
        self.position += lots
        self.trades.append([datetime, price, lots, note])
    def pnl(self):
        temp = 0
        pnl = 0
        for trade in self.trades:
            temp += trade[2]
            pnl -= trade[1] * trade[2]
        return pnl
