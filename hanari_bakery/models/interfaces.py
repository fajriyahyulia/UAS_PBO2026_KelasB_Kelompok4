# Dikerjakan oleh:
# Nama: Fajriyah Yulia Az Zahra
# NIM: K3525005

from abc import ABC, abstractmethod
from typing import List, Dict


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


# =============================================================================
# SERVICE INTERFACE (DIP)
# =============================================================================

class ProfitCalculatorInterface(ABC):
    """Interface untuk kalkulator profit. Bisa swap implementasinya kapan aja."""

    @abstractmethod
    def hitung_profit(self, product, jumlah_pcs: int) -> Dict:
        pass
