# Dikerjakan oleh:
# Nama: Vincensius Vicko Riska S
# NIM: K3525042

"""
produk_repository.py
Implementasi konkret penyimpanan produk (in-memory).
"""

from typing import List, Optional, Dict, Type
from hanari_bakery.models.interfaces import ProductRepositoryInterface
from hanari_bakery.models.produk_base import ProdukRoti


class InMemoryProductRepository(ProductRepositoryInterface):
    """
    Menyimpan produk di dictionary dalam memori.
    Key: kode produk (string), Value: instance ProdukRoti.
    """

    def __init__(self):
        self._storage: dict[str, ProdukRoti] = {}

    def save(self, product: ProdukRoti) -> None:
        self._storage[product.kode] = product

    def find_by_code(self, code: str) -> Optional[ProdukRoti]:
        return self._storage.get(code.upper())

    def find_all(self) -> List[ProdukRoti]:
        return list(self._storage.values())

    def delete(self, code: str) -> bool:
        code = code.upper()
        if code in self._storage:
            del self._storage[code]
            return True
        return False

    def exists(self, code: str) -> bool:
        return code.upper() in self._storage


def seed_default_products(repo: ProductRepositoryInterface, registry: Dict[str, Type[ProdukRoti]]) -> None:
    """
    KINI 100% DIP: Mengisi katalog awal secara dinamis menggunakan registry yang disuntikkan.
    """
    for class_produk in registry.values():
        repo.save(class_produk())
