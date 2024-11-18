from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def get_prompt(self, service_type, user_input):
        prompts = {
            'analysis': f"""
                Veri analisti olarak aşağıdaki konuyu detaylı analiz et:
                
                KONU: {user_input}
                
                Lütfen şu başlıklar altında analiz yap:
                
                # ÖZET ANALİZ
                # TEMEL BULGULAR
                # ÖNERİLER
                # SONUÇ
            """,
            
            'writing': f"""
                İçerik yazarı olarak aşağıdaki konuda profesyonel bir metin oluştur:
                
                KONU: {user_input}
                
                Lütfen şu özelliklere dikkat et:
                - SEO uyumlu
                - Akıcı anlatım
                - Özgün içerik
                - Dikkat çekici başlıklar
            """,
            
            'coding': f"""
                Yazılım geliştirici olarak aşağıdaki problemi çöz:
                
                PROBLEM: {user_input}
                
                Lütfen şunları sağla:
                # ÇÖZÜM AÇIKLAMASI
                # KOD ÖRNEĞİ
                # KULLANIM KILAVUZU
                # NOTLAR
            """,
            
            'translation': f"""
                Profesyonel çevirmen olarak aşağıdaki metni çevir:
                
                METİN: {user_input}
                
                Lütfen şunlara dikkat et:
                - Kültürel uyarlamalar
                - Deyimsel karşılıklar
                - Profesyonel terminoloji
                - Akıcı anlatım
            """,
            
            'research': f"""
                Araştırmacı olarak aşağıdaki konuyu detaylı incele:
                
                KONU: {user_input}
                
                Lütfen şu başlıklar altında raporla:
                # MEVCUT DURUM
                # ARAŞTIRMA BULGULARI
                # KARŞILAŞTIRMALI ANALİZ
                # SONUÇ VE ÖNERİLER
            """
        }
        return prompts.get(service_type, f"Uzman olarak şu konuyu değerlendir: {user_input}")

    def generate_response(self, service_type, user_input):
        try:
            prompt = self.get_prompt(service_type, user_input)
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                max_tokens=4000
            )
            
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
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
