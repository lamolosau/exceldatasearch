import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = 'Z:\\Données\\Téléchargements\\test\\uploads'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        search_value = request.form.get("search_value")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath, engine='openpyxl')
        except Exception as e:
            return jsonify(error=str(e))

        mask = df.isin([search_value])
        results = df[mask.any(axis=1)].to_dict(orient="records")
        return jsonify(results=results)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
