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
		temp.append(x[0])
		temp.append(x[1][0])
		kembalian.append(temp)
	return kembalian;

def initConfig(matkul, ruangan, hasil):	# matkul == dataJadwal
																				# ruangan == dataRuang
																				# hasil == hasil initConfig
	i = 0
	for result in hasil:
		x = random.randint(matkul[i][2], matkul[i][3]-matkul[i][4])
		j = x
		result.append(x)
		result.append(x + matkul[i][4])
		result.append(matkul[i][4])
		x = random.randint(0,len(matkul[i][5])-1)
		result.append(matkul[i][5][x])
		hari = matkul[i][5][x]
		if (len(matkul[i][1]) > 1):
			for ruang in ruangan:
				if (matkul[i][1][1] in ruang):
					idx = ruang[0]
					break
			result.append(ruangan[idx][0])
			result.append(matkul[i][1][1])
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
				day = []
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
	for hari in range(1,6):
		days = []
		for h in hasil:
			if hari == h[5]:
				day = []
				days.append(h) # menambahkan 1 matkul ke 1 hari
				days.append(r)


def findConflict(hasil):	# hasil == config, complete assignment
													# return value : list of idx_jadwal
	pass
	confs[[], []] # idx == 0, jadwal bentrok | # idx == 1
	for hari in range(1,6):
		days = []
		for h in hasil:
			if hari == h[5]:
				day = []
				days.append(h) # menambahkan 1 matkul ke 1 slot hari
		
		# membandingkan kemungkinan semua
		for i in range(0,len(days)-1):
			for j in range(i,len(days)):
				if i == j:
					continue
				else:
					check = set(range(days[i][2],days[i][3])).intersection(set(range(days[j][2],days[j][3])))
					if check != set([]):
						pass
						# conf += len(list(check)) 
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

print "ruangan :"	
for x in dataRuang:
	print x

initConfig(dataJadwal, dataRuang, matkul)

for x in matkul:
	print x
print "conflict = ", conflict(matkul)

# print unusedDays(matkul)

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
				2 batas bawah jam alokasi
				3 batas atas jam alokasi
				4 batas hari alokasi

	hasilinit=>
				0 idx
				1 nama matakuliah
				2 jam alokasi awal matakuliah
				3 jam alokasi akhir matakuliah
				4 durasi alokasi jam matakuliah
				5 hari alokasi mata kuliah
				6 ruangan

"""

# GLOBAL ALGORITHM
# initialize config
# Eval
# random move but not changing the config yet
# eval the random move
# case analyze between evals