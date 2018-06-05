import numpy as np
import sys

def find_rank(data, event, wcaid):
	# Extract rankings for particular event
	event_ranks = data[np.where(data['eventid'] == event)]
	# Find your ranking
	your_rank = np.where(event_ranks['ID'] == wcaid)[0]
	if not your_rank:
		return np.zeros(0)
	else:
		# Else return the WCAIDs of everyone faster
		return event_ranks[:your_rank[0]+1]['ID']

if len(sys.argv) > 1:
	ID = sys.argv[1]
else:
	ID = '2009METH01'

# Import database
single = np.genfromtxt('WCA_export_RanksSingle.tsv', \
dtype=('|S10', '|S10', int, int, int), \
names = ['ID', 'eventid', 'time', 'wr', 'cr', 'nr'], \
unpack = True)[1:]
average = np.genfromtxt('WCA_export_RanksAverage.tsv', \
dtype=('|S10', '|S10', int, int, int, int), \
names = ['ID', 'eventid', 'time', 'wr', 'cr', 'nr'], \
unpack = True)[1:]

events = ['333', '222', '444', '555', '666', '777', '333bf', \
'333fm', '333oh', '333ft', 'clock', 'minx', 'pyram', 'skewb', \
'sq1', '444bf', '555bf', '333mbf']

nem = set(find_rank(single, '333', ID))

# Find nemeses
for i in events:
	rank_single = find_rank(single, i, ID)
	if rank_single.size:
		nem = nem & set(rank_single)
		if i != '444bf' and i != '555bf' and i != '333mbf':
			rank_average = find_rank(average, i, ID)
			if rank_average.size:
				nem = nem & set(rank_average)

nem = np.array(list(nem))
nem.sort()

np.savetxt(ID + '_Nemeses.dat', nem, fmt = '%s')

print ID + ' has ' + str(len(nem) - 1) + ' nemeses.\nThey have been written to the file ' + ID + '_Nemeses.dat.'






















