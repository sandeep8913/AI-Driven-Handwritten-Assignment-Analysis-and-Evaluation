from flask import Flask, request, jsonify, render_template
import os
import io
import pymysql
from pymysql.cursors import DictCursor
from pdf2image import convert_from_path
from google.cloud import vision
from reportlab.pdfgen import canvas
from flask import session
from evaluator import evaluate_assignment

# Ensure necessary directories exist
os.makedirs("./uploads", exist_ok=True)
os.makedirs("./results", exist_ok=True)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your google vision api key'

client = vision.ImageAnnotatorClient()


# Serve homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    roll_number = data.get('rollNumber')
    password = data.get('password')

    # Connect to 'students' database
    conn_students = pymysql.connect(host='localhost', user='root', password='', database='students')
    cursor_students = conn_students.cursor()

    cursor_students.execute("SELECT q1, q2, q3, q4, q5 FROM details WHERE id=%s AND pass=%s", (roll_number, password))
    result = cursor_students.fetchone()
    conn_students.close()

    if result:
        session['roll_number'] = roll_number
        q_ids = list(result)  # Now contains [q1, q2, q3, q4, q5]

        # Connect to 'oop' database
        conn_oop = pymysql.connect(host='localhost', user='root', password='', database='oop')
        cursor_oop = conn_oop.cursor()

        # Fetch questions based on IDs
        format_strings = ','.join(['%s'] * len(q_ids))
        cursor_oop.execute(f"SELECT id, question FROM assignment_1 WHERE id IN ({format_strings})", q_ids)
        fetched_questions = cursor_oop.fetchall()
        conn_oop.close()

        # Map id to question for correct ordering
        q_map = {q[0]: q[1] for q in fetched_questions}
        ordered_questions = [q_map.get(qid, '') for qid in q_ids]

        return jsonify(success=True, questions=ordered_questions)
    else:
        return jsonify(success=False, error="Invalid credentials")
    


# Handle file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        images = convert_from_path(
            file_path,
            poppler_path=r"C:\Users\sande\OneDrive\Desktop\majproj\Release-24.08.0-0\poppler-24.08.0\Library\bin"
        )

        full_text = ""
        for i, image in enumerate(images, start=1):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()

            vision_image = vision.Image(content=img_bytes)
            response = client.text_detection(image=vision_image)

            text = response.text_annotations[0].description if response.text_annotations else "No text detected"
            full_text += f"{text}"

        # Save extracted text to a PDF
        output_pdf = f"./results/extracted_text_{file.filename}"


        c = canvas.Canvas(output_pdf)
        c.setFont("Helvetica", 10)
        y_position = 800

        for line in full_text.split("\n"):
            c.drawString(50, y_position, line)
            y_position -= 15
            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y_position = 800

        c.save()
        roll_number = session.get('roll_number', 'Unknown User')
        print(roll_number)

        roll_number = session.get('roll_number', 'Unknown User')
        output_pdf = f"./results/extracted_text_{file.filename}"

        # Call evaluation
        evaluation_result = evaluate_assignment(roll_number, output_pdf)

        # Return both messages
        return jsonify({
            'message': f'Text extracted and saved to {output_pdf}',
            'evaluation': evaluation_result
        })

    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
