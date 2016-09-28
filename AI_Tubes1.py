import random

class Ruangan:
	def __init__(self, nama, jamBuka, jamTutup, hari):
		self.nama = nama
		self.jamBuka = int(jamBuka[:2])
		self.jamTutup = int(jamTutup[:2])
		self.hari = hari #list hari apa aja Ruangan buka
		self.sel = [] #tabel projeksi antara jam dan hari (slot time), mempermudah menghitung konflik
		for i in range(0, 11):
			self.sel.append([0, 0, 0, 0, 0])
	def slotPlus(self, hari, jamMulai, jamSelesai): #tambahkan matkul ke slot time
		for i in range(jamMulai, jamSelesai):
			self.sel[i - 7][hari - 1] += 1; #dikurang 7 untuk jam, dikurang 1 untuk hari
	def slotMinus(self, hari, jamMulai, jamSelesai): #hapus matkul dari slot time
		for i in range(jamMulai, jamSelesai):
			self.sel[i - 7][hari - 1] -= 1; #dikurang 7 untuk jam, dikurang 1 untuk hari

class Matkul:
	def __init__(self, nama, jamMulai, jamSelesai, sks, hari):
		self.nama = nama
		self.jamMulai = int(jamMulai[:2])
		self.jamSelesai = int(jamSelesai[:2])
		self.sks = int(sks[:2])
		self.hari = hari #list hari apa aja Matkul tersedia
	def addListDomain(self, listDomain):
		self.listDomain = listDomain
		self.lengthList = len(self.listDomain) #banyaknya domain
	def setIdxDomain(self, idxDomain): #untuk initialize random
		self.idxDomain = idxDomain
		#update slot time
		domain = self.listDomain[self.idxDomain]
		domain.ptrRuangan.slotPlus(domain.hari, domain.jamMulai, domain.jamSelesai)
	def idxPlus(self): #ganti domain dengan menambah indexnya
		domain = self.listDomain[self.idxDomain]
		domain.ptrRuangan.slotMinus(domain.hari, domain.jamMulai, domain.jamSelesai)
		self.idxDomain += 1
		self.idxDomain %= self.lengthList #supaya tidak out of bond
		#update slot time
		domain.ptrRuangan.slotPlus(domain.hari, domain.jamMulai, domain.jamSelesai)
	def idxMinus(self): #ganti domain dengan mengurang indexnya
		domain = self.listDomain[self.idxDomain]
		domain.ptrRuangan.slotMinus(domain.hari, domain.jamMulai, domain.jamSelesai)
		self.idxDomain -= 1
		if self.idxDomain < 0:
			self.idxDomain = self.lengthList - 1 #supaya tidak out of bond
		#update slot time
		domain.ptrRuangan.slotPlus(domain.hari, domain.jamMulai, domain.jamSelesai)

class Domain:
	def __init__(self, ptrRuangan, hari, jamMulai, jamSelesai):
		self.ptrRuangan = ptrRuangan #Ruangan yang ditempati
		self.hari = int(hari)
		self.jamMulai = int(jamMulai)
		self.jamSelesai = int(jamSelesai)

def bacaTestcase(namaFile):
	#HARUSNYA read file
	testcase = []
	testcase.append("Ruangan")
	testcase.append("7602;07.00;14.00;1,2,3,4,5")
	testcase.append("7603;07.00;14.00;1,3,5")
	testcase.append("7610;09.00;12.00;1,2,3,4,5")
	testcase.append("Labdas2;10.00;14.00;2,4")
	testcase.append("")
	testcase.append("Jadwal")
	testcase.append("IF2110;7602;07.00;12.00;4;1,2,3,4,5")
	testcase.append("IF2130;-;10.00;16.00;3;3,4")
	testcase.append("IF2150;-;09.00;13.00;2;1,3,5")
	testcase.append("IF2170;7610;07.00;12.00;3;1,2,3,4,5")
	testcase.append("IF3110;7602;07.00;09.00;2;1,2,3,4,5")
	testcase.append("IF3130;-;07.00;12.00;2;3,4,5")
	testcase.append("IF3170;7602;07.00;09.00;2;1,2,3,4,5")
	testcase.append("IF3111;-;07.00;12.00;2;1,2,3,4,5")

	#parsing
	for line in testcase:
		if line == "Ruangan": #bagian Ruangan
			status = "r"
		elif line == "Jadwal": #bagian Jadwal
			status = "j"
		elif line == "": #pemisah antar bagian
			continue
		else:
			if status == "r":
				parsed = line.split(";")
				newObjekRuangan = Ruangan(parsed[0], parsed[1], parsed[2], parsed[3].split(","))
				listRuangan.append(newObjekRuangan) #daftarkan objek baru ke list
			elif status == "j":
				parsed = line.split(";")
				newObjekMatkul = Matkul(parsed[0], parsed[2], parsed[3], parsed[4], parsed[5].split(","))
				domain = makeListDomain(newObjekMatkul, parsed[1]) #cari domain mana saja yang memungkinkan
				newObjekMatkul.addListDomain(domain)
				listMatkul.append(newObjekMatkul) #daftarkan objek baru ke list

def makeListDomain(matkul, consRuangan):
	listHasil = []
	#telusuri semua Ruangan yang tersedia (cari Ruangan yang cocok)
	for ruang in listRuangan:
		if consRuangan != "-" and ruang.nama != consRuangan:
			continue #Matkul tidak bisa berada di Ruangan ini (constraint)
		else:
			#projeksi hari-hari yang tersedia antara Matkul dengan Ruangan (cari hari yang cocok)
			for hariRuangan in ruang.hari:
				for hariMatkul in matkul.hari:
					if hariRuangan != hariMatkul:
						continue #Matkul tidak bisa berada di Ruangan ini, di hari ini
					else:
						#cari jam yang cocok, mainkan batasan jam yang dibutuhkan Matkul dengan batasan jam yang tersedia di Ruangan pada hari ini
						jamMulai = matkul.jamMulai
						while jamMulai + matkul.sks <= ruang.jamTutup:
							if jamMulai >= ruang.jamBuka:
								#dapat 1 kandidat Matkul BISA ditempatkan di Ruangan ini, di hari ini, dan di jam segini
								newObjekDomain = Domain(ruang, hariRuangan, jamMulai, jamMulai + matkul.sks)
								listHasil.append(newObjekDomain)
							jamMulai += 1

	return listHasil

def initializeRandom():
	#HARUSNYA ada heuristik supaya bukan pure random
	for matkul in listMatkul:
		matkul.setIdxDomain(random.randint(0, matkul.lengthList - 1))

def countConflicts():
	hasil = 0
	#konflik berdasarkan per Ruangan
	for ruangan in listRuangan:
		#cek di setiap sel slot time nya
		for i in range(0, 11):
			for j in range(0, 5):
				#ada lebih dari 1 matkul (konflik)
				if ruangan.sel[i][j] > 1:
					for k in range(1, ruangan.sel[i][j]): #permutasi
						hasil += k
	return hasil

def hillClimbing():
	return "UNDER CONSTRUCTION"

def printStatus():
	#print buat testing doang, abaikan aja
	for matkul in listMatkul:
		print matkul.nama, "domain:"
		for idx in range(matkul.lengthList):
			if idx == matkul.idxDomain:
				print " ->", matkul.listDomain[idx].ptrRuangan.nama, matkul.listDomain[idx].hari, matkul.listDomain[idx].jamMulai, matkul.listDomain[idx].jamSelesai

#variabel
listRuangan = []
listMatkul = []

#program utama
bacaTestcase("Testcase.txt")
initializeRandom()
hillClimbing()
printStatus()
print "konflik: ", countConflicts()