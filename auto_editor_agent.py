from advanced_media_effects import apply_cinematic_fade, optimize_audio_track
import json
import os
import random
import time
import requests
from PIL import Image, ImageDraw, ImageFont

# استيراد MoviePy 2.x المباشر والتأثيرات
from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
)
import moviepy.video.fx as vfx

# استخدام المكتبة الحديثة google.genai
try:
    from google import genai
    from google.genai.errors import APIError

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False


class AutoEditorAgent:

    def __init__(
        self,
        pixabay_api_key="58120140-a6ea6fbae71b028fcb0070500",
        spec_file="current_channel_spec.json",
    ):
        self.pixabay_api_key = pixabay_api_key or os.environ.get(
            "PIXABAY_API_KEY"
        )
        self.spec_file = spec_file

        self.dynamic_bg_queries = [
            "peaceful nature clouds sky stars",
            "stunning mountains sunset calm",
            "green valley river flowing",
            "starry night galaxy space glowing",
            "ocean waves gentle peaceful",
            "forest trees sunlight peaceful"
        ]

        print(
            "🎬 [وكيل المونتاج السينمائي]: جاهز ومزود بنظام المسارات الفريدة وعلاج تكدس النصوص."
        )

    def _load_spec(self):
        """قراءة عقد المواصفات المشترك للتكيف مع أسلوب القناة"""
        if os.path.exists(self.spec_file):
            try:
                with open(self.spec_file, "r", encoding="utf-8") as f:
                    spec = json.load(f)
                    return spec
            except Exception as e:
                print(f"⚠️ تنبيه أثناء قراءة عقد المواصفات في المونتاج: {e}")
        return {}

    def _fetch_pixabay_video(self, query=None, unique_id=""):
        """جلب فيديو خلفية بمسار مؤقت فريد لمنع تداخل الملفات"""
        if not self.pixabay_api_key:
            return None

        if not query:
            spec = self._load_spec()
            visual_style = spec.get("visual_style", {})
            query = visual_style.get("background_query") or random.choice(self.dynamic_bg_queries)

        try:
            print(f"🎥 [Pixabay Video]: البحث عن فيديو خلفية بكلمة: '{query}'...")
            url = f"https://pixabay.com/api/videos/?key={self.pixabay_api_key}&q={requests.utils.quote(query)}&per_page=15&orientation=vertical"
            res = requests.get(url, timeout=12).json()
            hits = res.get("hits", [])
            if hits:
                video_item = random.choice(hits)
                videos = video_item.get("videos", {})
                v_url = (
                    videos.get("medium", {}).get("url")
                    or videos.get("large", {}).get("url")
                    or videos.get("small", {}).get("url")
                )
                if v_url:
                    v_res = requests.get(v_url, timeout=15)
                    if v_res.status_code == 200 and len(v_res.content) > 10000:
                        output_path = f"temp_pixabay_bg_{unique_id}.mp4"
                        with open(output_path, "wb") as f:
                            f.write(v_res.content)
                        return output_path
        except Exception as e:
            print(f"⚠️ [تجاوز Pixabay]: {e}")
        return None

    def _fetch_pexels_open_video(self, query="peaceful nature", unique_id=""):
        try:
            url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&per_page=10&orientation=portrait"
            res = requests.get(url, timeout=8).json()
            if res.get("videos"):
                video = random.choice(res["videos"])
                video_files = video.get("video_files", [])
                for vf in video_files:
                    if vf.get("width") and vf.get("width") >= 720:
                        v_url = vf.get("link")
                        v_res = requests.get(v_url, timeout=12)
                        if v_res.status_code == 200:
                            output_path = f"temp_pexels_bg_{unique_id}.mp4"
                            with open(output_path, "wb") as f:
                                f.write(v_res.content)
                            return output_path
        except Exception:
            pass
        return None

    def _create_text_image(
        self,
        text,
        output_path,
        width=1080,
        height=1920,
        font_size=48,
    ):
        """إنشاء صورة شفافة للسطر في المنتصف مع ضبط الاتجاه العربي"""
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        processed_text = text
        if ARABIC_SUPPORT:
            try:
                reshaped = arabic_reshaper.reshape(text)
                processed_text = get_display(reshaped)
            except Exception:
                pass

        font = None
        font_paths = [
            "arial.ttf",
            "tahoma.ttf",
            "seguiui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        for fp in font_paths:
            try:
                font = ImageFont.truetype(fp, size=font_size)
                break
            except Exception:
                continue
        if not font:
            font = ImageFont.load_default()

        # رسم النص في المنتصف بوضوح تام مع ظل أسود للوضوح البصري
        draw.text((width // 2 + 3, height // 2 + 3), processed_text, font=font, fill=(0, 0, 0, 240), anchor="mm")
        draw.text((width // 2, height // 2), processed_text, font=font, fill=(255, 255, 255, 255), anchor="mm")

        img.save(output_path)
        return output_path

    def _create_subtitles_clips(
        self, text_script, duration, unique_id, width=1080, height=1920, font_size=48
    ):
        """توزيع السطور بمعرفات فريدة وتصحيح ترتيب التدفق لمنع التكدس والمقلوب"""
        raw_lines = [l.strip() for l in text_script.split("\n") if l.strip()]
        if not raw_lines:
            raw_lines = [text_script]

        # 🌟 التصحيح الهيكلي: عكس مصفوفة الأسطر لتسير بالترتيب الصحيح 100%
        raw_lines = raw_lines[::-1]

        time_per_segment = duration / len(raw_lines)
        subtitle_clips = []
        temp_image_paths = []

        for i, line_text in enumerate(raw_lines):
            img_path = f"temp_sub_{unique_id}_{i}.png"
            temp_image_paths.append(img_path)
            self._create_text_image(
                line_text,
                output_path=img_path,
                width=width,
                height=height,
                font_size=font_size,
            )

            start_t = i * time_per_segment
            sub_clip = (
                ImageClip(img_path)
                .with_start(start_t)
                .with_duration(time_per_segment)
            )
            subtitle_clips.append(sub_clip)

        return subtitle_clips, temp_image_paths

    def generate_thumbnail(self, title_text="تلاوة قرآنية مباركة", reciter_name="قناة سبيل الرشد", unique_id=""):
        """توليد صورة مصغرة احترافية للفيديوهات الطويلة برقم فريد"""
        try:
            width, height = 1280, 720
            img = Image.new("RGB", (width, height), (15, 23, 42))
            draw = ImageDraw.Draw(img)

            title_display = title_text
            reciter_display = f"القارئ: {reciter_name}"

            if ARABIC_SUPPORT:
                try:
                    title_display = get_display(arabic_reshaper.reshape(title_text))
                    reciter_display = get_display(arabic_reshaper.reshape(reciter_name))
                except Exception:
                    pass

            font_large, font_small = None, None
            font_paths = ["arial.ttf", "tahoma.ttf", "seguiui.ttf"]
            for fp in font_paths:
                try:
                    font_large = ImageFont.truetype(fp, size=56)
                    font_small = ImageFont.truetype(fp, size=36)
                    break
                except Exception:
                    continue
            if not font_large:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()

            draw.text((width // 2, height // 2 - 40), title_display, font=font_large, fill=(255, 255, 255), anchor="mm")
            draw.text((width // 2, height // 2 + 50), reciter_display, font=font_small, fill=(212, 175, 55), anchor="mm")

            output_path = f"thumbnail_{unique_id}.jpg"
            img.save(output_path)
            print(f"🖼️ [الصورة المصغرة]: تم توليد وتخزين صورة الغلاف بنجاح: {output_path}")
            return output_path
        except Exception as e:
            print(f"⚠️ تعذر توليد الصورة المصغرة: {e}")
            return None

    def render_final_video(
        self,
        audio_file="voice.mp3",
        text_script="بسم الله الرحمن الرحيم",
        is_shorts=True,
        reciter_name="القارئ",
        output_video=None,  # 🌟 معامل اختياري متوافق تماماً مع الاستدعاء الخارجي
    ):
        if not os.path.exists(audio_file):
            print(f"❌ ملف الصوت غير موجود: {audio_file}")
            return None

        # 🌟 توليد معرف فريد لكل جلسة إنتاج لمنع التداخل نهائياً
        unique_id = str(int(time.time()))
        
        if not output_video:
            output_video = f"final_output_{unique_id}.mp4"
        else:
            name, ext = os.path.splitext(output_video)
            output_video = f"{name}_{unique_id}{ext}"

        spec = self._load_spec()
        visual_style = spec.get("visual_style", {})
        bg_query = visual_style.get("background_query", "peaceful nature clouds sky stars")
        font_size = visual_style.get("font_size", 48)

        width, height = (1080, 1920) if is_shorts else (1920, 1080)

        print(f"🎨 [جلسة جديدة - ID: {unique_id}]: خلفية ('{bg_query}') | الوضع: {'Shorts' if is_shorts else 'Long'}")

        try:
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration

            bg_video_path = self._fetch_pixabay_video(query=bg_query, unique_id=unique_id)
            if not bg_video_path:
                bg_video_path = self._fetch_pexels_open_video(query="nature peaceful sky", unique_id=unique_id)

            bg_image_path = None
            if (
                not bg_video_path
                and GEMINI_AVAILABLE
                and os.environ.get("GEMINI_API_KEY")
            ):
                try:
                    client = genai.Client()
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Write a short cinematic visual prompt in English for a peaceful Islamic background based on: {text_script}",
                    )
                    if response and response.text:
                        img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(response.text.strip())}?width={width}&height={height}&nologo=true"
                        img_res = requests.get(img_url, timeout=12)
                        if img_res.status_code == 200:
                            bg_image_path = f"temp_ai_bg_{unique_id}.jpg"
                            with open(bg_image_path, "wb") as f:
                                f.write(img_res.content)
                except Exception:
                    pass

            if bg_video_path and os.path.exists(bg_video_path):
                raw_video = VideoFileClip(bg_video_path).resized(new_size=(width, height))
                video_clip = raw_video.with_effects([vfx.Loop(duration=duration)]) if raw_video.duration < duration else raw_video.subclipped(0, duration)
            elif bg_image_path and os.path.exists(bg_image_path):
                video_clip = ImageClip(bg_image_path).with_duration(duration)
            else:
                video_clip = ColorClip(size=(width, height), color=(15, 23, 42)).with_duration(duration)

            sub_clips, temp_sub_imgs = self._create_subtitles_clips(
                text_script=text_script,
                duration=duration,
                unique_id=unique_id,
                width=width,
                height=height,
                font_size=font_size,
            )

            composite_layers = [video_clip] + sub_clips
            final_clip = (
                CompositeVideoClip(composite_layers, size=(width, height))
                .with_duration(duration)
                .with_audio(audio_clip)
            )

            print("⚡ [المونتاج]: جاري تصدير الفيديو النهائي بالمسار الفريد...")
            final_clip.write_videofile(
                output_video,
                codec="libx264",
                audio_codec="aac",
                fps=24,
                preset="fast",
            )

            # 🌟 توليد الصورة المصغرة آلياً إذا كان الفيديو طويلاً
            if not is_shorts:
                self.generate_thumbnail(title_text=text_script.split("\n")[0], reciter_name=reciter_name, unique_id=unique_id)

            # تنظيف الملفات المؤقتة الخاصة بهذه الجلسة حصراً
            cleanup_files = [
                f"temp_pixabay_bg_{unique_id}.mp4",
                f"temp_pexels_bg_{unique_id}.mp4",
                f"temp_ai_bg_{unique_id}.jpg",
            ] + temp_sub_imgs

            for p in cleanup_files:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass

            print(f"✅ [نجح تام]: تم إنتاج الفيديو بالمعرف الفريد بنجاح: {output_video}")
            return output_video

        except Exception as e:
            print(f"❌ حدث خطأ غير متوقع في المونتاج: {e}")
            return None


if __name__ == "__main__":
    editor = AutoEditorAgent()
    editor.render_final_video()