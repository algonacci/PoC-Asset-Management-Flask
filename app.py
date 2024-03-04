import qrcode
from flask import Flask, render_template, jsonify, request, send_file
from helpers import read_file_data

app = Flask(__name__)


@app.route("/")
def index():
    data = read_file_data()
    return render_template("index.html", assets=data)


@app.route("/api/assets")
def get_assets():
    assets = read_file_data()
    response = {
        "status": {
            "code": 200,
            "message": "Success fetching all assets"
        },
        "data": assets
    }
    return jsonify(response)


@app.route("/api/assets/search")
def search_assets():
    keyword = request.args.get("keyword")
    assets = read_file_data()

    if keyword:
        search_result = []
        for asset in assets:
            if keyword.lower() in asset["nama"].lower() or keyword.lower() in asset["deskripsi"].lower():
                search_result.append(asset)
        return jsonify({
            "status": {
                "code": 200,
                "message": "Success fetching search results",
            },
            "data": search_result,
        }), 200
    else:
        return jsonify({
            "status": {
                "code": 400,
                "message": "Keyword not provided",
            },
            "data": None
        }), 400


@app.route("/api/assets/search/<int:id>")
def search_assets_by_id(id):
    assets = read_file_data()

    if id:
        search_result = [asset for asset in assets if str(
            asset["id"]) == str(id)]  # mengonversi id menjadi string
        if search_result:
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success fetching search results"
                },
                "data": search_result
            }), 200
        else:
            return jsonify({
                "status": {
                    "code": 404,
                    "message": "Asset not found with the provided ID"
                },
                "data": None
            }), 404
    else:
        return jsonify({
            "status": {
                "code": 400,
                "message": "ID not provided in the query parameters"
            },
            "data": None
        }), 400


@app.route("/generate_qr/<int:id>")
def generate_qr(id):

    url = request.url_root + f"/api/assets/search/{id}"

    # Membuat QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Membuat gambar QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Menyimpan gambar QR code
    img_path = f"static/qr_codes/asset_{id}.png"
    img.save(img_path)

    # Update path QR code di dataset
    update_qr_code_path(id, img_path)

    # Mengembalikan path gambar QR code
    return img_path


def update_qr_code_path(id, path):
    # Membaca dataset
    with open("data.txt", "r") as file:
        lines = file.readlines()

    # Menyimpan path QR code ke dalam dataset
    updated_lines = []
    for line in lines:
        if line.startswith(str(id)):
            updated_line = f"{line.strip()}{path}\n"
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # Menulis kembali dataset dengan path QR code yang diperbarui
    with open("data.txt", "w") as file:
        file.writelines(updated_lines)


@app.route("/show_qr/<int:id>")
def show_qr(id):
    img_path = f"static/qr_codes/asset_{id}.png"
    return send_file(img_path, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
