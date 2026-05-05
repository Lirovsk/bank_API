from ..app import db
from ..app.models.user_account import User

from flask import Blueprint, request, jsonify
from http import HTTPStatus

app = Blueprint("user", __name__, url_prefix="/users")


# function responsible to create a new user, it will receive a json with the name and email of the user, if the email already exists it will raise an error
def create_user(data: dict):
    try:
        user = User(name=data["name"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully", "user": {"id": user.id, "name": user.name, "email": user.email}}, HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return {"message": "Error creating user", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


# function responsible to search for all users, if none it will return an empty list
def search_users():
    try:
        users = db.session.execute(db.select(User)).scalars().all()
        return {"message": "Users fetched successfully", "users": [{"name": user.name, "email": user.email} for user in users]}, HTTPStatus.OK
    
    except Exception as e:
        return {"message": "Error fetching users", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


# function responsible to search for one user by email, if none it will raise an error
def search_user(user_email: str):
    try:
        user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
        if user:
            return {"message": "User fetched successfully", "user": {"name": user.name, "email": user.email}}, HTTPStatus.OK
        else:
            raise ValueError("User not found")
    except Exception as e:
        if str(e) == "User not found":
            return {"message": str(e)}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "Error fetching user", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


# function responsible to delete a user by email, if none it will raise an error
def delete_user(user_email: str):
    try:
        user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, HTTPStatus.OK
        else:
            raise ValueError("User not found")
    except Exception as e:
        if str(e) == "User not found":
            return {"message": str(e)}, HTTPStatus.NOT_FOUND
        else:
            db.session.rollback()
            return {"message": "Error deleting user", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        

# function responsible to update a user by email, it will receive a json with the name and email of the user, if the email already exists it will raise an error       
def update_user(user_email: str, data: dict):
    try:
        user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
        if user:
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            db.session.commit()
            return {"message": "User updated successfully", "user": {"name": user.name, "email": user.email}}, HTTPStatus.OK
        else:
            raise ValueError("User not found")
    except Exception as e:
        if str(e) == "User not found":
            return {"message": str(e)}, HTTPStatus.NOT_FOUND
        else:
            db.session.rollback()
            return {"message": "Error updating user", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


# route to handle the users, it will accept GET and POST requests, if GET it will return all users, if POST it will create a new user
@app.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result, status = search_users()
        return result, status
    else:
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, HTTPStatus.BAD_REQUEST

        result, status = create_user(data)
        return result["message"], status
    

# route to handle the user detail, it will accept GET requests, if GET it will return the user detail by email
@app.route("/<user_email>", methods=["GET"])
def user_detail(user_email):
    if request.method == "GET":
        result, status = search_user(user_email)
        return result, status
    
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED


# route responsible to handle deletions of users, it will accept DELETE requests, if DELETE it will delete the user by email
@app.route("/<user_email>", methods=["DELETE"])
def user_delete(user_email):
    if request.method == "DELETE":
        result, status = delete_user(user_email)
        return result, status
    
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED
    

# route responsible to handle updates of users, it will accept PATCH requests, if PATCH it will update the user by email, it will receive a json with the name and email of the user, if the email already exists it will raise an error
@app.route("update_name/<user_email>", methods=["PATCH"])
def user_update(user_email):
    if request.method == "PATCH":
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, HTTPStatus.BAD_REQUEST
        result, status = update_user(user_email, data)
        return result, status
        
    else:
        return {"message": "Method not allowed"}, HTTPStatus.METHOD_NOT_ALLOWED
    
    
@app.route("/update_email/<user_email>", methods=["PATCH"])
def user_update_email(user_email):
    return {"message": "This endpoint is not implemented yet"}, HTTPStatus.NOT_IMPLEMENTED