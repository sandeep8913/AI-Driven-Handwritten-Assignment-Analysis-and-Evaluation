import os
import fitz
import re
import pymysql
from sentence_transformers import SentenceTransformer, CrossEncoder
from sympy import sympify, simplify
from textblob import TextBlob
from openpyxl import load_workbook

# ✅ Set HuggingFace cache paths
os.environ['HF_HOME'] = 'C:/ai_cache/huggingface'
os.environ['SENTENCE_TRANSFORMERS_HOME'] = 'C:/ai_cache/sentence_transformers'

# ✅ Load models
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/stsb-roberta-large')

def db_connection():
    return pymysql.connect(host='localhost', user='root', password='', database='oop')

def evaluate_assignment(student_id, pdf_file):
    print(pdf_file)
    full_text = ""
    with fitz.open(pdf_file) as pdf:
        for page in pdf:
            full_text += page.get_text()

    answers = re.split(r"\?", full_text)
    print("hi")
    
    # Fetch student questions
    student_db = pymysql.connect(host='localhost', user='root', password='', database='students')
    student_cursor = student_db.cursor()
    student_cursor.execute(f"SELECT q1, q2, q3, q4, q5 FROM details WHERE id='{student_id}'")
    student_questions = student_cursor.fetchone()
    student_db.close()

    if not student_questions:
        return {'error': 'Student not found in database'}

    # Fetch correct answers for those questions
    connection = db_connection()
    cursor = connection.cursor()
    question_answers = {}

    for q in student_questions:
        cursor.execute(f"SELECT question, answer FROM assignment_1 WHERE id={q}")
        row = cursor.fetchone()
        if row:
            question, answer = row
            question_answers[q] = {'question': question, 'answer': answer}

    connection.close()

    total_score = 0
    results = []

    # Evaluation criteria
    min_length_ratio = 0.6
    partial_credit_thresholds = [0.85, 0.75, 0.65, 0.55, 0.45]
    partial_scores = [10, 9, 8, 7, 6]
    j = 1
    x_scores=[]
    for i, (q_num, data) in enumerate(question_answers.items(), start=1):
        std_answer = answers[i].strip()
        correct_answer = data['answer']

        # Semantic similarity
        similarity = cross_encoder.predict([(correct_answer, std_answer)])

        # Length check
        length_score = 10 if len(std_answer) >= len(correct_answer) * min_length_ratio else 7

        # Key point coverage
        key_points = correct_answer.split(",")
        covered_points = sum(1 for point in key_points if point.strip().lower() in std_answer.lower())
        coverage_score = ((covered_points / len(key_points)) * 10) if key_points else 10

        # Formula correctness
        try:
            correct_formula = sympify(correct_answer)
            student_formula = sympify(std_answer)
            formula_score = 10 if simplify(correct_formula - student_formula) == 0 else 5
        except:
            formula_score = 5

        # Writing style bonus
        polarity = TextBlob(std_answer).sentiment.polarity
        style_bonus = 2 if polarity > 0 else 1

        # Final score calculation
        score = max(4, round(float(similarity) * 10))
        for threshold, partial_score in zip(partial_credit_thresholds, partial_scores):
            if similarity >= threshold:
                score = partial_score
                break

        final_score = round(
            (0.6 * score) + (0.15 * length_score) + (0.15 * coverage_score) + (0.1 * formula_score) + style_bonus
        )
        x_scores.append(final_score)
        final_score
        results.append({
            'question': j,
            'score': final_score
        })
        j += 1
        if final_score>=5:
            total_score += 1

    print("Total Score:", total_score)

    # ✅ Write result to marks.xlsx
    try:
        excel_path = 'marks.xlsx'
        wb = load_workbook(excel_path)
        ws = wb.active

        found = False
        for row in ws.iter_rows(min_row=2, max_col=6):
            if row[0].value == student_id:
                row[1].value = total_score
                for i in range(2,6):
                    row[i].value=x_scores[i-2]
                found = True
                break

        if not found:
            ws.append([student_id, total_score]+x_scores)

        wb.save(excel_path)
        print(f"✅ Marks saved/updated for {student_id} in Excel.")
    except Exception as e:
        print(f"❌ Excel error: {e}")

    return results
