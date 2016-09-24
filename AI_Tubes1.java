package imk_tubes1;
import java.util.ArrayList;

public class IMK_Tubes1 {
    class Slot {
        @SuppressWarnings("Convert2Diamond")
        ArrayList<Matkul> isi = new ArrayList<Matkul>();
    }
    
    class Ruangan {
        private final int nJam = 11;
        private final int nHari = 5;
        final String namaRuangan;
        final int jamBuka;
        final int jamTutup;
        final int[] hariBuka;
        final boolean[][] isSlotBuka = new boolean[nJam][nHari];
        final Slot slot[][] = new Slot[nJam][nHari];
        
        Ruangan(String namaRuangan, int jamBuka, int jamTutup, int[] hariBuka) {
            this.namaRuangan = namaRuangan;
            this.jamBuka = jamBuka;
            this.jamTutup = jamTutup;
            this.hariBuka = hariBuka;
            //array awalnya kosong semua
            for(int i = 0; i < nJam; i++) {
                for(int j = 0; j < nHari; j++) {
                    isSlotBuka[i][j] = false;
                    slot[i][j] = new Slot();
                }
            }
            //atur slot ruangannya available/tidak
            jamBuka -= 7; //jam 7 = index ke-0
            jamTutup -= 7; //jam 7 = index ke-0
            for(int i = jamBuka; i < jamTutup; i++) {
                for(int j : hariBuka) {
                    isSlotBuka[i][j - 1] = true; //senin = index ke-0
                }
            }
        }
        
        void printSlot() {
            for(Slot[] i : slot) {
                for(Slot j : i) {
                    if(j.isi.isEmpty()) {
                        System.out.print(" x ");
                    } else {
                        for(Matkul m : j.isi) {
                            System.out.print(m.namaMatkul);
                        }
                    }
                }
                System.out.println();
            }
        }
    }
    
    class Matkul {
        int plottedJam;
        int plottedHari;
        Ruangan plottedRuangan;
        final String namaMatkul;
        final ArrayList<Ruangan> tempat;
        final int jamMulai;
        final int jamAkhir;
        final int sks;
        final int[] hari;
        
        Matkul(String namaMatkul, ArrayList<Ruangan> tempat, int jamMulai,
            int jamAkhir, int sks, int[] hari) {
            this.namaMatkul = namaMatkul;
            this.tempat = tempat;
            this.jamMulai = jamMulai;
            this.jamAkhir = jamAkhir;
            this.sks = sks;
            this.hari = hari;
        }
    }
    
    @SuppressWarnings("Convert2Diamond")
    private final ArrayList<Ruangan> listRuangan = new ArrayList<Ruangan>();
    @SuppressWarnings({"Convert2Diamond",
        "MismatchedQueryAndUpdateOfCollection"})
    private final ArrayList<Matkul> listMatkul = new ArrayList<Matkul>();
    
    public void bacaRuangan() {
        //read file harusnya
        String[] testcase = {
            "7602;07.00;14.00;1,2,3,4,5",
            "7603;07.00;14.00;1,3,5",
            "7610;09.00;12.00;1,2,3,4,5",
            "Labdas2;10.00;14.00;2,4"
        };
        //parse
        for(String lineRuangan : testcase) {
            //split
            String[] split1 = lineRuangan.split(";");
            //ambil data
            String nama = split1[0];
            int jamBuka = (int) Double.parseDouble(split1[1]);
            int jamTutup = (int) Double.parseDouble(split1[2]);
            String[] split2 = split1[3].split(",");
            int[] hariBuka = new int[split2.length];
            for(int i = 0; i < split2.length; i++) {
                hariBuka[i] = Integer.parseInt(split2[i]);
            }
            //add
            listRuangan.add(new Ruangan(nama, jamBuka, jamTutup, hariBuka));
        }
    }
    public void bacaMatkul() {
        //read file harusnya
        String[] testcase = {
            "F2110;7602;07.00;12.00;4;1,2,3,4,5",
            "F2130;-;10.00;16.00;3;3,4",
            "F2150;-;09.00;13.00;2;1,3,5",
            "F2170;7610;07.00;12.00;3;1,2,3,4,5",
            "F3110;7602;07.00;09.00;2;1,2,3,4,5",
            "F3130;-;07.00;12.00;2;3,4,5",
            "F3170;7602;07.00;09.00;2;1,2,3,4,5",
            "F3111;-;07.00;12.00;2;1,2,3,4,5"
        };
        //parse
        for(String lineMatkul : testcase) {
            //split
            String[] split1 = lineMatkul.split(";");
            //ambil data
            String nama = split1[0];
            ArrayList<Ruangan> tempat = cariRuangan(split1[1]);
            int mulai = (int) Double.parseDouble(split1[2]);
            int akhir = (int) Double.parseDouble(split1[3]);
            int sks = Integer.parseInt(split1[4]);
            String[] split2 = split1[5].split(",");
            int[] hari = new int[split2.length];
            for(int i = 0; i < split2.length; i++) {
                hari[i] = Integer.parseInt(split2[i]);
            }
            //add
            listMatkul.add(new Matkul(nama, tempat, mulai, akhir, sks, hari));
        }
    }
    
    private ArrayList<Ruangan> cariRuangan(String namaRuangan) {
        if(namaRuangan.equals("-")) {
            return listRuangan; //gapunya constraint, bisa di semua ruangan
        }
        @SuppressWarnings("Convert2Diamond")
        ArrayList<Ruangan> hasil = new ArrayList<Ruangan>();
        for(Ruangan r : listRuangan) {
            if(namaRuangan.equals(r.namaRuangan)) {
                hasil.add(r); //bisanya di ruangan itu doang
                break;
            }
        }
        return hasil; //bisa null kalo ruangan gak ditemukan
    }
    private void addMatkulToRuangan(Matkul m, Ruangan r, int jamMulai,
        int hari) {
        if(m.plottedRuangan != null) {
            return; //variabel matkul sudah di plot, gabisa ngeplot lagi
        }
        jamMulai -= 7; //jam 7 = index ke-0
        hari -= 1; //senin = index ke-0
        for(int i = jamMulai; i < jamMulai + m.sks; i++) {
            r.slot[i][hari].isi.add(m);
        }
        m.plottedJam = jamMulai;
        m.plottedHari = hari;
        m.plottedRuangan = r; //tandain supaya gak diambil lagi
    }
    private void delMatkulFromRuangan(Matkul m) {
        if(m.plottedRuangan == null) {
            return; //variabel matkul belum di plot, gaada yg dihapus
        }
        for(int i = m.plottedJam; i < m.plottedJam + m.sks; i++) {
            m.plottedRuangan.slot[i][m.plottedHari].isi.remove(m);
        }
        m.plottedRuangan = null; //bisa diambil lagi
    }
    
    //testing
    public void proses() {
        for(Ruangan r : listRuangan) {
            System.out.println(r.namaRuangan);
            r.printSlot();
            System.out.println();
        }
        addMatkulToRuangan(listMatkul.get(0), listRuangan.get(0), 7, 1);
        for(Ruangan r : listRuangan) {
            System.out.println(r.namaRuangan);
            r.printSlot();
            System.out.println();
        }
        delMatkulFromRuangan(listMatkul.get(0));
        for(Ruangan r : listRuangan) {
            System.out.println(r.namaRuangan);
            r.printSlot();
            System.out.println();
        }
    }
    public static void main(String[] args) {
        IMK_Tubes1 imk = new IMK_Tubes1();
        imk.bacaRuangan();
        imk.bacaMatkul();
        imk.proses();
    }
}

/*private void printJamXRuangan() {
    //hiasan print gapenting
    int pukul;
    for(Ruangan r : listRuangan) {
        System.out.println("Ruang " + r.namaRuangan);
        System.out.println("      Senin Selasa Rabu Kamis Jumat");
        pukul = 7;
        for(boolean[] jam : r.isSlotBuka) {
            System.out.printf("%2d:00 ", pukul);
            for(boolean hari : jam) {
                System.out.printf("  %c   ", hari ? 'v' : ' ');
            }
            System.out.println();
            pukul++;
        }
        System.out.println();
    }
}
private void printJamXHari() {
    //coming soon
}
private void printPerMatkul() {
    //hiasan print gapenting
    for(Matkul m : listMatkul) {
        System.out.println("Matkul " + m.namaMatkul);
        System.out.print("Ruangan ");
        for(Ruangan r : m.tempat) {
            System.out.print(r.namaRuangan + " ");
        }
        System.out.println();
        System.out.printf("Jam %d:00-%d:00\n", m.jamMulai,
            m.jamAkhir);
        System.out.println("SKS " + m.sks);
        System.out.print("Hari ");
        for(int x : m.hari) {
            switch(x) {
                case 1 : System.out.print("Senin "); break;
                case 2 : System.out.print("Selasa "); break;
                case 3 : System.out.print("Rabu "); break;
                case 4 : System.out.print("Kamis "); break;
                case 5 : System.out.print("Jumat "); break;
            }
        }
        System.out.println("\n");
    }
}*/