"""
main.py
Entry point dan Composition Root aplikasi Hanari Bakery.
Semua dependensi dirakit di sini, tidak ada yang buat sendiri di dalam class.
"""

from hanari_bakery.repositories.produk_repository import InMemoryProductRepository, seed_default_products
from hanari_bakery.repositories.stok_repository import InMemoryStokRepository, seed_stok_default
from hanari_bakery.repositories.history_repository import InMemoryHistoryRepository
from hanari_bakery.services.produk_service import ProductService, ProfitCalculator
from hanari_bakery.ui.menu import MenuUtama

# Import kelas konkret dilakukan di level paling luar aplikasi (Composition Root)
from hanari_bakery.models.produk_konkret import RotiManis, Croissant, ButterCookies, Muffin


def main():
    # 1. Rakit semua infrastruktur penyimpanan (Repositories)
    repository   = InMemoryProductRepository()
    stok_manager = InMemoryStokRepository()
    history_repo = InMemoryHistoryRepository()
    calculator   = ProfitCalculator()

    # 2. Definisikan peta produk terdaftar toko secara terpusat (Penerapan OCP)
    default_registry = {
        "RM-001": RotiManis,
        "CR-001": Croissant,
        "BC-001": ButterCookies,
        "MF-001": Muffin,
    }

    # 3. Suntikkan semua dependensi termasuk registry produk ke Service Layer (Penerapan DIP)
    service = ProductService(
        repository=repository,
        calculator=calculator,
        stok_manager=stok_manager,
        history_repo=history_repo,
        product_registry=default_registry
    )

    # 4. Lakukan seeding data awal ke memory storage
    seed_default_products(repository, default_registry)
    seed_stok_default(stok_manager)

    # 5. Jalankan Antarmuka Terminal (UI)
    menu = MenuUtama(service=service)
    menu.tampilkan()


if __name__ == "__main__":
    main()