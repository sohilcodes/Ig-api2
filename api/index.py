from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url')
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run()
