#
# Copyright 2015 Quantopian, Inc.
# Copyright 2015 Intersect Technologies CC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class PerShare(object):
    """
    Calculates a commission for a transaction based on a per
    share cost with an optional minimum cost per trade.
    """

    def __init__(self, cost=0.03, min_trade_cost=None):
        """
        Cost parameter is the cost of a trade per-share. $0.03
        means three cents per share, which is a very conservative
        (quite high) for per share costs.
        min_trade_cost parameter is the minimum trade cost
        regardless of the number of shares traded (e.g. $1.00).
        """
        self.cost = float(cost)
        self.min_trade_cost = None if min_trade_cost is None\
            else float(min_trade_cost)

    def __repr__(self):
        return "{class_name}(cost={cost}, min trade cost={min_trade_cost})"\
            .format(class_name=self.__class__.__name__,
                    cost=self.cost,
                    min_trade_cost=self.min_trade_cost)

    def calculate(self, transaction):
        """
        returns a tuple of:
        (per share commission, total transaction commission)
        """
        commission = abs(transaction.amount * self.cost)
        if self.min_trade_cost is None:
            return self.cost, commission
        else:
            commission = max(commission, self.min_trade_cost)
            return abs(commission / transaction.amount), commission


class PerTrade(object):
    """
    Calculates a commission for a transaction based on a per
    trade cost.
    """

    def __init__(self, cost=5.0):
        """
        Cost parameter is the cost of a trade, regardless of
        share count. $5.00 per trade is fairly typical of
        discount brokers.
        """
        # Cost needs to be floating point so that calculation using division
        # logic does not floor to an integer.
        self.cost = float(cost)

    def calculate(self, transaction):
        """
        returns a tuple of:
        (per share commission, total transaction commission)
        """
        if transaction.amount == 0:
            return 0.0, 0.0

        return abs(self.cost / transaction.amount), self.cost


class PerDollar(object):
    """
    Calculates a commission for a transaction based on a per
    dollar cost.
    """

    def __init__(self, cost=0.0015):
        """
        Cost parameter is the cost of a trade per-dollar. 0.0015
        on $1 million means $1,500 commission (=1,000,000 x 0.0015)
        """
        self.cost = float(cost)

    def __repr__(self):
        return "{class_name}(cost={cost})".format(
            class_name=self.__class__.__name__,
            cost=self.cost)

    def calculate(self, transaction):
        """
        returns a tuple of:
        (per share commission, total transaction commission)
        """
        cost_per_share = transaction.price * self.cost
        return cost_per_share, abs(transaction.amount) * cost_per_share
    
class PerRand(object):
    
    '''
    Calculates a commission for a transaction based on a per  Rand cost.
    Default values based on JSE trading
    
    STT: 0.25%
    IPL: 0.0002%
    STRATE: R 10.92
    Broker Commision: 0.4%
	
    	VAT @ 14% on VAT = (Broker + STRATE + IPL)*0.14
    '''			
    
    def __init__(self, broker=0.4, min_rand = 100, STT=0.25, IPL=0.0002, STRATE=10.92):
        """
        Cost parameter is the cost of a trade per-rand. 0.004
        on R1 million means R4 000 commission (=1,000,000 x 0.0015)
        """
        self.broker = float(broker) / 100
        self.min_rand = min_rand * 100
        self.STRATE = STRATE*100
        self.IPL = float(IPL) / 100
        self.STT = float(STT)

    def __repr__(self):
        return "{class_name}(cost={cost})".format(
            class_name=self.__class__.__name__,
            cost=self.cost)

    def calculate(self, transaction):
        '''
        returns a tuple of:
        (per share commission, total transaction commission)
        '''
        
        ipl = self.IPL*transaction.price # IPL
        # Commisions
        comm = max(self.broker*transaction.price, self.min_rand) 
        
        # VAT
        vat = (comm + self.STRATE + ipl) * 0.14 
    
        if transaction.amount > 0:
            # STT only valid on Buy Transactions
            stt = self.STT * transaction.price
            
        else:
            stt = 0
            
        total_cost = comm + self.STRATE + ipl + vat + stt
        cost_per_share = total_cost / abs(transaction.amount)
        return cost_per_share, total_cost
	