import pandas as pd
import numpy as np
from itertools import islice
import datetime

speeding = pd.read_csv('speeding_dec14-21.csv', error_bad_lines=False, encoding='latin-1')

cols = ['ID', 'Vehicle', 'Group', 'Average Speed', 'Minimum Speed', 'Min Location', 'Maximum Speed', 'Max Location', 'Date', 'Estimated Start Time', 'Estimated End Time', 'Estimated Duration']

speeding_out = pd.DataFrame(columns=cols)

n = 0

tlist = []
llist = []

tlist.append(speeding.iloc[0]['Speed'])
llist.append(speeding.iloc[0]['Location'])

for index, row in islice(speeding.iterrows(), 1, None):

    if row['Rover'] == speeding.iloc[index-1]['Rover'] and int(pd.to_timedelta(pd.to_datetime(row['Stamp']) - pd.to_datetime(speeding.iloc[index - 1]['Stamp'])) / pd.Timedelta('1 minute')) < 1:

        tlist.append(row['Speed'])
        llist.append(row['Location'])

    else:

        speeding_out.loc[n] = pd.Series({'ID': n, 'Vehicle': speeding.iloc[index - 1]['Rover'], 'Group': speeding.iloc[index - 1]['name'], 'Average Speed': np.mean(tlist),
                                        'Minimum Speed': min(tlist), 'Min Location': llist[tlist.index(min(tlist))], 'Maximum Speed': max(tlist), 'Max Location': llist[tlist.index(min(tlist))], 'Date': pd.to_datetime(speeding.iloc[index - 1]['Stamp']).date(), 'Estimated Start Time': pd.to_datetime(pd.to_datetime(speeding.iloc[index - len(tlist)]['Stamp']) - datetime.timedelta(seconds=10)).time(), 'Estimated End Time': pd.to_datetime(speeding.iloc[index - 1]['Stamp']).time(),
                                        'Estimated Duration': int(pd.to_timedelta(pd.to_datetime(speeding.iloc[index - 1]['Stamp']) - (pd.to_datetime(speeding.iloc[index - len(tlist)]['Stamp']) - datetime.timedelta(seconds=10))) / pd.to_timedelta('1 second'))})
        n += 1

        del tlist[:]
        del llist[:]

        tlist.append(row['Speed'])
        llist.append(row['Location'])

speeding_out.loc[n] = pd.Series({'ID': n, 'Vehicle': speeding.iloc[index - 1]['Rover'], 'Group': speeding.iloc[index - 1]['name'], 'Average Speed': np.mean(tlist), 'Minimum Speed': min(tlist), 'Min Location': llist[tlist.index(min(tlist))], 'Maximum Speed': max(tlist), 'Max Location': llist[tlist.index(min(tlist))], 'Date': pd.to_datetime(speeding.iloc[index - 1]['Stamp']).date(), 'Estimated Start Time': pd.to_datetime(pd.to_datetime(speeding.iloc[index - (len(tlist) - 1)]['Stamp']) - datetime.timedelta(seconds=10)).time(),
                                 'Estimated End Time': pd.to_datetime(speeding.iloc[index]['Stamp']).time(),
                                 'Estimated Duration': int(pd.to_timedelta(pd.to_datetime(speeding.iloc[index]['Stamp']) - (pd.to_datetime(speeding.iloc[index - (len(tlist) - 1)]['Stamp']) - datetime.timedelta(seconds=10))) / pd.to_timedelta('1 second'))})

speeding_out.to_csv('speeding_dec14-21_out.csv', index=False)
