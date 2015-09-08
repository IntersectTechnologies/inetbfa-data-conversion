
def update_nwu_momentum_portfolio():
    
    enddt = last_month_end()
    tmpd = enddt - dt.timedelta(days=365)
    startdt = dt.date(tmpd.year, tmpd.month+1, 1)
    mom = NWUMomentum(startdt, enddt)

    mom.calc_momentum()
    mom.save()

def update_growth_portfolio():
    enddt = last_month_end()
    tmpd = enddt - dt.timedelta(days=365)
    startdt = dt.date(tmpd.year, tmpd.month+1, 1)
    mom = Momentum(startdt, enddt)

    mom.calc_momentum()
    mom.save()


def task_portfolios():
    return {
        'actions':['update_nwu_momentum_portfolio', 'update_growth_portfolio']
    }