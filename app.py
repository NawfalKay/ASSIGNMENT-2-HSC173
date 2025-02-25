from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

uri = "mongodb+srv://NAFWAL:PANFAL@cluster0.3tnvy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri)
db = client["Phaethon"]
collection = db["Esp32_sensor"]

@app.route('/', methods=['GET'])
def home():
    return "Server sudah berjalan"

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        print("Received data:", data)  

        suhu = data.get("suhu")
        kelembaban = data.get("kelembaban")
        jarak = data.get("jarak")

        if suhu is None or kelembaban is None or jarak is None:
            return jsonify({"error": "suhu, kelembaban, dan jarak are required."}), 400

        record = {"suhu": suhu, "kelembaban": kelembaban, "jarak": jarak}
        collection.insert_one(record)

        return jsonify({"message": "Data saved successfully."}), 201
    
    except Exception as error:
        print("Error inserting to MongoDB:", error)
        return jsonify({"error": str(error)}), 500

if __name__ == "_main_":
    app.run(host='0.0.0.0', debug=True)