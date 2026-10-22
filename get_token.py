import os
from google_auth_oauthlib.flow import InstalledAppFlow

# نطاق الصلاحيات الشامل لإدارة ورفع الفيديوهات
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def generate_youtube_token():
  print("🚀 جاري بدء عملية التوثيق الشامل لقناة سبيل الرشد...")
  try:
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token_file:
      token_file.write(creds.to_json())

    print("\n✅ تم ربط القناة وحفظ ملف التوثيق (token.json) بنجاح تام!")
  except Exception as e:
    print(f"\n❌ حدث خطأ أثناء التوثيق: {e}")


if __name__ == "__main__":
  generate_youtube_token()