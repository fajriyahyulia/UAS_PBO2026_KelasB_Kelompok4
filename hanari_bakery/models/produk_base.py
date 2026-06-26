
# Dikerjakan oleh:
# Nama: Fajriyah Yulia Az Zahra
# NIM: K3525005

"""
produk_base.py
Kelas induk abstrak ProdukRoti. Ini pondasi dari seluruh hierarki inheritance.
SRP: class ini hanya nyimpen DATA produk dan template proses produksi.
OCP: terbuka buat extension (subclass baru), tertutup buat modifikasi.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class BahanBaku:
    """
    Value object sederhana. Nama bahan + jumlah per resep.
    Kenapa dataclass? Karena dia murni nampung data, ga ada logika bisnis.
    """
    nama: str
    jumlah: float
    satuan: str

    def __str__(self):
        return f"{self.nama}: {self.jumlah} {self.satuan}"


class ProdukRoti(ABC):
    """
    Kelas induk abstrak untuk SEMUA produk Hanari Bakery.

    LSP: setiap subclass WAJIB bisa menggantikan ProdukRoti tanpa ada
    perilaku aneh atau exception yang ga diharapkan.
    
    Template Method Pattern diterapin di sini lewat `jalankan_produksi()`.
    """

    def __init__(
        self,
        nama: str,
        kode: str,
        bahan_baku: List[BahanBaku],
        biaya_produksi_per_n: float,
        harga_jual_per_n: float,
        jumlah_per_resep: int
    ):
        self._nama = nama
        self._kode = kode
        self._bahan_baku = bahan_baku
        self._biaya_produksi_per_n = biaya_produksi_per_n
        self._harga_jual_per_n = harga_jual_per_n
        self._jumlah_per_resep = jumlah_per_resep

    # -------------------------------------------------------------------------
    # Properties (enkapsulasi proper, bukan public attribute biasa)
    # -------------------------------------------------------------------------

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def kode(self) -> str:
        return self._kode

    @property
    def bahan_baku(self) -> List[BahanBaku]:
        return self._bahan_baku.copy()  # defensive copy biar ga bisa diubah sembarangan

    @property
    def biaya_produksi_per_n(self) -> float:
        return self._biaya_produksi_per_n

    @property
    def harga_jual_per_n(self) -> float:
        return self._harga_jual_per_n

    @property
    def jumlah_per_resep(self) -> int:
        return self._jumlah_per_resep

    # -------------------------------------------------------------------------
    # Abstract method yang WAJIB diimplementasi subclass
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_jenis(self) -> str:
        """Kembalikan string jenis produk, e.g. 'Roti Manis', 'Croissant'."""
        pass

    @abstractmethod
    def get_proses_produksi(self) -> List[str]:
        """
        Kembalikan list langkah proses produksi yang berlaku untuk produk ini.
        Subclass menentukan sendiri proses mana yang relevan.
        """
        pass

    # -------------------------------------------------------------------------
    # Template Method: urutan produksi sudah ditentukan di sini,
    # tapi detail tiap langkah didelegasikan ke subclass / mixin interface.
    # -------------------------------------------------------------------------

    def jalankan_produksi(self) -> List[Tuple[str, str]]:
        """
        Jalankan semua proses produksi yang relevan secara berurutan.
        Return list of (nama_proses, hasil_deskripsi).
        """
        hasil = []
        proses_list = self.get_proses_produksi()

        for nama_proses in proses_list:
            if nama_proses == "pengadonan" and hasattr(self, "pengadonan"):
                hasil.append(("Pengadonan", self.pengadonan()))
            elif nama_proses == "pengembangan" and hasattr(self, "pengembangan"):
                hasil.append(("Pengembangan", self.pengembangan()))
            elif nama_proses == "pemanggangan" and hasattr(self, "pemanggangan"):
                hasil.append(("Pemanggangan", self.pemanggangan()))
            elif nama_proses == "topping" and hasattr(self, "topping"):
                hasil.append(("Topping", self.topping()))

        return hasil

    # -------------------------------------------------------------------------
    # Concrete methods: logika yang sama buat semua produk
    # -------------------------------------------------------------------------

    def info_singkat(self) -> str:
        return (
            f"[{self._kode}] {self._nama} ({self.get_jenis()}) "
            f"| Harga: Rp {self._harga_jual_per_n:,.0f}/{self._jumlah_per_resep} pcs"
        )

    def info_lengkap(self) -> str:
        bahan_str = "\n  ".join(str(b) for b in self._bahan_baku)
        proses_str = ", ".join(self.get_proses_produksi())
        return (
            f"\n{'='*55}\n"
            f"  {self._nama} [{self._kode}]\n"
            f"{'='*55}\n"
            f"  Jenis         : {self.get_jenis()}\n"
            f"  Bahan Baku    :\n  {bahan_str}\n"
            f"  Per Resep     : {self._jumlah_per_resep} pcs\n"
            f"  Biaya Produksi: Rp {self._biaya_produksi_per_n:,.0f}\n"
            f"  Harga Jual    : Rp {self._harga_jual_per_n:,.0f}\n"
            f"  Proses        : {proses_str}\n"
            f"{'='*55}"
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} kode={self._kode!r}>"
