# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 17:24:48 2015

@author: Niel
"""

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

    def __call__(self, quantity):
        """
        returns a tuple of:
        (per share commission, total transaction commission)
        """
        commission = abs(quantity * self.cost)
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

    def __call__(self, quantity):
        """
        returns a tuple of:
        (per share commission, total transaction commission)
        """
        if transaction.amount == 0:
            return 0.0, 0.0

        return abs(self.cost / quantity), self.cost


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

    def __call__(self, quantity):
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

    def __call__(self, quantity):
        '''
        returns a tuple of:
        (per share commission, total transaction commission)
        '''
        
        ipl = self.IPL*transaction.price # IPL
        # Commisions
        comm = max(self.broker*transaction.price, self.min_rand) 
        
        # VAT
        vat = (comm + self.STRATE + ipl) * 0.14 
    
        if quantity > 0:
            # STT only valid on Buy Transactions
            stt = self.STT * transaction.price
            
        else:
            stt = 0
            
        total_cost = comm + self.STRATE + ipl + vat + stt
        cost_per_share = total_cost / abs(quantity)
        return cost_per_share, total_cost

class SlippageModel(with_metaclass(abc.ABCMeta)):

    @property
    def volume_for_bar(self):
        return self._volume_for_bar

    @abc.abstractproperty
    def process_order(self, event, order):
        pass

    def simulate(self, event, current_orders):

        self._volume_for_bar = 0

        for order in current_orders:

            if order.open_amount == 0:
                continue

            order.check_triggers(event)
            if not order.triggered:
                continue

            txn = self.process_order(event, order)

            if txn:
                self._volume_for_bar += abs(txn.amount)
                yield order, txn

    def __call__(self, event, current_orders, **kwargs):
        return self.simulate(event, current_orders, **kwargs)


class VolumeShareSlippage(SlippageModel):

    def __init__(self,
                 volume_limit=.25,
                 price_impact=0.1):

        self.volume_limit = volume_limit
        self.price_impact = price_impact

    def process_order(self, event, order):

        max_volume = self.volume_limit * event.Volume

        # price impact accounts for the total volume of transactions
        # created against the current minute bar
        remaining_volume = max_volume - self.volume_for_bar
        if remaining_volume < 1:
            # we can't fill any more transactions
            return

        # the current order amount will be the min of the
        # volume available in the bar or the open amount.
        cur_volume = int(min(remaining_volume, abs(order.open_amount)))

        if cur_volume < 1:
            return

        # tally the current amount into our total amount ordered.
        # total amount will be used to calculate price impact
        total_volume = self.volume_for_bar + cur_volume

        volume_share = min(total_volume / event.Volume,
                           self.volume_limit)

        simulated_impact = volume_share ** 2 \
            * math.copysign(self.price_impact, order.direction) \
            * event.Price

        return create_transaction(
            event,
            order,
            # In the future, we may want to change the next line
            # for limit pricing
            event.Price + simulated_impact,
            math.copysign(cur_volume, order.direction)
        )


class VolumeShareMinSlippage(SlippageModel):
    '''
    
    Quadratic    
    
    Slippage = k * Volume **2 * price
    k - price impact
    
    At least 1 cent slippage
    
    '''
    
    def __init__(self, volume_limit=.25, price_impact=0.1):

        self.volume_limit = volume_limit
        self.price_impact = price_impact

    def process_order(self, event, order):

        max_volume = self.volume_limit * event.Volume

        # price impact accounts for the total volume of transactions
        # created against the current minute bar
        remaining_volume = max_volume - self.volume_for_bar
        if remaining_volume < 1:
            # we can't fill any more transactions
            return

        # the current order amount will be the min of the
        # volume available in the bar or the open amount.
        cur_volume = int(min(remaining_volume, abs(order.open_amount)))

        if cur_volume < 1:
            return

        # tally the current amount into our total amount ordered.
        # total amount will be used to calculate price impact
        total_volume = self.volume_for_bar + cur_volume

        volume_share = min(total_volume / event.Volume,
                           self.volume_limit)

        simulated_impact = max(volume_share ** 2 * math.copysign(self.price_impact, order.direction) * event.Price, 1)

        return create_transaction(
            event,
            order,
            # In the future, we may want to change the next line
            # for limit pricing
            event.Price + simulated_impact,
            math.copysign(cur_volume, order.direction)
        )


class FixedSlippage(SlippageModel):

    def __init__(self, spread=0.0):
        """
        Use the fixed slippage model, which will just add/subtract
        a specified spread spread/2 will be added on buys and subtracted
        on sells per share
        """
        self.spread = spread

    def process_order(self, event, order):
        return create_transaction(
            event,
            order,
            event.price + (self.spread / 2.0 * order.direction),
            order.amount,
        )