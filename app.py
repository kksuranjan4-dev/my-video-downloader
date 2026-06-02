from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# වෙබ් පේජ් එක ලෝඩ් කරන කොටස
@app.route('/')
def index():
    return render_template('index.html')

# වීඩියෝ ලින්ක් එක හොයන API එක
@app.route('/api/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'කරුණාකර ලින්ක් එකක් ඇතුලත් කරන්න'}), 400

    # yt-dlp සඳහා සැකසුම් (හොඳම කොලිටි එක ගන්න)
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # වීඩියෝ එකේ විස්තර ගන්නවා (ඩවුන්ලෝඩ් කරන්නේ නෑ)
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            title = info_dict.get('title', 'Video')

            return jsonify({
                'title': title,
                'download_url': video_url
            })
    except Exception as e:
        return jsonify({'error': 'මේ ලින්ක් එකෙන් වීඩියෝ එකක් හොයාගන්න බැහැ!'}), 500

if __name__ == '__main__':
    app.run(debug=True)