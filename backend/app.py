from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# File to store attendance
attendance_file = "attendance_records.xlsx"

# Ensure the file exists
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Date", "Time", "Employee ID", "Name", "Status"])
    df.to_excel(attendance_file, index=False)

@app.route("/")
def home():
    return "Welcome to the Attendance System API!"

@app.route("/submit", methods=["POST"])
def submit_attendance():
    data = request.get_json()
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Employee ID": data["empId"],
        "Name": data["name"],
        "Status": data["status"],
    }
    try:
        df = pd.read_excel(attendance_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(attendance_file, index=False)
        return jsonify({"message": "Attendance marked successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
