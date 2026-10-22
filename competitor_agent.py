import datetime
import json
import os
import random


class CompetitorTrendAgent:

  def __init__(self, spec_file="current_channel_spec.json"):
    self.spec_file = spec_file
    print(
        "🔍 [وكيل التريندات والمنافسين الذكي]: جاهز لتحليل الأنماط والمناسبات"
        " وتوليد التوصيات بناءً على عقد المواصفات."
    )

  def _load_spec(self):
    """قراءة عقد المواصفات المشترك المستخرج من وكيل الروابط"""
    if os.path.exists(self.spec_file):
      try:
        with open(self.spec_file, "r", encoding="utf-8") as f:
          spec = json.load(f)
          print(
              f"🔗 [وكيل التريندات]: تم تحميل مواصفات العقد بنجاح (النوع:"
              f" {spec.get('content_type', 'default')})"
          )
          return spec
      except Exception as e:
        print(f"⚠️ تنبيه أثناء قراءة عقد المواصفات: {e}")
    return {}

  def get_smart_content_recommendation(self):
    """تحليل اليوم والمناسبة الحالية لتحديد أفضل موضوع وآيات ومنشور مجتمع بالتوافق مع العقد"""
    spec = self._load_spec()
    content_type = spec.get("content_type", "quran_recitation")

    today = datetime.datetime.now()
    day_of_week = today.weekday()  # 4 يعني يوم الجمعة في Python

    # إذا كان اليوم هو يوم الجمعة
    if day_of_week == 4:
      friday_topics = [
          {
              "type": "friday_special",
              "recommended_surah": {"surah": 18, "start": 1, "end": 10},
              "theme": "سورة الكهف ونور يوم الجمعة",
              "post_idea": (
                  "✨ **نور ما بين الجمعتين** ✨\n\nلا تنسوا قراءة سورة الكهف"
                  " والصلاة على النبي ﷺ في هذا اليوم المبارك.\n\nاللهم صَلِّ"
                  " وسلم وبارك على نبينا محمد ﷺ 🌿"
              ),
          },
          {
              "type": "friday_salawat",
              "recommended_surah": {"surah": 33, "start": 56, "end": 57},
              "theme": "الصلاة على النبي والآيات المرتبطة بها",
              "post_idea": (
                  "﴿إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ"
                  " ۚ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ"
                  " وَسَلِّمُوا تَسْلِيمًا﴾\n\nأكثروا من الصلاة على الحبيب"
                  " المصطفى ﷺ في يوم الجمعة ❤️"
              ),
          },
          {
              "type": "friday_sunnah",
              "recommended_surah": {"surah": 62, "start": 9, "end": 11},
              "theme": "سورة الجمعة والتذكير بالصلاة والسنن",
              "post_idea": (
                  "من سنن يوم الجمعة المباركة:\n1. الغُسل والتطيب 🧼\n2."
                  " الإكثار بقراءة سورة الكهف 📖\n3. الإكثار من الصلاة على"
                  " النبي ﷺ 📿\n4. تحري ساعة الاستجابة 🤲"
              ),
          },
      ]
      recommendation = random.choice(friday_topics)
      recommendation["content_type"] = content_type
      print(f"💡 [توصية مناسبة اليوم - الجمعة]: {recommendation['theme']}")
    else:
      # باقي أيام الأسبوع: مواضيع الاحتياج النفسي والسكينة
      general_topics = [
          {
              "type": "reassurance",
              "recommended_surah": {"surah": 13, "start": 28, "end": 29},
              "theme": "الطمأنينة وراحة البال",
              "post_idea": (
                  "﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾\n\nإذا تثاقلت"
                  " عليك الهموم، اذكر الله وابتسم.. فكل شيء بأمره سبحانه 🌿"
              ),
          },
          {
              "type": "sustenance_hope",
              "recommended_surah": {"surah": 65, "start": 2, "end": 3},
              "theme": "الرزق والفرج والتيسير",
              "post_idea": (
                  "﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا وَيَرْزُقْهُ مِنْ"
                  " حَيْثُ لَا يَحْتَسِبُ﴾\n\nثق بأن الله سيدبرها لك من حيث لا"
                  " تدري 🌱"
              ),
          },
          {
              "type": "patience_comfort",
              "recommended_surah": {"surah": 94, "start": 1, "end": 8},
              "theme": "سورة الشرح واليسر بعد العسر",
              "post_idea": (
                  "﴿فَإِنَّ مَعَ الْعُسْرِ يُسْرًا • إِنَّ مَعَ الْعُسْرِ"
                  " يُسْرًا﴾\n\nمهما اشتدت الظلمة، يُشرق الفرج قريباً بفضل الله"
                  " ☀️"
              ),
          },
          {
              "type": "mercy_repentance",
              "recommended_surah": {"surah": 39, "start": 53, "end": 54},
              "theme": "سعة رحمة الله والتوبة",
              "post_idea": (
                  "﴿قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ"
                  " لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ﴾\n\nباب التوبة مفتوح"
                  " دائماً، ولا يحجبك عن ربك شيء ✨"
              ),
          },
      ]
      recommendation = random.choice(general_topics)
      recommendation["content_type"] = content_type
      print(f"💡 [توصية الموضوع اليومي]: {recommendation['theme']}")

    # تحديث عقد المواصفات المشترك فوراً ليقرأه بقية وكلاء المنظومة
    try:
      spec["current_daily_topic"] = recommendation["theme"]
      spec["recommended_surah"] = recommendation["recommended_surah"]
      with open(self.spec_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    except Exception:
      pass

    return recommendation

  def analyze_and_suggest_hooks(self):
    return self.get_smart_content_recommendation()


if __name__ == "__main__":
  agent = CompetitorTrendAgent()
  print(agent.get_smart_content_recommendation())