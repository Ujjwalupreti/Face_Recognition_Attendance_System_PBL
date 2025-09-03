from flask import Flask, request, jsonify, send_from_directory,render_template
from flask_cors import CORS
import os
from db import DatabaseService
from face_model import FaceEncoder

DB = DatabaseService()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "../frontend/static"),
    static_url_path="/static"
)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html") 


@app.route("/register", methods=["POST"])
def register():
    """Register a new student and retrain the model."""
    name = request.form.get("name")
    roll = request.form.get("roll")
    course = request.form.get("course")
    image = request.files.get("image")

    if not (name and roll and image):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    image_bytes = image.read()

    # Register student with image directly
    result = DB.register_student(name, roll, course, image_bytes)

    if not result["success"]:
        return jsonify({"status": "error", "message": result["message"]}), 400

    # Retrain model using all images from the database
    encoder = FaceEncoder()
    if encoder.retrain_model():
        return jsonify({
            "status": "success",
            "message": "Student registered and model trained successfully"
        })
    else:
        conn = DB.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM take2 WHERE roll_no=%s", (roll,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return jsonify({
            "status": "error",
            "message": "Training failed. Student removed."
        }), 500


@app.route("/capture", methods=["POST"])
def capture():
    """Capture a frame, recognize face, and mark attendance."""
    file = request.files.get("frame")
    if not file:
        return jsonify({"status": "error", "message": "No frame received"}), 400

    frame_bytes = file.read()
    result = FaceEncoder.recognize_face(frame_bytes)

    if not result:
        return jsonify({"status": "error", "message": "Face not recognized"}), 404

    name, roll = result
    student = DB.get_student_by_roll(roll)
    if not student:
        return jsonify({"status": "error", "message": "Student not found"}), 404

    if DB.check_attendance_today(roll):
        return jsonify({
            "status": "error",
            "message": f"Attendance already marked today for {student['names']} ({roll})"
        }), 400

    if DB.mark_attendance(roll):
        return jsonify({
            "status": "success",
            "message": f"Attendance marked for {student['names']} ({roll})",
            "student": {
                "name": student["names"],
                "roll_no": student["roll_no"],
                "course": student["course"]
            }
        })
    else:
        return jsonify({"status": "error", "message": "Failed to mark attendance"}), 500


@app.route("/user_info")
def user_info():
    """Fetch user info and attendance history."""
    roll = request.args.get("roll")
    if not roll:
        return jsonify({"error": "Roll number required"}), 400

    student = DB.get_student_by_roll(roll)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    records = DB.get_attendance_records(roll)
    return jsonify({
        "name": student["names"],
        "roll_no": student["roll_no"],
        "course": student["course"],
        "attendance_count": len(records),
        "attendance": [str(r['date_time']) for r in records]
    })


if __name__ == "__main__":
    DB.init_tables()
    app.run(port=8000, debug=True, use_reloader=False)