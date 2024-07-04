#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_data = [
        {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.isoformat()  # Convert date to ISO format string
        }
        for article in articles
    ]
    return jsonify(articles_data), 200

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = db.session.get(Article, id)
        if article:
            article_data = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': article.author,
                'preview': article.preview,
                'minutes_to_read': article.minutes_to_read,
                'date': article.date.isoformat()  # Convert date to ISO format string
            }
            return jsonify(article_data), 200
        else:
            return {'message': 'Article not found'}, 404
    else:
        return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5000)
