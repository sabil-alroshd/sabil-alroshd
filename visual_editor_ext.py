import os
import random


def get_random_background():
  """اختيار خلفية فيديو عشوائية من مجلد الخلفيات المتاح"""
  # افتراض وجود مجلد اسمه assets/backgrounds/
  bg_folder = "assets/backgrounds"

  if os.path.exists(bg_folder):
    bg_files = [
        f
        for f in os.listdir(bg_folder)
        if f.endswith((".mp4", ".mov", ".avi"))
    ]
    if bg_files:
      chosen = random.choice(bg_files)
      print(f"🎬 [مكتبة الوسائط]: تم اختيار الخلفية المرئية: {chosen}")
      return os.path.join(bg_folder, chosen)

  # كبديل افتراضي إذا لم يوجد المجلد
  if os.path.exists("bg.mp4"):
    return "bg.mp4"
  elif os.path.exists("test.mp4"):
    return "test.mp4"

  print("⚠️ تنبيه: لم يتم العثور على ملفات خلفية فيديو، تأكد من توفر bg.mp4")
  return None


if __name__ == "__main__":
  bg = get_random_background()
  print(f"📁 مسار الخلفية المستخدمة: {bg}")