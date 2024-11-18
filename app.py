from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_response(self, service_type, user_input):
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user", 
                    "content": f"Hizmet: {service_type}\nDurum: {user_input}"
                }],
                max_tokens=4000
            )
            # response.content'i string'e çevir
            return {
                'success': True,
                'response': str(response.content) if response.content else "Yanıt alınamadı."
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Veri bulunamadı'})
        
        service_type = data.get('service_type')
        user_input = data.get('input')
        
        if not service_type or not user_input:
            return jsonify({'success': False, 'error': 'Eksik parametre'})
            
        assistant = AIAssistant()
        result = assistant.generate_response(service_type, user_input)
        
        # result zaten dictionary formatında
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
