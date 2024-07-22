import os
from flask import Flask, render_template, request, redirect, send_file
from google.cloud import storage
from google.oauth2 import service_account

app = Flask(__name__)

# Configuration (Replace placeholders)
BUCKET_NAME = 'processed_data112' 
PROJECT_ID = 'bold-camera-429007-i5'
SERVICE_ACCOUNT_JSON = 'C:/Users/tharu/Downloads/bold-camera-429007-i5-91902b197d30.json'

# Authentication (Dummy for this example)
DUMMY_USERNAME = 'tharun123'
DUMMY_PASSWORD = '12345'

# Cloud Storage Client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON
)
storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == DUMMY_USERNAME and request.form['password'] == DUMMY_PASSWORD:
            return redirect('/reports')
    return render_template('login.html')

@app.route('/reports')
def reports():
    blobs = bucket.list_blobs()
    return render_template('reports.html', blobs=blobs)

@app.route('/download/<filename>')
def download(filename):
    blob = bucket.blob(filename)
    return send_file(blob.download_as_bytes(), download_name=filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 
