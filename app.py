import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# OpenAI Client mit Environment Variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        text_type = data.get('text_type')
        era = data.get('era')
        context = data.get('context', '')
        
        # Validation
        if not text_type or not era:
            return jsonify({'error': 'Textart und Jahrhundert sind erforderlich'}), 400
        
        prompt = f"Schreibe einen {text_type} im Stil des {era}. Jahrhunderts. Beziehungskontext: {context}."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Kostengünstiger
            messages=[
                {"role": "system", "content": "Du bist ein kreativer Autor für romantische Texte im deutschen Sprachraum."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800,
            timeout=30
        )
        
        generated_text = response.choices[0].message.content
        return jsonify({'text': generated_text})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'error': 'Ein Fehler ist aufgetreten. Bitte versuche es erneut.'}), 500

if __name__ == '__main__':
    # Lokale Entwicklung
    app.run(debug=True, port=5000)
