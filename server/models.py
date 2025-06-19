from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Add validators
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Author name cannot be empty.')
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError("Author name must be unique.")
        return value

    @validates('phone_number')
    def Validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must be a 10-digit number.')
        return value 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validate_title(self, key, value):
        clickbait_phrases = [ "won't believe", "secret", "top", "guess"]
        if not any(phrase in value.lower() for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y (contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess').")
        return value

    @validates('content')
    def validate_content(self, key, value):
        if value and len(value) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return value
    
    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError('Summary must be at most 250 characters long.')
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either "fiction" or "non-fiction".')
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
