# app.py 
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set this to a random secret string

# Quiz questions and answers
questions = [
    {
        "question": "What should you do if you are contacted by an unknown individual on a social media website?",
        "options": [
            "Do not answer until I find out who they are.",
            "Introduce myself politely and tell them about my day.",
            "Add them to my friends."
        ],
        "correct": 0
    },
    {
        "question": "Which of the following is a strong password?",
        "options": [
            "password123",
            "qwerty",
            "P@ssw0rd!2023"
        ],
        "correct": 2
    },
    # Add more questions here...
]

@app.route('/')
def start_quiz():
    session['current_question'] = 0
    session['score'] = 0
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'current_question' not in session:
        return redirect(url_for('start_quiz'))

    if request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer = questions[session['current_question']]['correct']
        if user_answer == correct_answer:
            session['score'] += 1
        
        session['current_question'] += 1
        if session['current_question'] >= len(questions):
            return redirect(url_for('result'))
        return redirect(url_for('question'))
        
    current_question = questions[session['current_question']]
    return render_template('question.html', 
                           question=current_question,
                           question_number=session['current_question'] + 1,
                           total_questions=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(questions)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)