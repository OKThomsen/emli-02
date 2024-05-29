from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

def get_dates():
    photos_dir = './photos'
    print(f"Looking for photos in: {photos_dir}")
    return [folder for folder in os.listdir(photos_dir) if os.path.isdir(os.path.join(photos_dir, folder))]

def read_log():
    log_file = './logs/trigger_log.txt'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_entries = f.readlines()
        return log_entries
    return []

@app.route('/')
def index():
    dates = get_dates()
    log_entries = read_log()
    return render_template('index.html', dates=dates, log_entries=log_entries)

@app.route('/photos/<date>')
def view_photos(date):
    photos_dir = os.path.join('./photos', date)
    print(f"Accessing directory: {photos_dir}")
    photos = []
    if os.path.exists(photos_dir):
        for file_name in os.listdir(photos_dir):
            if file_name.endswith('.jpg'):
                photo_path = os.path.join(photos_dir, file_name)
                json_file = os.path.splitext(photo_path)[0] + '.json'
                if os.path.exists(json_file):
                    with open(json_file) as f:
                        metadata = f.read()
                    photos.append({'file_name': f'{date}/{file_name}', 'metadata': metadata})
    else:
        print(f"Directory does not exist: {photos_dir}")
    return render_template('photo_gallery.html', date=date, photos=photos)

@app.route('/photos/<path:filename>')
def serve_photos(filename):
    print(f"Serving photo: {filename}")
    return send_from_directory('photos', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
