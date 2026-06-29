# Dikerjakan Oleh:
# Nama: Vincensius Vicko Riska S
# NIM: K3525042

"""
history_repository.py
Implementasi penyimpanan history simulasi produksi (in-memory).

DIP: implement HistoryRepositoryInterface.
SRP: hanya urusan simpan & ambil data history, tidak ada logika bisnis.

Setiap record diberi ID autoincrement dan timestamp otomatis.
"""

from typing import List, Dict
from datetime import datetime
from hanari_bakery.models.interfaces import HistoryRepositoryInterface


class InMemoryHistoryRepository(HistoryRepositoryInterface):
    """
    Menyimpan history simulasi produksi dalam list.
    Setiap record mendapat ID unik (autoincrement) dan timestamp saat disimpan.
    """

    def __init__(self):
        self._records: List[Dict] = []
        self._counter: int = 0

    def simpan(self, record: Dict) -> None:
        self._counter += 1
        enriched = {
            "id": self._counter,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            **record,
        }
        self._records.append(enriched)

    def get_semua(self) -> List[Dict]:
        return list(self._records)

    def get_by_produk(self, kode: str) -> List[Dict]:
        return [r for r in self._records if r.get("kode_produk") == kode.upper()]
