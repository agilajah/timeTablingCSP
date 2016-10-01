from __future__ import division
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
        self.selAvailable = (self.jamTutup - self.jamBuka) * len(self.hari)

    def slotPlus(self, matkul, hari, jamMulai, jamSelesai): #tambahkan matkul ke slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].append(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari

    def slotMinus(self, matkul, hari, jamMulai, jamSelesai): #hapus matkul dari slot time
        for i in range(jamMulai, jamSelesai):
            self.sel[i - 7][hari - 1].remove(matkul) #dikurang 7 untuk jam, dikurang 1 untuk hari

    def deleteAllSel(self):
        for jam in self.sel:
            for hari in jam:
                del hari[:]

    def countFilledSel(self):
        hasil = 0
        for i in range(11): #cek tiap sel
            if i + 7 >= self.jamBuka and i + 7 <= self.jamTutup:
                for j in self.hari:
                    if len(self.sel[i][int(j) - 1]) > 0: #ada isinya
                        hasil += 1
        return hasil

    def countFitness(self):
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
        print self.nama, "\t", domain.ptrRuangan.nama, "\t", stringHari, "\t", domain.jamMulai, "-", domain.jamSelesai

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
                        while jamSelesai <= ruang.jamTutup and jamSelesai <= matkul.jamTutup:
                            if jamMulai >= ruang.jamBuka:
                                #dapat 1 kandidat Matkul BISA ditempatkan di Ruangan ini, di hari ini, dan di jam segini
                                newObjekDomain = Domain(ruang, hariRuangan, jamMulai, jamSelesai)
                                hasil.append(newObjekDomain)
                            jamMulai += 1
                            jamSelesai += 1
    return hasil

def initializeRandom():
    for matkul in listMatkul:
        matkul.setIdxDomain(random.randint(0, matkul.nDomain - 1))
        #heuristik = taruh matkul sepagi mungkin
        domainNow = matkul.getDomain()
        matkul.idxPlus()
        domainNew = matkul.getDomain()
        #lakukan idxPlus terus menerus sampai menemukan jam paling pagi di hari esoknya
        while(domainNew.jamMulai > domainNow.jamMulai):
            domainNow = domainNew
            matkul.idxPlus()
            domainNew = matkul.getDomain()

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

def hillOrStimulated(tempMax, tempMin, threshold, decrease):
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
        #heuristik = geser matkul yang konflik menjadi tepat setelah matkul lawannya (tidak overlap lagi)
        foundBetter = False
        for matkul in listKonflikNow:
            #majuin terus sebanyak nDomain kali (1 cycle, kasus terburuk, matkul ini gabisa diapa2in lagi)
            for i in range(matkul.nDomain):
                step += 1
                tempMax -= decrease
                matkul.idxPlus() #saat dimajuin, listKonflik berubah namun listKonflikNow tetap
                nKonflikNew = countConflicts()
                if nKonflikNew < nKonflikNow: #bandingkan konflik
                    foundBetter = True
                    break #break for i
                else: #nKonflikNew >= nKonflikNow
                    if tempMax > threshold: #masih mungkin random
                        hasilRandom = random.randint(tempMin, tempMax);
                        if hasilRandom >= threshold: #ambil walaupun lebih banyak konflik
                            foundBetter = True
                            break #break for i
            nKonflikNow = nKonflikNew #berhasil atau tidak menemukan yang lebih baik, tetap ambil nilainya
            if foundBetter == True:
                break #break for matkul
            elif matkul == listKonflikNow[len(listKonflikNow) - 1]:
                lokalMaks = True #matkul terakhir, tetep gak nemu lebih baik
        if lokalMaks == True: #gak bisa ngapa2in lagi udah mentok
            print "    LOKAL MAKSIMUM"
            break #break while
    #sudah iterasi sebanyak step, atau sudah menemukan solusi
    if nKonflikNow == 0:
        print "SOLUSI DITEMUKAN DALAM", step, "ITERASI"
    else:
        print nKonflikNow, "KONFLIK DALAM", step, "ITERASI:"
        for matkul in listKonflik:
            print " ", matkul.nama

def geneticAlgorithm():
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
            for ruang in listRuangan:
                ruang.deleteAllSel()
            for j in range(len(listGen[i])):
                listMatkul[j].setIdxDomain(listGen[i][j])
            fitness.append(0)
            for ruang in listRuangan:
                fitness[i] += ruang.countFitness() #total sel yang tidak konflik
            if fitness[i] == fitnessMax:
                print "SOLUSI DITEMUKAN DALAM", keturunan, "GENERASI:"
        #cari gen terjelek dan terbagus
        idxMin = fitness.index(min(fitness))
        idxMax = fitness.index(max(fitness))
        keturunan += 1
        if keturunan == 10:
            #udah sekian kali kawin silang dan gak nemu, keluarin aja fitness yang terbaik
            del listKonflik[:]
            for ruang in listRuangan:
                ruang.deleteAllSel()
            for i in range(len(listGen[idxMax])):
                listMatkul[i].setIdxDomain(listGen[idxMax][i])
            print countConflicts(), "KONFLIK DALAM", keturunan, "GENERASI:"
            for matkul in listKonflik:
                print " ", matkul.nama
            return
        else:
            #paling jelek timpa dengan paling bagus
            for i in range(len(listMatkul)):
                listGen[idxMin][i] = listGen[idxMax][i]
            #kawin silang tanpa mutasi
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

def restart():
    del listKonflik[:]
    for ruang in listRuangan:
        ruang.deleteAllSel()
    initializeRandom()

def printHasil():
    print "MATKUL\tRUANG\tHARI\tPUKUL"
    for matkul in listMatkul:
        matkul.printConsole()
    totalSel = 0
    selTerisi = 0
    for ruang in listRuangan:
        totalSel += ruang.selAvailable
        selTerisi += ruang.countFilledSel()
    print "Persentasi keefektifan =", "%.2f" % (selTerisi / totalSel * 100), "persen.\n"

#PROGRAM UTAMA
listRuangan = []
listMatkul = []
listKonflik = []
listGen = [[], [], [], []] #list of list of idxDomain untuk GA only
bacaTestcase("Testcase.txt")
print "====HILL CLIMBING===="
restart()
hillOrStimulated(1, 1, 5, 1) #atur temperatur menjadi low
printHasil()
print "====STIMULATED ANNEALING===="
restart()
hillOrStimulated(100, 1, 5, 1)
printHasil()
print "====GENETIC ALGORITHM (4 GENES)===="
for gen in listGen:
    del gen[:]
    #initializeRandom() tanpa heuristik
    for matkul in listMatkul:
        gen.append(random.randint(0, matkul.nDomain - 1)); #masukkan ke gen idxDomain nya saja
geneticAlgorithm()
printHasil()