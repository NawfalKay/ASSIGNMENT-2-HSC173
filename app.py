from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(_name_)

uri = "mongodb+srv://NAFWAL:PANFAL@cluster0.3tnvy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri)
db = client["Phaethon"]
collection = db["Esp32_sensor"]

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging log
        
        suhu = data.get("suhu")
        kelembaban = data.get("kelembaban")

        if suhu is None or kelembaban is None:
            return jsonify({"error": "suhu and kelembaban are required."}), 400

        record = {"suhu": suhu, "kelembaban": kelembaban}
        collection.insert_one(record)

        return jsonify({"message": "Data saved successfully."}), 201
    
    except Exception as error:  # Ganti 'e' dengan 'error'
        print("Error inserting to MongoDB:", error)  # Debugging log
        return jsonify({"error": str(error)}), 500

if _name_ == "_main_":
    app.run(host='0.0.0.0', debug=True)
