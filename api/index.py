import re
import time

def clean_instagram_url(url):
    match = re.search(r"(https://www\.instagram\.com/reel/[^/?]+)", url)
    return match.group(1) if match else url


def fetch_video(api_url, retries=2):
    for i in range(retries):
        try:
            response = HTTP.get(api_url)

            if response and response.status_code == 200:
                return response.json()

        except Exception:
            time.sleep(1)

    return None


try:
    url = message.get('text')

    # ❌ Invalid link check
    if not url or "instagram.com" not in url:
        bot.sendMessage("❌ Please send a valid Instagram Reel link.")
        return

    # 🔥 Clean URL
    clean_url = clean_instagram_url(url)

    bot.sendChatAction(action="typing")
    bot.sendMessage("⏳ Processing your reel...")

    # 🔥 Primary API
    api_url = f"https://ig-api2.vercel.app/api?url={clean_url}"

    data = fetch_video(api_url)

    if data and data.get("status") == "success":
        video_url = data.get("video_url")
        title = data.get("title", "Instagram Reel")

        if not video_url:
            bot.sendMessage("❌ Video not found. Try another link.")
            return

        # 🎥 Send video
        try:
            bot.sendChatAction(action="upload_video")

            bot.sendVideo(
                video=video_url,
                caption=f"🎬 {title}"
            )

        except Exception:
            # ⚠️ If direct send fails → send link fallback
            bot.sendMessage(
                f"⚠️ Video too large or failed to send.\n\nDownload here:\n{video_url}"
            )

    else:
        bot.sendMessage("❌ Failed to fetch video. Try again later.")

except Exception as e:
    bot.sendMessage(f"⚠️ Unexpected error:\n{str(e)}")
