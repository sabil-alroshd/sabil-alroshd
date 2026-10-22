import os
import random
import requests

# قائمة بروابط أرشيفية مباشرة لأجمل المحافل الخارجية والتلاوات الخاشعة
LIVE_CONCERTS_ARCHIVE = [
    {
        "reciter": "الشيخ محمد صديق المنشاوي",
        "title": "حفل خارجي نادر - سورة الحشر",
        "url": "https://archive.org/download/Minshawy_Live_Concerts/059_Hashr.mp3",
    },
    {
        "reciter": "الشيخ عبد الباسط عبد الصمد",
        "title": "مقطع من محفل خارجي شهير - سورة التكوير",
        "url": "https://archive.org/download/Abdulbasit_Live_Concerts/081_Takweer.mp3",
    },
    {
        "reciter": "الشيخ خالد الجليل",
        "title": "تلاوة خاشعة من صلاة التراويح",
        "url": "https://server10.mp3quran.net/jleel/036.mp3",
    },
]


class LiveConcertsAgent:
  """وكيل جلب واقتصاص المحافل الخارجية والتلاوات الخاشعة آلياً"""

  def __init__(self):
    print(
        "🎙️ [وكيل المحافل الخارجية]: تم التفعيل والربط مع أرشيف المحافل"
        " المفتوح."
    )

  def fetch_and_clip_live_segment(self, output_audio="voice.mp3"):
    """جلب حفل خارجي واقتصاص مقطع خاشع منه تلقائياً"""
    chosen_concert = random.choice(LIVE_CONCERTS_ARCHIVE)
    print(
        f"🔍 [الأرشيف]: تم اختيار ({chosen_concert['reciter']}) -"
        f" {chosen_concert['title']}..."
    )

    try:
      # جلب المقطع الصوتي من منصة الأرشيف
      response = requests.get(chosen_concert["url"], stream=True)
      if response.status_code == 200:
        temp_full_audio = "temp_concert.mp3"
        with open(temp_full_audio, "wb") as f:
          for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
              f.write(chunk)

        # اقتصاص دقيقة واحدة خاشعة تلقائياً من المحفل للمونتاج
        # (يمكن استخدام pydub أو moviepy لاقتصاص المقطع بدقة)
        from moviepy import AudioFileClip

        full_clip = AudioFileClip(temp_full_audio)
        # اقتصاص مقطع مميز بمدة 45 ثانية من وسط المحفل
        start_time = min(30, max(0, full_clip.duration - 50))
        end_time = min(start_time + 45, full_clip.duration)

        sub_clip = full_clip.subclipped(start_time, end_time)
        sub_clip.write_audiofile(output_audio)

        # مسح الملف المؤقت الحفل الكامل
        full_clip.close()
        if os.path.exists(temp_full_audio):
          os.remove(temp_full_audio)

        print(
            f"✅ [نجاح الاقتصاص]: تم سحب واقتصاص المقطع بنجاح من محفل"
            f" {chosen_concert['reciter']}!"
        )
        return {
            "reciter": chosen_concert["reciter"],
            "title": chosen_concert["title"],
            "audio": output_audio,
        }

    except Exception as e:
      print(f"❌ حدث خطأ أثناء سحب المحفل: {e}")
      return None


if __name__ == "__main__":
  agent = LiveConcertsAgent()
  agent.fetch_and_clip_live_segment()