"""
interfaces.py
Kumpulan interface kecil-kecil sesuai ISP (Interface Segregation Principle).
Kalau digabung jadi satu interface raksasa, itu pelanggaran ISP yang klasik banget.
"""

"""
interfaces.py
Kumpulan interface kecil-kecil sesuai ISP (Interface Segregation Principle).
Kalau digabung jadi satu interface raksasa, itu pelanggaran ISP yang klasik banget.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


# =============================================================================
# PRODUCTION PROCESS INTERFACES (ISP: tiap interface punya tanggung jawab sendiri)
# =============================================================================

class Mixable(ABC):
    """Semua produk roti pasti bisa dicampur/diuleni adonan."""
    @abstractmethod
    def pengadonan(self) -> str:
        pass


class Developable(ABC):
    """Hanya roti manis, croissant, muffin yang perlu proses pengembangan ragi."""
    @abstractmethod
    def pengembangan(self) -> str:
        pass


class Bakeable(ABC):
    """Semua produk dipanggang."""
    @abstractmethod
    def pemanggangan(self) -> str:
        pass


class Toppable(ABC):
    """Hanya produk kering (butter cookies, muffin) yang ada topping."""
    @abstractmethod
    def topping(self) -> str:
        pass


# =============================================================================
# REPOSITORY INTERFACE (DIP: depend ke abstraksi)
# =============================================================================

class ProductRepositoryInterface(ABC):
    """Abstraksi layer penyimpanan produk. Implementasinya bisa ganti-ganti."""

    @abstractmethod
    def save(self, product) -> None:
        pass

    @abstractmethod
    def find_by_code(self, code: str):
        pass

    @abstractmethod
    def find_all(self) -> List:
        pass

    @abstractmethod
    def delete(self, code: str) -> bool:
        pass

    @abstractmethod
    def exists(self, code: str) -> bool:
        pass


# =============================================================================
# SERVICE INTERFACE (DIP)
# =============================================================================

class ProfitCalculatorInterface(ABC):
    """Interface untuk kalkulator profit. Bisa swap implementasinya kapan aja."""

    @abstractmethod
    def hitung_profit(self, product, jumlah_pcs: int) -> Dict:
        pass


# =============================================================================
# STOK INTERFACE (ISP: dipisah dari repository produk)
# =============================================================================

class StokManagerInterface(ABC):
    """Abstraksi manajemen stok bahan baku."""

    @abstractmethod
    def set_stok(self, nama_bahan: str, jumlah: float, satuan: str) -> None:
        pass

    @abstractmethod
    def get_stok(self, nama_bahan: str) -> Optional[float]:
        pass

    @abstractmethod
    def get_semua_stok(self) -> Dict:
        pass

    @abstractmethod
    def kurangi_stok(self, nama_bahan: str, jumlah: float) -> bool:
        pass

    @abstractmethod
    def cek_kecukupan(self, kebutuhan: List) -> Dict:
        pass


# =============================================================================
# HISTORY INTERFACE
# =============================================================================

class HistoryRepositoryInterface(ABC):
    """Abstraksi penyimpanan history produksi."""

    @abstractmethod
    def simpan(self, record: Dict) -> None:
        pass

    @abstractmethod
    def get_semua(self) -> List[Dict]:
        pass

    @abstractmethod
    def get_by_produk(self, kode: str) -> List[Dict]:
        pass


# =============================================================================
# LAPORAN INTERFACE
# =============================================================================

class LaporanGeneratorInterface(ABC):
    """Abstraksi generator laporan."""

    @abstractmethod
    def generate_rekap(self, produk_list: List, history: List[Dict]) -> str:
        pass