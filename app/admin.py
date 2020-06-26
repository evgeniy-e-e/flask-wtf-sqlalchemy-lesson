from app.models import User, Post
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


admin = Admin(app, name='blog-admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
