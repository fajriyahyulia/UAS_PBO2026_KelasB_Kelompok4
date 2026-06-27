#Dikerjakan Oleh
#Abid Satriyo Maulana [K3525045]
"""
menu.py
Antarmuka pengguna berbasis terminal.
SRP: hanya tanggung jawab tampilan dan interaksi user.
"""

import os
from hanari_bakery.services.produk_service import ProductService
from hanari_bakery.services.laporan_service import LaporanGenerator


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def garis(char="=", p=58):
    print(char * p)

def header(judul):
    garis()
    print(f"  {judul}")
    garis()

def pause():
    input("\n  Tekan Enter untuk kembali ke menu...")

def wrap_print(teks, lebar=54, indent="  "):
    words = teks.split()
    line = indent
    for word in words:
        if len(line) + len(word) + 1 > lebar + len(indent):
            print(line)
            line = indent + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)


class MenuUtama:
    def __init__(self, service: ProductService):
        self._service = service
        self._laporan = LaporanGenerator()

    def tampilkan(self):
        while True:
            clear_screen()
            garis()
            print("  HANARI BAKERY")
            print("  Sistem Informasi Produksi & Manajemen Produk")
            garis()
            print("  [1] Tambah Produk Baru")
            print("  [2] Tampilkan Semua Produk")
            print("  [3] Kalkulator Estimasi Profit")
            print("  [4] Simulasi Proses Produksi")
            print("  [5] Manajemen Stok Bahan Baku")
            print("  [6] History Produksi")
            print("  [7] Laporan Rekapitulasi")
            print("  [8] Hapus Produk")
            print("  [0] Keluar")
            garis("-")
            pilihan = input("  Pilih menu: ").strip()

            actions = {
                "1": self._menu_tambah_produk,
                "2": self._menu_tampilkan_semua,
                "3": self._menu_kalkulator_profit,
                "4": self._menu_simulasi_produksi,
                "5": self._menu_stok,
                "6": self._menu_history,
                "7": self._menu_laporan,
                "8": self._menu_hapus_produk,
            }

            if pilihan == "0":
                print("\n  Sampai jumpa! Selamat berproduction~")
                break
            elif pilihan in actions:
                actions[pilihan]()
            else:
                print("\n  Pilihan tidak valid.")
                pause()

    def _menu_tambah_produk(self):
        clear_screen()
        header("TAMBAH PRODUK BARU")
        print("  [1] Pilih dari produk default")
        print("  [2] Tambah produk variasi baru (custom)")
        garis("-")
        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            self._tambah_produk_default()
        elif pilihan == "2":
            self._tambah_produk_custom()
        else:
            print("  Pilihan tidak valid.")
            pause()

    def _tambah_produk_default(self):
        clear_screen()
        header("TAMBAH PRODUK DEFAULT")
        tersedia = self._service.get_produk_tersedia()
        print("  Produk tersedia:")
        for kode, nama in tersedia.items():
            print(f"    {kode}  ->  {nama}")
        garis("-")
        kode = input("  Masukkan kode produk: ").strip()
        sukses, pesan = self._service.tambah_produk(kode)
        print(f"\n  {'[OK]' if sukses else '[GAGAL]'} {pesan}")
        pause()

    def _tambah_produk_custom(self):
        clear_screen()
        header("TAMBAH PRODUK VARIASI BARU")
        print("  Isi data produk baru. Tekan Enter untuk lanjut.")
        garis("-")

        nama = input("  Nama produk       : ").strip()
        if not nama:
            print("  Nama tidak boleh kosong.")
            pause()
            return

        kode = input("  Kode produk (contoh: DN-001): ").strip().upper()
        if not kode:
            print("  Kode tidak boleh kosong.")
            pause()
            return

        print("  Jenis produk:")
        print("    [1] Roti Manis")
        print("    [2] Croissant")
        print("    [3] Kue Kering")
        print("    [4] Lainnya (ketik sendiri)")
        pilihan_jenis = input("  Pilih jenis: ").strip()
        jenis_map = {"1": "Roti Manis", "2": "Croissant", "3": "Kue Kering"}
        if pilihan_jenis in jenis_map:
            jenis = jenis_map[pilihan_jenis]
        else:
            jenis = input("  Nama jenis: ").strip() or "Lainnya"

        from hanari_bakery.models.produk_base import BahanBaku
        bahan_list = []
        print(f"\n  Input bahan baku (ketik 'selesai' untuk berhenti):")
        while True:
            nama_bahan = input(f"  Nama bahan [{len(bahan_list)+1}]: ").strip()
            if nama_bahan.lower() == "selesai" or nama_bahan == "":
                if len(bahan_list) == 0:
                    print("  Minimal 1 bahan baku!")
                    continue
                break
            try:
                jumlah = float(input(f"  Jumlah       : ").strip())
                satuan = input(f"  Satuan (gram/ml/butir/sdt): ").strip()
                bahan_list.append(BahanBaku(nama_bahan, jumlah, satuan))
                print(f"  [+] {nama_bahan} {jumlah} {satuan} ditambahkan.")
            except ValueError:
                print("  Jumlah harus angka, coba lagi.")

        print("\n  Pilih proses produksi (bisa lebih dari satu):")
        semua_proses = ["pengadonan", "pengembangan", "pemanggangan", "topping"]
        for i, p in enumerate(semua_proses, 1):
            print(f"    [{i}] {p.capitalize()}")
        print("  Contoh input: 1 3 (pengadonan + pemanggangan)")
        pilihan_proses = input("  Pilih nomor proses: ").strip().split()
        proses_dipilih = []
        for p in pilihan_proses:
            try:
                idx = int(p) - 1
                if 0 <= idx < len(semua_proses):
                    proses_dipilih.append(semua_proses[idx])
            except ValueError:
                pass
        if not proses_dipilih:
            proses_dipilih = ["pengadonan", "pemanggangan"]
            print("  Tidak ada proses dipilih, pakai default: pengadonan + pemanggangan")

        try:
            jumlah_per_resep = int(input("\n  Jumlah pcs per resep  : ").strip())
            biaya = float(input("  Biaya produksi/resep  : Rp ").strip())
            harga = float(input("  Harga jual/resep      : Rp ").strip())
        except ValueError:
            print("  Input angka tidak valid.")
            pause()
            return

        clear_screen()
        header("KONFIRMASI PRODUK BARU")
        print(f"  Nama          : {nama}")
        print(f"  Kode          : {kode}")
        print(f"  Jenis         : {jenis}")
        print(f"  Bahan baku    : {len(bahan_list)} item")
        print(f"  Proses        : {', '.join(proses_dipilih)}")
        print(f"  Per resep     : {jumlah_per_resep} pcs")
        print(f"  Biaya produksi: Rp {biaya:,.0f}")
        print(f"  Harga jual    : Rp {harga:,.0f}")
        margin = ((harga - biaya) / harga * 100) if harga > 0 else 0
        print(f"  Margin profit : {margin:.1f}%")
        garis("-")
        konfirmasi = input("  Simpan produk ini? (y/n): ").strip().lower()

        if konfirmasi == "y":
            sukses, pesan = self._service.tambah_produk_custom(
                nama=nama, kode=kode, jenis=jenis,
                bahan_baku=bahan_list, biaya=biaya, harga=harga,
                jumlah_per_resep=jumlah_per_resep, proses=proses_dipilih,
            )
            print(f"\n  {'[OK]' if sukses else '[GAGAL]'} {pesan}")
        else:
            print("  Dibatalkan.")
        pause()

    def _menu_tampilkan_semua(self):
        clear_screen()
        header("DAFTAR SEMUA PRODUK")
        produk_list = self._service.tampilkan_semua_produk()
        if not produk_list:
            print("  Belum ada produk terdaftar.")
        else:
            for p in produk_list:
                print(p.info_lengkap())
        pause()

    def _menu_kalkulator_profit(self):
        clear_screen()
        header("KALKULATOR ESTIMASI PROFIT")
        produk_list = self._service.tampilkan_semua_produk()
        if not produk_list:
            print("  Belum ada produk. Tambahkan dulu!")
            pause()
            return

        print("  Pilih produk:")
        for p in produk_list:
            print(f"    [{p.kode}] {p.nama} | {p.jumlah_per_resep} pcs/resep | ~{p.total_waktu_produksi()} mnt/resep")

        garis("-")
        kode = input("  Kode produk: ").strip()
        try:
            jumlah = int(input("  Jumlah pcs yang diproduksi: ").strip())
            if jumlah <= 0:
                raise ValueError
        except ValueError:
            print("\n  Input tidak valid.")
            pause()
            return

        hasil = self._service.estimasi_profit(kode, jumlah)
        if not hasil:
            print(f"\n  Produk '{kode}' tidak ditemukan.")
            pause()
            return

        # ---- TAMPILAN NOTA ANALISIS DUA KONDISI PROFIT ----
        print("\n" + "="*58)
        print(f" HASIL ESTIMASI PRODUKSI: {hasil['produk']}")
        print("="*58)
        print(f" Jumlah diminta      : {hasil['jumlah_pcs_diminta']} pcs")
        print(f" Jumlah resep        : {hasil['jumlah_resep']} resep")
        print(f" Total diproduksi    : {hasil['total_pcs_diproduksi']} pcs")
        print(f" Est. waktu produksi : ~{hasil['estimasi_waktu_menit']} menit")
        print("-"*58)
        print(" KONDISI A: JIKA SEMUA HASIL PRODUKSI HABIS TERJUAL")
        print("-"*58)
        print(f" Total Pendapatan    : Rp {hasil['total_pendapatan']:,}")
        print(f" TOTAL PROFIT MAKS   : Rp {hasil['total_profit']:,}")
        print(f" Margin Profit Maks  : {hasil['margin_profit']:.1f}%")
        print("-"*58)
        print(" KONDISI B: JIKA HANYA TERJUAL SESUAI PERMINTAAN USER")
        print("-"*58)
        print(f" Total Pendapatan    : Rp {hasil['pendapatan_riil']:,}")
        print(f" TOTAL PROFIT RIIL   : {hasil['profit_riil']}")
        
        # Logika catatan baru berbasis BEP Matematika Industri
        if hasil['angka_profit_riil'] < 0:
            print(f" STATUS              : RUGI SEMENTARA (Sisa {hasil['sisa_pcs']} pcs di etalase)")
            print(f" Catatan             : Harus menjual minimal {hasil.get('pcs_tambahan_lagi', 1)} pcs lagi untuk balik modal")
        else:
            print(f" STATUS              : TETAP UNTUNG (Sisa {hasil['sisa_pcs']} pcs jadi bonus etalase)")
            
        print("="*58 + "\n")
        input("  Tekan Enter untuk kembali ke menu...")

    def _menu_simulasi_produksi(self):
        clear_screen()
        header("SIMULASI PROSES PRODUKSI")
        produk_list = self._service.tampilkan_semua_produk()
        if not produk_list:
            print("  Belum ada produk.")
            pause()
            return

        print("  Pilih produk:")
        for p in produk_list:
            print(f"    [{p.kode}] {p.nama}")

        garis("-")
        kode = input("  Kode produk: ").strip()
        try:
            jumlah = int(input("  Jumlah pcs yang akan diproduksi: ").strip())
            if jumlah <= 0:
                raise ValueError
        except ValueError:
            print("\n  Input tidak valid.")
            pause()
            return

        hasil = self._service.simulasi_produksi(kode, jumlah)
        if not hasil:
            print(f"\n  Produk '{kode}' tidak ditemukan.")
            pause()
            return

        produk = hasil["produk"]
        cek_stok = hasil["cek_stok"]

        clear_screen()
        header(f"SIMULASI PRODUKSI: {produk.nama}")
        print(f"  Target produksi : {jumlah} pcs ({hasil['jumlah_resep']} resep)")
        print(f"  Est. total waktu: ~{hasil['total_waktu']} menit")

        garis("-")
        status_stok = "[CUKUP]" if cek_stok["cukup"] else "[PERHATIAN]"
        print(f"  CEK STOK BAHAN BAKU {status_stok}")
        garis("-")
        print(f"  {'BAHAN':<35} {'BUTUH':>8} {'TERSEDIA':>10} STATUS")
        print(f"  {'-'*56}")
        for d in cek_stok["detail"]:
            status_icon = "OK" if d["status"] == "CUKUP" else "!!"
            print(
                f"  [{status_icon}] {d['nama']:<32} "
                f"{d['dibutuhkan']:>6.0f} {d['satuan'][:2]}"
                f"  {d['tersedia']:>6.0f} {d['satuan'][:2]}"
                f"  {d['status']}"
            )

        if not cek_stok["cukup"]:
            print("\n  PERINGATAN: Stok tidak mencukupi!")
            print("  Silakan update stok di menu [5] sebelum produksi.")

        garis("-")
        print("  LANGKAH-LANGKAH PRODUKSI:")
        garis("-")
        for i, (nama_proses, deskripsi, durasi) in enumerate(hasil["langkah"], 1):
            print(f"\n  LANGKAH {i}: {nama_proses.upper()} (~{durasi} menit)")
            wrap_print(deskripsi)

        if hasil["profit_info"]:
            p = hasil["profit_info"]
            garis("-")
            print(f"  Estimasi Profit: Rp {p['total_profit']:,.0f} | Margin: {p['margin_profit']:.1f}%")

        garis()
        print("  [Simulasi ini telah disimpan ke history produksi]")
        pause()

    def _menu_stok(self):
        while True:
            clear_screen()
            header("MANAJEMEN STOK BAHAN BAKU")
            print("  [1] Lihat semua stok")
            print("  [2] Update/tambah stok bahan")
            print("  [0] Kembali")
            garis("-")
            pilihan = input("  Pilih: ").strip()

            if pilihan == "0":
                break
            elif pilihan == "1":
                self._tampilkan_stok()
            elif pilihan == "2":
                self._update_stok()

    def _tampilkan_stok(self):
        clear_screen()
        header("STATUS STOK GUDANG")
        stok = self._service.get_semua_stok()
        if not stok:
            print("  Gudang kosong.")
        else:
            print(f"  {'BAHAN BAKU':<40} {'JUMLAH':>10}")
            garis("-")
            for key, data in stok.items():
                print(f"  {data['nama_asli']:<40} {data['jumlah']:>8.1f} {data['satuan']}")
        pause()

    def _update_stok(self):
        clear_screen()
        header("UPDATE STOK BAHAN BAKU")
        nama = input("  Nama bahan baku: ").strip()
        try:
            jumlah = float(input("  Jumlah: ").strip())
        except ValueError:
            print("  Input tidak valid.")
            pause()
            return
        satuan = input("  Satuan (gram/ml/butir/sdt): ").strip()
        self._service.set_stok_bahan(nama, jumlah, satuan)
        print(f"\n  [OK] Stok '{nama}' diupdate: {jumlah} {satuan}")
        pause()

    def _menu_history(self):
        clear_screen()
        header("HISTORY PRODUKSI")
        history = self._service.get_history()
        if not history:
            print("  Belum ada simulasi produksi yang dijalankan.")
        else:
            print(f"  Total simulasi: {len(history)}x\n")
            print(f"  {'#':<4} {'WAKTU':<17} {'PRODUK':<14} {'PESANAN':>8} {'PRODUKSI':>9} {'PROFIT':>12} {'STOK'}")
            garis("-", 72) 
            for h in history:
                stok_ok = "OK" if h["stok_cukup"] else "KURANG"
                
                pesanan = h.get("jumlah_pcs", 0)
                produksi = h.get("total_pcs_diproduksi", pesanan) if h["stok_cukup"] else 0
                
                print(
                    f"  {h['id']:<4} {h['timestamp'][:16]:<17} " 
                    f"{h['nama_produk']:<14} "
                    f"{pesanan:>4} pcs  "
                    f"{produksi:>4} pcs   "
                    f"Rp {h['profit']:>8,.0f} "
                    f"[{stok_ok}]"
                )
        pause()

    def _menu_laporan(self):
        clear_screen()
        header("LAPORAN REKAPITULASI")
        produk_list = self._service.tampilkan_semua_produk()
        history = self._service.get_history()
        laporan = self._laporan.generate_rekap(produk_list, history)
        print(laporan)
        pause()

    def _menu_hapus_produk(self):
        clear_screen()
        header("HAPUS PRODUK")
        produk_list = self._service.tampilkan_semua_produk()
        if not produk_list:
            print("  Tidak ada produk.")
            pause()
            return
        for p in produk_list:
            print(f"  [{p.kode}] {p.nama}")
        garis("-")
        kode = input("  Kode produk yang dihapus: ").strip()
        konfirmasi = input(f"  Yakin hapus '{kode}'? (y/n): ").strip().lower()
        if konfirmasi == "y":
            sukses, pesan = self._service.hapus_produk(kode)
            print(f"\n  {'[OK]' if sukses else '[GAGAL]'} {pesan}")
        else:
            print("  Dibatalkan.")
        pause()
