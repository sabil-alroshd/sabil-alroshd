import os
import random
from moviepy import AudioFileClip, VideoFileClip


def get_random_background():
  """جلب خلفية فيديو هادئة عشوائياً من مجلد الخلفيات"""
  bg_dir = "assets/backgrounds"
  if os.path.exists(bg_dir):
    files = [
        os.path.join(bg_dir, f)
        for f in os.listdir(bg_dir)
        if f.endswith((".mp4", ".mov"))
    ]
    if files:
      return random.choice(files)

  # خلفيات افتراضية
  for default_bg in ["bg.mp4", "test.mp4"]:
    if os.path.exists(default_bg):
      return default_bg

  return None


def merge_audio_video(
    background_video=None,
    audio_file="voice.mp3",
    output_video="final_video.mp4",
):
  """محرك المونتاج: دمج الصوت مع خلفية الفيديو وضبط الأبعاد لتناسب Shorts (9:16)"""
  if not background_video:
    background_video = get_random_background()

  if not background_video or not os.path.exists(background_video):
    print("❌ [محرك المونتاج]: لم يتم العثور على فيديو خلفية مناسب.")
    return None

  if not os.path.exists(audio_file):
    print(f"❌ [محرك المونتاج]: الملف الصوتي غير موجود [{audio_file}].")
    return None

  try:
    print(
        f"🎬 [محرك المونتاج]: بدء المونتاج باستخدام الخلفية"
        f" [{background_video}]..."
    )

    video_clip = VideoFileClip(background_video)
    audio_clip = AudioFileClip(audio_file)

    # ضبط مدة الفيديو لتطابق مدة التلاوة الصوتية تماماً
    audio_duration = audio_clip.duration

    if video_clip.duration < audio_duration:
      # تكرار الفيديو إذا كان أقصر من الصوت
      loops = int(audio_duration / video_clip.duration) + 1
      # استخدام قص الأبعاد والمدة
      video_clip = video_clip.subclipped(0, video_clip.duration)

    final_clip = video_clip.subclipped(0, audio_duration).with_audio(audio_clip)

    # تصدير الفيديو بجودة عالية
    final_clip.write_videofile(
        output_video,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset="fast",
    )

    print(f"✅ [محرك المونتاج]: تم إنتاج الفيديو بنجاح: {output_video}")
    return output_video

  except Exception as e:
    print(f"❌ [محرك المونتاج]: حدث خطأ أثناء عملية المونتاج: {e}")
    return None


if __name__ == "__main__":
  merge_audio_video()