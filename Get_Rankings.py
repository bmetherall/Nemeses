import numpy as np
import sys

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

if len(sys.argv) > 1:
	ID = sys.argv[1]
else:
	ID = '2009METH01'

nem = np.loadtxt(ID + '_Nemeses.dat', dtype = 'S10')

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

results = np.zeros((len(nem), 33), dtype = int)

for i in range(len(nem)):
	wcaid = nem[i]
	count = 0
	for j in events:
		results[i, count] = find_result(single, j, wcaid)
		count += 1
		if j != '444bf' and j != '555bf' and j != '333mbf':
			results[i, count] = find_result(average, j, wcaid)
			count += 1

headings = ['WCAID']

for i in events:
	headings.append(i + '_single')
	if i != '444bf' and i != '555bf' and i != '333mbf':
		headings.append(i + '_average')

headings = np.array(headings)

np.savetxt('data.dat', np.vstack((headings, np.hstack((nem[:, None], results)))), fmt = '%s')





















