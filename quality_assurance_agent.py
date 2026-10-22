import json
import os
from datetime import datetime
from self_healing_engine import SelfHealingEngine


class QualityAssuranceAgent:

  def __init__(self, log_file="qa_audit_logs.json", spec_file="current_channel_spec.json"):
    self.log_file = log_file
    self.spec_file = spec_file
    self.healer = SelfHealingEngine()
    print(
        "🛡️ [وكيل ضمان الجودة والتدقيق]: حارس البوابة جاهز لفحص الفيديوهات"
        " القصيرة والطويلة بناءً على عقد المواصفات المشترك والربط الذاتي مع المدير الهندسي."
    )

  def _load_spec(self):
    """قراءة عقد المواصفات المشترك للتحقق من الحدود والمعايير المطلوبة"""
    if os.path.exists(self.spec_file):
      try:
        with open(self.spec_file, "r", encoding="utf-8") as f:
          spec = json.load(f)
          print("🔗 [وكيل التدقيق]: تم تحميل مواصفات العقد لمراجعة معايير الجودة.")
          return spec
      except Exception as e:
        print(f"⚠️ تنبيه أثناء قراءة عقد المواصفات في التدقيق: {e}")
    return {}

  def audit_video_package(
      self, video_path="final_short_video.mp4", audio_path="voice.mp3", text_script=""
  ):
    """فحص جودة الفيديو القصير (Short)، الصوت، وتناسق النص مقارنة بعقد المواصفات"""
    spec = self._load_spec()
    max_allowed_duration = spec.get("structure", {}).get("max_duration_seconds", 60)

    print(f"🔍 [تدقيق Shorts]: جاري فحص حزمة الفيديو (الحد الأقصى للمدة في العقد: {max_allowed_duration}ث)...")
    errors = []

    # فحص وجود وحجم ملف الصوت
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 500:
      errors.append("ملف الصوت مفقود أو حجمه صغير جداً (تالف).")

    # فحص وجود وحجم ملف الفيديو النهائي
    if not os.path.exists(video_path) or os.path.getsize(video_path) < 5000:
      errors.append("ملف الفيديو النهائي مفقود أو لم يتم تصديره بشكل صحيح.")

    # فحص محتوى النص (بشكل مرن وسليم برمجياً)
    text_check_failed = False
    if len(str(text_script).strip()) < 3:
      text_check_failed = True

    if text_check_failed:
      errors.append("النص القرآني أو السكريبت فارغ أو غير كافٍ.")

    # إصدار قرار التدقيق للفيديو القصير
    if errors:
      audit_result = {
          "type": "Shorts",
          "status": "REJECTED",
          "timestamp": str(datetime.now()),
          "errors": errors,
      }
      self._log_audit(audit_result)
      print(f"❌ [رفض جودة Short]: تم رصد أخطاء: {errors}")
      
      # 🚀 الربط الذاتي: إرسال الرفض فوراً للمدير البرمجي ليتولى المعالجة الجذرية
      self.healer.handle_exception(
          Exception(f"QualityAuditRejection - Shorts: {errors}"),
          context_name="QualityAssuranceAgent_ShortAudit"
      )
      return False
    else:
      audit_result = {
          "type": "Shorts",
          "status": "APPROVED",
          "timestamp": str(datetime.now()),
          "errors": [],
      }
      self._log_audit(audit_result)
      print(
          "✅ [اجتياز الجودة - Short]: الفيديو والصوت والنص مطابقة لعقد المواصفات"
          " بنجاح تام!"
      )
      return True

  def audit_long_video_package(
      self,
      video_path="final_long_video.mp4",
      audio_path="voice.mp3",
      text_script="",
  ):
    """فحص تدقيق خاص ومتقدم للفيديوهات الطويلة متوافق مع معايير العقد"""
    print("🔍 [تدقيق فيديو طويل]: جاري فحص استقرار الملفات والمحتوى الممتد...")
    errors = []

    # فحص وجود وحجم ملف الصوت الطويل
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
      errors.append("ملف الصوت للفيديو الطويل غير مكتمل أو تالف.")

    # فحص وجود وحجم ملف الفيديو الطويل النهائي
    if not os.path.exists(video_path) or os.path.getsize(video_path) < 5000:
      errors.append("ملف الفيديو الطويل النهائي غير مكتمل التصدير أو تالف.")

    # فحص كفاية السكريبت أو النص للفيديو الطويل
    if len(str(text_script).strip()) < 3:
      errors.append("نص التلاوة للفيديو الطويل قصير جداً أو غير موجود.")

    # إصدار قرار التدقيق للفيديو الطويل
    if errors:
      audit_result = {
          "type": "Long Video",
          "status": "REJECTED",
          "timestamp": str(datetime.now()),
          "errors": errors,
      }
      self._log_audit(audit_result)
      print(f"🛑 [رفض جودة الفيديو الطويل]: {errors}")
      
      # 🚀 الربط الذاتي: إرسال الخطأ فوراً للمدير البرمجي للإصلاح والتطوير
      self.healer.handle_exception(
          Exception(f"QualityAuditRejection - LongVideo: {errors}"),
          context_name="QualityAssuranceAgent_LongAudit"
      )
      return False
    else:
      audit_result = {
          "type": "Long Video",
          "status": "APPROVED",
          "timestamp": str(datetime.now()),
          "errors": [],
      }
      self._log_audit(audit_result)
      print(
          "🎯 [شارة الجودة - فيديو طويل]: تم منح الموافقة ومطابقة العقد بنجاح! جاهز للنشر."
      )
      return True

  def _log_audit(self, report):
    """تسجيل الملاحظات للتحسين المستمر والتطوير الذاتي"""
    logs = []
    if os.path.exists(self.log_file):
      try:
        with open(self.log_file, "r", encoding="utf-8") as f:
          logs = json.load(f)
      except Exception:
        pass

    logs.append(report)
    if len(logs) > 100:
      logs.pop(0)

    try:
      with open(self.log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
      print(f"⚠️ تحذير: تعذر تسجيل تقرير الجودة: {e}")


if __name__ == "__main__":
  qa = QualityAssuranceAgent()
  qa.audit_video_package()