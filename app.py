from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os, json

app = Flask(__name__)
app.secret_key = os.urandom(24)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

with open('amawal.json', 'r', encoding='utf-8') as f:
    AMAWAL = json.load(f)

VETS_DB = {
    "خنيفرة": {"name": "د. موحى الأطلسي", "phone": "0633445566"},
    "الناظور": {"name": "د. كريم الريفي", "phone": "0634556677"},
    "أكادير": {"name": "د. حسناء السوسية", "phone": "0667890123"},
}

PROMPTS = {
    "atlas": "كشم أتݣت Tamurt-GPT-Pro. ساول س تمازيغت ن الأطلس غاس. إيغ أور تفهمت، سقسا س تبسيط. استعمل كلمات من أماڤال IRCAM. إيغ إݣا وانطان يخشن، مّل أس أبيطار أمازيغ.",
    "rif": "شك ذ Tamurt-GPT-Pro. ساوار غاس س ثاريفيث. إيغ أور تفهمذ، سقسي س تبسيط. سقذغ ثيرزا ن IRCAM. ماغار ذين يوعار أطان، مّر اس طبيب ن ييضان.",
    "souss": "كيي تݣيت Tamurt-GPT-Pro. ساول غاس س تشلحيت. إغ أور تفهمت، سقسا س تبسيط. سخدم تيرزا ن IRCAM. إغ إيݣا لمرض إخلن، مّل اس طبيب لبهايم."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set_lang', methods=['POST'])
def set_lang():
    session['lang'] = request.json.get('lang')
    return jsonify({'status': 'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    lang = data.get('lang', 'atlas')
    system_prompt = PROMPTS.get(lang, PROMPTS['atlas'])
    
    response = model.generate_content(f"{system_prompt}\n\nأسقسي: {message}")
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
