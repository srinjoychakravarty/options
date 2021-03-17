import os, xlrd, numpy

# constructs a spread position and longs the call at k1 and shorts the call at k2
def state_price_density(c_0303, strike_0303, st):       
    '''contingent claim, payoff when s&p 500 hits certain value'''
    N = len(c_0303)
    P = numpy.zeros((N, 1))             # (N, 1) returns a 100 rows by 1 column matrix of zeros if N = 100
    total = 0
    for n in range(0, N-1):
        if (n == 0):
            P[0] = 1 - ( (st - c_0303[0]) / strike_0303[0])
            total += P[0]
        else:
            P[n] = (1 - (c_0303[n] - c_0303[n - 1]) ) / (strike_0303[n] - strike_0303[n - 1]) 
            total += P[n]

    P[N - 1] = 1 - numpy.sum(P[0 : N - 1])      # sum all values of the 100 (rows) x 1 (column) matrix and assigns it to the last row of the matrix
    P = numpy.sort(P, axis = 0)                 # sorts the values of the 100 rows in ascending order (smallest -> largest)

    dividend = (P[1 : N] - P[0 : N - 1])
    divisor = numpy.array(strike_0303[1 : N]) - numpy.array(strike_0303[0 : N - 1])         # converts both lists to numpy as you cant substract list from a list
    SPD = numpy.divide(dividend, divisor)
    SPD = numpy.nan_to_num(SPD)                 # Replace NaN with zero and infinity with large finite numbers
    SPD = SPD[2 : -1]
    
    return SPD

def filter_calls_from_puts(contracts_worksheet):
    '''populates individual lists for call and put contracts'''
   
    rowcount = contracts_worksheet.nrows
    contract_types = []                                                 # list of option types for 3 Mar                                
    for i in range (1, rowcount):
        contract_types.append(contracts_worksheet.cell_value(i, 3))
    
    call_contracts = []
    put_contracts = []

    for i in range (1, rowcount):
        if ("C" in contract_types[i - 1]):
            call_contracts.append(contracts_worksheet.row(i))
        else:
            put_contracts.append(contracts_worksheet.row(i))

    return (call_contracts, put_contracts)
    

def list_bids():
    ''' '''

def list_asks():
    ''' '''

def list_bid_ask_call_spreads(call_contract_count, bid_list, ask_list):
    '''returns a list of bid-ask spreads for call options for a given expiry date'''
    call_spreads = []
    for i in range (0, call_contract_count):
        call_spreads.append( ( ( bid_list[i] + ask_list[i] ) / 2) )
    return call_spreads
    
if __name__ == "__main__":
    directory = os.getcwd()
    filepath = f"{directory}/OPTIONS.xls"
    workbook = xlrd.open_workbook(filepath, on_demand = True)
    sheet_names = workbook.sheet_names()
    worksheets = []
    for i in range (0, len(sheet_names)):
        worksheets.append({sheet_names[i]: workbook.sheet_by_index(i)})

    # st = state, total market value (top 500 US Securities) at time T (Mar 3, 2021)
    st = 3819.72 

    # analysis for option contracts expiring Mar 3, 2021
    options_expiring_0303 = worksheets[0].get('0303')
  
    (call_contracts, put_contracts)  = filter_calls_from_puts(options_expiring_0303)

    put_contract_count_0303 = len(put_contracts)
    call_contract_count_0303 = len(call_contracts)

    # list of STRIKE PRICES for CALL options on 3 Mar. 2021
    strike_0303 = []
    for i in range (0, call_contract_count_0303):
        strike_0303.append(call_contracts[i][2].value)
    # print(f"Strike Prices (Calls): {strike_0303}")

    # list of IMPLIED VOLATILITIES for CALL options on 3 Mar. 2021
    implied_vol_0303 = []
    for i in range (0, call_contract_count_0303):
        implied_vol_0303.append(call_contracts[i][11].value)
    # print(f"Implied Volatilties (Calls): {implied_vol_0303}")

    # list of BIDS for CALL options on 3 Mar. 2021
    bid_list_0303 = []
    for i in range (0, call_contract_count_0303):
        bid_list_0303.append(call_contracts[i][5].value)
    # print(f"Bids (Calls): {bid_0303}")

    # list of ASKS for CALL options on 3 Mar. 2021
    ask_list_0303 = []
    for i in range (0, call_contract_count_0303):
        ask_list_0303.append(call_contracts[i][6].value)
    # print(f"Asks (Calls): {ask_0303}")

    ask_list_0303 = list_asks()

    # list of BID-ASK SPREADS for CALL options on 3 Mar. 2021
    c_0303 = list_bid_ask_call_spreads(call_contract_count_0303, bid_list_0303, ask_list_0303)

    spd_0303 = state_price_density(c_0303, strike_0303, st)
    print(spd_0303)
    
    # print(worksheets)