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
            # print(f"Base Case: {P[0]}")
        else:
            P[n] = (1 - (c_0303[n] - c_0303[n-1]) ) / (strike_0303[n] - strike_0303[n - 1]) 
            total += P[n]
            # print(f"Recursive Case: {P[n]}")

    P[N-1] = 1 - numpy.sum(P[0:N-1])    # sum all values of the 100 (rows) x 1 (column) matrix and assigns it to the last row of the matrix
    P = numpy.sort(P, axis = 0)         # sorts the values of the 100 rows in ascending order (smallest -> largest)
    print(P)
            

if __name__ == "__main__":
    directory = os.getcwd()
    filepath = f"{directory}/OPTIONS.xls"
    workbook = xlrd.open_workbook(filepath, on_demand = True)
    sheet_names = workbook.sheet_names()
    worksheets = []
    for i in range (0, len(sheet_names) - 1):
        worksheets.append({sheet_names[i]: workbook.sheet_by_index(i)})

    # st = state, total market value (top 500 US Securities) at time T (Mar 3, 2021)
    st = 3819.72 

    # analysis for option contracts expiring Mar 3, 2021
    options_expiring_0303 = worksheets[0].get('0303')
    options_expiring_0303_rowcount = options_expiring_0303.nrows

    # list of option types for 3 Mar
    type_0303 = []                                                     
    for i in range (1, options_expiring_0303_rowcount):
        type_0303.append(options_expiring_0303.cell_value(i, 3))
    # print(f"Option Types (March 3): {type_0303}")

    call_contracts = []
    put_contracts = []
    for i in range (1, options_expiring_0303_rowcount):
        if ("C" in type_0303[i - 1]):
            call_contracts.append(options_expiring_0303.row(i))
        else:
            put_contracts.append(options_expiring_0303.row(i))

    call_contract_count = len(call_contracts)
    put_contract_count = len(put_contracts)

    # list of STRIKE PRICES for CALL options on 3 Mar. 2021
    strike_0303 = []
    for i in range (0, call_contract_count):
        strike_0303.append(call_contracts[i][2].value)
    # print(f"Strike Prices (Calls): {strike_0303}")

    # list of IMPLIED VOLATILITIES for CALL options on 3 Mar. 2021
    implied_vol_0303 = []
    for i in range (0, call_contract_count):
        implied_vol_0303.append(call_contracts[i][11].value)
    # print(f"Implied Volatilties (Calls): {implied_vol_0303}")

    # list of BIDS for CALL options on 3 Mar. 2021
    bid_0303 = []
    for i in range (0, call_contract_count):
        bid_0303.append(call_contracts[i][5].value)
    # print(f"Bids (Calls): {bid_0303}")

    # list of ASKS for CALL options on 3 Mar. 2021
    ask_0303 = []
    for i in range (0, call_contract_count):
        ask_0303.append(call_contracts[i][6].value)
    # print(f"Asks (Calls): {ask_0303}")

    # list of BID-ASK SPREADS for CALL options on 3 Mar. 2021
    c_0303 = []
    for i in range (0, call_contract_count):
        c_0303.append( ( ( bid_0303[i] + ask_0303[i] ) / 2) )
    # print(f"Bid Ask Spread (Calls): {c_0303}")

    spd_0303 = state_price_density(c_0303, strike_0303, st)