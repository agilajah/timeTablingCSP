import random

class Ruangan:
    def __init__(self, nama, jamBuka, jamTutup, hari):
        self.nama = nama
        self.jamBuka = int(jamBuka[:2])
        self.jamTutup = int(jamTutup[:2])
        self.hari = hari #list hari apa aja Ruangan buka
        self.sel = [] #tabel projeksi antara jam dan hari (slot time), mempermudah menghitung konflik
        for i in range(11):
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

    def getDomain(self):
        return self.__listDomain[self.__idxDomain]

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
        domain = self.getDomain()
        domain.ptrRuangan.slotPlus(self, domain.hari, domain.jamMulai, domain.jamSelesai)

    def __deleteFromSlot(self):
        domain = self.getDomain()
        domain.ptrRuangan.slotMinus(self, domain.hari, domain.jamMulai, domain.jamSelesai)

    def printConsole(self): #print data-data ke console
        domain = self.getDomain()
        idxHari = domain.hari
        if idxHari == 1:
            stringHari = "Senin"
        elif idxHari == 2:
            stringHari = "Selasa"
        elif idxHari == 3:
            stringHari = "Rabu"
        elif idxHari == 4:
            stringHari = "Kamis"
        else: #idxHari == 5
            stringHari = "Jumat"
        print self.nama, "\t\t", domain.ptrRuangan.nama, "\t\t", stringHari, "\t\t", domain.jamMulai, "-", domain.jamSelesai

class Domain:
    def __init__(self, ptrRuangan, hari, jamMulai, jamSelesai):
        self.ptrRuangan = ptrRuangan #Ruangan yang ditempati
        self.hari = int(hari)
        self.jamMulai = int(jamMulai)
        self.jamSelesai = int(jamSelesai)

def bacaTestcase(namaFile):
    #no try catch
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
        elif status == "r":
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
    hasil = []
    #telusuri semua Ruangan yang tersedia (cari Ruangan yang cocok)
    for ruang in listRuangan:
        if consRuangan == "-" or ruang.nama == consRuangan:
            #projeksi hari-hari yang tersedia antara Matkul dengan Ruangan (cari hari yang cocok)
            for hariRuangan in ruang.hari:
                for hariMatkul in matkul.hari:
                    if hariRuangan == hariMatkul:
                        #cari jam yang cocok, mainkan batasan jam yang dibutuhkan Matkul dengan batasan jam yang tersedia di Ruangan pada hari ini
                        jamMulai = matkul.jamBuka
                        jamSelesai = jamMulai + matkul.sks
                        while jamSelesai <= ruang.jamTutup:
                            if jamMulai >= ruang.jamBuka:
                                #dapat 1 kandidat Matkul BISA ditempatkan di Ruangan ini, di hari ini, dan di jam segini
                                newObjekDomain = Domain(ruang, hariRuangan, jamMulai, jamSelesai)
                                hasil.append(newObjekDomain)
                            jamMulai += 1
                            jamSelesai += 1
    return hasil

def initializeRandom():
    #masih pure random
    for matkul in listMatkul:
        matkul.setIdxDomain(random.randint(0, matkul.nDomain - 1))

def countConflicts():
    del listKonflik[:] #list yang di program utama di hapus dulu karena mau di generate ulang
    hasil = 0 #banyaknya konflik
    listKonflikLokal = [] #list konflik lokal (beda dari yang di program utama)
    #cari konflik per Ruangan
    for ruangan in listRuangan:
        #cek di setiap slot time nya
        for i in range(11):
            for j in range(5):
                a_sel = ruangan.sel[i][j]
                nMatkul = len(a_sel)
                #ada lebih dari 1 matkul di sel itu (konflik)
                if nMatkul > 1:
                    for k in range(nMatkul):
                        listKonflikLokal.append(a_sel[k]) #siapa saja yang konflik pada sel itu
                        hasil += k #permutasi, 0 + 1 + 2 + ... + (nMatkul - 1)
    #remove duplicate dari list konflik lokal untuk ditaruh di list program utama
    for x in listKonflikLokal:
        if not(x in listKonflik):
            listKonflik.append(x)
    #sort agar yang di geser duluan adalah yang punya domain banyak
    listKonflik.sort(key=lambda matkul: matkul.nDomain, reverse=True)
    return hasil

def hillClimbing():
    lokalMaks = False #kalo terjebak di lokal maks, bernilai true
    step = 0 #sudah berapa kali iterasi
    listKonflikNow = [] #list konflik lokal (beda dari yang di program utama)
    nKonflikNow = countConflicts()
    #mulai hill climbing, iterasi dibatasi  sebanyak step
    while nKonflikNow > 0:
        #copy list supaya gak ribet pointer-pointer nya berubah
        del listKonflikNow[:]
        for matkul in listKonflik:
            listKonflikNow.append(matkul)
        #mulai heuristik
        foundBetter = False
        for matkul in listKonflikNow:
            #majuin terus sebanyak nDomain kali (1 cycle)
            for i in range(matkul.nDomain):
                step += 1
                matkul.idxPlus() #saat dimajuin, listKonflik berubah namun listKonflikNow tetap
                nKonflikNew = countConflicts()
                if nKonflikNew < nKonflikNow: #bandingkan konflik
                    foundBetter = True
                    break #break for i
            nKonflikNow = nKonflikNew #berhasil atau tidak menemukan yang lebih baik, tetap ambil nilainya
            if foundBetter == True:
                break #break for matkul
            elif matkul == listKonflikNow[len(listKonflikNow) - 1]:
                lokalMaks = True #matkul terakhir, tetep gak nemu lebih baik
        if lokalMaks == True: #gak bisa ngapa2in lagi udah mentok
            print "LOKAL MAKSIMUM"
            break #break while
    #sudah iterasi sebanyak step, atau sudah menemukan solusi
    if nKonflikNow == 0:
        print "SOLUSI DITEMUKAN DALAM", step, "ITERASI"
    else:
        print nKonflikNow, "KONFLIK DALAM", step, "ITERASI:"
        for matkul in listKonflik:
            print " ", matkul.nama

#variabel program utama
listRuangan = []
listMatkul = []
listKonflik = []

#program utama
#"""
bacaTestcase("Testcase.txt")
initializeRandom()
hillClimbing()
print "Mata Kuliah\tRuang\t\tHari\t\tPukul"
for matkul in listMatkul:
    matkul.printConsole()
#"""