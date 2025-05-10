from flask import Flask, render_template, redirect, url_for
import mysql.connector
import random
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, redirect, url_for, request, flash, session


app = Flask(__name__)
app.secret_key = 'supersecretkey'
# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="students"
    )

# Function to generate random numbers
def generate_numbers_for_empty_rows():
    db = connect_db()
    cursor = db.cursor()

    # Fetch all rows with empty q1-q5
    cursor.execute("SELECT id FROM details WHERE q1 IS NULL OR q1 = ''")
    rows = cursor.fetchall()

    # Generate and update numbers for each student row if q1-q5 are empty
    for row in rows:
        numbers = random.sample(range(1, 11), 5)
        cursor.execute(
            "UPDATE details SET q1=%s, q2=%s, q3=%s, q4=%s, q5=%s WHERE id=%s",
            (*numbers, row[0])
        )

    db.commit()
    cursor.close()
    db.close()

# Route to display data
@app.route('/')
def index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM details")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('rand.html', data=data)

# Route to handle the button click and generate numbers
@app.route('/generate', methods=['POST'])
def generate():
    generate_numbers_for_empty_rows()
    return redirect(url_for('index'))

# Route to send emails
@app.route('/send_emails', methods=['POST'])
def send_emails():
    success = send_emails_to_students()
    if success:
        flash("Emails sent successfully!", "success")
    else:
        flash("Some emails failed to send!", "error")
    return redirect(url_for('index'))


# Function to send emails
def send_emails_to_students():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, q1, q2, q3, q4, q5 FROM details")
    students = cursor.fetchall()
    cursor.close()
    db.close()

    sender_email = "sandeepreddy8913@gmail.com"
    sender_password = "psdd iwkq vzuj wlvz"

    all_success = True  # track status

    con=mysql.connector.connect( host="localhost",
        user="root",
        password="",
        database="oop")
    cursor = con.cursor()

    for student in students:
        roll_no = student[0]
        question_ids = student[1:6]
        receiver_email = f"{roll_no}@gcet.edu.in"
        questions = []
        for q_id in question_ids:
            cursor.execute("SELECT question FROM assignment_1 WHERE id = %s", (q_id,))
            result = cursor.fetchone()
            if result:
                questions.append(result[0])  # Append the actual question text to the list

        # Prepare the email content
        subject = "Your OOP Assignment Questions"
        body = f"Hello {roll_no},\n\nHere are your OOP assignment questions:\n\n" + \
            f"Q1: {questions[0]}\nQ2: {questions[1]}\nQ3: {questions[2]}\nQ4: {questions[3]}\nQ5: {questions[4]}\n\n" + \
            "Best of luck!\nGCET"

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            print(f"✅ Email sent to {receiver_email}")
        except Exception as e:
            print(f"❌ Failed to send email to {receiver_email}: {e}")
            all_success = False

    return all_success



# Run the app
if __name__ == "__main__":
    app.run(debug=True)
