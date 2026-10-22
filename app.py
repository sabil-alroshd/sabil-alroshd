import os
import json
from flask import Flask, redirect, url_for
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

app = Flask(__name__)

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.json"

@app.route('/')
def index():
    if os.path.exists(TOKEN_FILE):
        return '<h2>قناة سبيل الرشد - بوابة النشر الآلي</h2><p>✅ تم ربط الحساب وحفظ التوثيق بنجاح! يمكنك إغلاق هذه الصفحة.</p>'
    return '<h2>قناة سبيل الرشد - بوابة النشر الآلي</h2><a href="/login"><button style="padding:10px 20px;font-size:16px;">تسجيل الدخول وربط قناة اليوتيوب</button></a>'

@app.route('/login')
def login():
    try:
        # استخدام InstalledAppFlow لفتح المتصفح وأخذ التوثيق بلمسة واحدة وبدون أخطاء جلسات
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, 
            scopes=SCOPES
        )
        # فتح منفذ تلقائي محلي للتوثيق
        creds = flow.run_local_server(port=5000, authorization_prompt_message="جاري فتح متصفح التوثيق...")
        
        # حفظ التوثيق في ملف token.json لاستخدامه مستقبلاً تلقائياً
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
        return redirect(url_for('index'))
    except Exception as e:
        return f"حدث خطأ أثناء التوثيق: {e}"

if __name__ == '__main__':
    app.run(port=5001, debug=True)