from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import json
import os
from gtts import gTTS
import io

app = Flask(__name__)

# مهم: من بعد ما نطلقو البوت فـ Render، غادي نحطو API Key ديال Gemini هنا
# دابا خليها هاكا مؤقتا
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "AIzaSy...بدلها_بالكود_ديالك")
genai.configure(api_key=GEMINI_API_KEY)

# نقراو القاموس ديالنا
with open('amawal.json', 'r', encoding='utf-8') as f:
    AMAWAL = json.load(f)

model = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    dialect = request.json['dialect']

    # 1. قلبو فالقاموس ديالنا الأول باش نعطيو جواب دقيق
    direct_answer = ""
    for key, value in AMAWAL.items():
        if key in user_message:
            direct_answer += f"{key} → {value[dialect]}\n"

    # 2. صيفطو لـ Gemini باش يجاوب و يناقش و يعلم
    prompt = f"""
    أنت Tamurt-GPT-Pro، أقوى مساعد ذكي أمازيغي فالمغرب. كتهضر تشلحيت، ريفية، أطلسية، و العربية.
    المستخدم اختار لهجة: {dialect}. جاوب بنفس اللهجة ديالو. كن ذكي و ناقش المواضيع و شرح الدروس.

    هذا هو القاموس الأمازيغي ديالك للمرجع. استعملو باش تجاوب بدقة:
    {json.dumps(AMAWAL, ensure_ascii=False)}

    الكلمات اللي لقيتيها فالقاموس من سؤال المستخدم:
    {direct_answer}

    سؤال المستخدم: {user_message}

    المطلوب منك:
    1. إلى كان السؤال ترجمة و لقيتي الكلمة فالقاموس، عطيها.
    2. إلى كان السؤال نقاش ولا شرح ولا سؤال عام، جاوب جواب كامل و مفصل و ذكي.
    3. دايما جاوب بنفس لهجة المستخدم: {dialect}.
    """

    response = model.generate_content(prompt)
    final_answer = direct_answer + "\n" + response.text.strip()

    return jsonify({'answer': final_answer})

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json['text']
    # gTTS كيقرا الدارجة و الشلحة مزيان. lang='ar' خدامة ليهم بجوج
    tts = gTTS(text=text, lang='ar', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return send_file(fp, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
