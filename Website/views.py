import os, sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from datetime import date
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from .models import Note, file, User, assigns, ClassSchedule
from .__init__ import scrape_updates
from . import db 
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note-todo')
        if(len(note) < 1):
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')

    today = date.today()
    class_list = []
    
    classes = ClassSchedule.query.filter_by(date=today).all()
    class_list = [{
            'id': c.id,
            'date': str(c.date),
            'time': (c.time),
            'class_name': c.class_name,
            'instructor': c.instructor
        } for c in classes]
    updates = scrape_updates()

    return render_template("home.html", user=current_user, class_list=class_list, date=today.strftime("%d-%m-%Y"),updates=updates)


@views.route('/refresh_notice',methods=['POST'])
def refresh():
    updates = scrape_updates()
    today = date.today()
    class_list = []
    
    classes = ClassSchedule.query.filter_by(date=today).all()
    class_list = [{
            'id': c.id,
            'date': str(c.date),
            'time': (c.time),
            'class_name': c.class_name,
            'instructor': c.instructor
        } for c in classes]
    return render_template("home.html", user=current_user,class_list=class_list, date=today.strftime("%d-%m-%Y"), updates=updates)

@views.route('/canvas')
def embedded():
    return render_template('canvas.html')

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})


@views.route('/delete-file/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
        file_data = json.loads(request.data)
        f = file.query.get(file_id)
        if f and f.user_id == current_user.id:
            db.session.delete(f)
            file_path = os.path.join('uploads/', f.author)
            os.remove(file_path)
            db.session.commit()
            
            flash("Deleted Successfully", category="success")
        else:
            flash("Error", category="failure")


@views.route('/upload-pdf-note', methods=['POST'])
def upload_note():
    
    if 'file' in request.files:
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join('uploads', filename))

        new_file = file(author=filename, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        flash('Note Uploaded!', category='success')
        
    else:
        flash("No File Selected", category='failure')
   
    return redirect(url_for('views.home'))


@views.route('/notes')
@login_required
def library():
    pdf_files = file.query.all()
    return render_template('library.html',user=current_user, pdf_files=pdf_files, User=User)

@views.route('/download-pdf/<filename>')
def download_pdf(filename):
    path = 'D:/Arshnoor/Almanac/uploads/' + filename
    return send_file(path, as_attachment=True)


@views.route('/assignments')
def assignments():
    return render_template('assignments.html', user=current_user, all_users = User, assigns = assigns.query.all())

@views.route('/publish-assign', methods=['POST'])
def new_assignemnt():
    title = request.form.get('title')
    date = datetime.strptime(request.form.get('deadline'), '%Y-%m-%d') 
    subject = request.form.get('subject')
    description = request.form.get('description')

    new = assigns(title=title, deadline=date, description=description, subject=subject, user_id=current_user.id)
    db.session.add(new)
    db.session.commit()
    flash('Assignment Published!', category='success')

    return redirect(url_for('views.assignments'))
