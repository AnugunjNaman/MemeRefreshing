#!/bin/python
import os
from flask import Flask, render_template
import praw
from dotenv import load_dotenv
import random

load_dotenv()

app = Flask(__name__)

reddit_instance = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

@app.route('/')
def index():
    subreddit = reddit_instance.subreddit('memes')
    posts = [post for post in subreddit.hot(limit=50) if not post.stickied]
    random_post = random.choice(posts)
    meme_url = random_post.url
    meme_title = random_post.title

    # Fetching top 5 comments
    comments = []
    for comment in random_post.comments:
        if len(comments) >= 5:  # Limit to 5 comments
            break
        if isinstance(comment, praw.models.Comment):
            comments.append({
                'author': comment.author.name if comment.author else 'Unknown',
                'text': comment.body
            })

    return render_template('index.html', meme_url=meme_url, meme_title=meme_title, comments=comments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
