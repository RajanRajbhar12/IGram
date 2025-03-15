from flask import Flask, render_template, request, send_file
import instaloader
import requests
import io
from urllib.parse import quote as url_quote


app = Flask(__name__)

# Create an Instaloader instance
L = instaloader.Instaloader()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ads')
def ads():
    return render_template('ads.txt')

@app.route('/download', methods=['POST'])
def download():
    instagram_url = request.form.get('instagram_url')

    if not instagram_url:
        return "Error: Please provide a valid Instagram URL.", 400

    try:
        # Extract the shortcode from the URL
        shortcode = instagram_url.split("/")[-2]

        # Fetch the post using the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_video:
            # For videos, fetch the video content and send it as a downloadable file
            video_response = requests.get(post.video_url)
            video_stream = io.BytesIO(video_response.content)
            return send_file(
                video_stream,
                as_attachment=True,
                download_name=f'{shortcode}.mp4',
                mimetype='video/mp4'
            )
        else:
            # For images, fetch the image content and send it as a downloadable file
            image_response = requests.get(post.url)
            image_stream = io.BytesIO(image_response.content)
            return send_file(
                image_stream,
                as_attachment=True,
                download_name=f'{shortcode}.jpg',
                mimetype='image/jpeg'
            )

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Failed to download content. Please check the URL and try again.")

if __name__ == '__main__':
    app.run(debug=True)
