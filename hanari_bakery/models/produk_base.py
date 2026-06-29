# Dikerjakan oleh:
# Nama: Fajriyah Yulia Az Zahra
# NIM: K3525005

"""
produk_base.py
Kelas induk abstrak ProdukRoti. Fondasi seluruh hierarki inheritance.
SRP: class ini hanya nyimpen DATA produk dan template proses produksi.
OCP: terbuka buat extension (subclass baru), tertutup buat modifikasi.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class BahanBaku:
    nama: str
    jumlah: float
    satuan: str

    def __str__(self):
        return f"{self.nama}: {self.jumlah} {self.satuan}"


class ProdukRoti(ABC):
    """
    Kelas induk abstrak untuk SEMUA produk Hanari Bakery.
    LSP: setiap subclass WAJIB bisa menggantikan ProdukRoti tanpa perilaku aneh.
    Template Method Pattern diterapin lewat jalankan_produksi().
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

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def kode(self) -> str:
        return self._kode

    @property
    def bahan_baku(self) -> List[BahanBaku]:
        return self._bahan_baku.copy()

    @property
    def biaya_produksi_per_n(self) -> float:
        return self._biaya_produksi_per_n

    @property
    def harga_jual_per_n(self) -> float:
        return self._harga_jual_per_n

    @property
    def jumlah_per_resep(self) -> int:
        return self._jumlah_per_resep

    @abstractmethod
    def get_jenis(self) -> str:
        pass

    @abstractmethod
    def get_proses_produksi(self) -> List[str]:
        pass

    def jalankan_produksi(self) -> List[Tuple[str, str, int]]:
        """
        Jalankan semua proses produksi secara berurutan.
        Return list of (nama_proses, deskripsi, durasi_menit).
        """
        hasil = []
        for nama_proses in self.get_proses_produksi():
            if nama_proses == "pengadonan" and hasattr(self, "pengadonan"):
                durasi = getattr(self, "durasi_pengadonan", lambda: 15)()
                hasil.append(("Pengadonan", self.pengadonan(), durasi))
            elif nama_proses == "pengembangan" and hasattr(self, "pengembangan"):
                durasi = getattr(self, "durasi_pengembangan", lambda: 60)()
                hasil.append(("Pengembangan", self.pengembangan(), durasi))
            elif nama_proses == "pemanggangan" and hasattr(self, "pemanggangan"):
                durasi = getattr(self, "durasi_pemanggangan", lambda: 25)()
                hasil.append(("Pemanggangan", self.pemanggangan(), durasi))
            elif nama_proses == "topping" and hasattr(self, "topping"):
                durasi = getattr(self, "durasi_topping", lambda: 10)()
                hasil.append(("Topping", self.topping(), durasi))
        return hasil

    def total_waktu_produksi(self) -> int:
        """Total estimasi waktu produksi dalam menit."""
        return sum(d for _, _, d in self.jalankan_produksi())

    def kebutuhan_bahan_untuk(self, jumlah_resep: int) -> List[Dict]:
        """Hitung kebutuhan total bahan baku untuk sejumlah resep."""
        return [
            {
                "nama": b.nama,
                "jumlah_dibutuhkan": b.jumlah * jumlah_resep,
                "satuan": b.satuan
            }
            for b in self._bahan_baku
        ]

    def info_singkat(self) -> str:
        waktu = self.total_waktu_produksi()
        return (
            f"[{self._kode}] {self._nama} ({self.get_jenis()}) "
            f"| Harga: Rp {self._harga_jual_per_n:,.0f}/{self._jumlah_per_resep} pcs"
            f" | Waktu: ~{waktu} menit/resep"
        )

    def info_lengkap(self) -> str:
        bahan_str = "\n  ".join(str(b) for b in self._bahan_baku)
        proses_str = ", ".join(self.get_proses_produksi())
        waktu = self.total_waktu_produksi()
        return (
            f"\n{'='*58}\n"
            f"  {self._nama} [{self._kode}]\n"
            f"{'='*58}\n"
            f"  Jenis           : {self.get_jenis()}\n"
            f"  Bahan Baku      :\n  {bahan_str}\n"
            f"  Per Resep       : {self._jumlah_per_resep} pcs\n"
            f"  Biaya Produksi  : Rp {self._biaya_produksi_per_n:,.0f}/resep\n"
            f"  Harga Jual      : Rp {self._harga_jual_per_n:,.0f}/resep\n"
            f"  Proses          : {proses_str}\n"
            f"  Est. Waktu      : ~{waktu} menit/resep\n"
            f"{'='*58}"
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} kode={self._kode!r}>"
