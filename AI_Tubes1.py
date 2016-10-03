from __future__ import division
import random

"""
variable : jadwal matkul
domain : <ruang, jam, hari>
constraint :
1. ruangan yang sesuai (jika ada syarat ruangan tertentu di jadwal matkul)
2. waktu (jam dan hari) yang sesuai dengan syarat jadwal matkul
3. alldiff (tidak konflik di ruang, jam, dan hari yang sama)
"""

class Ruangan:
    def __init__(self, nama, jamBuka, jamTutup, hari):
        self.nama = nama
        self.jamBuka = int(jamBuka[:2])
        self.jamTutup = int(jamTutup[:2])
        self.hari = hari #list hari apa aja Ruangan buka
        self.sel = [] #tabel projeksi antara jam dan hari (slot time)
        for i in range(11):
            self.sel.append([[], [], [], [], []]) #tiap sel berisi list of Matkul
        self.selAvailable = (self.jamTutup - self.jamBuka) * len(self.hari) #untuk persen keefektifan

    def slotPlus(self, matkul, hari, jamMulai, jamSelesai): #tambahkan matkul ke slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].append(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari

    def slotMinus(self, matkul, hari, jamMulai, jamSelesai): #hapus matkul dari slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].remove(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari

    def deleteAllSel(self): #semua sel di kosongin lagi
        for jam in self.sel:
            for hari in jam:
                del hari[:]

    def countFilledSel(self): #untuk hitung persen keefektifan
        hasil = 0
        for i in range(11): #cek tiap sel
            if i + 7 >= self.jamBuka and i + 7 <= self.jamTutup:
                for j in self.hari:
                    if len(self.sel[i][int(j) - 1]) > 0: #ada isinya
                        hasil += 1
        return hasil

    def countFitness(self): #untuk GA
        hasil = 0
        for i in range(11): #cek tiap sel
            if i + 7 >= self.jamBuka and i + 7 <= self.jamTutup:
                for j in self.hari:
                    if len(self.sel[i][int(j) - 1]) == 1: #tidak konflik
                        hasil += 1
        return hasil

class Matkul:
    def __init__(self, nama, jamBuka, jamTutup, sks, hari):
        self.nama = nama
        self.jamBuka = int(jamBuka[:2]) #BUKAN jamMulai
        self.jamTutup = int(jamTutup[:2])
        self.sks = int(sks[:2])
        self.hari = hari #list hari apa aja Matkul tersedia

    def addListDomain(self, listDomain):
        self.listDomain = listDomain
        self.nDomain = len(self.listDomain) #banyaknya domain

    def setIdxDomain(self, idxDomain): #pilih satu domain dari listDomain berdasarkan indexnya
        self.idxDomain = idxDomain
        self.addToSlot()

    def getDomain(self):
        return self.listDomain[self.idxDomain]

    def idxPlus(self): #ganti domain dengan menambah 1 index di listDomain nya
        self.deleteFromSlot()
        self.idxDomain += 1
        self.idxDomain %= self.nDomain #supaya tidak out of bond
        self.addToSlot()

    def addToSlot(self):
        domain = self.getDomain()
        domain.ptrRuangan.slotPlus(self, domain.hari, domain.jamMulai, domain.jamSelesai)

    def deleteFromSlot(self):
        domain = self.getDomain()
        domain.ptrRuangan.slotMinus(self, domain.hari, domain.jamMulai, domain.jamSelesai)

    def printConsole(self): #print data-data ke console, gaperlu dimengerti ini hiasan doang
        domain = self.getDomain()
        idxHari = domain.hari
        if idxHari == 1:
            stringHari = "Senin"
        elif idxHari == 2:
            stringHari = "Selasa"
        elif idxHari == 3:
            stringHari = "Rabu "
        elif idxHari == 4:
            stringHari = "Kamis"
        else: #idxHari == 5
            stringHari = "Jumat"
        if len(domain.ptrRuangan.nama) <= 4:
            print "|", self.nama, "\t|", domain.ptrRuangan.nama, "\t\t|", stringHari, "\t\t|", domain.jamMulai, "-", domain.jamSelesai, "\t|"
        else:
            print "|", self.nama, "\t|", domain.ptrRuangan.nama, "\t|", stringHari, "\t\t|", domain.jamMulai, "-", domain.jamSelesai, "\t|"

class Domain:
    #hanya butuh pointer ke Ruangan, karena objek dia sendiri sudah dipegang oleh class Matkul di dalam listDomain
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
        line = stringBuffer.split("\n")[0] #menghilangkan ENTER di karakter terakhir
        if line == "Ruangan": #bagian Ruangan
            status = "r"
        elif line == "Jadwal": #bagian Jadwal
            status = "j"
        elif line == "": #pemisah antar bagian
            continue
        elif status == "r":
            parsed = line.split(";") #string nama, int jamBuka, int jamTutup, int[] hari
            newObjekRuangan = Ruangan(parsed[0], parsed[1], parsed[2], parsed[3].split(","))
            listRuangan.append(newObjekRuangan) #daftarkan objek baru ke list
        elif status == "j":
            parsed = line.split(";") #string nama, string constraint ruang, int jamBuka, int jamTutup, int sks, int[] hari
            newObjekMatkul = Matkul(parsed[0], parsed[2], parsed[3], parsed[4], parsed[5].split(","))
            domain = makeListDomain(newObjekMatkul, parsed[1]) #cari tempat dan waktu mana saja yang memungkinkan
            newObjekMatkul.addListDomain(domain) #daftarkan domain-domain tersebut ke listDomain
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
                        #lihat jam yang tersedia oleh Ruangan dengan yang dibutuhkan Matkul (cari jam yang cocok)
                        jamMulai = matkul.jamBuka
                        jamSelesai = jamMulai + matkul.sks
                        while jamSelesai <= ruang.jamTutup and jamSelesai <= matkul.jamTutup:
                            if jamMulai >= ruang.jamBuka:
                                #dapat 1 kandidat: Matkul BISA ditempatkan di Ruangan ini, di hari ini, dan di jam segini
                                newObjekDomain = Domain(ruang, hariRuangan, jamMulai, jamSelesai)
                                hasil.append(newObjekDomain)
                            jamMulai += 1
                            jamSelesai += 1
    hasil.sort(key=lambda domain: domain.jamMulai)
    return hasil

def initializeRandom():
    for matkul in listMatkul:
        matkul.setIdxDomain(random.randint(0, matkul.nDomain - 1)) #pure random
        #heuristik = idxPlus terus menerus sampai menemukan jam paling pagi di hari esoknya
        domainNow = matkul.getDomain()
        matkul.idxPlus()
        domainNew = matkul.getDomain()
        while(domainNew.jamMulai > domainNow.jamMulai):
            domainNow = domainNew
            matkul.idxPlus()
            domainNew = matkul.getDomain()

def countConflicts():
    del listKonflik[:] #list yang di program utama di hapus dulu karena mau di generate ulang
    hasil = 0 #banyaknya konflik
    listKonflikLokal = [] #list konflik lokal (beda dari yang di program utama) supaya pointer tidak kemana mana
    #cari konflik per Ruangan
    for ruangan in listRuangan:
        #cek di setiap sel nya
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

def hillOrStimulated(tempMax, tempMin, threshold, decrease):
    lokalMaks = False #kalo terjebak di lokal maks, bernilai true
    step = 0 #sudah berapa kali iterasi
    listKonflikLokal = [] #list konflik lokal (beda dari yang di program utama)
    nKonflikNow = countConflicts()
    #mulai hill climbing, iterasi tidak dibatasi (sampai dapat solusi atau sampai lokal maksimum)
    while nKonflikNow > 0 and lokalMaks == False:
        #copy list konflik di program utama ke list konflik lokal (agar pointer tidak berantakan)
        del listKonflikLokal[:]
        for matkul in listKonflik:
            listKonflikLokal.append(matkul)
        #heuristik = geser matkul yang konflik menjadi tepat setelah matkul lawannya selesai (tidak overlap lagi)
        foundBetter = False
        for matkul in listKonflikLokal:
            #majuin terus sebanyak nDomain kali (kasus terburuk yaitu semua domain dicoba dan gaada yang lebih baik)
            for i in range(matkul.nDomain):
                step += 1 #iterasi bertambah
                tempMax -= decrease #toleransi berkurang
                matkul.idxPlus()
                nKonflikNew = countConflicts() #prosedur ini merubah list konflik program utama saja (lokal tetap aman)
                if nKonflikNew < nKonflikNow: #ternyata domain setelah dimajuin 1 jadi lebih baik
                    foundBetter = True
                    break #break for i
                else: #sama aja atau bahkan lebih buruk, cek apakah bisa ditolerir untuk tetap diambil
                    probability = exp(abs(nKonflikNow - nKonflikNew)*1000/tempMax)
                    if probability > threshold: #random walk
                        hasilRandom = random.randint(0,1);
                        if hasilRandom == 1: #ambil walaupun lebih banyak konflik
                            foundBetter = True
                            break #break for i
                        elif hasilRandom == 0: # tidak mengambil konfigurasi baru
    #hasil : dapat solusi atau terjebak lokal maksimum
    if nKonflikNow == 0:
        print "SOLUSI DITEMUKAN DALAM", step, "ITERASI"
    else:
        print nKonflikNow, "KONFLIK DALAM", step, "ITERASI:"
        for matkul in listKonflik:
            print " ", matkul.nama

def geneticAlgorithm(generasi):
    #fitness function max kalau semua matkul domainnya alldiff
    fitnessMax = 0
    for matkul in listMatkul:
        fitnessMax += matkul.sks
    fitness = []
    #genetic algorithm
    keturunan = 0
    while True:
        #hitung fitness tiap gen
        del fitness[:]
        for i in range(len(listGen)):
            #pasangkan dulu matkul dengan domain sesuai dengan yang ada pada gen, agar sel di tiap Ruangan sesuai
            restart()
            for j in range(len(listGen[i])):
                listMatkul[j].setIdxDomain(listGen[i][j])
            #hitung total sel yang tidak konflik, ini fitnessnya
            fitness.append(0)
            for ruang in listRuangan:
                fitness[i] += ruang.countFitness()
            if fitness[i] == fitnessMax:
                print "SOLUSI DITEMUKAN DALAM GENERASI", keturunan
                return
        #cari gen terjelek dan terbagus
        idxMin = fitness.index(min(fitness))
        idxMax = fitness.index(max(fitness))
        keturunan += 1
        #gak nemu solusi sampai keturunan ke-generasi
        if keturunan == generasi:
            #pasangkan lagi matkul dengan domain kepunyaan gen terbaik (fitness terbesar)
            restart()
            for i in range(len(listGen[idxMax])):
                listMatkul[i].setIdxDomain(listGen[idxMax][i])
            #hitung konflik
            print countConflicts(), "KONFLIK DALAM GENERASI", keturunan
            for matkul in listKonflik:
                print " ", matkul.nama
            break #break while infinite
        else:
            #gen jelek timpa dengan gen bagus
            for i in range(len(listMatkul)):
                listGen[idxMin][i] = listGen[idxMax][i]
            #kawin silang TANPA mutasi, mulai dari idxBelah (random) sampai index terakhir
            idxBelah = random.randint(1, len(listMatkul) - 2)
            for i in range(idxBelah, len(listMatkul)):
                #swap idx 0 dan 1
                temp = listGen[0][i]
                listGen[0][i] = listGen[1][i]
                listGen[1][i] = temp
                #swap idx 2 dan 3
                temp = listGen[2][i]
                listGen[2][i] = listGen[3][i]
                listGen[3][i] = temp
            #mutasi = matkul ke-matkulMutasi di gen, domainnya berubah menjadi domainMutasi
            for gen in listGen:
                matkulMutasi = random.randint(0, len(listMatkul) - 1)
                domainMutasi = random.randint(0, listMatkul[matkulMutasi].nDomain - 1)
                gen[matkulMutasi] = domainMutasi

def pindahJadwal(namaMatkul, namaRuangan, hariBaru, jamBaru):
    #cari matkul berdasarkan nama
    matkulPindah = None
    for matkul in listMatkul:
        if matkul.nama == namaMatkul:
            matkulPindah = matkul
            break
    if matkulPindah is None:
        print "Jadwal tidak ditemukan"
    else: #ketemu
        idxDomainLama = matkulPindah.idxDomain
        idxDomainBaru = idxDomainLama
        #cari idxDomainBaru
        listDomain = matkulPindah.listDomain
        for idx in range(len(listDomain)):
            domain = listDomain[idx]
            if domain.ptrRuangan.nama == namaRuangan and domain.hari == hariBaru and domain.jamMulai == jamBaru:
                idxDomainBaru = idx #ketemu
                break
        #domain gak ketemu atau dipindahin ke domain yg sama -_-
        if idxDomainBaru == idxDomainLama:
            print "Jadwal tetap"
        else:
            #pindahin
            matkulPindah.deleteFromSlot()
            matkulPindah.setIdxDomain(idxDomainBaru)
            #hitung conflik baru
            nKonflik = countConflicts()
            if nKonflik == 0:
                print "SOLUSI DITEMUKAN SETELAH EDIT"
            else:
                print nKonflik, "KONFLIK SETELAH EDIT:"
                for matkul in listKonflik:
                    print " ", matkul.nama
            printHasil()

def restart(): #hapus data agar bisa dipakai ulang
    del listKonflik[:]
    for ruang in listRuangan:
        ruang.deleteAllSel()

def printHasil(): #gaperlu dimengerti, hiasan print doang
    print "========================================================================="
    print "| MATKUL\t| RUANG\t\t| HARI\t\t\t| PUKUL\t\t|"
    print "========================================================================="
    for matkul in listMatkul:
        matkul.printConsole()
    totalSel = 0
    selTerisi = 0
    for ruang in listRuangan:
        totalSel += ruang.selAvailable
        selTerisi += ruang.countFilledSel()
    print "Persentasi keefektifan =", "%.2f" % (selTerisi / totalSel * 100), "persen.\n"

def execHC():
    print "====HILL CLIMBING===="
    restart()
    initializeRandom()
    hillOrStimulated(1, 1, 5, 1) #atur temperatur menjadi low
    printHasil()

def execSA():
    print "====STIMULATED ANNEALING===="
    restart()
    initializeRandom()
    hillOrStimulated(100, 1, 50, 1)
    printHasil()

def execGA():
    print "====GENETIC ALGORITHM (4 GENES)===="
    for gen in listGen:
        del gen[:]
        #initializeRandom() tanpa heuristik
        for matkul in listMatkul:
            gen.append(random.randint(0, matkul.nDomain - 1)); #masukkan ke gen idxDomain nya saja
    geneticAlgorithm(20)
    printHasil()

#PROGRAM UTAMA
listRuangan = []
listMatkul = []
listKonflik = []
listGen = [[], [], [], []] #list of list of idxDomain for GA only
bacaTestcase("Testcase.txt")
execHC()
execSA()
execGA()
#parameter pindah jadwal = nama matkul yang ingin dipindah, nama ruangan tujuan, hari tujuan (senin = 1), jam mulai tujuan
#contoh dibawah = Matkul IF3111 dipindah ke Ruangan 7610 hari Rabu dimulai dari jam 9
pindahJadwal("IF3111", "7610", 3, 9)
#berhubung algo terakhir yang digunakan adalah GA, maka yang dipindah jadwalnya adalah jadwal hasil si GA
