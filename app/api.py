from flask import Blueprint, jsonify
from app.models import Post


api = Blueprint('api_module', __name__)


@api.route('/posts')
def posts_api():
    posts = []
    for post in Post.query.all():
        posts.append({
            'userId': post.author_id,
            'id': post.id,
            'title': post.heading,
            'body': post.intro_text
        })
    return jsonify(posts)