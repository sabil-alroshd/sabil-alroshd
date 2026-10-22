import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_authenticated_service():
  """جلب جلسة التوثيق المستقرة"""
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open("token.json", "w") as token_file:
      token_file.write(creds.to_json())

  return build("youtube", "v3", credentials=creds)


def upload_video(file_path, title, description, tags=None, category_id="22"):
  """دالة رفع الفيديو تلقائياً إلى يوتيوب"""
  try:
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["سبيل الرشد", "إسلاميات", "Shorts"],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": "private",  # نرفعه كـ "خاص" في البداية للاختبار والتأكد
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        file_path, chunksize=-1, resumable=True, mimetype="video/*"
    )

    print(f"🚀 جاري رفع الفيديو: {file_path} ...")
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    response = None
    while response is None:
      status, response = request.next_chunk()
      if status:
        print(f"⏳ تقدم الرفع: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print(f"\n✅ تم رفع الفيديو بنجاح!")
    print(f"🔗 رابط الفيديو (خاص): https://youtu.be/{video_id}")
    return video_id

  except Exception as e:
    print(f"❌ حدث خطأ أثناء رفع الفيديو: {e}")
    return None


if __name__ == "__main__":
  # تجربة رفع فيديو (تأكد من وجود فيديو باسم test.mp4 أو ضع مسار أي فيديو لديك)
  video_file = "test.mp4"

  if os.path.exists(video_file):
    upload_video(
        file_path=video_file,
        title="سبيل الرشد | فيديو تجريبي",
        description="فيديو اختباري لنظام النشر الآلي لقناة سبيل الرشد.",
        tags=["سبيل_الرشد", "قرآن", "Shorts"],
    )
  else:
    print(
      f"⚠️ لم يتم العثور على ملف الفيديو [{video_file}] في مجلد المشروع."
    )
    print(
        "💡 يرجى وضع فيديو قصير بصيغة mp4 باسم test.mp4 داخل مجلد sabil-alroshd"
        " لاختباره."
    )