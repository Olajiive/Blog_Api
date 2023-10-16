from flask_restx import Namespace, Resource,fields
from ..models.user import User
from ..models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ..utils import db
from http import HTTPStatus

post_namespace =Namespace("posts", description= "name space for post")

post_model=post_namespace.model(
    "Post", {
        "id": fields.Integer(description="An ID"),
        "title":fields.String(description="Title of an Post", required=True),
        "content":fields.String(description="Content of a Post", required=True,),
        "author":fields.String(description="Author of a Post", required=True),
        
    }
)

post_status_model=post_namespace.model(
    "PostStatus", {
         "id": fields.Integer(description="An ID"),
        "title":fields.String(description="Title of an Post", required=True),
        "content":fields.String(description="Content of a Post", required=True,),
        "author":fields.String(description="Author of a Post", required=True),
        "timestamp":fields.String(description="Datetime of a Post cretion", required=True)
    }
)
@post_namespace.route("/posts")
class PostGetCreate(Resource):
    @post_namespace.marshal_with(post_status_model)

    @jwt_required()
    def get(self):
        """
            get all posts
        """
        posts = Post.query.all()

        return posts, HTTPStatus.OK
    

    @post_namespace.expect(post_model)
    @post_namespace.marshall_with(post_status_model)
    @jwt_required()
    def post(self):
        """
            place an order
        """

        username= get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        data = post_namespace.payload
        
        title= data.get("title")
        content=data.get("content")
        author = data.get("author")

        new_post=Post(title=title, content=content, author=author)
        
        new_post.user=current_user

        new_post.save()

        return new_post, HTTPStatus.CREATED
        
@post_namespace.route("/post/<int:post_id>")
class GetUpdateDelete(Resource):

    @post_namespace.marshal_with(post_status_model)
    @jwt_required()
    def get(self, post_id):
        """
           Retrieving a post by id
        """
        post = Post.get_by_id(post_id)
        return post, HTTPStatus.OK
    
    @post_namespace.expect(post_model)
    @post_namespace.marshal_with(post_status_model)
    @jwt_required()
    def put(self, post_id):
        """
           Update a post by id
        """
        post_to_update = Post.get_by_id(post_id)
        data=post_namespace.payload

        post_to_update.title= data.get("title")
        post_to_update.content=data.get("content")
        post_to_update.author = data.get("author")

        db.session.commit()

        return post_to_update, HTTPStatus.OK

    @jwt_required()
    def delete(self, post_id):
        """
           Delete a post by id
        """
        post = Post.get_by_id(post_id)

        db.session.delete(post)
        db.session.commit()

        return {"message": "Post has been succesfully deleted"}