import time
from google import genai
import requests

# مفتاح API الخاص بك
api_key = "AQ.Ab8RN6L--iqENEF4tyCQ2nzSAwQXg4V6HezsUC5nAQh9vXIiKg"
client = genai.Client(api_key=api_key)


def get_verified_quran_verse(surah_num, ayah_num):
  """جلب الآية بدقة تامة وبدون خطأ إملائي من المصدر الموثوق (Quran.com API)"""
  url = f"https://api.quran.com/api/v4/verses/by_key/{surah_num}:{ayah_num}?fields=text_uthmani"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()["verse"]["text_uthmani"]
    return "آية كريمة من القرآن الكريم."
  except Exception:
    return "آية من كتاب الله."


def run_sabil_agents_team():
  # جلب آية موثقة برمجياً (سورة البقرة - الآية 286 كعينة)
  verse = get_verified_quran_verse(2, 286)

  prompt = f"""
    أنت مدير نظام فريق وكلاء قناة "سبيل الرشد". 
    الآية الموثوقة لعمل اليوم من المصدر الرسمي: "{verse}"
    
    قم بما يلي:
    1. جهّز سكريبت فيديو قصير (Shorts) يومي بمقدمة خطّافة وجذابة في أول 3 ثوانٍ.
    2. صغ فكرة ومحاور فيديو طويل (لسلسلة كل يومين).
    3. صغ منشوراً تفاعلياً لمنتدى القناة لزيادة مشاركة المتابعين.
    """

  print("🤖 جاري تشغيل فريق وكلاء قناة 'سبيل الرشد'...")

  # محاولة التوليد مع إعادة المحاولة الذكية عند ضغط السيرفر
  for attempt in range(1, 4):
    try:
      response = client.models.generate_content(
          model="gemini-3.8-flash", contents=prompt
      )

      output_filename = "today_script.txt"
      with open(output_filename, "w", encoding="utf-8") as f:
        f.write(response.text)

      print(
          f"\n✅ تم حفظ تقرير وسكريبتات اليوم بنجاح في الملف: {output_filename}"
      )
      print(
          "💡 يمكنك فتح الملف لقراءة النص العربي المنسق والواضح تماماً."
      )
      break

    except Exception as e:
      print(
          f"⚠️ محاولة {attempt} من 3: حدث تنبيه أثناء الاتصال بالنموذج:"
          f" {e}"
      )
      if attempt < 3:
        time.sleep(5)
      else:
        print("❌ تعذر الاستجابة بعد 3 محاولات.")


# اختصار للتوافق التام مع خط الإنتاج الآلي sabil_auto_pipeline.py
def run_sabil_agent():
  run_sabil_agents_team()


if __name__ == "__main__":
  run_sabil_agents_team()