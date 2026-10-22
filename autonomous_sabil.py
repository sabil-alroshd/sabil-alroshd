import os
import sys
import time
from ai_agents_intelligence import self_improvement_agent
from auto_editor_agent import AutoEditorAgent
from auto_publisher_agent import AutoPublisherAgent
from community_agent import CommunityAgent
from competitor_agent import CompetitorTrendAgent
from quality_assurance_agent import QualityAssuranceAgent
from smart_clipper_agent import SmartClipperAgent
from url_analyzer_agent import URLChannelAnalyzerAgent
from video_editor_advanced import add_text_overlay_to_video
from quran_sync_agent import QuranSyncAgent  # 👈 استيراد وكيل التزامن والتوقيت الدقيق الجديد


def run_self_improvement_with_retry(retries=3, delay=5):
    """حماية آمنة لوكيل التطوير الذاتي ضد أخطاء الضغط 503 ومشاكل الخادم"""
    for attempt in range(1, retries + 1):
        try:
            print(f"📈 [وكيل التطوير الذاتي]: تقييم الأداء (محاولة {attempt} من {retries})...")
            self_improvement_agent()
            return True
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"⚠️ ضغط مؤقت على الخادم (503). إعادة المحاولة بعد {delay} ثوانٍ...")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"⚠️ تنبيه طارئ لوكيل التطوير الذاتي: {e}")
                break
    print("ℹ️ تم تخطي التحديث الذاتي لهذه الدورة مؤقتاً لضمان استمرار السكربت دون توقف.")
    return False


def run_fully_autonomous_pipeline(
    target_url=None, publish_community=True, publish_short=True, publish_long=True
):
    """دورة الإنتاج والنشر المستقلة والذكية مع إمكانية التحكم الفردي ودعم التزامن القرآني الدقيق"""
    print("🌟 =============================================================== 🌟")
    print("🤖 [أستوديو سبيل الرشد]: بدء دورة الإنتاج والنشر المستقلة والتعليمية (Auto-Pilot)...")
    print("🌟 =============================================================== 🌟")

    # 0. وكيل تحليل الروابط والقنوات
    if target_url:
        print("\n0️⃣ [الخطوة 0]: تحليل أسلوب الرابط أو القناة المستهدفة بناءً على الطلب...")
        try:
            url_agent = URLChannelAnalyzerAgent()
            url_agent.analyze_url_or_channel(target_url)
        except Exception as e:
            print(f"⚠️ [تنبيه وكيل الروابط]: {e}. جاري الاستمرار بالبصمة الافتراضية...")
    else:
        print("\nℹ️ [الخطوة 0]: لم يُحدد رابط جديد، جاري الاعتماد على آخر بصمة أسلوبية مسجلة.")

    # 1. وكيل تحليل التريندات والمنافسين
    print("\n1️⃣ [الخطوة 1]: تحليل أساليب العرض وزوايا الجذب...")
    try:
        trend_agent = CompetitorTrendAgent()
        trend_agent.analyze_and_suggest_hooks()
    except Exception as e:
        print(f"⚠️ [تنبيه التريندات]: {e}. جاري الاستمرار في الدورة...")

    # 2. وكيل منشورات المجتمع والتفاعل اليومي
    if publish_community:
        print("\n2️⃣ [الخطوة 2]: تجهيز ونشر محتوى التفاعل لمنشورات المجتمع...")
        try:
            comm_agent = CommunityAgent()
            comm_agent.publish_community_post()
        except Exception as e:
            print(f"⚠️ [تنبيه المنتدى]: {e}. جاري الاستمرار في الدورة...")
    else:
        print("\n⏭️ [تخطي الخطوة 2]: تم تعطيل منشور المجتمع بناءً على إعدادات هذه الدورة.")

    # ----------------------------------------------------
    # 3. مسار إنتاج ونشر الفيديوهات القصيرة (Shorts)
    # ----------------------------------------------------
    if publish_short:
        print("\n📱 [مسار الفيديوهات القصيرة - Shorts]: جاري بدء عملية الإنتاج والنشر...")
        max_attempts = 10
        attempt = 0
        short_approved = False

        while attempt < max_attempts and not short_approved:
            attempt += 1
            print(f"\n🔄 --- [إنتاج Short رقم {attempt} من أصل {max_attempts}] ---")

            clipper_agent = SmartClipperAgent()
            content_data = clipper_agent.fetch_and_prepare_best_segment(
                content_type="quran"
            )

            if not content_data or not content_data.get("audio_file"):
                print("❌ تعذر تجهيز الحزمة الصوتية للـ Short، إعادة المحاولة...")
                continue

            audio_path = content_data.get("audio_file")
            reciter_name = content_data.get("reciter", "")
            
            # جلب النص المضبوط والمزامن عبر وكيل التزامن الجديد
            sync_agent = QuranSyncAgent()
            surah_id = content_data.get("surah_num", 13)
            start_v = content_data.get("start_ayah", 28)
            end_v = content_data.get("end_ayah", 29)
            
            verified_verses = sync_agent.fetch_verified_ayahs(surah_id, start_v, end_v)
            script_text = " ".join([v["text"] for v in verified_verses]) if verified_verses else content_data.get("text", "")

            editor_agent = AutoEditorAgent()
            base_video = editor_agent.render_final_video(
                audio_file=audio_path,
                text_script=script_text,
                output_video="final_short_video.mp4",
                is_shorts=True,
            )

            if not base_video or not os.path.exists(base_video):
                continue

            final_video = "final_short_processed.mp4"
            try:
                processed_v = add_text_overlay_to_video(
                    input_video=base_video,
                    text_content=script_text,
                    output_video=final_video,
                )
                if processed_v and os.path.exists(processed_v):
                    final_video = processed_v
                else:
                    final_video = base_video
            except Exception:
                final_video = base_video

            # فحص الجودة للفيديو القصير
            qa_agent = QualityAssuranceAgent()
            if qa_agent.audit_video_package(
                video_path=final_video,
                audio_path=audio_path,
                text_script=script_text.strip() if script_text else "تلاوة قرآنية مباركة",
            ):
                short_approved = True
                publisher_agent = AutoPublisherAgent()
                
                # 🌟 التأمين والربط الذكي للعنوان لمنع خطأ العنوان الفارغ
                trend_topic = "تلاوة قرآنية مباركة تطمئن القلوب"
                try:
                    spec_data = editor_agent._load_spec()
                    if spec_data and "latest_trend" in spec_data:
                        trend_topic = spec_data["latest_trend"]
                except Exception:
                    pass

                clean_snippet = script_text[:30].strip().replace("\n", " ") if script_text else trend_topic
                video_title = (
                    f"تلاوة خاشعة بصوت {reciter_name} | {clean_snippet} #Shorts #سبيل_الرشد"
                )
                video_desc = (
                    f"آيات مباركة:\n{script_text}\n\nالقارئ: {reciter_name}\nقناة سبيل الرشد - نأخذكم في رحاب القرآن الكريم."
                )

                url = publisher_agent.publish_video(
                    video_file=final_video,
                    title=video_title,
                    description=video_desc,
                    tags=["قرآن كريم", "تلاوة خاشعة", "Shorts", "سبيل_الرشد", reciter_name],
                )
                if url:
                    run_self_improvement_with_retry()
                    print("🎉 [نجح Short]: تم إنتاج ونشر الفيديو القصير بنجاح!")
                break
    else:
        print("\n⏭️ [تخطي مسار Shorts]: تم تعطيل إنتاج الفيديو القصير بناءً على الإعدادات.")

    # ----------------------------------------------------
    # 4. مسار إنتاج ونشر الفيديوهات الطويلة (Long-form)
    # ----------------------------------------------------
    if publish_long:
        print("\n🎥 [مسار الفيديوهات الطويلة - Long-form]: جاري بدء عملية الإنتاج والنشر...")
        long_approved = False
        attempt_long = 0

        while attempt_long < 5 and not long_approved:
            attempt_long += 1
            print(f"\n🔄 --- [إنتاج فيديو طويل رقم {attempt_long}] ---")

            clipper_agent = SmartClipperAgent()
            content_data = clipper_agent.fetch_and_prepare_best_segment(
                content_type="quran"
            )

            if not content_data or not content_data.get("audio_file"):
                continue

            audio_path = content_data.get("audio_file")
            reciter_name = content_data.get("reciter", "")

            # جلب النص المضبوط للفيديو الطويل
            sync_agent = QuranSyncAgent()
            surah_id = content_data.get("surah_num", 1)
            start_v = content_data.get("start_ayah", 1)
            end_v = content_data.get("end_ayah", 7)
            
            verified_verses = sync_agent.fetch_verified_ayahs(surah_id, start_v, end_v)
            script_text = " ".join([v["text"] for v in verified_verses]) if verified_verses else content_data.get("text", "")

            editor_agent = AutoEditorAgent()
            base_video = editor_agent.render_final_video(
                audio_file=audio_path,
                text_script=script_text,
                output_video="final_long_video.mp4",
                is_shorts=False,
            )

            if not base_video or not os.path.exists(base_video):
                continue

            final_video = "final_long_processed.mp4"
            try:
                processed_v = add_text_overlay_to_video(
                    input_video=base_video,
                    text_content=script_text,
                    output_video=final_video,
                )
                if processed_v and os.path.exists(processed_v):
                    final_video = processed_v
                else:
                    final_video = base_video
            except Exception:
                final_video = base_video

            # فحص الجودة للفيديو الطويل
            qa_agent = QualityAssuranceAgent()
            if qa_agent.audit_long_video_package(
                video_path=final_video,
                audio_path=audio_path,
                text_script=script_text.strip() if script_text else "تلاوة قرآنية مباركة كاملة",
            ):
                long_approved = True
                publisher_agent = AutoPublisherAgent()
                
                trend_topic = "تلاوة تطمئن القلوب"
                try:
                    spec_data = editor_agent._load_spec()
                    if spec_data and "latest_trend" in spec_data:
                        trend_topic = spec_data["latest_trend"]
                except Exception:
                    pass

                video_title = (
                    f"سورة مباركة بتلاوة خاشعة بصوت الشيخ {reciter_name} | {trend_topic}"
                )
                video_desc = (
                    f"تلاوة عطرة:\n{script_text}\n\nالقارئ: {reciter_name}\nقناة سبيل الرشد."
                )

                url = publisher_agent.publish_video(
                    video_file=final_video,
                    title=video_title,
                    description=video_desc,
                    tags=["قرآن كريم", "تلاوة هادئة", "فيديو طويل", "سبيل_الرشد", reciter_name],
                )
                if url:
                    run_self_improvement_with_retry()
                    print("🎉 [نجاح Long]: تم إنتاج ونشر الفيديو الطويل بنجاح!")
                break
    else:
        print("\n⏭️ [تخطي مسار Long-form]: تم تعطيل إنتاج الفيديو الطويل بناءً على الإعدادات.")

    print("\n🏁 [تمت الدورة بنجاح]: اكتملت المهام المحددة لهذا التشغيل.")


if __name__ == "__main__":
    sample_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    run_fully_autonomous_pipeline(
        target_url=sample_url,
        publish_community=True,
        publish_short=True,
        publish_long=False,
    )