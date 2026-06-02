from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'කරුණාකර ලින්ක් එකක් ඇතුලත් කරන්න'}), 400

    # yt-dlp සඳහා සැකසුම් (YouTube App එකක් ලෙස හැසිරීමට සකසා ඇත)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios']  # මෙන්න මේකෙන් බ්ලොක් එක පනිනවා
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/19.10.37 (Linux; U; Android 11; Galaxy S21)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_path = os.path.join(base_dir, 'cookies.txt')

    if os.path.exists(cookie_path):
        print("🟢 COOKIES FILE FOUND AND LOADED SUCCESS!")
        ydl_opts['cookiefile'] = cookie_path
    else:
        print(f"🔴 COOKIES FILE NOT FOUND AT: {cookie_path}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            title = info_dict.get('title', 'Video')

            return jsonify({
                'title': title,
                'download_url': video_url
            })
    except Exception as e:
        print(f"❌ Actual Error: {str(e)}") 
        return jsonify({'error': 'මේ ලින්ක් එකෙන් වීඩියෝ එකක් හොයාගන්න බැහැ!'}), 500

if __name__ == '__main__':
    app.run(debug=True)
