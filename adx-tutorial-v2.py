import pandas as pd 
pd.options.mode.chained_assignment = None


stock_data = pd.read_csv('data/cs-adx.csv')
stock_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

print()
print()

high, low, close = 'High', 'Low', 'Close'

columns = ['Date', high, low, close]

stock_data = stock_data[columns]



def calc_val(df, column):
    prev_val = df.loc[i-1, column]
    curr_val = df.loc[i, column]
    return(curr_val, prev_val)

def calc_dm(df, index):
    curr_high, prev_high = calc_val(df, high)
    curr_low, prev_low = calc_val(df, low)

    dm_pos = curr_high - prev_high
    dm_neg = prev_low - curr_low
    
    if dm_pos > dm_neg:
        if dm_pos < 0:
            dm_pos = 0.00
        dm_neg = 0.00
        return(dm_pos, dm_neg)

    elif dm_pos < dm_neg:
        if dm_neg < 0:
            dm_neg = 0.00
        dm_pos = 0.00
        return(dm_pos, dm_neg)
    
    else:
        if dm_pos < 0:
            dm_pos = 0.00
        dm_neg = 0.00
        return(dm_pos, dm_neg)

def calc_tr(df, index):
    curr_high, prev_high = calc_val(df, high)
    curr_low, prev_low = calc_val(df, low)
    curr_close, prev_close = calc_val(df, close)
    ranges = [curr_high - curr_low, abs(curr_high - prev_close), abs(curr_low - prev_close)]
    TR = max(ranges)
    return(TR)

def calc_first_14(df, index, column):
    result = 0
    for i in range(index-13, index+1):
        result += df.loc[i, column]
    return(result)

def calc_subsequent_14(df, index, column):
    return(df.loc[index-1, column+'14'] - (df.loc[index-1, column+'14']/14) + df.loc[index, column])


def calc_first_adx(df, index):
    result = 0
    for i in range(index-13, index+1):
        result += df.loc[i, 'DX']
    return(result/14)

def calc_adx(df, index):
    return(round(((df.loc[index-1, 'ADX']*13) + df.loc[index, 'DX'])/14, 2))


for i in range(1, len(stock_data)):
    dm_pos, dm_neg = calc_dm(stock_data, i)
    TR = calc_tr(stock_data, i)
    stock_data.loc[i, '+DM'] = dm_pos
    stock_data.loc[i, '-DM'] = dm_neg
    stock_data.loc[i, 'TR'] = TR

    if stock_data.TR.count() == 14:
        stock_data.loc[i, 'TR14'] = calc_first_14(stock_data, i, 'TR')
        stock_data.loc[i, '+DM14'] = calc_first_14(stock_data, i, '+DM')
        stock_data.loc[i, '-DM14'] = calc_first_14(stock_data, i, '-DM')

    elif stock_data.TR.count() >= 14:
        stock_data.loc[i, 'TR14'] = round(calc_subsequent_14(stock_data, i, 'TR'),2)
        stock_data.loc[i, '+DM14'] = round(calc_subsequent_14(stock_data, i, '+DM'), 2)
        stock_data.loc[i, '-DM14'] = round(calc_subsequent_14(stock_data, i, '-DM'), 2)
    
    if 'TR14' in stock_data.columns:
        stock_data.loc[i, '+DI'] = round((stock_data.loc[i, '+DM14'] / stock_data.loc[i, 'TR14'])*100, 2)
        stock_data.loc[i, '-DI'] = round((stock_data.loc[i, '-DM14'] / stock_data.loc[i, 'TR14'])*100, 2)

        stock_data.loc[i, 'DX'] = round((abs(stock_data.loc[i, '+DI'] - stock_data.loc[i, '-DI'])/abs(stock_data.loc[i, '+DI'] + stock_data.loc[i, '-DI']) )*100 , 2)

    if 'DX' in stock_data.columns:
        if stock_data.DX.count() == 14:
            stock_data.loc[i, 'ADX'] = calc_first_adx(stock_data, i)
        
        elif stock_data.DX.count() >= 14:
            stock_data.loc[i, 'ADX'] = calc_adx(stock_data, i)

print(stock_data.head(50))
print(stock_data.tail(5))
