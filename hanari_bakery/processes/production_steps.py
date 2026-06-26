# Dikerjakan oleh:
# Nama: Riska Nur Rahmawati
# NIM: K3525039

"""
production_steps.py
Implementasi konkret dari tiap interface proses produksi.
Setiap proses kini punya DURASI WAKTU yang bisa diakumulasi untuk estimasi total waktu produksi.
"""

from hanari_bakery.models.interfaces import Mixable, Developable, Bakeable, Toppable


class PengadonanMixin(Mixable):
    DURASI_PENGADONAN = 15  # menit

    def pengadonan(self) -> str:
        return (
            f"Mencampur bahan kering (tepung, gula, garam) terlebih dahulu, "
            f"lalu masukkan bahan basah (telur, mentega, susu). "
            f"Uleni hingga adonan {self._nama} elastis dan tidak lengket, sekitar 10-15 menit."
        )

    def durasi_pengadonan(self) -> int:
        return self.DURASI_PENGADONAN


class PengembanganMixin(Developable):
    DURASI_PENGEMBANGAN = 60  # menit

    def pengembangan(self) -> str:
        return (
            f"Diamkan adonan {self._nama} di tempat hangat (suhu 27-30°C) "
            f"selama 45-60 menit hingga mengembang dua kali lipat. "
            f"Tutup dengan kain lembab agar tidak kering."
        )

    def durasi_pengembangan(self) -> int:
        return self.DURASI_PENGEMBANGAN


class PemanggangangMixin(Bakeable):
    DURASI_PEMANGGANGAN = 25  # menit

    def pemanggangan(self) -> str:
        return (
            f"Panaskan oven 180°C. Panggang {self._nama} selama 20-25 menit "
            f"hingga permukaannya kecokelatan sempurna dan matang merata. "
            f"Jangan buka oven di 15 menit pertama!"
        )

    def durasi_pemanggangan(self) -> int:
        return self.DURASI_PEMANGGANGAN


class ToppingMixin(Toppable):
    DURASI_TOPPING = 10  # menit

    def topping(self) -> str:
        return (
            f"Tambahkan topping khas untuk {self._nama}: "
            f"taburkan bahan topping secara merata di atas permukaan. "
            f"Pastikan menempel sebelum dipanggang agar tidak jatuh."
        )

    def durasi_topping(self) -> int:
        return self.DURASI_TOPPING


class CroissantPengadonanMixin(Mixable):
    DURASI_PENGADONAN = 90  # menit (lebih lama karena lamination)

    def pengadonan(self) -> str:
        return (
            "Buat adonan detrempe (adonan dasar croissant) dari tepung, ragi, "
            "gula, garam, susu, dan sedikit mentega. Istirahatkan 30 menit. "
            "Lakukan proses lamination: masukkan lembaran mentega dingin (beurrage), "
            "lipat dan giling adonan 3x (single fold) dengan jeda pendinginan 20 menit "
            "tiap gilasan. Total 27 lapisan mentega yang bikin croissant flaky!"
        )

    def durasi_pengadonan(self) -> int:
        return self.DURASI_PENGADONAN


class CroissantPemanggangangMixin(Bakeable):
    DURASI_PEMANGGANGAN = 18  # menit

    def pemanggangan(self) -> str:
        return (
            "Olesi permukaan croissant dengan egg wash (kuning telur + susu). "
            "Panggang di oven 200°C selama 15-18 menit hingga berwarna golden brown "
            "dan terdengar suara hollow saat diketuk bagian bawahnya."
        )

    def durasi_pemanggangan(self) -> int:
        return self.DURASI_PEMANGGANGAN


class MuffinToppingMixin(Toppable):
    DURASI_TOPPING = 8  # menit

    def topping(self) -> str:
        return (
            "Taburkan streusel (campuran tepung, gula, mentega dingin yang diremas-remas) "
            "di atas adonan muffin sebelum dipanggang. "
            "Bisa juga tambahkan choco chips atau blueberry sesuai varian. "
            "Ini yang bikin muffin punya 'cap' renyah di atasnya!"
        )

    def durasi_topping(self) -> int:
        return self.DURASI_TOPPING
