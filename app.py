import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, File
from werkzeug.utils import secure_filename
import random

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Used for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables within an application context
# This replaces the removed @app.before_first_request decorator
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Create operation - file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get filename from form
        filename = request.form.get('filename')
        
        if not filename:
            flash('Please enter a filename', 'error')
            return redirect(url_for('upload_file'))
        
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(filename)
        
        # Create a simulated file size (random between 1KB and 10MB)
        size = random.randint(1024, 10 * 1024 * 1024)
        
        # Determine mime type based on file extension
        mime_type = "application/octet-stream"  # Default
        if '.' in filename:
            ext = filename.rsplit('.', 1)[1].lower()
            if ext == 'txt':
                mime_type = 'text/plain'
            elif ext in ['jpg', 'jpeg']:
                mime_type = 'image/jpeg'
            elif ext == 'png':
                mime_type = 'image/png'
            elif ext == 'pdf':
                mime_type = 'application/pdf'
        
        # Create a new file record in the database
        new_file = File(filename=filename, size=size, mime_type=mime_type)
        db.session.add(new_file)
        db.session.commit()
        
        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('list_files'))
    
    return render_template('upload.html')

# Read operation - list all files
@app.route('/files')
def list_files():
    files = File.query.all()
    return render_template('files.html', files=files)

# Update operation - modify filename
@app.route('/update/<int:file_id>', methods=['GET', 'POST'])
def update_file(file_id):
    file = File.query.get_or_404(file_id)
    
    if request.method == 'POST':
        new_filename = request.form.get('filename')
        
        if not new_filename:
            flash('Please enter a filename', 'error')
            return redirect(url_for('update_file', file_id=file_id))
        
        # Secure the new filename
        new_filename = secure_filename(new_filename)
        
        # Update the file
        file.filename = new_filename
        db.session.commit()
        
        flash(f'File updated successfully to "{new_filename}"!', 'success')
        return redirect(url_for('list_files'))
    
    return render_template('update.html', file=file)

# Delete operation
@app.route('/delete/<int:file_id>')
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    
    # Store filename for the flash message
    filename = file.filename
    
    # Delete the file
    db.session.delete(file)
    db.session.commit()
    
    flash(f'File "{filename}" deleted successfully!', 'success')
    return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(debug=True)
