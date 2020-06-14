from flask import render_template, flash, redirect, url_for, request
from app import app, db, images
from app.forms import UploadForm
from app.models import User, Report, Image
from app.predict import TFLiteObjectDetection
import json, PIL

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            username = form.username.data

            filename = images.save(request.files['image'])
            url = images.url(filename)

            #---------------------

            result = predict(filename)

            #---------------------

            user = User.query.filter_by(username = username).first()
            if user is None: user = User(username = username)

            report = Report(user = user, data = json.dumps(result))

            image = Image(report = report)

            image.image_filename = filename
            image.image_url = url

            db.session.add(user)
            db.session.add(report)
            db.session.add(image)

            db.session.commit()

            flash('User Report for username: {} generated. '.format(form.username.data), 'success')
            return redirect(url_for('report', report_id = report.id))
        else:
            flash_errors(form)
            flash('ERROR! Report was not generated.', 'error')

    return render_template('upload.html', title = 'Upload', form = form)

@app.route('/report/<report_id>', methods=['GET', 'POST'])
def report(report_id):  
    report = Report.query.get(report_id)
    data = json.loads(report.data)
    image = report.image.first()
    user_report = {
        'username': report.user.username,
        'data': data,
        'image_url': image.image_url,
        'image_filename': image.image_filename
        }
    return render_template('report.html', title = 'Report', report = user_report)

@app.route('/user/<user_id>')
def user(user_id):
    user = User.query.get(user_id)
    reports = user.reports.all()
    return render_template('user.html', title = 'User', username = user.username, reports = reports)

@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', title = 'Dashboard', users = users)

def predict(image_filename):
    MODEL_FILENAME = 'model.tflite'
    LABELS_FILENAME = 'labels.txt'
    
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]
    od_model = TFLiteObjectDetection(MODEL_FILENAME, labels)

    image = PIL.Image.open('app/static/img/' + image_filename)
    
    return od_model.predict_image(image)