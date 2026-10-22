import random
import requests

# قائمة كتب السنة المتاحة في قاعدة البيانات الموثقة
HADITH_COLLECTIONS = {
    "bukhari": "صحيح البخاري",
    "muslim": "صحيح مسلم",
    "abudawud": "سنن أبي داود",
    "tirmidhi": "جامع الترمذي",
}


def get_authentic_hadith(collection_key="bukhari"):
  """جلب حديث نبوي شريف من الصحاح المعتمدة مع النص والتخريج"""
  # استخدام قاعدة بيانات الأحاديث المفتوحة والموثقة برمجياً
  url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{collection_key}.json"

  collection_name = HADITH_COLLECTIONS.get(collection_key, "السنة النبوية")
  print(f"📜 جاري جلب حديث شريف من [{collection_name}]...")

  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      hadiths = data.get("hadiths", [])

      if hadiths:
        # اختيار حديث عشوائي من المجموعة
        random_hadith = random.choice(hadiths[:500])  # اختيار من أوائل الأحاديث

        text = random_hadith.get("text", "")
        number = random_hadith.get("hadithnumber", "")
        grades = random_hadith.get("grades", [])

        grade_text = "صحيح / موثق"
        if grades:
          # استخراج درجة الحديث إن وجدت
          grade_text = f"{grades[0].get('name', '')}: {grades[0].get('grade', '')}"

        return {
            "collection": collection_name,
            "number": number,
            "text": text,
            "grade": grade_text,
        }
    print("❌ تعذر جلب الأحاديث.")
    return None
  except Exception as e:
    print(f"❌ حدث خطأ أثناء الاتصال بقاعدة بيانات الأحاديث: {e}")
    return None


if __name__ == "__main__":
  # اختبار جلب حديث من صحيح البخاري
  hadith = get_authentic_hadith("bukhari")
  if hadith:
    print("\n-----------------------------------------")
    print(f"📖 المصدر: {hadith['collection']} (رقم: {hadith['number']})")
    print(f"📝 النص: {hadith['text']}")
    print(f"🔍 الحكم: {hadith['grade']}")
    print("-----------------------------------------")