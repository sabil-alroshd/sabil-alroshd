import os
import requests

# قائمة القراء الشاملة (تشمل القراء الرسميين وعمالقة دولة التلاوة والمحافل)
QURAN_RECITERS = {
    # 1. كبار القراء والمحدثين عبر API الرسمي
    "alafasy": {
        "name": "مشاري راشد العفاسي",
        "type": "api",
        "server": "https://api.alquran.cloud/v1/ayah/{}/ar.alafasy",
    },
    "minshawi": {
        "name": "محمد صديق المنشاوي (مرتل)",
        "type": "api",
        "server": "https://api.alquran.cloud/v1/ayah/{}/ar.minshawi",
    },
    "sudais": {
        "name": "عبد الرحمن السديس",
        "type": "api",
        "server": "https://api.alquran.cloud/v1/ayah/{}/ar.sudais",
    },
    "abdulbasit": {
        "name": "عبد الباسط عبد الصمد (مرتل)",
        "type": "api",
        "server": "https://api.alquran.cloud/v1/ayah/{}/ar.abdulbasit",
    },
    "ghamdi": {
        "name": "سعد الغامدي",
        "type": "api",
        "server": "https://api.alquran.cloud/v1/ayah/{}/ar.shaatree",
    },
    # 2. عمالقة دولة التلاوة المصرية والمحافل الخالدة (روابط أرشيفية ومباشرة)
    "rifaat": {
        "name": "الشيخ محمد رفعت (أسطورة القراء)",
        "type": "archive",
        "server": "https://everyayah.com/data/Mohamed_Rifaat_128kbps/{}.mp3",
    },
    "bahtimi": {
        "name": "الشيخ كامل يوسف البهتيمي",
        "type": "archive",
        "server": "https://everyayah.com/data/Bahtimi_128kbps/{}.mp3",
    },
    "nainaa": {
        "name": "الشيخ أحمد نعينع",
        "type": "archive",
        "server": "https://everyayah.com/data/Ahmed_Nainaa_128kbps/{}.mp3",
    },
    "khaled_jalil": {
        "name": "الشيخ خالد الجليل (تلاوات خاشعة)",
        "type": "archive",
        "server": "https://server10.mp3quran.net/jleel/{}.mp3",
    },
}


def get_verified_ayah_text(verse_key="2:255"):
  """جلب النص العثماني الموثق للآية من Quran.com API"""
  url = f"https://api.quran.com/api/v4/verses/by_key/{verse_key}?fields=text_uthmani"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json().get("verse", {}).get("text_uthmani", "")
  except Exception as e:
    print(f"❌ خطأ في جلب النص: {e}")
  return ""


def get_recitation_audio(verse_key="2:255", reciter_key="alafasy"):
  """جلب التلاوة الصوتية الخاشعة وحفظها كملف صوتي MP3 مع دعم القراء المتميزين"""
  reciter_info = QURAN_RECITERS.get(reciter_key, QURAN_RECITERS["alafasy"])
  print(
      f"🎙️ جاري جلب التلاوة بصوت القارئ: [{reciter_info['name']}] للآية"
      f" ({verse_key})..."
  )

  try:
    if reciter_info["type"] == "api":
      url = reciter_info["server"].format(verse_key)
      response = requests.get(url)
      if response.status_code == 200:
        data = response.json()
        audio_url = data.get("data", {}).get("audio")
        if audio_url:
          audio_data = requests.get(audio_url)
          with open("voice.mp3", "wb") as f:
            f.write(audio_data.content)
          print(f"✅ تم تحميل تلاوة {reciter_info['name']} بنجاح!")
          return "voice.mp3"
    else:
      # لمعالجة القراء الأرشيفيين (مثل الشيخ محمد رفعت والبهتيمي)
      # سيقوم النظام بسحب الملف أو استخدام التلاوة البديلة الخاشعة لضمان عدم توقف المنظومة
      parts = verse_key.split(":")
      surah_num = parts[0].zfill(3)
      ayah_num = parts[1].zfill(3)
      file_code = f"{surah_num}{ayah_num}"

      url = reciter_info["server"].format(file_code)
      response = requests.get(url)
      if response.status_code == 200:
        with open("voice.mp3", "wb") as f:
          f.write(response.content)
        print(f"✅ تم تحميل تلاوة العِزّ والفخر للشيخ {reciter_info['name']}!")
        return "voice.mp3"

    # خطة بديلة (Fallback) في حال تعذر السحب المباشر لتلاوة معينة
    print("⚠️ تعذر جلب المقطع بهذا الصوت، جاري استخدام التلاوة الاحتياطية...")
    fallback_url = QURAN_RECITERS["alafasy"]["server"].format(verse_key)
    fallback_res = requests.get(fallback_url)
    if fallback_res.status_code == 200:
      with open("voice.mp3", "wb") as f:
        f.write(fallback_res.content)
      return "voice.mp3"

    return None
  except Exception as e:
    print(f"❌ حدث خطأ أثناء جلب تلاوة القارئ: {e}")
    return None


if __name__ == "__main__":
  import random

  # اختبار عشوائي متجدد بالكامل
  test_verses = ["2:255", "2:286", "13:28", "94:5"]
  chosen_verse = random.choice(test_verses)
  chosen_reciter = random.choice(list(QURAN_RECITERS.keys()))

  print(f"🧪 [اختبار الملف مباشرة]: جلب الآية {chosen_verse} بصوت {chosen_reciter}")
  text = get_verified_ayah_text(chosen_verse)
  print(f"📖 النص: {text}")
  get_recitation_audio(chosen_verse, chosen_reciter)