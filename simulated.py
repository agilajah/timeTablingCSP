# simulated annealing search algorithm
# var : s(h, j)
# domain : mk by code, r by name & mk
"""
	Time mapping :
		s[][0] -> s[][7]
		s[][1] -> s[][7+1]
		.
		.
		.
		s[][10] -> s[][7+10]

	Day mapping :
		s[0][] -> s[1][]
		s[1][] -> s[1+1][]
		.
		.
		s[4][] -> s[4+1][]

	Room and Course mapping :
		room : ruang[]
		course : mk[]
"""

import random
import array

# read file function	
def getFile(filename):
	try:
		f = open(filename, "r")
		listOfParsed_ruang = []
		listOfParsed_jadwal = []
		listOfParsed = []
		status = ''
		for aline in f:
			line = aline.split('\n')
			aline = line[0]
			if (aline == "Ruangan" or aline == "" or aline == "Jadwal"):
				if aline == "Ruangan":
					status = 'r'
				elif aline == "Jadwal":
					status = 'j'
				continue
			else:
				listOfParsedData = aline.split(';')
				if status == 'r':
					listOfParsed_ruang.append(listOfParsedData)
				elif status == 'j':
					listOfParsedData.append(0)
					listOfParsed_jadwal.append(listOfParsedData)
		pass
	except Exception, e:
		raise e
	listOfParsed.append(listOfParsed_ruang)
	listOfParsed.append(listOfParsed_jadwal)
	return listOfParsed;

def getMatkul(matkul):
	result = random.randint(0,len(matkul)-1)
	matkul[result][len(matkul[result])-1] = 1
	return matkul[result]

# check constraint
def constraint_check():
	

# init
def initialize(sel, ruangan, matkul):
	pass
	# sel <- ruangan + matkul
	# sel_pos <- randomized between 0 and 10 (hours) and 0 and 4 (days)
	# every assignment decrease count
	count = len(matkul)
	while count > 0:
		posx = random.randint(0,4) # days
		posy = random.randint(0,10) # hours/time
		mk = getMatkul(matkul)
		if (constraint_check()):
			pass

def eval(selx, sely, matkul):
	mapping_matkul = []
	i = 0
	for x in matkul:
		himpunan = [] # contains idx, matkulcode, and 
		himpunan.append(i)
		himpunan.append(matkul[0]) # matkul code
		himpunan.append(int(matkul[2])-7) # start hour
		himpunan.append(matkul[4]) # clock duration
		himpunan.append(matkul[5]) # matkul available days
		mapping_matkul.append(himpunan) # append himpunan to mapping

def parse(lists):
	if len(lists) == 4:
		mapping_ruang = []
		for x in lists:
			himpunan = []
			himpunan.append(lists[0]) # nama ruangan
			himpunan.append(int(lists[1][:2]) - 7) # nama 
	elif len(lists) == 6:
		pass


ruang = getFile('Testcase.txt')[0]
mk = getFile('Testcase.txt')[1]
#parseruang && mk
#print mk
s = []
# initialize config
# initialize(s, ruang, mk)
# Eval


# random move but not changing the config yet
# eval the random move
# case analyze between evals

# shj = [][]
# for i in range(0,9): # python random algorithm
# 	print randint(0,9)