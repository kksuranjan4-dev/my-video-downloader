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

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    # නිවැරදිම absolute path එක ලබා ගැනීම
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_path = os.path.join(base_dir, 'cookies.txt')

    # Cookies ෆයිල් එක තියෙනවාද කියා සර්වර් ලොග්ස් වල පෙන්වීමට
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
