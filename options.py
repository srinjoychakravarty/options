import os, xlrd

directory = os.getcwd()
filepath = f"{directory}/OPTIONS.xls"
workbook = xlrd.open_workbook(filepath, on_demand = True)
sheet_names = workbook.sheet_names()
worksheets = []
for i in range (0, len(sheet_names) - 1):
    worksheets.append({sheet_names[i]: workbook.sheet_by_index(i)})

# measure of price performance of top 500 securities (by total market value) in US as of Mar 3, 2021
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

# list of ___ for CALL options on 3 Mar. 2021
c_0303 = []
for i in range (0, call_contract_count):
    c_0303.append( ( ( bid_0303[i] + ask_0303[i] ) / 2) )
print(f"C (Calls): {c_0303}")
