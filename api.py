import os
from flask import Flask, make_response, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from gridfs import GridFS
from pymongo import MongoClient
from bson.json_util import dumps
import json

DISEASES_IMAGES_UPLOAD_FOLDER = '/home/duka/thuru_care_v3/tensorflask/diseases_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

client = MongoClient('mongodb://thurucare:thurucare@cluster0-shard-00-00-uaw3w.mongodb.net:27017,cluster0-shard-00-01-uaw3w.mongodb.net:27017,cluster0-shard-00-02-uaw3w.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
db = client.thuru_care
grid_fs = GridFS(db)

app = Flask(__name__, static_url_path ="/static")
app.secret_key = "dukaadsdad383i3DFSDDF5d5FDSF5D4R*DFD#@QW#()*"
app.config['DISEASES_IMAGES_UPLOAD_FOLDER'] = DISEASES_IMAGES_UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Welcome to Python Flask!"

@app.route("/add_diseases", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        if user_name and user_contact:
            status = db.diseases.insert({
                "name" : user_name,
                "contact" : user_contact
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/get_all_diseases", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.diseases.find()
        return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash('file {} saved'.format(file.filename))
            file.save(os.path.join(app.config['DISEASES_IMAGES_UPLOAD_FOLDER'], filename))
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':

    # Initialize the Flask Service
    port = int(os.environ.get('PORT', 9000))
    app.run(host='0.0.0.0', port=port, debug=True)

