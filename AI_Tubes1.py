import random

class Ruangan:
    def __init__(self, nama, jamBuka, jamTutup, hari):
        self.nama = nama
        self.jamBuka = int(jamBuka[:2])
        self.jamTutup = int(jamTutup[:2])
        self.hari = hari #list hari apa aja Ruangan buka
        self.sel = [] #tabel projeksi antara jam dan hari (slot time), mempermudah menghitung konflik
        for i in range(0, 11):
            self.sel.append([[], [], [], [], []]) #tiap sel berisi list of Matkul
    def slotPlus(self, matkul, hari, jamMulai, jamSelesai): #tambahkan matkul ke slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].append(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari
    def slotMinus(self, matkul, hari, jamMulai, jamSelesai): #hapus matkul dari slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].remove(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari

class Matkul:
    def __init__(self, nama, jamBuka, jamTutup, sks, hari):
        self.nama = nama
        self.jamBuka = int(jamBuka[:2])
        self.jamTutup = int(jamTutup[:2])
        self.sks = int(sks[:2])
        self.hari = hari #list hari apa aja Matkul tersedia
    def addListDomain(self, listDomain): #yang boleh mengakses listDomain dan idxDomain hanya class Matkul
        self.__listDomain = listDomain
        self.nDomain = len(self.__listDomain) #banyaknya domain
    def setIdxDomain(self, idxDomain): #untuk initialize random
        self.__idxDomain = idxDomain
        self.__addToSlot()
    def idxPlus(self): #ganti domain dengan menambah indexnya
        self.__deleteFromSlot()
        self.__idxDomain += 1
        self.__idxDomain %= self.nDomain #supaya tidak out of bond
        self.__addToSlot()
    def idxMinus(self): #ganti domain dengan mengurang indexnya
        self.__deleteFromSlot()
        self.__idxDomain -= 1
        if self.__idxDomain < 0:
            self.__idxDomain = self.nDomain - 1 #supaya tidak out of bond
        self.__addToSlot()
    def __addToSlot(self): #yang boleh menambah dan menghapus dari slot time hanya class Matkul
        domain = self.__listDomain[self.__idxDomain]
        domain.ptrRuangan.slotPlus(self, domain.hari, domain.jamMulai, domain.jamSelesai)
    def __deleteFromSlot(self):
        domain = self.__listDomain[self.__idxDomain]
        domain.ptrRuangan.slotMinus(self, domain.hari, domain.jamMulai, domain.jamSelesai)
    def printConsole(self): #print data-data ke console
        domain = self.__listDomain[self.__idxDomain]
        print "\nMata kuliah ", self.nama
        print "Ruang       ", domain.ptrRuangan.nama
        idxHari = domain.hari
        if idxHari == 1:
            print "Hari         Senin"
        elif idxHari == 2:
            print "Hari         Selasa"
        elif idxHari == 3:
            print "Hari         Rabu"
        elif idxHari == 4:
            print "Hari         Kamis"
        else: #idxHari == 5
            print "Hari         Jumat"
        print "Pukul       ", domain.jamMulai, "-", domain.jamSelesai

class Domain:
    def __init__(self, ptrRuangan, hari, jamMulai, jamSelesai):
        self.ptrRuangan = ptrRuangan #Ruangan yang ditempati
        self.hari = int(hari)
        self.jamMulai = int(jamMulai)
        self.jamSelesai = int(jamSelesai)

def bacaTestcase(namaFile):
    fileTestcase = open(namaFile, "r")
    #parsing
    for stringBuffer in fileTestcase:
        line = stringBuffer.split("\n")[0]
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
                        jamMulai = matkul.jamBuka
                        jamSelesai = jamMulai + matkul.sks
                        while jamSelesai <= ruang.jamTutup:
                            if jamMulai >= ruang.jamBuka:
                                #dapat 1 kandidat Matkul BISA ditempatkan di Ruangan ini, di hari ini, dan di jam segini
                                newObjekDomain = Domain(ruang, hariRuangan, jamMulai, jamSelesai)
                                listHasil.append(newObjekDomain)
                            jamMulai += 1
                            jamSelesai += 1

    return listHasil

def initializeRandom():
    #HARUSNYA HEURISTIK
    for matkul in listMatkul:
        matkul.setIdxDomain(random.randint(0, matkul.nDomain - 1)) #ini baru pure random

def countConflicts():
    hasil = 0
    #konflik berdasarkan per Ruangan
    for ruangan in listRuangan:
        #cek di setiap sel slot time nya
        for i in range(0, 11):
            for j in range(0, 5):
                #ada lebih dari 1 matkul (konflik)
                nMatkul = len(ruangan.sel[i][j])
                if nMatkul > 1:
                    for k in range(1, nMatkul):
                        listKonflik.append(ruangan.sel[i][j][k - 1]) #siapa saja yang konflik pada sel itu
                        hasil += k #konflik pada sel itu = permutasi
                    listKonflik.append(ruangan.sel[i][j][nMatkul - 1]) #siapa saja yang konflik pada sel itu
    return hasil

def hillClimbing():
    step = 0
    nKonflikNow = countConflicts()
    #mulai hill climbing
    while step < 10 and nKonflikNow > 0:
        #HARUSNYA HEURISTIK
        listKonflik[0].idxPlus() #ini baru geser elemen pertama aja, gak peduli setelah geser konfliknya nambah atau ngurang
        #persiapan untuk iterasi selanjutnya
        step += 1
        del listKonflik[:]
        nKonflikNow = countConflicts()
    #sudah iterasi sebanyak step, atau sudah menemukan solusi
    if nKonflikNow == 0:
        print "SOLUSI DITEMUKAN DALAM", step, "ITERASI"
    else:
        print nKonflikNow, "KONFLIK DALAM", step, "ITERASI:"
        for matkul in listKonflik:
            print " ", matkul.nama

def printMatkul():
    for matkul in listMatkul:
        matkul.printConsole()

#variabel
listRuangan = []
listMatkul = []
listKonflik = []

#program utama
bacaTestcase("Testcase.txt")
initializeRandom()
hillClimbing()
printMatkul()