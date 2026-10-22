import random
import re
import requests


def get_ayah_tafsir(verse_key="2:255", tafsir_id=169):
  """جلب التفسير المعتمد للآية الكريمة (مثل تفسير السعدي) من Quran.com API"""
  # معرف 169 يمثل تفسير السعدي الميسر والموثق
  url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_key/{verse_key}"
  print(f"📚 جاري جلب التفسير المعتمد للآية ({verse_key})...")

  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      tafsir_text = data.get("tafsir", {}).get("text", "")
      # تنظيف وسوم HTML إن وجدت ليكون النص نقياً
      clean_text = re.sub("<.*?>", "", tafsir_text)
      return clean_text
    print("❌ تعذر جلب التفسير.")
    return None
  except Exception as e:
    print(f"❌ خطأ في الاتصال بـ API التفاسير: {e}")
    return None


def get_daily_adhkar():
  """جلب ذكر أو دعاء من حصن المسلم والأذكار اليومية المأثورة"""
  url = "https://raw.githubusercontent.com/nawafalqari/azkar-api/main/azkar.json"
  print("📿 جاري جلب الأذكار والأدعية اليومية...")

  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      categories = list(data.keys())
      if categories:
        # اختيار قسم عشوائي من الأذكار (مثل أذكار الصباح، المساء، الاستغفار)
        random_category = random.choice(categories[:10])
        items = data[random_category]
        if items:
          random_item = random.choice(items)
          return {
              "category": random_category,
              "content": random_item.get("content", ""),
              "description": random_item.get("description", ""),
          }
    print("❌ تعذر جلب الأذكار.")
    return None
  except Exception as e:
    print(f"❌ خطأ في جلب الأذكار: {e}")
    return None


if __name__ == "__main__":
  # اختبار جلب التفسير
  tafsir = get_ayah_tafsir("2:255", 169)
  if tafsir:
    print(f"\n📖 التفسير:\n{tafsir[:350]}...\n")

  # اختبار جلب الأذكار
  dhikr = get_daily_adhkar()
  if dhikr:
    print(f"\n📿 القسم: {dhikr['category']}")
    print(f"📝 النص: {dhikr['content']}")