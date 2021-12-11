""" API routes """
import json
import os

from werkzeug.utils import secure_filename
from flask import jsonify, request, send_from_directory
from flask_jwt_extended import set_access_cookies, jwt_required, current_user

from app import jwtManager, database
from app import app, User, Todo



@app.before_first_request
def create_tables():
    """ create tables """
    database.create_all()


@app.route("/")
def index():
    """ home """
    return jsonify('SaltySugar REST_API_server')


@app.route("/health/")
def get_env():
    """ get env """
    return jsonify({"ENV": os.environ['FLASK_ENV']})


@app.route('/user/', methods=['POST'])
def add_user():
    """ add user """
    query_body = request.form
    if 'username' not in query_body or 'password' not in query_body:
        return jsonify('Invalid request. Parameters missing.'), 422

    user = User.auth(**query_body)
    if user == 0:
        user = User(**query_body)
        access_token = user.get_token()
        response = jsonify({"msg": user.save_in_database(), "access_token": access_token})
        set_access_cookies(response, access_token)
        return response, 201

    if user == 1:
        return jsonify('Invalid credentials.'), 401

    access_token = user.get_token()
    response = jsonify({'msg': 'User authorized', 'access_token': access_token})
    set_access_cookies(response, access_token)
    return response, 200


@app.route('/todo/')
@jwt_required()
def get_todo():
    """ get tasks """
    tasks = current_user.tasks
    response = json.dumps([
        dict({
            "id": task.id,
            "description": task.description
        }) for task in tasks
    ])
    return response, 200


@app.route('/todo/', methods=['POST'])
@jwt_required()
def add_todo():
    """ add task """
    query_body = request.form
    if "description" not in query_body:
        return jsonify('Invalid request. Parameters missing.'), 422

    user_id = current_user.id
    task = Todo(**query_body)
    task.user_id = user_id
    task.save_in_database()
    return jsonify('New TODO added: ' + str(task.id)), 201


@app.route('/todo/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(task_id):
    """ delete task """
    if task_id <= 0:
        return jsonify('Invalid request. Parameters missing.'), 422

    task = Todo.query.filter(Todo.id == task_id).first()

    if task is None:
        return jsonify('TODO not found.'), 404

    # cannot delete somebody else's task
    user_id = current_user.id
    if task.user_id != user_id:
        return jsonify('Missing permissions.'), 401

    task.delete_from_database()
    return jsonify('TODO deleted'), 200


@app.route('/todo/<int:task_id>', methods=['PUT'])
@jwt_required()
def put_todo(task_id):
    """ update task """
    query_body = request.form
    if task_id <= 0 or 'description' not in query_body:
        return jsonify('Invalid request. Parameters missing.'), 422

    task = Todo.query.filter(Todo.id == task_id).first()
    user_id = current_user.id
    if task.user_id != user_id:
        return jsonify('Missing permissions.'), 401

    if task is None:
        return jsonify('TODO not found.'), 404

    task.description = query_body['description']
    task.save_in_database()
    return jsonify('TODO updated.'), 200


@jwtManager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """ idk, it doesnt work without this """
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


""" 
--------------------------------------------------------------------------------------------------------------------
----------------------------------------------- File Storage -------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- 
"""


def check_extension(filename: str):
    """ check supported file extension"""
    extensions = ('.txt', '.png', '.jpg')
    return filename.endswith(extensions)


@app.route('/files/', methods=['POST'])
@jwt_required()
def post_files():
    """ post files """
    if 'file' not in request.files:
        return jsonify('Invalid request. Parameters missing.'), 422

    file = request.files['file']
    if check_extension(file.filename):
        filename = secure_filename(file.filename)
        user_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username + '/')
        if not os.path.exists(user_path):
            os.makedirs(user_path)

        file.save(os.path.join(user_path, filename))
        return jsonify('File uploaded.'), 200

    return jsonify('Invalid file extension.'), 422


@app.route('/files/', methods=['GET'])
@jwt_required()
def get_files():
    """ get files """
    user_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username + '/')
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    files_list = os.listdir(user_path)
    response = json.dumps([
        dict({
            "file": str(file),
            # beautiful
            "size": str(os.path.getsize(os.path.join(user_path, file))) + " bytes"
        }) for file in files_list
    ])
    return response, 200


@app.route("/files/<string:name>", methods=['GET'])
@jwt_required()
def download_file(name):
    """ download file """
    user_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username + '/')
    files_list = os.listdir(user_path)
    if name not in files_list:
        return jsonify("File not found."), 404

    return send_from_directory(user_path, name, as_attachment=True), 200


@app.route("/files/<string:name>", methods=['DELETE'])
@jwt_required()
def delete_file(name):
    """ delete file """
    user_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username + '/')
    if not os.path.exists(user_path + name):
        return jsonify('File not found.'), 404

    os.remove(user_path + name)
    return jsonify('File deleted.'), 200
