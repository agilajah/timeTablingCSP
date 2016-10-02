# simulated annealing search algorithm
# var : s(h, j)
# domain : mk by code, r by name & mk
# constraints : (for all mk to all mk & all ruang)
"""
	1. mk1.jammulai != mk2.jammulai 
	2. mk1.jamselesai < mk2.jammulai
	3. mk1.jamselesai > mk2.jammulai && mk1.ruang != mk2.ruang
	4. ruangavailable(mk1.jammulai, mk1.jammulai+mk1.durasi) # sesuai ruang.jambuka dan ruang.jamtutup
	5. ruangavailable(mk1.hari) # sesuai ruang.haribuka
"""
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
		room : r[]
		course : mappedmk[]
	sel =>
		0 idx_jadwal
		1 idx_ruang
		2
"""

import random

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
					listOfParsed_jadwal.append(listOfParsedData)
		pass
	except Exception, e:
		raise e
	listOfParsed.append(listOfParsed_ruang)
	listOfParsed.append(listOfParsed_jadwal)
	return listOfParsed;

# mapping matkul data function
def mappingMatkul(matkul):
	mapping_matkul = []
	i = 0
	for x in matkul:
		himpunan = [] # contains idx, matkulcode, and 
		himpunan.append(i)
		if (matkul[i][1] == '-'): # matkul code
			temp = []
			temp.append(matkul[i][0])
			himpunan.append(temp) 
		else:
			himpunan.append(list(matkul[i][:2]))
		himpunan.append(int(matkul[i][2][:2])-7) # start hour
		himpunan.append(int(matkul[i][3][:2])-7) # finish hour
		himpunan.append(int(matkul[i][4])) # clock duration
		temp = matkul[i][5].split(',')
		himpunan.append(list(int(j) for j in temp)) # matkul available days
		mapping_matkul.append(himpunan) # append himpunan to mapping
		i += 1
	return mapping_matkul;

# mapping ruang data function
def mappingRuangan(ruang):
	mapping_ruang = []
	i = 0
	for x in ruang:
		himpunan = [] # contains idx, ruangcode, and 
		himpunan.append(i)
		himpunan.append(ruang[i][0]) # ruang code
		himpunan.append(int(ruang[i][1][:2])-7) # start hour
		himpunan.append(int(ruang[i][2][:2]) - int(ruang[i][1][:2])) # clock duration
		temp = ruang[i][3].split(',')
		himpunan.append(list(int(j) for j in temp)) # ruang available days
		mapping_ruang.append(himpunan) # append himpunan to mapping
		i += 1
	return mapping_ruang;

# fetch random matkul function
def getMatkul(mmatkul):
	result = random.randint(0,len(mmatkul)-1)
	if len(mmatkul[result]) > 6: # mmatkul already got before
		while True:
			result = random.randint(0,len(mmatkul)-1)
			if len(mmatkul[result]) <= 6:
				break
			else:
				continue
	mmatkul[result].append("ok") # status already taken for config (when eval, pop())
	return mmatkul[result];

# check constraint of matkul and ruang
def constraint_check_matkul(days, hour, mmatkul):
	if days+1 in mmatkul[5]:
		if mmatkul[2] <= hour or hour <= mmatkul[3]:
			return True;
	else:
		return False;

def constraint_check_ruang(days, hour, ruang):
	if days in ruang[-1]:
		if hour < ruang[-2] and hour > ruang[-3]:
			return True;
	else:
		return False;

def special(ruang, ruangan, mmatkul):
	if len(mmatkul[1]) > 1:
		for n in ruangan:
			if (mmatkul[1][1] in n):
				idx = ruangan.index(n)
		ruang = ruangan[idx]
	return ruang;

# init
def initialize(sel, ruangan, mmatkul):
	# sel <- ruangan + matkul
	# sel_pos <- randomized between 0 and 10 (hours) and 0 and 4 (days)
	# every assignment decrease count
	count = len(mmatkul)
	while count > 0:
		ruang = ruangan[random.randint(0,len(ruangan)-1)]
		mk = getMatkul(mmatkul)
		posx = random.randint(0,4) # days
		posy = random.randint(0,10) # hours/time
		looping = 0
		while not set(range(posy,posy+mk[4])).issubset(set(range(mk[2],mk[3]))):
			posy = random.randint(0,10) # hours/time
		ruang = special(ruang, ruangan, mk) # assign member of ruangan to ruang that in mk
		if (constraint_check_matkul(posx, posy, mk)):
			if (constraint_check_ruang(posx, posy, ruang)):
				temp = []
				temp.append(mk)
				temp.append(ruang)
				sel[posy][posx].append(temp)
			else:
				temp = []
				temp.append(mk)
				temp.append(ruang)
				sel[posy][posx].append(temp)
		else:
			temp = []
			temp.append(mk)
			temp.append(ruang)
			sel[posy][posx].append(temp)
		count -= 1

def init5(sel):
	i = 0
	for x in range(0,11):
		sel.append([])
		for y in range(0,5):
			sel[i].append([])
		i += 1

def conflictCounter(sel):
	# menghitung jumlah konflik dalam satu sel
	pass
	j = 0
	for x in sel:
		if x != []:
			j += sum(range(len(x)))
			return j;
		else:
			return 0;

def conflicts(sels):
	i = 0
	for x in s:
		print "x", i," = ", x
		print "conflictCounter = ", conflictCounter(x)
		i += 1

def nextConfig(sel, ruangan, mmatkul):
	pass

ruang = getFile('Testcase.txt')[0]
mk = getFile('Testcase.txt')[1]
mappedmk = mappingMatkul(mk)
r = mappingRuangan(ruang)
s = [] # sel-sel (hari, jam) -> hari = sb-x/second iterated, jam = sb-y/first iterated

# for x in mappedmk:
# 	print x
init5(s)
initialize(s, r, mappedmk)
conflicts(s)
# GLOBAL ALGORITHM IMPLEMENTATION
"""
init5(s)
initialize(s, r, mappedmk)

"""


# GLOBAL ALGORITHM
# initialize config
# Eval
# random move but not changing the config yet
# eval the random move
# case analyze between evals

