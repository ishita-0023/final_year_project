import openai

openai.api_key = 'sk-_eLPqG7VU5AgsWJCOEgYtCw5-HXdhdNPQ9MuYU6IKNT3BlbkFJWQ-laMk9Pbmbn84rPi3I9R4cWjXib4KIJP26CKtxAA'

def get_essay_feedback(essay):
    prompt = f"""
    Analyze the following essay and provide feedback:
    
    {essay}
    
    Please provide:
    1. Three strengths of the essay
    2. Three areas for improvement
    3. Three specific suggestions for enhancing the essay
    
    Format your response as a JSON object with keys: 'strengths', 'areas_for_improvement', and 'suggestions'.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides feedback on essays."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']

# In your Flask/FastAPI/etc. route handler:
@app.route('/get-essay-feedback', methods=['POST'])
def essay_feedback():
    essay = request.json['essay']
    feedback = get_essay_feedback(essay)
    return jsonify(json.loads(feedback))