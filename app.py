from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']

        article = Article(name=name, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except Exception as e:
            print(f"Error: {e}")
            return "Error"
    else:
        return render_template("create_article.html")
# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return f'User page: {name} - {id}'.format(name=name, id=id)


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception as e:
        print(f"Error: {e}")
        return "Error"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.name = request.form['name']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except Exception as e:
            print(f"Error: {e}")
            return "Error"
    else:
        return render_template("post_update.html", article=article)


@app.route('/posts/<int:id>')
def post(id):
    article = Article.query.get(id)
    return render_template("post.html", article=article)


# Creating tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
