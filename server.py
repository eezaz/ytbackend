from flask import Flask, request, jsonify
import yt_dlp
from flask_cors import CORS
import os  # 🔹 Import os to get the port from the environment

app = Flask(__name__)
CORS(app)  # 🔹 This allows requests from any frontend

@app.route('/get_video', methods=['GET'])
def get_video():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_url = info.get('url')
            
            if video_url:
                return jsonify({"url": video_url})
            else:
                return jsonify({"error": "Failed to fetch video"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))  # 🔹 Use Railway’s assigned port
    app.run(host="0.0.0.0", port=PORT)  # 🔹 Required for Railway
