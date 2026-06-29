# Dikerjakan oleh:
# Nama: Riska Nur Rahmawati
# NIM: K3525039

"""
production_steps.py
Mixin classes untuk setiap langkah proses produksi.

Kenapa Mixin? Karena Python multiple inheritance memungkinkan kita
"menyuntikkan" kemampuan tertentu ke class tanpa hierarki yang kaku.
Setiap Mixin hanya punya SATU tanggung jawab (SRP).

ISP terbukti di sini: produk yang tidak butuh suatu proses
tidak perlu inherit Mixin yang tidak relevan.
"""

from hanari_bakery.models.interfaces import Mixable, Developable, Bakeable, Toppable


class PengadonanMixin(Mixable):
    def pengadonan(self) -> str:
        return (
            "Campur tepung, gula, garam, dan ragi instan dalam wadah besar. "
            "Buat lubang di tengah, masukkan telur dan susu cair sedikit demi sedikit. "
            "Uleni dengan tangan atau mixer selama 10 menit hingga adonan elastis. "
            "Masukkan mentega tawar, uleni lagi 5 menit hingga kalis dan tidak lengket."
        )

    def durasi_pengadonan(self) -> int:
        return 15


class PengembanganMixin(Developable):
    def pengembangan(self) -> str:
        return (
            "Bulatkan adonan dan letakkan dalam wadah yang sudah dioles minyak. "
            "Tutup dengan plastik wrap atau kain lembab. "
            "Diamkan di tempat hangat (27-30°C) selama 60 menit atau hingga "
            "adonan mengembang dua kali lipat dari ukuran semula. "
            "Setelah mengembang, kempiskan adonan dan bentuk sesuai keinginan."
        )

    def durasi_pengembangan(self) -> int:
        return 60


class PemanggangangMixin(Bakeable):
    def pemanggangan(self) -> str:
        return (
            "Panaskan oven pada suhu 180°C selama 10 menit sebelum memanggang. "
            "Letakkan adonan yang sudah dibentuk di atas loyang yang dialasi baking paper. "
            "Panggang selama 18-22 menit hingga permukaan berwarna keemasan. "
            "Keluarkan dari oven, biarkan di loyang 5 menit, lalu pindahkan ke cooling rack."
        )

    def durasi_pemanggangan(self) -> int:
        return 25


class ToppingMixin(Toppable):
    def topping(self) -> str:
        return (
            "Siapkan topping pilihan (meses, keju parut, selai, atau krim). "
            "Oleskan atau taburkan topping secara merata di atas permukaan produk. "
            "Pastikan topping menempel baik sebelum produk dipanggang atau disajikan."
        )

    def durasi_topping(self) -> int:
        return 10


class CroissantPengadonanMixin(Mixable):
    def pengadonan(self) -> str:
        return (
            "Campur tepung, gula, garam, dan ragi. Tambahkan susu cair dingin, "
            "uleni minimal 8 menit hingga adonan halus tapi tidak terlalu kalis. "
            "Istirahatkan adonan di kulkas 30 menit (retard). "
            "Siapkan beurrage: mentega tawar dingin dipukul-pukul hingga pipih berbentuk persegi. "
            "LAMINATION: bungkus beurrage dalam adonan, gilas memanjang, lipat 3 (single fold). "
            "Ulangi proses gilas-lipat 3x dengan istirahat 20 menit di kulkas setiap sesi. "
            "Teknik ini menghasilkan lapisan-lapisan tipis yang bikin croissant flaky."
        )

    def durasi_pengadonan(self) -> int:
        return 30


class CroissantPemanggangangMixin(Bakeable):
    def pemanggangan(self) -> str:
        return (
            "Panaskan oven pada suhu 200°C (api atas-bawah). "
            "Oles permukaan croissant dengan egg wash (kuning telur + sedikit susu). "
            "Panggang 18-20 menit hingga berwarna cokelat keemasan yang dalam dan mengkilap. "
            "JANGAN buka oven di 15 menit pertama agar uap mentega tidak keluar. "
            "Croissant matang sempurna saat terdengar suara hollow saat diketuk bagian bawahnya."
        )

    def durasi_pemanggangan(self) -> int:
        return 20


class MuffinToppingMixin(Toppable):
    def topping(self) -> str:
        return (
            "Buat streusel: campur tepung, gula, dan mentega dingin yang dipotong dadu. "
            "Remas-remas dengan jari hingga teksturnya seperti remahan pasir kasar. "
            "Simpan streusel di kulkas sementara menyiapkan adonan muffin. "
            "Taburi streusel di atas adonan muffin yang sudah dituang ke dalam cup "
            "sebelum dipanggang, hingga menutupi permukaannya secara merata."
        )

    def durasi_topping(self) -> int:
        return 10