from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, default=0)  # Simulated file size in bytes
    mime_type = db.Column(db.String(100), default="application/octet-stream")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<File {self.filename}>"
