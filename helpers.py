def read_file_data():
    with open("data.txt", "r") as file:
        lines = file.readlines()

    assets = []
    for line in lines[1:]:
        asset_data = line.strip().split(",")
        asset = {
            "id": int(asset_data[0]),  # tambahkan id sebagai atribut
            "nama": asset_data[1],
            "deskripsi": asset_data[2],
            "penyusutan": format_rupiah(float(asset_data[3])),
            "url_gambar": asset_data[4],
            "harga": int(asset_data[5]),
            "harga_rupiah": format_rupiah(int(asset_data[5])),
            "tanggal_pembelian": asset_data[6],
            "qr_code_path": asset_data[7],
        }
        assets.append(asset)

    return assets


def format_rupiah(harga):
    rupiah = "Rp {:,.0f}".format(harga)
    return rupiah
