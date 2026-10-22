import os
from gtts import gTTS


def generate_audio_from_script(
    script_file="today_script.txt", output_audio="voice.mp3"
):
  """تحويل نص السكريبت إلى ملف صوتي باللغة العربية"""
  if not os.path.exists(script_file):
    print(f"⚠️ لم يتم العثور على ملف السكريبت [{script_file}]")
    return None

  try:
    with open(script_file, "r", encoding="utf-8") as f:
      text = f.read()

    # اقتطاع جزء السكريبت الدعوي للتسجيل الصوتي
    print("🎙️ جاري تحويل النص الدعوي إلى ملف صوتي...")
    tts = gTTS(text=text[:500], lang="ar", slow=False)
    tts.save(output_audio)

    print(f"✅ تم توليد الملف الصوتي بنجاح: {output_audio}")
    return output_audio
  except Exception as e:
    print(f"❌ حدث خطأ أثناء تحويل النص إلى صوت: {e}")
    return None


if __name__ == "__main__":
  generate_audio_from_script()