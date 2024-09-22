from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade_essay():
    try:
        essay_text = request.form['essay']
        word_count = len(essay_text.split())
        if word_count < 50:
            return jsonify({'error': 'Essay is too short. Please write at least 50 words.'}), 400
        
        # For now, just return a dummy grade based on word count
        dummy_grade = min(10, word_count / 100)
        return jsonify({'grade': round(dummy_grade, 1)})
    except Exception as e:
        app.logger.error(f"Error grading essay: {str(e)}")
        return jsonify({'error': 'An error occurred while grading the essay. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)