import json
import os
import re
import requests


class URLChannelAnalyzerAgent:

  def __init__(self, spec_file="current_channel_spec.json"):
    self.spec_file = spec_file
    print(
        "🔍 [وكيل تحليل الروابط والقنوات]: جاهز لسحب وتحليل أساليب الفيديوهات"
        " والقنوات وترجمتها لمواصفات قياسية."
    )

  def extract_video_id(self, url):
    """استخراج المعرف الخاص بالفيديو من رابط يوتيوب"""
    pattern = r"(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

  def analyze_url_or_channel(self, url):
    """تحليل أسلوب فيديو أو قناة بناءً على الرابط الممرر"""
    print(f"🌐 [جاري التحليل]: فحص واستخراج البصمة الأسلوبية من: {url}")

    # التوزيع الافتراضي للبصمة الأسلوبية المستخرجة (Style Blueprint)
    style_spec = {
        "source_url": url,
        "content_type": "quran_recitation",
        "pacing": "balanced",  # slow, balanced, fast
        "visual_style": {
            "text_layout": "centered_subtitles",
            "font_size": 48,
            "background_query": "peaceful nature clouds sky stars",
            "text_color": "white_with_black_shadow",
        },
        "audio_style": {
            "reciter_type": "hafs_murattal",
            "volume_boost": True,
        },
        "structure": {
            "max_duration_seconds": 60,
            "lines_per_view": 1,
        },
    }

    # إذا كان الرابط لفيديو محدد، نقوم بجلب تفاصيله الأولية
    video_id = self.extract_video_id(url)
    if video_id:
      try:
        # جلب عنوان وبيانات مقطع يوتيوب عبر oEmbed بدون الحاجة لمفاتيح API معقدة
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        res = requests.get(oembed_url, timeout=10)
        if res.status_code == 200:
          data = res.json()
          style_spec["video_title"] = data.get("title", "")
          style_spec["author_name"] = data.get("author_name", "")
          print(f"✅ [تم استخراج البيانات]: {style_spec['video_title']} | القناة: {style_spec['author_name']}")
      except Exception as e:
        print(f"⚠️ تنبيه أثناء جلب تفاصيل الرابط: {e}")

    # حفظ عقد المواصفات المشترك في ملف JSON ليقرأه باقي الوكلاء
    self._save_spec(style_spec)
    return style_spec

  def _save_spec(self, spec_data):
    """حفظ وثيقة المواصفات لاستخدامها عبر الوكلاء المترابطين"""
    try:
      with open(self.spec_file, "w", encoding="utf-8") as f:
        json.dump(spec_data, f, ensure_ascii=False, indent=4)
      print(
          f"📄 [عقد المواصفات]: تم تصدير وثيقة المواصفات بنجاح إلى"
          f" {self.spec_file}"
      )
    except Exception as e:
      print(f"❌ تعذر حفظ وثيقة المواصفات: {e}")

  def get_current_spec(self):
    """قراءة آخر مواصفات تم تحليلها"""
    if os.path.exists(self.spec_file):
      try:
        with open(self.spec_file, "r", encoding="utf-8") as f:
          return json.load(f)
      except Exception:
        pass
    return None


if __name__ == "__main__":
  analyzer = URLChannelAnalyzerAgent()
  # تجربة تحليل رابط فيديو
  test_spec = analyzer.analyze_url_or_channel(
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  )
  print("المواصفات المستخرجة:", test_spec)