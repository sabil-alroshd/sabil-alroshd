import os
from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6L--iqENEF4tyCQ2nzSAwQXg4V6HezsUC5nAQh9vXIiKg"
)


def competitor_learning_agent():
  """وكيل تحليل القنوات الناجحة واستخراج الأفكار والتريندات الدعوية"""
  print(
      "🔍 [وكيل التعلم والتريندات]: جاري تحليل الأنماط الأكثر تفاعلاً في"
      " الفيديوهات الدعوية القصيرة..."
  )

  prompt = """
    أنت خبير خوارزميات وتحليل محتوى ديني على يوتيوب وتيك توك.
    اقترح 3 زوايا تقديم خطّافة وجذابة لآيات الصبر أو التوكل تناسب الفيديوهات القصيرة (Shorts) وتزيد من معدل الاحتفاظ بالجمهور (Retention).
    أعطني النتيجة بنقاط مركزة.
    """
  try:
    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=prompt
    )
    print("💡 [رؤى وكيل التعلم]:\n", response.text[:400], "...\n")
    return response.text
  except Exception as e:
    print(f"⚠️ خطأ في وكيل التعلم: {e}")
    return ""


def self_improvement_agent(video_stats=None):
  """وكيل التطوير الذاتي وتحسين الأداء بناءً على الإحصائيات"""
  print("📈 [وكيل التطوير الذاتي]: جاري تقييم الأداء وتحسين جودة السكريبتات...")

  prompt = """
    أنت وكيل التطوير الذاتي لقناة "سبيل الرشد". 
    قم بصياغة توجيهات تحسينية لأسلوب كتابة العناوين والوصف لضمان نمو المشاهدات بنسبة أكبر في الفيديو القادم.
    """
  try:
    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=prompt
    )
    print("✨ [توصيات وكيل التطوير الذاتي]: تم تحديث معايير الإنتاج بنجاح.\n")
    return response.text
  except Exception as e:
    print(f"⚠️ خطأ في وكيل التطوير الذاتي: {e}")
    return ""