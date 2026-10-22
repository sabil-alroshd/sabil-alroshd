import os
import json
from moviepy import CompositeVideoClip, TextClip, VideoFileClip

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False


def add_text_overlay_to_video(
    input_video="final_video.mp4",
    text_content="اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",
    output_video="final_video_with_text.mp4",
):
    """مكتبة التعديل المتقدم: تركيب النصوص القرآنية كلمة بكلمة بالتزامن الحي وبدون تداخل أو انعكاس"""
    print("🎨 [مكتبة التعديل المتقدم]: جاري معالجة وتراكب النصوص المتزامنة على الفيديو...")

    if not os.path.exists(input_video):
        print(f"❌ لم يتم العثور على الفيديو الأساسي [{input_video}]")
        return input_video

    try:
        video = VideoFileClip(input_video)

        # التحقق من مسارات الخطوط العربية المتاحة
        font_paths = [
            "assets/fonts/Amiri-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
        ]
        font_path = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_path = fp
                break

        # معالجة النص العربي لضمان ظهوره بشكل صحيح غير مقلوب (RTL)
        processed_text = text_content
        if ARABIC_SUPPORT:
            try:
                reshaped = arabic_reshaper.reshape(text_content)
                processed_text = get_display(reshaped)
            except Exception:
                pass

        # تقسيم النص إلى كلمات أو عبارات متتابعة للتزامن
        words = [w.strip() for w in processed_text.split() if w.strip()]
        if not words:
            words = [processed_text]

        num_words = len(words)
        word_duration = video.duration / num_words if num_words > 0 else video.duration

        text_clips = []

        for i, word in enumerate(words):
            start_time = i * word_duration
            curr_dur = word_duration if i < num_words - 1 else (video.duration - start_time)

            txt_clip = (
                TextClip(
                    text=word,
                    font_size=48,
                    color="white",
                    font=font_path if font_path else "Arial",
                    size=(int(video.w * 0.85), int(video.h * 0.25)),
                    method="caption",
                )
                .with_position(("center", "center"))
                .with_start(start_time)
                .with_duration(curr_dur)
            )
            text_clips.append(txt_clip)

        # دمج الفيديو الأصلي مع طبقات النصوص المتزامنة دون ازدواجية ضارة
        final_composite = CompositeVideoClip([video] + text_clips)
        final_composite.write_videofile(
            output_video,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="fast",
        )

        print(f"✅ [التعديل المتقدم]: تم تركيب النصوص المتزامنة وتصدير الفيديو بنجاح: {output_video}")
        return output_video

    except Exception as e:
        print(
            f"⚠️ تنبيه أثناء إضافة النص (سيتم الحفاظ على الفيديو الأساسي): {e}"
        )
        return input_video


if __name__ == "__main__":
    add_text_overlay_to_video()