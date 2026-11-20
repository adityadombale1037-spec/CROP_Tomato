from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        crop = request.form.get("crop")
        farm_size = request.form.get("farm_size")
        budget = request.form.get("budget")
        image = request.files.get("image")

        if not crop or not farm_size or not budget or not image:
            return render_template("index.html", error="Please fill all fields.")

        try:
            farm_size = float(farm_size)
            budget = float(budget)

            if farm_size <= 0 or budget <= 0:
                raise ValueError

        except ValueError:
            return render_template("index.html", error="Enter valid farm size and budget.")

        if crop != "Tomato":
            return render_template("index.html", error="Only Tomato crop is supported.")

        if image.filename == "":
            return render_template("index.html", error="Please select an image.")

        if not allowed_file(image.filename):
            return render_template("index.html", error="Upload JPG, JPEG or PNG image.")

        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return render_template(
            "index.html",
            success="Image uploaded successfully!",
            crop=crop,
            farm_size=farm_size,
            budget=budget,
            filename=filename
        )

    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)