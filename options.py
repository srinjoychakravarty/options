import os, xlrd, numpy
import matplotlib.pyplot

def state_price_density(c_0303, strike_0303, st):                            # constructs a spread position and longs the call at k1 and shorts the call at k2      
    '''contingent claim, payoff when s&p 500 hits certain value'''
    N = len(c_0303)
    P = numpy.zeros((N, 1))                                                                 # (N, 1) returns a 100 rows by 1 column matrix of zeros if N = 100
    total = 0
    for n in range(0, N-1):
        if (n == 0):
            P[0] = 1 - ( (st - c_0303[0]) / strike_0303[0])
            total += P[0]
        else:
            P[n] = (1 - (c_0303[n] - c_0303[n - 1]) ) / (strike_0303[n] - strike_0303[n - 1]) 
            total += P[n]
    P[N - 1] = 1 - numpy.sum(P[0 : N - 1])                  # sum all values of the 100 (rows) x 1 (column) matrix and assigns it to the last row of the matrix
    P = numpy.sort(P, axis = 0)                              # sorts the values of the 100 rows in ascending order (smallest -> largest)
    dividend = (P[1 : N] - P[0 : N - 1])
    divisor = numpy.array(strike_0303[1 : N]) - numpy.array(strike_0303[0 : N - 1])         # converts both lists to numpy as you cant substract list from a list
    SPD = numpy.divide(dividend, divisor)
    SPD = numpy.nan_to_num(SPD)                                                             # Replace NaN with zero and infinity with large finite numbers
    SPD = SPD[2 : -1]
    return SPD

def process_call_contracts(contracts_worksheet):
    '''populates individual lists for call and put contracts'''
    rowcount = contracts_worksheet.nrows
    contract_types = []                                                 # list of option types                                
    for i in range (1, rowcount):
        contract_types.append(contracts_worksheet.cell_value(i, 3))
    call_contracts = []
    put_contracts = []
    for i in range (1, rowcount):
        if ("C" in contract_types[i - 1]):
            call_contracts.append(contracts_worksheet.row(i))
        else:
            put_contracts.append(contracts_worksheet.row(i))
    put_contract_count = len(put_contracts)
    call_contract_count = len(call_contracts)
    bids = []                                                           # list of BIDS for CALL options
    for i in range (0, call_contract_count):
        bids.append(call_contracts[i][5].value)
    asks = []                                                           # list of ASKS for CALL options
    for i in range (0, call_contract_count):
        asks.append(call_contracts[i][6].value)
    strikes = []                                                        # list of STRIKE PRICES for CALL options
    for i in range (0, call_contract_count):
        strikes.append(call_contracts[i][2].value)
    implied_volatilities = []                                           # list of IMPLIED VOLATILITIES for CALL options
    for i in range (0, call_contract_count):
        implied_volatilities.append(call_contracts[i][11].value)
    return (call_contract_count, bids, asks, strikes)

def list_bid_ask_call_spreads(call_contract_count, bids, asks):
    '''returns a list of bid-ask spreads for call options for a given expiry date'''
    call_spreads = []
    for i in range (0, call_contract_count):
        call_spreads.append( ( ( bids[i] + asks[i] ) / 2) )
    return call_spreads

def plot_contracts(spds):
    '''iterates and charts out state price densities for options contracts using matplotlib'''
    colours = ["blue", "orange", "green", "grey", "red", "black"]
    markers = ["o", "D", "o", "D", "o", "D"]
    for i in range(0, len(spds)):
        current_spd = spds[i]
        expiry_date = current_spd.get('expiry_date')
        current_spd_data = current_spd.get('spd')
        figure = matplotlib.pyplot.figure()
        axis = figure.add_subplot(111)
        axis.set_title(f"Call Option Expires: {expiry_date[0:2]}/{expiry_date[2:4]}")
        axis.set_xlabel('Dollars ($)')
        axis.set_ylabel('Bid / Ask Spread')
        axis.text(0.99, 0.5, 'General rule: Low spread < 0.3 = more liquid, willing market', style = 'italic', verticalalignment = 'bottom', horizontalalignment = 'right', transform = axis.transAxes, fontsize = 10)
        axis.plot(current_spd_data, marker = markers[i], color = colours[i], alpha = 0.3)
        matplotlib.pyplot.axhline(y = 0.31, color = 'r', linestyle = '-', label = 'less liquid spread' )
        matplotlib.pyplot.axhline(y = 0.29, color = 'b', linestyle = '--', label = 'more liquid spread' )
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
        # matplotlib.pyplot.savefig(f"{expiry_date}.png")

if __name__ == "__main__":
    directory = os.getcwd()
    filepath = f"{directory}/OPTIONS.xls"
    workbook = xlrd.open_workbook(filepath, on_demand = True)
    sheet_names = workbook.sheet_names()
    worksheets = []
    for i in range (0, len(sheet_names)):
        worksheets.append({sheet_names[i]: workbook.sheet_by_index(i)})
    state = 3819.72                                                                # state = total market value (top 500 US Securities) at time T (Mar 3, 2021)
    call_spds = []
    for i in range(0, len(worksheets)):
        expiry_date = list(worksheets[i].keys())[0]
        options_chain = worksheets[i].get(expiry_date)                                          # retrieves options chain for contracts at each expiry date
        (call_contract_count, bids, asks, strikes) = process_call_contracts(options_chain)      # lists key metrics of CALL contracts from options chain
        c_ = list_bid_ask_call_spreads(call_contract_count, bids, asks)                         # list of BID-ASK SPREADS for CALL options at each expiry date
        spd = state_price_density(c_, strikes, state)                                           # returns state price densities at each expiry date
        call_spds.append({'expiry_date': expiry_date, 'spd': spd, 'strike': strikes})
    plot_contracts(call_spds)