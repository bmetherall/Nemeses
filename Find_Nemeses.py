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

def find_result(data, event, wcaid):
	# Extract rankings for particular event
	event_ranks = data[np.where(data['eventid'] == event)]
	# Find your ranking
	your_rank = np.where(event_ranks['ID'] == wcaid)[0]
	if not your_rank:
		return -1
	else:
		# Return your result
		return event_ranks[your_rank[0]]['time']

# Import database
single = np.genfromtxt('WCA_export_RanksSingle.tsv', \
dtype=('|S10', '|S10', int, int, int), \
names = ['ID', 'eventid', 'time', 'wr', 'cr', 'nr'], \
unpack = True)[1:]
average = np.genfromtxt('WCA_export_RanksAverage.tsv', \
dtype=('|S10', '|S10', int, int, int, int), \
names = ['ID', 'eventid', 'time', 'wr', 'cr', 'nr'], \
unpack = True)[1:]

# List of events
events = ['333', '222', '444', '555', '666', '777', '333bf', \
'333fm', '333oh', '333ft', 'clock', 'minx', 'pyram', 'skewb', \
'sq1', '444bf', '555bf', '333mbf']

if len(sys.argv) > 1:
	ID = sys.argv[1]
else:
	ID = '2009METH01'

# Find nemeses
nem = set(find_rank(single, '333', ID))
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

# Array for all nemeses results
results = np.zeros((len(nem), 33), dtype = int)

# Loop over nemeses
for i in range(len(nem)):
	wcaid = nem[i]
	count = 0
	# Loop over events
	for j in events:
		results[i, count] = find_result(single, j, wcaid)
		count += 1
		if j != '444bf' and j != '555bf' and j != '333mbf':
			results[i, count] = find_result(average, j, wcaid)
			count += 1

# Create column headings
headings = ['WCAID']
for i in events:
	headings.append(i + '_s')
	if i != '444bf' and i != '555bf' and i != '333mbf':
		headings.append(i + '_a')
headings = np.array(headings)

# Write nemeses results to file
np.savetxt(ID + '.dat', np.vstack((headings, np.hstack((nem[:, None], results)))), fmt = '%s', delimiter = '\t')

print ID + ' has ' + str(len(nem) - 1) + ' nemeses. Their results have been written to ' + ID + '.dat'

