import pandas as pd
from itertools import islice  # iteration
import datetime
# import os - for the automatic opening ng file

peak = pd.read_csv('Routes Matrix.csv', error_bad_lines=False, encoding='latin-1')

columns = ['ID', 'startdesti', 'Start Grid ID', 'enddestina', 'End Grid ID', 'duration', 'Grid Route', 'Min Duration', 'Max Duration', 'Sum of Durations', 'Count', 'Average Duration']

new_peak = pd.DataFrame(columns=columns)

n = 0

tlist = []
mlist = []

for index, row in islice(peak.iterrows(), 0, len(peak) - 1):

        if str(row['Grid Route']) == str(peak.iloc[index + 1]['Grid Route']):

            tlist.append(int(row['duration']))

        else:

            if len(tlist) == 0:

                new_peak.loc[n] = pd.Series({'ID': str(peak.iloc[index]['ID']), 'startdesti': str(peak.iloc[index]['startdesti']), 'Start Grid ID': str(peak.iloc[index]['Start Grid ID']), 'enddestina': str(peak.iloc[index]['enddestina']), 'End Grid ID': str(peak.iloc[index]['End Grid ID']), 'duration': str(peak.iloc[index]['duration']), 'Grid Route': str(peak.iloc[index]['Grid Route']), 'Min Duration': str(peak.iloc[index]['duration']), 'Max Duration': str(peak.iloc[index]['duration']), 'Sum of Durations': str(peak.iloc[index]['duration']), 'Count': "1",
                                             'Average Duration': str(peak.iloc[index]['duration'])})

                n += 1

            else:

                mlist.append(int(peak.iloc[index]['duration']))

                new_peak.loc[n] = pd.Series({'ID': str(peak.iloc[index]['ID']), 'startdesti': str(peak.iloc[index]['startdesti']), 'Start Grid ID': str(peak.iloc[index]['Start Grid ID']), 'enddestina': str(peak.iloc[index]['enddestina']), 'End Grid ID': str(peak.iloc[index]['End Grid ID']), 'duration': str(peak.iloc[index]['duration']), 'Grid Route': str(peak.iloc[index]['Grid Route']), 'Sum of Durations': str(sum(tlist) + int(peak.iloc[index]['duration'])), 'Count': str(len(tlist) + 1),
                                             'Min Duration': min(tlist + mlist),
                                             'Max Duration': max(tlist + mlist),
                                             'Average Duration': (sum(tlist) + int(peak.iloc[index]['duration'])) / (len(tlist) + 1)})

                del tlist[:]
                del mlist[:]

                n += 1


new_peak.to_csv('Routes Matrix with Average Duration.csv', index=False)
