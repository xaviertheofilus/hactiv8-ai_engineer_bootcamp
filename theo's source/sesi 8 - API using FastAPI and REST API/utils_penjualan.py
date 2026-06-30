import math
from datetime import datetime


def hitung_subtotal(unit, harga_satuan):
    """subtotal dari unit dikali harga satuan."""
    return unit * harga_satuan


def hitung_diskon(subtotal, persen_diskon=0):
    """nilai diskon dalam rupiah."""
    return subtotal * persen_diskon / 100


def hitung_total(subtotal, persen_diskon=0):
    """total setelah diskon. Memanggil hitung_diskon di dalamnya."""
    diskon = hitung_diskon(subtotal, persen_diskon)
    return subtotal - diskon


def buat_laporan(data_penjualan, persen_diskon=0):
    """
    Membuat laporan penjualan lengkap.
    """
    detail = []
    grand_total = 0
    total_unit = 0

    for item in data_penjualan:
        subtotal = hitung_subtotal(item["unit"], item["harga_satuan"])
        diskon = hitung_diskon(subtotal, persen_diskon)
        total = hitung_total(subtotal, persen_diskon)

        detail.append({
            **item,
            "subtotal": subtotal,
            "diskon": diskon,
            "total": total
        })

        grand_total += total
        total_unit += item["unit"]

    rata_unit = round(total_unit / len(data_penjualan), 2)

    return {
        "detail": detail,
        "grand_total": grand_total,
        "rata_unit": rata_unit
    }


def tambahkan_timestamp(laporan):
    laporan["dibuat_pada"] = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    return laporan


def statistik_penjualan(data_penjualan):
    """
    statistik penjualan: total_unit, max_subtotal,
    min_subtotal, dan std_subtotal (dihitung manual).
    """
    subtotals = [hitung_subtotal(i["unit"], i["harga_satuan"]) for i in data_penjualan]
    total_unit = sum(i["unit"] for i in data_penjualan)

    max_subtotal = subtotals[0]
    min_subtotal = subtotals[0]
    for s in subtotals:
        if s > max_subtotal:
            max_subtotal = s
        if s < min_subtotal:
            min_subtotal = s

    rata = sum(subtotals) / len(subtotals)
    varians = sum((s - rata) ** 2 for s in subtotals) / len(subtotals)
    std_subtotal = math.sqrt(varians)

    return {
        "total_unit": total_unit,
        "max_subtotal": max_subtotal,
        "min_subtotal": min_subtotal,
        "std_subtotal": round(std_subtotal, 2)
    }
