# Dikerjakan oleh
# Nama: Fatimah Az Zahra
# NIM : K3525006

"""
produk_konkret.py
Implementasi konkret semua produk Hanari Bakery.

Pola inheritance di sini:
  ProdukRoti (abstract base)
    ├── RotiManis   (+ PengadonanMixin, PengembanganMixin, PemanggangangMixin)
    ├── Croissant   (+ CroissantPengadonanMixin, PengembanganMixin, CroissantPemanggangangMixin)
    └── KueKering   (abstract intermediate)
          ├── ButterCookies (+ PengadonanMixin, PemanggangangMixin, ToppingMixin)
          └── Muffin        (+ PengadonanMixin, PengembanganMixin, PemanggangangMixin, MuffinToppingMixin)

LSP: semua subclass bisa dipake sebagai ProdukRoti tanpa masalah.
"""

from typing import List
from hanari_bakery.models.produk_base import ProdukRoti, BahanBaku
from hanari_bakery.processes.production_steps import (
    PengadonanMixin, PengembanganMixin, PemanggangangMixin, ToppingMixin,
    CroissantPengadonanMixin, CroissantPemanggangangMixin, MuffinToppingMixin
)


# =============================================================================
# ROTI MANIS
# =============================================================================

class RotiManis(PengadonanMixin, PengembanganMixin, PemanggangangMixin, ProdukRoti):
    """
    Roti manis klasik Hanari Bakery. Proses: adonan > kembang > panggang.
    Tidak ada topping (jika ada varian topping, buat subclass baru).
    """

    def __init__(self):
        bahan = [
            BahanBaku("Tepung terigu protein tinggi", 500, "gram"),
            BahanBaku("Ragi instan", 11, "gram"),
            BahanBaku("Gula pasir", 100, "gram"),
            BahanBaku("Garam", 8, "gram"),
            BahanBaku("Telur", 2, "butir"),
            BahanBaku("Susu cair", 200, "ml"),
            BahanBaku("Mentega tawar", 75, "gram"),
        ]
        super().__init__(
            nama="Roti Manis",
            kode="RM-001",
            bahan_baku=bahan,
            biaya_produksi_per_n=35_000,
            harga_jual_per_n=65_000,
            jumlah_per_resep=12
        )

    def get_jenis(self) -> str:
        return "Roti Manis"

    def get_proses_produksi(self) -> List[str]:
        return ["pengadonan", "pengembangan", "pemanggangan"]


# =============================================================================
# CROISSANT
# =============================================================================

class Croissant(CroissantPengadonanMixin, PengembanganMixin, CroissantPemanggangangMixin, ProdukRoti):
    """
    Croissant Prancis autentik dengan teknik lamination.
    Override pengadonan dan pemanggangan karena prosesnya beda banget dari roti biasa.
    """

    def __init__(self):
        bahan = [
            BahanBaku("Tepung terigu protein tinggi", 500, "gram"),
            BahanBaku("Ragi instan", 10, "gram"),
            BahanBaku("Gula pasir", 55, "gram"),
            BahanBaku("Garam", 10, "gram"),
            BahanBaku("Susu cair", 300, "ml"),
            BahanBaku("Mentega tawar (beurrage)", 250, "gram"),
            BahanBaku("Kuning telur (egg wash)", 1, "butir"),
        ]
        super().__init__(
            nama="Croissant",
            kode="CR-001",
            bahan_baku=bahan,
            biaya_produksi_per_n=42_000,
            harga_jual_per_n=85_000,
            jumlah_per_resep=8
        )

    def get_jenis(self) -> str:
        return "Croissant"

    def get_proses_produksi(self) -> List[str]:
        return ["pengadonan", "pengembangan", "pemanggangan"]


# =============================================================================
# KUE KERING (abstract intermediate) - Level tambahan inheritance
# =============================================================================

class KueKering(ProdukRoti):
    """
    Intermediate abstract class untuk kategori kue kering.
    Kalau ada atribut/method yang sama buat semua kue kering, taruh di sini.
    Ini contoh hierarki inheritance yang lebih dari 2 level.
    """

    def get_jenis(self) -> str:
        return f"Kue Kering - {self.get_subtipe()}"

    @property
    def is_kue_kering(self) -> bool:
        return True

    def get_subtipe(self) -> str:
        raise NotImplementedError("Subclass KueKering harus override get_subtipe()")


# =============================================================================
# BUTTER COOKIES
# =============================================================================

class ButterCookies(PengadonanMixin, PemanggangangMixin, ToppingMixin, KueKering):
    """
    Butter cookies klasik. TIDAK ada proses pengembangan (bukan adonan beragi).
    Ada proses topping karena itu yang bikin cookies-nya istimewa.

    Ini bukti ISP berhasil: ButterCookies tidak implement Developable
    karena memang dia tidak butuh proses pengembangan ragi.
    """

    def __init__(self):
        bahan = [
            BahanBaku("Tepung terigu protein rendah", 250, "gram"),
            BahanBaku("Mentega tawar", 200, "gram"),
            BahanBaku("Gula halus", 100, "gram"),
            BahanBaku("Kuning telur", 2, "butir"),
            BahanBaku("Vanili ekstrak", 1, "sdt"),
            BahanBaku("Garam", 2, "gram"),
            BahanBaku("Susu bubuk", 30, "gram"),
        ]
        super().__init__(
            nama="Butter Cookies",
            kode="BC-001",
            bahan_baku=bahan,
            biaya_produksi_per_n=28_000,
            harga_jual_per_n=55_000,
            jumlah_per_resep=24
        )

    def get_subtipe(self) -> str:
        return "Butter Cookies"

    def get_proses_produksi(self) -> List[str]:
        return ["pengadonan", "topping", "pemanggangan"]

    def pengadonan(self) -> str:
        return (
            "Kocok mentega dan gula halus hingga pucat dan fluffy (creaming method). "
            "Masukkan kuning telur dan vanili, kocok rata. "
            "Ayak tepung dan susu bubuk, masukkan bertahap sambil aduk dengan spatula "
            "hingga adonan bisa dibentuk. Jangan over-mix atau cookies jadi keras!"
        )

    def topping(self) -> str:
        return (
            "Masukkan adonan ke dalam piping bag dengan spuit bintang. "
            "Semprotkan adonan di atas loyang yang sudah dialasi baking paper "
            "dengan jarak 2cm antar cookies. Bisa tambahkan choco chip, "
            "almond slice, atau cherry di tengahnya sesuai selera."
        )

    def pemanggangan(self) -> str:
        return (
            "Panaskan oven 160°C (api bawah). Panggang butter cookies selama "
            "18-22 menit hingga tepi bawah mulai kecokelatan tapi bagian atas "
            "masih pucat. Jangan tunggu cokelat semua, dia akan set saat dingin!"
        )


# =============================================================================
# MUFFIN
# =============================================================================

class Muffin(PengadonanMixin, PengembanganMixin, PemanggangangMixin, MuffinToppingMixin, KueKering):
    """
    Muffin termasuk kategori kue kering tapi punya pengembangan (baking powder/soda),
    juga ada proses topping streusel yang khas.
    """

    def __init__(self):
        bahan = [
            BahanBaku("Tepung terigu serbaguna", 240, "gram"),
            BahanBaku("Gula pasir", 150, "gram"),
            BahanBaku("Baking powder", 10, "gram"),
            BahanBaku("Garam", 3, "gram"),
            BahanBaku("Telur", 2, "butir"),
            BahanBaku("Susu cair", 240, "ml"),
            BahanBaku("Minyak sayur", 80, "ml"),
            BahanBaku("Vanili ekstrak", 1, "sdt"),
            # Topping streusel
            BahanBaku("Tepung (streusel)", 60, "gram"),
            BahanBaku("Gula (streusel)", 50, "gram"),
            BahanBaku("Mentega dingin (streusel)", 45, "gram"),
        ]
        super().__init__(
            nama="Muffin",
            kode="MF-001",
            bahan_baku=bahan,
            biaya_produksi_per_n=32_000,
            harga_jual_per_n=60_000,
            jumlah_per_resep=12
        )

    def get_subtipe(self) -> str:
        return "Muffin"

    def get_proses_produksi(self) -> List[str]:
        return ["pengadonan", "pengembangan", "topping", "pemanggangan"]

    def pengadonan(self) -> str:
        return (
            "Campur semua bahan kering (tepung, gula, baking powder, garam) di satu wadah. "
            "Di wadah lain, kocok telur, susu, minyak, dan vanili hingga rata. "
            "Tuang campuran basah ke kering, aduk HANYA sampai rata (adonan boleh sedikit bergerindil). "
            "Jangan over-mix! Itu rahasia muffin yang lembut dan mengembang sempurna."
        )

    def pengembangan(self) -> str:
        return (
            "Istirahatkan adonan muffin 5-10 menit di suhu ruang sambil menyiapkan streusel. "
            "Baking powder akan mulai bereaksi dan membentuk gelembung udara kecil "
            "yang nanti bikin muffin mengembang cantik di oven."
        )

    def pemanggangan(self) -> str:
        return (
            "Panaskan oven 190°C. Isi cup muffin hingga 3/4 penuh "
            "lalu taburi streusel di atasnya. Panggang 20-22 menit. "
            "Test dengan tusuk gigi, kalau keluar bersih berarti matang. "
            "Biarkan di loyang 5 menit sebelum dipindahkan ke cooling rack."
        )


# =============================================================================
# PRODUK CUSTOM (OCP: tambah produk baru tanpa ubah kode lama sama sekali)
# =============================================================================

class ProdukCustom(ProdukRoti):
    """
    Produk fleksibel yang bisa dibuat langsung dari input user di menu.
    Ini bukti OCP paling nyata: sistem terbuka untuk produk baru
    tanpa programmer harus sentuh kode apapun yang sudah ada.

    LSP tetap terjaga: ProdukCustom bisa dipakai di mana saja ProdukRoti dipakai.
    Simulasi produksi, kalkulator profit, laporan, semua jalan normal.
    """

    _DESKRIPSI_DEFAULT = {
        "pengadonan": (
            "Campur semua bahan kering terlebih dahulu, lalu masukkan bahan basah "
            "satu per satu. Aduk dan uleni hingga adonan tercampur rata dan bertekstur "
            "sesuai jenis produk yang dibuat."
        ),
        "pengembangan": (
            "Diamkan adonan di tempat hangat selama 45-60 menit hingga mengembang. "
            "Tutup dengan kain lembab agar permukaan adonan tidak mengering."
        ),
        "pemanggangan": (
            "Panaskan oven sesuai suhu yang dibutuhkan. Panggang hingga matang merata "
            "dan permukaan berwarna kecokelatan. Lakukan tes tusuk gigi untuk memastikan "
            "bagian dalam sudah matang sempurna."
        ),
        "topping": (
            "Tambahkan topping sesuai resep di atas produk sebelum atau sesudah dipanggang. "
            "Pastikan topping menempel merata untuk hasil yang menarik dan konsisten."
        ),
    }

    _DURASI_DEFAULT = {
        "pengadonan": 15,
        "pengembangan": 60,
        "pemanggangan": 25,
        "topping": 10,
    }

    def __init__(
        self,
        nama: str,
        kode: str,
        jenis: str,
        bahan_baku: List[BahanBaku],
        biaya_produksi_per_n: float,
        harga_jual_per_n: float,
        jumlah_per_resep: int,
        proses_produksi: List[str],
        deskripsi_proses: dict = None,
    ):
        super().__init__(
            nama=nama,
            kode=kode,
            bahan_baku=bahan_baku,
            biaya_produksi_per_n=biaya_produksi_per_n,
            harga_jual_per_n=harga_jual_per_n,
            jumlah_per_resep=jumlah_per_resep,
        )
        self._jenis = jenis
        self._proses_produksi = proses_produksi
        self._deskripsi_proses = deskripsi_proses or {}

    def get_jenis(self) -> str:
        return self._jenis

    def get_proses_produksi(self) -> List[str]:
        return self._proses_produksi

    def jalankan_produksi(self):
        hasil = []
        for proses in self._proses_produksi:
            deskripsi = self._deskripsi_proses.get(
                proses, self._DESKRIPSI_DEFAULT.get(proses, f"Proses {proses}.")
            )
            durasi = self._DURASI_DEFAULT.get(proses, 15)
            hasil.append((proses.capitalize(), deskripsi, durasi))
        return hasil