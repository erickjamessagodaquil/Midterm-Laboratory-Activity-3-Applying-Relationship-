from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration (Switchable)
db_type = os.environ.get('DB_TYPE', 'sqlite')
if db_type == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
elif db_type == 'postgresql':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/mydatabase')
elif db_type == 'mysql':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@localhost/mydatabase')
else:
    raise ValueError("Invalid DB_TYPE. Must be 'sqlite', 'postgresql' or 'mysql'.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db = SQLAlchemy(app)

# Models
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

# Routes
@app.route('/')
def index():
    authors = Author.query.all()
    return render_template('Read.html', authors=authors)

@app.route('/author/create', methods=['GET', 'POST'])
def create_author():
    if request.method == 'POST':
        name = request.form['name']
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
        flash('Author created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('Create.html', type='Author')

@app.route('/book/create', methods=['GET', 'POST'])
def create_book():
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        book = Book(title=title, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        flash('Book created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('Create.html', authors=authors, type='Book')

@app.route('/author/<int:author_id>')
def read_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)

@app.route('/author/update/<int:author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    author = Author.query.get_or_404(author_id)
    if request.method == 'POST':
        author.name = request.form['name']
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('Update.html', author=author, type='Author')

@app.route('/book/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    authors = Author.query.all()
    if request.method == 'POST':
        book.title = request.form['title']
        book.author_id = request.form['author_id']
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('Update.html', book=book, authors=authors, type='Book')

@app.route('/author/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/author/<int:author_id>/comment', methods=['POST'])
def add_comment(author_id):
    author = Author.query.get_or_404(author_id)
    text = request.form['comment']
    comment = Comment(text=text, author=author)
    db.session.add(comment)
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('read_author', author_id=author_id))

@app.route('/comment/delete/<int:comment_id>/<int:author_id>', methods=['POST'])
def delete_comment(comment_id, author_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('read_author', author_id=author_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)