import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# استخدام نطاق الإدارة الشامل لقناة يوتيوب ليتوافق مع token.json
SCOPES = ["https://www.googleapis.com/auth/youtube"]


class AutoPublisherAgent:
  """وكيل النشر والإدارة الفورية لقناة «سَبِيلُ الرُّشْدِ»"""

  def __init__(self):
    print(
        "🚀 [وكيل النشر والفورية]: جاري إعداد المصادقة والاتصال بـ YouTube"
        " API..."
    )
    self.youtube_service = self._authenticate_youtube()

  def _authenticate_youtube(self):
    """مصادقة وتوثيق الاتصال بيوتيوب باستخدام token.json"""
    creds = None
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        try:
          creds.refresh(Request())
        except Exception:
          print(
              "⚠️ انتهت صلاحية التوكن، يرجى إعادة توليد `token.json` عبر سكريبت"
              " المصادقة."
          )
          return None
      else:
        print("⚠️ تنبيه: ملف `token.json` غير صالح أو غير موجود.")
        return None

    return build("youtube", "v3", credentials=creds)

  def publish_video(
      self,
      video_file="final_video.mp4",
      title="آية الكرسي بصوت خاشع | آيات تبث الطمأنينة في القلوب #Shorts",
      description=(
          "تدبر آية الكرسي. قناة سبيل الرشد للمحتوى الديني الموثق."
      ),
      tags=["آية الكرسي", "Quran", "Shorts", "سبيل الرشد"],
  ):
    """رفع ونشر الفيديو تلقائياً على يوتيوب"""
    if not self.youtube_service:
      print("❌ [خطأ]: خدمة يوتيوب غير متاحة لعدم اكتمال المصادقة.")
      return None

    if not os.path.exists(video_file):
      print(f"❌ [خطأ]: ملف الفيديو المراد رفعه غير موجود [{video_file}].")
      return None

    print(
        f"📤 جاري رفع الفيديو [{video_file}] ونشره على قناة «سَبِيلُ الرُّشْدِ»..."
    )

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",  # أو private للاختبار
            "selfDeclaredMadeForKids": False,
        },
    }

    try:
      media = MediaFileUpload(
          video_file, chunksize=-1, resumable=True, mimetype="video/mp4"
      )
      request = self.youtube_service.videos().insert(
          part="snippet,status", body=body, media_body=media
      )

      response = None
      while response is None:
        status, response = request.next_chunk()
        if status:
          print(f"⏳ نسبة الرفع: {int(status.progress() * 100)}%")

      video_id = response.get("id")
      video_url = f"https://youtu.be/{video_id}"
      print(f"\n🎉 [نجاح تام]: تم نشر الفيديو بنجاح على الرابط: {video_url} 🚀")
      return video_url

    except Exception as e:
      print(f"❌ حدث خطأ أثناء رفع الفيديو على يوتيوب: {e}")
      return None


if __name__ == "__main__":
  publisher = AutoPublisherAgent()
  publisher.publish_video()