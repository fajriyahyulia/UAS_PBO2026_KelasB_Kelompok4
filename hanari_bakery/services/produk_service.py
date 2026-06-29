"""
produk_service.py
Layer service: tempat logika bisnis tinggal.
Dibuat oleh: Wijang Pratama Putra
NIM : K3525043
"""

import math
from typing import List, Dict, Optional, Tuple, Type
from hanari_bakery.models.interfaces import (
    ProductRepositoryInterface, ProfitCalculatorInterface,
    StokManagerInterface, HistoryRepositoryInterface
)
from hanari_bakery.models.produk_base import ProdukRoti, BahanBaku
from hanari_bakery.models.produk_konkret import ProdukCustom


# FIX: helper WAJIB di atas class, bukan di bawah
def profit_colored(nilai: float) -> str:
    """Format rupiah positif atau negatif."""
    if nilai < 0:
        return f"-Rp {abs(nilai):,.0f}"
    return f"Rp {nilai:,.0f}"


class ProfitCalculator(ProfitCalculatorInterface):
    def hitung_profit(self, product: ProdukRoti, jumlah_pcs: int) -> Dict:
        resep = product.jumlah_per_resep
        jumlah_resep = math.ceil(jumlah_pcs / resep)
        total_pcs_diproduksi = jumlah_resep * resep

        total_biaya = jumlah_resep * product.biaya_produksi_per_n
        pendapatan_maksimal = jumlah_resep * product.harga_jual_per_n
        profit_maksimal = pendapatan_maksimal - total_biaya
        margin_maksimal = (profit_maksimal / pendapatan_maksimal * 100) if pendapatan_maksimal > 0 else 0

        harga_per_pcs = product.harga_jual_per_n / resep
        pendapatan_permintaan = jumlah_pcs * harga_per_pcs
        profit_permintaan = pendapatan_permintaan - total_biaya

        sisa_pcs = total_pcs_diproduksi - jumlah_pcs
        potensi_kerugian_sisa = sisa_pcs * (product.biaya_produksi_per_n / resep)

        return {
            "produk": product.nama,
            "kode": product.kode,
            "jumlah_pcs_diminta": jumlah_pcs,
            "jumlah_resep": jumlah_resep,
            "total_pcs_diproduksi": total_pcs_diproduksi,
            "total_biaya": total_biaya,
            "total_pendapatan": pendapatan_maksimal,
            "total_profit": profit_maksimal,
            "margin_profit": margin_maksimal,
            "profit_per_pcs": profit_maksimal / total_pcs_diproduksi if total_pcs_diproduksi > 0 else 0,
            "pendapatan_riil": pendapatan_permintaan,
            "profit_riil": profit_colored(profit_permintaan),  # FIX: fungsi sudah di atas
            "angka_profit_riil": profit_permintaan,
            "sisa_pcs": sisa_pcs,
            "potensi_rugi_sisa": potensi_kerugian_sisa,
            "estimasi_waktu_menit": product.total_waktu_produksi() * jumlah_resep,
        }


class ProductService:
    """
    Service utama. OCP: registry disuntikkan dari luar. DIP: semua dependensi lewat constructor.
    """
    def __init__(
        self,
        repository: ProductRepositoryInterface,
        calculator: ProfitCalculatorInterface,
        stok_manager: StokManagerInterface,
        history_repo: HistoryRepositoryInterface,
        product_registry: Dict[str, Type[ProdukRoti]] = None
    ):
        self._repo = repository
        self._calc = calculator
        self._stok = stok_manager
        self._history = history_repo
        self._product_registry = product_registry or {}

    def tambah_produk(self, kode: str) -> Tuple[bool, str]:
        kode = kode.upper()
        if self._repo.exists(kode):
            return False, f"Produk dengan kode {kode} sudah ada di sistem."
        if kode not in self._product_registry:
            tersedia = ", ".join(self._product_registry.keys())
            return False, f"Kode '{kode}' tidak dikenali. Pilihan tersedia: {tersedia}"
        produk = self._product_registry[kode]()
        self._repo.save(produk)
        return True, f"Produk '{produk.nama}' berhasil ditambahkan ke katalog!"

    # FIX: parameter nama cocok dengan panggilan dari menu.py
    def tambah_produk_custom(
        self,
        nama: str,
        kode: str,
        jenis: str,
        bahan_baku: list,
        biaya: float,
        harga: float,
        jumlah_per_resep: int,
        proses: list,
    ) -> Tuple[bool, str]:
        kode = kode.upper()
        if self._repo.exists(kode):
            return False, f"Kode '{kode}' sudah dipakai produk lain."
        produk = ProdukCustom(
            nama=nama, kode=kode, jenis=jenis,
            bahan_baku=bahan_baku, biaya_produksi_per_n=biaya,
            harga_jual_per_n=harga, jumlah_per_resep=jumlah_per_resep,
            proses_produksi=proses,
        )
        self._repo.save(produk)
        return True, f"Produk variasi baru '{nama}' berhasil didaftarkan!"

    def tampilkan_semua_produk(self) -> List[ProdukRoti]:
        return self._repo.find_all()

    def hapus_produk(self, kode: str) -> Tuple[bool, str]:
        kode = kode.upper()
        produk = self._repo.find_by_code(kode)
        if not produk:
            return False, f"Produk dengan kode '{kode}' tidak ditemukan."
        self._repo.delete(kode)
        return True, f"Produk '{produk.nama}' berhasil dihapus."

    def simulasi_produksi(self, kode: str, jumlah_pcs: int = 0) -> Optional[Dict]:
        produk = self._repo.find_by_code(kode)
        if not produk:
            return None

        resep_pack = produk.jumlah_per_resep
        jumlah_resep = max(1, math.ceil(jumlah_pcs / resep_pack)) if jumlah_pcs > 0 else 1

        kebutuhan = produk.kebutuhan_bahan_untuk(jumlah_resep)
        cek_stok = self._stok.cek_kecukupan(kebutuhan)

        profit_info = None
        if cek_stok["cukup"]:
            self._stok.konsumsi_stok(kebutuhan)
            if jumlah_pcs > 0:
                profit_info = self._calc.hitung_profit(produk, jumlah_pcs)

        pcs_diproduksi_riil = profit_info["total_pcs_diproduksi"] if profit_info else (jumlah_resep * resep_pack if cek_stok["cukup"] else 0)
        profit_maks_riil = profit_info["total_profit"] if profit_info else 0
        profit_permintaan_riil = profit_info["angka_profit_riil"] if profit_info else 0

        self._history.simpan({
            "kode_produk": produk.kode,
            "nama_produk": produk.nama,
            "jumlah_pcs": jumlah_pcs if jumlah_pcs > 0 else resep_pack,
            "total_pcs_diproduksi": pcs_diproduksi_riil,
            "jumlah_resep": jumlah_resep,
            "stok_cukup": cek_stok["cukup"],
            "profit": profit_maks_riil,
            "angka_profit_riil": profit_permintaan_riil,
        })

        return {
            "produk": produk,
            "langkah": produk.jalankan_produksi(),
            "jumlah_resep": jumlah_resep,
            "cek_stok": cek_stok,
            "profit_info": profit_info,
            "total_waktu": produk.total_waktu_produksi() * jumlah_resep,
        }

    def get_semua_stok(self) -> Dict:
        return self._stok.get_semua_stok()

    def set_stok_bahan(self, nama: str, jumlah: float, satuan: str) -> None:
        self._stok.set_stok(nama, jumlah, satuan)

    def get_history(self) -> List[Dict]:
        return self._history.get_semua()

    def get_produk_tersedia(self) -> Dict[str, str]:
        return {k: v().nama for k, v in self._product_registry.items()}

    def estimasi_profit(self, kode: str, jumlah_pcs: int) -> Optional[Dict]:
        produk = self._repo.find_by_code(kode)
        if not produk:
            return None
        data_hasil = self._calc.hitung_profit(produk, jumlah_pcs)
        resep = produk.jumlah_per_resep
        harga_per_pcs = produk.harga_jual_per_n / resep
        total_biaya = data_hasil["total_biaya"]
        total_pcs_butuh_bep = math.ceil(total_biaya / harga_per_pcs) if harga_per_pcs > 0 else 0
        data_hasil["pcs_tambahan_lagi"] = max(0, total_pcs_butuh_bep - jumlah_pcs)
        return data_hasil
