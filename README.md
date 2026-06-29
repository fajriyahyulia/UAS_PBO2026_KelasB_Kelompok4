# Sistem Informasi Produksi dan Manajemen Produk Hanari Bakery

Proyek UAS mata kuliah Pemrograman Berorientasi Objek (PBO) 2026 — Kelas B, Kelompok 4.

---

## Identitas Kelompok

| NIM       | Nama                        | Username GitHub        | Tugas                                                  |
|-----------|-----------------------------|------------------------|--------------------------------------------------------|
| K3525005  | Fajriyah Yulia Az Zahra     | fajriyahyulia          | main.py, interfaces.py, produk_base.py, stok_repository.py |
| K3525006  | Fatimah Az Zahra            | fatimahzahrara         | produk_konkret.py                                      |
| K3525039  | Riska Nur Rahmawati         | riskarahmaa11          | production_steps.py                                    |
| K3525042  | Vincensius Vicko Riska S.   | pikoopikk              | produk_repository.py, history_repository.py            |
| K3525043  | Wijang Pratama Putra        | pratamaputra-pemula    | produk_service.py, laporan_service.py                  |
| K3525045  | Abid Satriyo Maulana        | maurinho011            | menu.py                                                |

---

## Deskripsi Proyek

Sistem ini merupakan aplikasi berbasis terminal (CLI) untuk mengelola proses produksi, stok bahan baku, estimasi profit, dan pelaporan operasional toko roti Hanari Bakery. Program dibangun menggunakan Python dengan penerapan penuh prinsip SOLID dan paradigma Object-Oriented Programming.

---

## Struktur Direktori

```
hanari_bakery/
├── main.py
├── models/
│   ├── interfaces.py
│   ├── produk_base.py
│   └── produk_konkret.py
├── processes/
│   └── production_steps.py
├── repositories/
│   ├── produk_repository.py
│   ├── stok_repository.py
│   └── history_repository.py
├── services/
│   ├── produk_service.py
│   └── laporan_service.py
└── ui/
    └── menu.py
```

---

## Cara Menjalankan Program

**Prasyarat:** Python 3.10 atau lebih baru.

```bash
# Clone repository
git clone https://github.com/fajriyahyulia/UAS_PBO2026_KelasB_Kelompok4
cd UAS_PBO2026_KelasB_Kelompok4

# Jalankan program
python main.py
```

Tidak ada dependensi eksternal. Program hanya menggunakan modul standar Python (`abc`, `math`, `dataclasses`, `datetime`, `os`).

---

## Fitur Menu

| Menu | Fitur |
|------|-------|
| `[1]` | Tambah produk baru — pilih dari produk default atau buat produk custom |
| `[2]` | Tampilkan seluruh produk yang terdaftar di katalog |
| `[3]` | Kalkulator estimasi profit — analisis dua kondisi (ideal vs riil) beserta status BEP |
| `[4]` | Simulasi proses produksi — cek stok, potong stok, cetak langkah dapur |
| `[5]` | Manajemen stok bahan baku — lihat stok gudang dan tambah stok |
| `[6]` | History produksi — log seluruh simulasi yang pernah dijalankan |
| `[7]` | Laporan rekapitulasi — agregasi kinerja pabrik, total profit riil, analisis sisa etalase |
| `[8]` | Hapus produk dari katalog |
| `[0]` | Keluar dari program |

---

## Arsitektur dan Prinsip SOLID

### Hierarki Kelas

```
ProdukRoti (abstract)
├── RotiManis       + PengadonanMixin, PengembanganMixin, PemanggangangMixin
├── Croissant       + CroissantPengadonanMixin, PengembanganMixin, CroissantPemanggangangMixin
├── KueKering (abstract intermediate)
│   ├── ButterCookies  + PengadonanMixin, PemanggangangMixin, ToppingMixin
│   └── Muffin         + PengadonanMixin, PengembanganMixin, PemanggangangMixin, MuffinToppingMixin
└── ProdukCustom    (dibuat secara dinamis dari input pengguna)
```

### Penerapan Prinsip SOLID

**SRP — Single Responsibility Principle**
Setiap kelas memiliki tepat satu tanggung jawab. `MenuUtama` hanya menangani tampilan dan interaksi pengguna. `ProductService` hanya mengelola logika bisnis. `ProfitCalculator` hanya menghitung profit. `LaporanGenerator` hanya membuat laporan. Masing-masing repository hanya bertanggung jawab atas satu jenis penyimpanan data.

**OCP — Open/Closed Principle**
Sistem terbuka untuk penambahan produk baru tanpa mengubah kode yang sudah ada. Produk default baru cukup didaftarkan ke `default_registry` di `main.py`. Produk custom dapat dibuat langsung dari terminal melalui fitur `ProdukCustom` tanpa menyentuh kode apapun.

**LSP — Liskov Substitution Principle**
Seluruh subclass dapat menggantikan `ProdukRoti` tanpa mengubah perilaku program. Fungsi simulasi produksi, kalkulator profit, dan laporan rekapitulasi bekerja secara polimorfik untuk semua jenis produk termasuk `ProdukCustom`.

**ISP — Interface Segregation Principle**
Interface dipecah menjadi unit kecil sesuai kebutuhan masing-masing produk. `ButterCookies` tidak dipaksa mengimplementasikan `Developable` karena tidak membutuhkan proses pengembangan ragi. Hal ini terbukti secara teknis: `isinstance(ButterCookies(), Developable)` menghasilkan `False`.

**DIP — Dependency Inversion Principle**
`ProductService` bergantung pada abstraksi `ProductRepositoryInterface`, `ProfitCalculatorInterface`, `StokManagerInterface`, dan `HistoryRepositoryInterface`, bukan pada implementasi konkret. Seluruh dependensi dirakit dan disuntikkan dari `main.py` sebagai Composition Root (Dependency Injection).

---

## Interface yang Digunakan

**Interface Proses Produksi (ISP)**

| Interface     | Abstract Method    | Diimplementasikan Oleh                                  |
|---------------|--------------------|---------------------------------------------------------|
| `Mixable`     | `pengadonan()`     | `PengadonanMixin`, `CroissantPengadonanMixin`           |
| `Developable` | `pengembangan()`   | `PengembanganMixin`                                     |
| `Bakeable`    | `pemanggangan()`   | `PemanggangangMixin`, `CroissantPemanggangangMixin`     |
| `Toppable`    | `topping()`        | `ToppingMixin`, `MuffinToppingMixin`                    |

**Interface Layer Data dan Service (DIP)**

| Interface                      | Diimplementasikan Oleh            |
|--------------------------------|-----------------------------------|
| `ProductRepositoryInterface`   | `InMemoryProductRepository`       |
| `StokManagerInterface`         | `InMemoryStokRepository`          |
| `HistoryRepositoryInterface`   | `InMemoryHistoryRepository`       |
| `ProfitCalculatorInterface`    | `ProfitCalculator`                |
| `LaporanGeneratorInterface`    | `LaporanGenerator`                |

---

## Data Default Sistem

**Produk Default (seed saat startup)**

| Kode    | Nama            | Resep    | Biaya/Resep | Harga/Resep | Waktu    |
|---------|-----------------|----------|-------------|-------------|----------|
| RM-001  | Roti Manis      | 12 pcs   | Rp 35.000   | Rp 65.000   | ~100 mnt |
| CR-001  | Croissant       | 8 pcs    | Rp 42.000   | Rp 85.000   | ~110 mnt |
| BC-001  | Butter Cookies  | 24 pcs   | Rp 28.000   | Rp 55.000   | ~50 mnt  |
| MF-001  | Muffin          | 12 pcs   | Rp 32.000   | Rp 60.000   | ~110 mnt |

**Stok Awal Bahan Baku (seed saat startup)**

| Bahan Baku                    | Jumlah  | Satuan |
|-------------------------------|---------|--------|
| Tepung terigu protein tinggi  | 5.000   | gram   |
| Tepung terigu protein rendah  | 2.000   | gram   |
| Tepung terigu serbaguna       | 2.000   | gram   |
| Ragi instan                   | 100     | gram   |
| Baking powder                 | 100     | gram   |
| Gula pasir                    | 2.000   | gram   |
| Mentega tawar                 | 2.000   | gram   |
| Susu cair                     | 3.000   | ml     |
| Telur                         | 50      | butir  |
| Minyak sayur                  | 500     | ml     |
| (dan bahan lainnya...)        |         |        |

---

## Logika Kalkulasi Profit

Program membedakan dua kondisi profit secara bersamaan dalam satu kalkulasi:

```
jumlah_resep       = ceil(jumlah_pcs_diminta / pcs_per_resep)
total_pcs_produksi = jumlah_resep × pcs_per_resep
total_biaya        = jumlah_resep × biaya_produksi_per_n

# Kondisi A — Semua hasil produksi habis terjual
pendapatan_maks    = jumlah_resep × harga_jual_per_n
profit_maks        = pendapatan_maks - total_biaya

# Kondisi B — Hanya terjual sesuai permintaan
harga_per_pcs      = harga_jual_per_n / pcs_per_resep
pendapatan_riil    = jumlah_pcs_diminta × harga_per_pcs
profit_riil        = pendapatan_riil - total_biaya

# Status
RUGI      → profit_riil < 0
BEP       → profit_riil == 0
UNTUNG    → profit_riil > 0
```

---

## Keterbatasan Sistem

- Data bersifat in-memory dan tidak persisten. Seluruh data produk custom dan history produksi akan hilang ketika program ditutup.
- Belum ada fitur autentikasi pengguna.
- Validasi input masih bersifat dasar.

---

## Rencana Pengembangan

- Migrasi penyimpanan ke database relasional (SQLite atau PostgreSQL) dengan mengganti implementasi repository tanpa mengubah kode service.
- Penambahan sistem hak akses berbasis role (Chef, Staff Gudang, Owner/Manajer).
- Fitur ekspor laporan ke format PDF atau Excel.
- Pengembangan antarmuka dari terminal menjadi aplikasi GUI atau web.
- Notifikasi otomatis ketika stok bahan baku mendekati batas minimum.

---

## Diagram

- **Class Diagram:** tersedia di folder `docs/` atau melalui tautan Google Drive di dokumen LKPD.
- **Flowchart Sistem:** tersedia di folder `docs/` atau melalui tautan Google Drive di dokumen LKPD.

---

## Referensi

- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.
- Python Software Foundation. (2024). *Python 3 Documentation — abc module*. https://docs.python.org/3/library/abc.html
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
