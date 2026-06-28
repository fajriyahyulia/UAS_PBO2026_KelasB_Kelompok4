# Dikerjakan oleh:
# Nama: Fajriyah Yulia Az Zahra
# NIM: K3525005

"""
stok_repository.py
Implementasi manajemen stok bahan baku (in-memory).
"""

from typing import Dict, List, Optional
from hanari_bakery.models.interfaces import StokManagerInterface


class InMemoryStokRepository(StokManagerInterface):
    """
    Menyimpan stok bahan baku dalam dictionary.
    Key: nama_bahan (dinormalisasi ke lowercase strip).
    Value: dict dengan 'nama_asli', 'jumlah', 'satuan'.
    """

    def __init__(self):
        self._storage: Dict[str, dict] = {}

    def _normalize(self, nama: str) -> str:
        return nama.lower().strip()

    def set_stok(self, nama_bahan: str, jumlah: float, satuan: str) -> None:
        key = self._normalize(nama_bahan)
        if key in self._storage:
            self._storage[key]["jumlah"] += jumlah
        else:
            self._storage[key] = {
                "nama_asli": nama_bahan,
                "jumlah": jumlah,
                "satuan": satuan,
            }

    def get_stok(self, nama_bahan: str) -> Optional[float]:
        key = self._normalize(nama_bahan)
        entry = self._storage.get(key)
        return entry["jumlah"] if entry else None

    def get_semua_stok(self) -> Dict:
        return self._storage

    def kurangi_stok(self, nama_bahan: str, jumlah: float) -> bool:
        key = self._normalize(nama_bahan)
        if key in self._storage and self._storage[key]["jumlah"] >= jumlah:
            self._storage[key]["jumlah"] -= jumlah
            return True
        return False

    def cek_kecukupan(self, kebutuhan: List) -> Dict:
        semua_cukup = True
        detail = []

        for b in kebutuhan:
            nama = b["nama"]
            butuh = b["jumlah_dibutuhkan"]
            satuan = b["satuan"]

            tersedia = self.get_stok(nama)
            if tersedia is None:
                tersedia = 0.0

            cukup = tersedia >= butuh
            if not cukup:
                semua_cukup = False

            detail.append({
                "nama": nama,
                "dibutuhkan": butuh,
                "tersedia": tersedia,
                "satuan": satuan,
                "status": "CUKUP" if cukup else "KURANG",
            })

        return {
            "cukup": semua_cukup,
            "detail": detail,
        }

    def konsumsi_stok(self, kebutuhan: List) -> bool:
        """Helper jembatan agar service baru bisa memotong stok bahan baku"""
        for b in kebutuhan:
            self.kurangi_stok(b["nama"], b["jumlah_dibutuhkan"])
        return True


def seed_stok_default(stok: InMemoryStokRepository) -> None:
    """
    Isi stok awal yang cukup untuk beberapa resep tiap produk.
    Dipanggil dari main.py saat startup.
    """
    stok_awal = [
        # Tepung
        ("Tepung terigu protein tinggi", 5000, "gram"),
        ("Tepung terigu protein rendah", 2000, "gram"),
        ("Tepung terigu serbaguna", 2000, "gram"),
        ("Tepung (streusel)", 500, "gram"),
        # Ragi & pengembang
        ("Ragi instan", 100, "gram"),
        ("Baking powder", 100, "gram"),
        # Gula
        ("Gula pasir", 2000, "gram"),
        ("Gula halus", 500, "gram"),
        ("Gula (streusel)", 300, "gram"),
        # Lemak
        ("Mentega tawar", 2000, "gram"),
        ("Mentega tawar (beurrage)", 1000, "gram"),
        ("Mentega dingin (streusel)", 300, "gram"),
        ("Minyak sayur", 500, "ml"),
        # Telur & susu
        ("Susu cair", 3000, "ml"),
        ("Susu cair dingin", 2000, "ml"),
        ("Telur", 50, "butir"),
        ("Kuning telur", 20, "butir"),
        # Topping & Isian
        ("Chocolate chips", 1000, "gram"),
        ("Garam", 200, "gram"),
        ("Ekstrak vanila", 100, "ml"),
    ]
    for nama, jml, sat in stok_awal:
        stok.set_stok(nama, jml, sat)