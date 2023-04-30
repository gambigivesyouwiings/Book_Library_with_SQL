from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

all_books = []


class Books(db.Model):
    # id = db.column(db.Integer, nullable=False)
    title = db.Column(db.String(250), primary_key=True, unique=True, nullable=False)
    author = db.Column(db.String(250),  nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# with app.app_context():
    # db.drop_all()

# with app.app_context():
#   db.create_all()

user = Books(title="Harry Potter", author="J. K. Rowling", rating=9.3)


@app.route('/')
def home():
    my_books = db.session.query(Books).all()

    return render_template("index.html", list=my_books)


@app.route('/del')
def delete():
    del_book_title = request.args.get('title')
    del_book_to_edit = Books.query.filter_by(title=del_book_title).first()
    db.session.delete(del_book_to_edit)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/edit", methods=["POST", "GET"])
def edit():
    book_title = request.args.get('title')
    book_to_edit = Books.query.filter_by(title=book_title)

    if request.method == "POST":
        t = request.form["title"]
        the_book = Books.query.filter_by(title=t).first()
        the_book.rating = request.form['rating']
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("editt.html", edit_book=book_to_edit)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        form_data = {"Title": request.form["title"],
                     "Author": request.form["author"],
                     "rating": request.form["rating"]}
        all_books.append(form_data)

        book_data = Books(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(book_data)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

