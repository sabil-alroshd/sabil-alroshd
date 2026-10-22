import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# استيراد وحدات النظام الأساسية
try:
  from make_video import merge_audio_video
  from sabil_master import run_sabil_agent
  from tts_engine import generate_audio_from_script
except ImportError as e:
  print(f"⚠️ تنبيه استيراد الوحدات: {e}")

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_authenticated_service():
  """جلب جلسة التوثيق المستقرة من token.json"""
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open("token.json", "w") as token_file:
      token_file.write(creds.to_json())

  return build("youtube", "v3", credentials=creds)


def upload_to_youtube(
    file_path, title, description, tags=None, privacy="private"
):
  """دالة رفع الفيديو النهائي إلى يوتيوب"""
  try:
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags
            or ["سبيل الرشد", "دعوة", "إسلاميات", "قرآن", "Shorts"],
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        file_path, chunksize=-1, resumable=True, mimetype="video/*"
    )

    print(f"\n🚀 [النشر الآلي] جاري رفع الفيديو النهائي: {file_path} ...")
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    response = None
    while response is None:
      status, response = request.next_chunk()
      if status:
        print(f"⏳ تقدم الرفع: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print(f"\n✅ تم نشر الفيديو النهائي بنجاح على يوتيوب!")
    print(f"🔗 رابط الفيديو: https://youtu.be/{video_id}\n")
    return video_id

  except Exception as e:
    print(f"\n❌ حدث خطأ أثناء النشر الآلي: {e}\n")
    return None


def run_full_pipeline():
  print("==================================================")
  print("🌟 بدء خط الإنتاج الآلي الشامل لقناة «سَبِيلُ الرُّشْدِ» 🌟")
  print("==================================================\n")

  # 1. جلب الآية وتوليد السكريبت اليومي
  print(
      "🤖 [الخطوة 1/4]: جاري جلب الآية الموثقة وتوليد السكريبت الدعوي عبر"
      " الوكلاء..."
  )
  try:
    run_sabil_agent()
  except Exception as e:
    print(f"⚠️ خطأ أثناء توليد السكريبت: {e}")

  time.sleep(1)

  # 2. تحويل السكريبت إلى ملف صوتي (TTS)
  print("\n🎙️ [الخطوة 2/4]: جاري تحويل النص الدعوي المولد إلى ملف صوتي...")
  generate_audio_from_script(
      script_file="today_script.txt", output_audio="voice.mp3"
  )

  # 3. دمج الصوت مع الفيديو وإنتاج final_video.mp4
  print("\n🎬 [الخطوة 3/4]: جاري مونتاج ودمج الصوت مع الفيديو...")
  final_video = merge_audio_video(
      background_video="test.mp4",
      audio_file="voice.mp3",
      output_video="final_video.mp4",
  )

  if not final_video or not os.path.exists(final_video):
    print("\n❌ تعذر إكمال العمل لعدم وجود الفيديو النهائي المدمج.")
    return

  # 4. قراءة السكريبت لاستخدامه في وصف الفيديو
  video_title = "سَبِيلُ الرُّشْدِ | آية وتدبر"
  video_desc = (
      "محتوى دعوي آلي تم توليده ونشره تلقائياً لـ قناة «سَبِيلُ"
      " الرُّشْدِ».\n\n#سبيل_الرشد #Shorts #إسلاميات #قرآن"
  )

  if os.path.exists("today_script.txt"):
    with open("today_script.txt", "r", encoding="utf-8") as f:
      content = f.read()
      video_desc = f"{content[:350]}...\n\n#سبيل_الرشد #Shorts #إسلاميات #قرآن"

  # 5. النشر الآلي على يوتيوب
  print("\n📤 [الخطوة 4/4]: جاري الرفع والنشر المباشر على يوتيوب...")
  upload_to_youtube(
      file_path=final_video,
      title=video_title,
      description=video_desc,
      privacy="private",  # يمكنك جعلها 'public' للنشر المباشر للجمهور
  )


if __name__ == "__main__":
  run_full_pipeline()