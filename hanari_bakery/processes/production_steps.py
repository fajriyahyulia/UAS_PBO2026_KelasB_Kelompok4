# Dikerjakan oleh:
# Nama: Riska Nur Rahmawati
# NIM: K3525039

"""
production_steps.py
Implementasi konkret dari tiap interface proses produksi.

Kenapa pakai Mixin pattern? Karena Python support multiple inheritance,
dan ini cara paling bersih buat compose behavior tanpa copy-paste kode.
SRP terjaga: tiap mixin hanya tau satu langkah produksi.
"""

from hanari_bakery.models.interfaces import Mixable, Developable, Bakeable, Toppable


class PengadonanMixin(Mixable):
    """
    Mixin pengadonan dasar. Semua produk pakai ini.
    Overrideable kalau ada produk yang proses adonannya beda banget.
    """
    def pengadonan(self) -> str:
        return (
            f"Mencampur bahan kering (tepung, gula, garam) terlebih dahulu, "
            f"lalu masukkan bahan basah (telur, mentega, susu). "
            f"Uleni hingga adonan {self._nama} elastis dan tidak lengket, sekitar 10-15 menit."
        )


class PengembanganMixin(Developable):
    """
    Hanya untuk roti beragi. Butter cookies tidak perlu ini.
    Ini contoh ISP: produk tanpa ragi tidak 'dipaksa' implement interface ini.
    """
    def pengembangan(self) -> str:
        return (
            f"Diamkan adonan {self._nama} di tempat hangat (suhu 27-30°C) "
            f"selama 45-60 menit hingga mengembang dua kali lipat. "
            f"Tutup dengan kain lembab agar tidak kering."
        )


class PemanggangangMixin(Bakeable):
    """Proses pemanggangan. Semua produk pake ini, tapi suhu bisa beda."""
    def pemanggangan(self) -> str:
        return (
            f"Panaskan oven 180°C. Panggang {self._nama} selama 20-25 menit "
            f"hingga permukaannya kecokelatan sempurna dan matang merata. "
            f"Jangan buka oven di 15 menit pertama!"
        )


class ToppingMixin(Toppable):
    """Khusus produk kering yang perlu topping sebelum atau sesudah dipanggang."""
    def topping(self) -> str:
        return (
            f"Tambahkan topping khas untuk {self._nama}: "
            f"taburkan bahan topping secara merata di atas permukaan. "
            f"Pastikan menempel sebelum dipanggang agar tidak jatuh."
        )


# =============================================================================
# Override khusus per produk jika perilakunya benar-benar berbeda
# =============================================================================

class CroissantPengadonanMixin(Mixable):
    """
    Croissant punya teknik lamination (lipat mentega berkali-kali).
    Ini beda banget dari pengadonan roti biasa, makanya di-override.
    """
    def pengadonan(self) -> str:
        return (
            "Buat adonan detrempe (adonan dasar croissant) dari tepung, ragi, "
            "gula, garam, susu, dan sedikit mentega. Istirahatkan 30 menit. "
            "Lakukan proses lamination: masukkan lembaran mentega dingin (beurrage), "
            "lipat dan giling adonan 3x (single fold) dengan jeda pendinginan 20 menit "
            "tiap gilasan. Total 27 lapisan mentega yang bikin croissant flaky!"
        )


class CroissantPemanggangangMixin(Bakeable):
    """Croissant butuh suhu lebih tinggi dan waktu lebih singkat."""
    def pemanggangan(self) -> str:
        return (
            "Olesi permukaan croissant dengan egg wash (kuning telur + susu). "
            "Panggang di oven 200°C selama 15-18 menit hingga berwarna golden brown "
            "dan terdengar suara hollow saat diketuk bagian bawahnya."
        )


class MuffinToppingMixin(Toppable):
    """Muffin punya topping streusel atau choco chips yang khas."""
    def topping(self) -> str:
        return (
            "Taburkan streusel (campuran tepung, gula, mentega dingin yang diremas-remas) "
            "di atas adonan muffin sebelum dipanggang. "
            "Bisa juga tambahkan choco chips atau blueberry sesuai varian. "
            "Ini yang bikin muffin punya 'cap' renyah di atasnya!"
        )
