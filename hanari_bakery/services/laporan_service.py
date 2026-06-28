class LaporanGenerator:
    def __init__(self):
        pass

    def generate_rekap(self, produk_list, history):
        sb = []
        
        # --- BAGIAN ATAS: DAFTAR PRODUK TERDAFTAR ---
        sb.append("=" * 64)
        sb.append(" LAPORAN REKAPITULASI HANARI BAKERY")
        sb.append("=" * 64)
        sb.append(f" {'KODE':<8} {'NAMA':<18} {'HARGA JUAL':<12} {'MARGIN':<8} {'WAKTU':<8}")
        sb.append("-" * 64)
        total_potensi = 0
        for p in produk_list:
            waktu = getattr(p, 'total_waktu_produksi', getattr(p, 'total_waktu_production', lambda: 0))()
            sb.append(f" {p.kode:<8} {p.nama:<18} Rp {p.harga_jual_per_n:<9,.0f} {((p.harga_jual_per_n - p.biaya_produksi_per_n)/p.harga_jual_per_n*100):>5.1f}% {waktu:>5} mnt")
            total_potensi += (p.harga_jual_per_n - p.biaya_produksi_per_n)
        sb.append("-" * 64)
        sb.append(f" Total produk terdaftar : {len(produk_list)}")
        sb.append(f" Total potensi profit   : Rp {total_potensi:,.0f}/resep gabungan\n")

        # --- BAGIAN BAWAH: RINGKASAN HISTORY PRODUKSI ---
        sb.append("=" * 64)
        sb.append(" RINGKASAN RIWAYAT SIMULASI & ANALISIS PENJUALAN")
        sb.append("=" * 64)
        sb.append(f" Total simulasi dijalankan: {len(history)}x\n")
        
        sb.append(f" {'#':<3} {'PRODUK':<14} {'STATUS':<8} {'PESANAN':<8} {'PRODUKSI':<9} {'PROFIT RIIL':<12}")
        sb.append("-" * 64)
        
        total_profit_riil = 0
        total_profit_maksimal = 0
        simulasi_sukses = 0
        kamus_rinci = {}
        
        for h in history:
            is_sukses = h.get("stok_cukup", False) or h.get("stok_ok", False) or (h.get("stok_cukup") == "OK")
            if "stok_cukup" in h and isinstance(h["stok_cukup"], bool):
                is_sukses = h["stok_cukup"]
                
            status_teks = "[OK]" if is_sukses else "[KURANG]"
            
            pcs_diminta = h.get("jumlah_pcs", 0)
            # Ambil nilai total_pcs_diproduksi riil yang dikirim oleh service baru kita
            pcs_diproduksi = h.get("total_pcs_diproduksi", pcs_diminta) if is_sukses else 0
            profit_riil = h.get("angka_profit_riil", h.get("profit", 0)) if is_sukses else 0
            
            sb.append(
                f" {h['id']:<3} {h['nama_produk']:<14} {status_teks:<8} "
                f"{pcs_diminta:>4} pcs  {pcs_diproduksi:>4} pcs   "
                f"Rp {profit_riil:>9,.0f}"
            )
            
            if is_sukses:
                simulasi_sukses += 1
                total_profit_riil += profit_riil
                total_profit_maksimal += h.get("profit", h.get("total_profit", 0))
                
                nama_p = h['nama_produk']
                if nama_p not in kamus_rinci:
                    kamus_rinci[nama_p] = {"diminta": 0, "diproduksi": 0}
                kamus_rinci[nama_p]["diminta"] += pcs_diminta
                kamus_rinci[nama_p]["diproduksi"] += pcs_diproduksi

        sb.append("-" * 64)
        sb.append(f" Rangkuman Validitas Operasional Pabrik:")
        sb.append(f"  • Total Simulasi Sukses    : {simulasi_sukses} dari {len(history)} percobaan")
        sb.append(f"  • Rincian Produk Berhasil Terjual & Diproduksi:")
        
        if not kamus_rinci:
            sb.append(f"    - Belum ada produk yang sukses diproduksi.")
        else:
            for nama_kue, data in kamus_rinci.items():
                sb.append(f"    -> {nama_kue:<15}: Sukses Jual {data['diminta']:>2} pcs | Dapur Bikin {data['diproduksi']:>2} pcs")
                
        sb.append("-" * 64)
        sb.append(f" TOTAL PROFIT RIIL MASUK    : Rp {total_profit_riil:,.0f}")
        
        # Hitung sisa kue untuk mendeteksi sisa produk etalase secara nyata
        total_diminta_all = sum(d["diminta"] for d in kamus_rinci.values())
        total_diproduksi_all = sum(d["diproduksi"] for d in kamus_rinci.values())
        sisa_kue = total_diproduksi_all - total_diminta_all
        
        if sisa_kue > 0:
            potensi_tertahan = total_profit_maksimal - total_profit_riil
            sb.append(f"  [!] Catatan Etalase       : Ada sisa total {sisa_kue} pcs kue belum terjual di etalase.")
            sb.append(f"  [!] Potensi Tambahan      : Rp {potensi_tertahan:,.0f} jika sisa produk di etalase habis.")
        else:
            sb.append("  [✓] Efisiensi Stok        : 100% Tidak ada sisa produk tertahan di etalase.")
            
        sb.append("=" * 64)
        return "\n".join(sb)
