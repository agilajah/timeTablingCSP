<<<<<<< HEAD
import random

# read file function	
def getFile(filename):
	"""
		IS : file sudah terisi dan sesuai format Testcase
		FS : Kembalian merupakan list berisi hasil parse list ruangan dan list jadwal
	"""
	try: # buka file di dalam try-except
		f = open(filename, "r")
		listOfParsed_ruang = []
		listOfParsed_jadwal = []
		listOfParsed = [] # akan diisi listOfParsed_jadwal dan listOfParsed_ruang
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
	# hasil parse file (matkul) di mapping ke representasi yang dapat diakses python
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
	# hasil parse file (ruang) di mapping ke representasi yang dapat diakses python
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

def getNamaRuang(dataRuang): # dataRuang == 
	ruang = []
	for ruangan in dataRuang:
		ruang.append(ruangan[1])
	return ruang;

def initHasil(hasilMapping): # hasilMapping == dataJadwal
	# menginisialisasi list nama mata kuliah dan nomornya untuk melakukan penjadwalan
	kembalian = []
	for x in hasilMapping:
		temp = []
		temp.append(x[0]) # nomor matkul
		temp.append(x[1][0]) # nama matkul
		kembalian.append(temp)
	return kembalian;

def initConfig(matkul, ruangan, hasil):	# matkul == dataJadwal
																				# ruangan == dataRuang
																				# hasil == hasil initConfig
	i = 0
	for result in hasil:
		x = random.randint(matkul[i][2], matkul[i][3]-matkul[i][4])
		j = x
		result.append(x) # 2 awal alokasi matkul
		result.append(x + matkul[i][4]) # 3 akhir alokasi matkul
		result.append(matkul[i][4]) # 4 durasi matkul
		x = random.randint(0,len(matkul[i][5])-1)
		result.append(matkul[i][5][x]) # 5 hari alokasi matkul
		hari = matkul[i][5][x]
		if (len(matkul[i][1]) > 1):
			for ruang in ruangan:
				if (matkul[i][1][1] in ruang):
					idx = ruang[0]
					break
			result.append(ruangan[idx][0]) # 6 idx ruangan
			result.append(matkul[i][1][1]) # 7 nama ruangan
			result.append(ruangan[idx][3]) # 8 jam buka ruangan
			result.append(ruangan[idx][4]) # 9 jam tutup ruangan
		else:
			y = random.randint(0,len(ruangan)-1)
			temp = 0
			while not set(range(j,j+matkul[i][4])).issubset(set(range(ruangan[y][2],ruangan[y][3]))) or not hari in ruangan[y][-1]:
				print "te"
				# cek hari
				if (hari == 5):
					hari = 1
				else:
					hari += 1
				# cek ruangan
				if y != len(ruangan)-1 and temp <= len(ruangan):
					y += 1
					temp += 1
				elif temp > len(ruangan):
					break
				else:
					y = 0
			result.pop()
			result.append(hari)
			result.append(ruangan[y][0])
			result.append(ruangan[y][1])
			result.append(ruangan[y][3])
			result.append(ruangan[y][4])
		i += 1


def unusedRuangan(matkulWithRuangan, listRuangan): 	# matkulWithRuangan == hasilinit
																										# listRuangan == dataRuang
	daftarRuang = []
	for ruangan in listRuangan:
		daftarRuang.append(ruangan[0])
	for jadwal in matkulWithRuangan:
		if jadwal[6] in daftarRuang:
			daftarRuang.remove(jadwal[6])
		elif daftarRuang == []:
			break
		else:
			continue
	return daftarRuang

def unusedDays(matkulWithDays): # matkulWithDays == hasilinit
	listDays = range(1,6)
	for jadwal in matkulWithDays:
		if jadwal[5] in listDays:
			listDays.remove(jadwal[5])
		elif listDays == []:
			break
		else:
			continue
	return listDays

def conflict(hasil): # hasil == config, complete assignment
	conf = 0
	for hari in range(1,6):
		days = []
		for h in hasil:
			if hari == h[5]:
				days.append(h) # menambahkan 1 matkul ke 1 slot hari
		
		# membandingkan kemungkinan semua
		for i in range(0,len(days)-1):
			for j in range(i,len(days)):
				if i == j:
					continue
				else:
					check = set(range(days[i][2],days[i][3])).intersection(set(range(days[j][2],days[j][3])))
					if check != set([]):
						conf += len(list(check))
					else:
						continue
	return conf;

def countConflict(hasil, ruang):	# hasil == config, complete assignment
																	# ruang == dataRuang
	pass


def findConflict(hasil, ruang):	# hasil == config, complete assignment
													# return value : list of idx_jadwal
	pass
	confs = [[], []] # idx == 0, jadwal bentrok | # idx == 1
	for hari in range(1,6):
		days = []
		for h in hasil: # menambahkan matkul yang diassign di hari tersebut
			if hari == h[5]:
				days.append(h)

		# room = []
		# for r in ruang:
		# 	if hari == r[5]:
		# 		pass
		
		# membandingkan kemungkinan semua konflik di satu hari
		for i in range(0,len(days)-1):
			for j in range(i,len(days)):
				if i == j:
					continue
				else:
					check = set(range(days[i][2],days[i][3])).intersection(set(range(days[j][2],days[j][3])))
					if check != set([]):
						pass
						temp = []
						temp.append(days[i]) # menambahkan matakuliah yang konflik di append bersama jam awal dan jam akhir konflik
						temp.append(days[j])
						confs[0].append(temp)
						if days[i][6] == days[j][6]: # menambahkan konflik ruangan yang digunakan
							temp = []
							temp.append(days[i][6])
							temp.append(days[i][7])
							temp.append(days[i][8])
							temp.append(days[i][9])
							confs[1].append(temp)
						else:
							confs[1].append([])
					else:
						continue
	return confs;
	
def getCurrentSuhu(suhu): # suhu == current suhu before
	return suhu-10;

def nextConfig(hasil, listOfConflicts):	# hasil == current config
																				# listOfConflicts == conflict position
	pass


#MAIN PROGRAM
fetch = getFile('Testcase.txt')
ruang = fetch[0]
matkul = fetch[1]
suhu = 100010

dataJadwal = mappingMatkul(matkul)
dataRuang = mappingRuangan(ruang)
namaRuang = getNamaRuang(dataRuang)

matkul = initHasil(dataJadwal)

print "jadwal :"	
for x in dataJadwal:
	print x

initConfig(dataJadwal, dataRuang, matkul)

listConflict = findConflict(matkul, dataRuang):


for x in matkul:
	print x
print conflict(matkul)



# for r in j:
# 	if r != 'dummy':
# 		print r
# for r in matkul:
# 	print r

# initialize config

"""
	Algoritma detil
		initConfig(mapmk, mapruang, hasil)
		while countConflict(hasil) > 0:
			getCurrentSuhu(suhu)
			[]fail_idx = findConflict(hasil)
			replaceConflict(hasil, fail_idx, alternative)
			if countConflict(alternative) < countConflict(hasil):
				hasil = alternative
			else:
				prob = getProbability(suhu)
				if highTemp(prob):
					if (random(0,1) == 1): # Randomnya berdasarkan suatu heuristik
						hasil = alternative
					else:
						continue
				else:
					break
		print hasil
"""

"""
	Mapping :

	dataJadwal=>
				0 idx
				1 nama
				2 batas bawah jam alokasi
				3 batas atas jam alokasi
				4 durasi
				5 batas hari alokasi

	dataRuang=>
				0 idx
				1 nama
				2 jam buka ruangan
				3 jam tutup ruangan
				4 hari buka ruangan

	hasilinit=>
				0 idx matakuliah
				1 nama matakuliah
				2 jam alokasi awal matakuliah
				3 jam alokasi akhir matakuliah
				4 durasi alokasi jam matakuliah
				5 hari alokasi mata kuliah
				6 idx ruangan
				7 ruangan
				8 jam buka ruangan
				9 jam tutup ruangan

"""

# GLOBAL ALGORITHM
# initialize config
# Eval
# random move but not changing the config yet
# eval the random move
=======
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
				i = posy
				for x in range(i, i+mk[4]):
					sel[i][posx].append(temp)
			else:
				temp = []
				temp.append(mk)
				temp.append(ruang)
				i = posy
				for x in range(i, i+mk[4]):
					sel[i][posx].append(temp)
		else:
			temp = []
			temp.append(mk)
			temp.append(ruang)
			i = posy
			for x in range(i, i+mk[4]):
				sel[i][posx].append(temp)
		count -= 1

def init5(sel):
	i = 0
	for x in range(0,11):
		sel.append([])
		for y in range(0,5):
			sel[i].append([])
		i += 1

def conflictCounter(sel): # sel adalah list dengan isi list matakuliah&ruangan yang digunakan pada suatu jam dan hari tertentu
	# menghitung jumlah konflik dalam satu sel
	pass
	j = 0
	for x in sel:
		if x != []:
			j += sum(range(len(x)))
			return j;
		else:
			return 0;

def popping(sel):
	pass
	for x in sel:
		for y in x:
			if y != []:
				y[0][0].pop()

def eval(sel): # sel yang merupakan current config
	pass
	jumlahConflict = 0
	for x in sel:
		for y in x:
			if y != []:
				jumlahConflict += conflictCounter(y)
	return jumlahConflict;

def nextConfig(sel, ruangan, mmatkul):
	pass

ruang = getFile('Testcase.txt')[0]
mk = getFile('Testcase.txt')[1]
mappedmk = mappingMatkul(mk)
mapped2 = mappingMatkul(mk)
r = mappingRuangan(ruang)
s = [] # sel-sel (hari, jam) -> hari = sb-x/second iterated, jam = sb-y/first iterated



init5(s)
initialize(s, r, mappedmk)

# for x in range(0,5):
# 	for y in range(0,11):
# 		if x == 4 and y == 2:
# 			print s[y][x]
# 			print "\n"


curreval = eval(s)
popping(s)
potential = []
i = 0
while True:
	temp = mapped2
	print i
	init5(potential)
	initialize(potential, r, temp)
	poteval = eval(potential)
	popping(potential)
	
	if (curreval > poteval):
		s = potential
		potential = []
	elif (curreval == 0):
		break
	else:
		potential = []
		# RANDOM WALK
	i += 1

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
>>>>>>> 57a7ac5650d0067c3198af6d9cfd7f8fc2689330
# case analyze between evals