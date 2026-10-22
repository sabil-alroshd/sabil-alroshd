import json
import os
import random
import requests

LAST_USED_FILE = "last_used.json"

try:
  from competitor_agent import CompetitorTrendAgent

  TREND_AGENT_AVAILABLE = True
except ImportError:
  TREND_AGENT_AVAILABLE = False


class SmartClipperAgent:

  def __init__(self):
    print(
        "✂️ [وكيل الموسوعة القرآنية المتقدم]: جاهز بالربط الهرمي المتعدد"
        " (Quran.com, AlQuran.Cloud, والمحافل القرآنية)."
    )

  def _load_memory(self):
    if os.path.exists(LAST_USED_FILE):
      try:
        with open(LAST_USED_FILE, "r", encoding="utf-8") as f:
          return json.load(f)
      except Exception:
        pass
    return {"used_passages": []}

  def _save_memory(self, memory):
    try:
      with open(LAST_USED_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)
    except Exception:
      pass

  def _clean_old_audio_files(self):
    """تنظيف جميع بقايا الملفات الصوتية القديمة لمنع تداخل القراء"""
    target_files = [
        "voice.mp3",
        "temp_quran_audio.mp3",
        "final_audio.mp3",
        "final_short_videoTEMP_MPY_wvf_snd.mp4",
        "final_long_videoTEMP_MPY_wvf_snd.mp4",
    ]
    for f_path in target_files:
      if os.path.exists(f_path):
        try:
          os.remove(f_path)
        except Exception:
          pass

  def fetch_and_prepare_best_segment(self, content_type="quran"):
    """الموسوعة القرآنية الكبرى: نظام البحث والتدوير الهرمي عبر عدة سيرفرات ومصادر (Quran.com -> AlQuran.Cloud -> المحافل)"""

    # تنظيف الملفات القديمة فور دخول الدالة قبل بدء التجهيز
    self._clean_old_audio_files()

    # موسوعة القراء مع تحديد هوياتهم وسيرفراتهم المختلفة
    reciters = [
        {
            "id": "ar.abdulbasit",
            "name": "الشيخ عبد الباسط عبد الصمد (مرتل)",
            "quran_cloud_id": "ar.abdulbasit",
        },
        {
            "id": "ar.minshawi",
            "name": "الشيخ محمد صديق المنشاوي (مرتل)",
            "quran_cloud_id": "ar.minshawi",
        },
        {
            "id": "ar.mustafaismail",
            "name": "الشيخ مصطفى إسماعيل",
            "quran_cloud_id": "ar.mustafaismail",
        },
        {
            "id": "ar.ahmedanees",
            "name": "الشيخ أحمد نعينع",
            "quran_cloud_id": "ar.ahmedanees",
        },
        {
            "id": "ar.mahmoudbana",
            "name": "الشيخ محمود علي البنا",
            "quran_cloud_id": "ar.mahmoudbana",
        },
        {
            "id": "ar.husary",
            "name": "الشيخ محمود خليل الحصري",
            "quran_cloud_id": "ar.husary",
        },
        {
            "id": "ar.alafasy",
            "name": "الشيخ مشاري العفاسي",
            "quran_cloud_id": "ar.alafasy",
        },
        {
            "id": "ar.sudais",
            "name": "الشيخ عبد الرحمن السديس",
            "quran_cloud_id": "ar.sudais",
        },
        {
            "id": "ar.shuraim",
            "name": "الشيخ سعود الشريم",
            "quran_cloud_id": "ar.shuraim",
        },
        {
            "id": "ar.yasseraldosari",
            "name": "الشيخ ياسر الدوسري",
            "quran_cloud_id": "ar.yasseraldosari",
        },
        {
            "id": "ar.mahermuaiqly",
            "name": "الشيخ ماهر المعيقلي",
            "quran_cloud_id": "ar.mahermuaiqly",
        },
        {
            "id": "ar.khalidjaleel",
            "name": "الشيخ خالد الجليل",
            "quran_cloud_id": "ar.khalidjaleel",
        },
        {
            "id": "ar.saadghamdi",
            "name": "الشيخ سعد الغامدي",
            "quran_cloud_id": "ar.saadghamdi",
        },
        {
            "id": "ar.muhammadayyoub",
            "name": "الشيخ محمد أيوب",
            "quran_cloud_id": "ar.muhammadayyoub",
        },
    ]

    # جلب التوصية الذكية من وكيل التريندات والمناسبات
    target_surah_info = None
    if TREND_AGENT_AVAILABLE:
      try:
        trend_agent = CompetitorTrendAgent()
        rec = trend_agent.get_smart_content_recommendation()
        if rec and "recommended_surah" in rec:
          target_surah_info = rec["recommended_surah"]
          print(f"🎯 [استلام التوصية الذكية]: الاعتماد على {rec.get('theme')}")
      except Exception as e:
        print(f"⚠️ تنبيه أثناء جلب التوصية: {e}")

    fallback_passages = [
        {"surah": 67, "start": 1, "end": 6, "name": "سورة الملك"},
        {"surah": 55, "start": 1, "end": 15, "name": "سورة الرحمن"},
        {"surah": 36, "start": 1, "end": 12, "name": "سورة يس"},
        {"surah": 18, "start": 1, "end": 10, "name": "سورة الكهف"},
        {"surah": 89, "start": 15, "end": 30, "name": "سورة الفجر"},
        {"surah": 56, "start": 1, "end": 16, "name": "سورة الواقعة"},
        {"surah": 94, "start": 1, "end": 8, "name": "سورة الشرح"},
        {"surah": 13, "start": 28, "end": 29, "name": "سورة الرعد (الطمأنينة)"},
    ]

    max_attempts = 15
    attempt = 0

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }

    while attempt < max_attempts:
      attempt += 1
      # إعادة التأكيد على تنظيف أي آثار صوتية قبل كل محاولة اختيار جديدة
      self._clean_old_audio_files()

      memory = self._load_memory()
      used_passages = memory.get("used_passages", [])

      if target_surah_info and attempt == 1:
        surah_num = target_surah_info["surah"]
        start_ayah = target_surah_info["start"]
        end_ayah = target_surah_info["end"]
        passage_name = f"سورة {surah_num} ({start_ayah}-{end_ayah})"
      else:
        chosen_p = random.choice(fallback_passages)
        surah_num = chosen_p["surah"]
        start_ayah = chosen_p["start"]
        end_ayah = chosen_p["end"]
        passage_name = chosen_p.get(
            "name", f"سورة {surah_num} ({start_ayah}-{end_ayah})"
        )

      chosen_reciter = random.choice(reciters)
      passage_key = f"{passage_name}_{chosen_reciter['id']}"

      if passage_key in used_passages[-5:]:
        continue

      print(
          f"🔄 [محاولة {attempt}]: جلب {passage_name} بصوت الشيخ"
          f" {chosen_reciter['name']} عبر التسلسل الهرمي..."
      )

      audio_chunks = []
      texts = []
      fetch_failed = False

      for ayah_num in range(start_ayah, end_ayah + 1):
        ayah_success = False

        # ----------------------------------------------------
        # المصدر الأول: API موقع Quran.com
        # ----------------------------------------------------
        try:
          quran_com_url = f"https://api.quran.com/api/v4/verses/by_key/{surah_num}:{ayah_num}?words=false"
          res = requests.get(quran_com_url, headers=headers, timeout=10).json()
          if "verse" in res:
            ayah_text = res["verse"].get("text_uthmani", "")
            audio_url = f"https://verses.quran.com/Alafasy/mp3/{surah_num:03d}{ayah_num:03d}.mp3"
            audio_res = requests.get(audio_url, headers=headers, timeout=10)
            if audio_res.status_code == 200 and len(audio_res.content) > 1000:
              audio_chunks.append(audio_res.content)
              texts.append(ayah_text)
              ayah_success = True
        except Exception:
          pass

        # ----------------------------------------------------
        # المصدر الثاني: AlQuran.Cloud
        # ----------------------------------------------------
        if not ayah_success:
          try:
            url_cloud = f"http://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/{chosen_reciter['quran_cloud_id']}"
            res_cloud = requests.get(
                url_cloud, headers=headers, timeout=15
            ).json()
            if res_cloud.get("code") == 200:
              data = res_cloud["data"]
              audio_url = data["audio"]
              ayah_text = data["text"]

              audio_res = requests.get(audio_url, headers=headers, timeout=15)
              if (
                  audio_res.status_code == 200
                  and len(audio_res.content) > 1000
              ):
                audio_chunks.append(audio_res.content)
                texts.append(ayah_text)
                ayah_success = True
          except Exception:
            pass

        # ----------------------------------------------------
        # المصدر الثالث: EveryAyah
        # ----------------------------------------------------
        if not ayah_success:
          try:
            everyayah_url = f"https://everyayah.com/data/Abdul_Basit_Murattal_192kbps/{surah_num:03d}{ayah_num:03d}.mp3"
            audio_res = requests.get(
                everyayah_url, headers=headers, timeout=15
            )
            if audio_res.status_code == 200 and len(audio_res.content) > 1000:
              texts.append(f"آية {ayah_num} من سورة {surah_num}")
              audio_chunks.append(audio_res.content)
              ayah_success = True
          except Exception:
            pass

        if not ayah_success:
          fetch_failed = True
          break

      if (
          fetch_failed
          or not audio_chunks
          or len(audio_chunks) != (end_ayah - start_ayah + 1)
      ):
        print(
            "❌ تعذر استكمال الحزمة عبر التسلسل الهرمي، جاري البدء من الصفر..."
        )
        continue

      audio_file = "voice.mp3"
      combined_audio = bytearray()
      for chunk in audio_chunks:
        combined_audio.extend(chunk)

      # كتابة نظيفة ومستقلة لملف الصوت النظيف
      with open(audio_file, "wb") as f:
        f.write(combined_audio)

      if not os.path.exists(audio_file) or os.path.getsize(audio_file) < 5000:
        print("❌ الملف الصوتي غير سليم، البدء من الصفر...")
        continue

      used_passages.append(passage_key)
      if len(used_passages) > 15:
        used_passages.pop(0)
      memory["used_passages"] = used_passages
      self._save_memory(memory)

      full_text = " \n ".join(texts)
      print(
          f"✅ [تم بنجاح عبر التسلسل الهرمي]: {passage_name} بصوت الشيخ"
          f" {chosen_reciter['name']}"
      )

      return {
          "audio_file": audio_file,
          "text": full_text,
          "title": (
              f"تلاوة خاشعة | {passage_name} بصوت الشيخ {chosen_reciter['name']}"
          ),
          "reciter": chosen_reciter["name"],
      }

    print("❌ تعذر إيجاد أو تحميل مقطع صوتي عبر جميع مصادر الموسوعة الهرمية.")
    return None


if __name__ == "__main__":
  agent = SmartClipperAgent()
  data = agent.fetch_and_prepare_best_segment()
  print("نتيجة الاختبار:", data)