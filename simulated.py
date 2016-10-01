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

def getNamaRuang(dataRuang):
	ruang = []
	for ruangan in dataRuang:
		ruang.append(ruangan[1])
	return ruang;

def initHasil(hasilMapping):
	# menginisialisasi list nama mata kuliah dan nomornya untuk melakukan penjadwalan
	kembalian = []
	for x in hasilMapping:
		temp = []
		temp.append(x[0])
		temp.append(x[1][0])
		kembalian.append(temp)
	return kembalian;

def initConfig(matkul, ruangan, hasil):
	i = 0
	for result in hasil:
		result.append(random.randint(matkul[i][2], matkul[i][3]-matkul[i][4]))
		result.append(matkul[i][3])
		result.append(matkul[i][4])
		x = random.randint(0,len(matkul[i][5])-1)
		result.append(matkul[i][5][x])
		if (len(matkul[i][1]) > 1):
			result.append(matkul[i][1][1])
		else:
			y = random.randint(0,len(ruangan)-1)
			result.append(ruangan[y][1])
		i += 1

def getCurrentSuhu(suhu):
	return suhu-10;

def countConflict(hasil):
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

initConfig(dataJadwal, dataRuang, matkul)


for r in matkul:
	print r

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