from app import jwtManager
from app import app, User, Task
from flask import jsonify, request
from flask_jwt_extended import set_access_cookies, jwt_required, current_user


# home
@app.route("/")
def index():
    return jsonify('home')


# add user
@app.route('/user', methods=['POST'])
def add_user():
    queryBody = request.form
    if 'username' not in queryBody or 'password' not in queryBody:
        return jsonify('invalid params'), 400

    user = User.authenticate(**queryBody)
    if user == 0:
        user = User(**queryBody)
        access_token = user.get_token()
        response = jsonify({"msg": user.save_in_database(), "access_token": access_token})
        set_access_cookies(response, access_token)
        return response, 201
    elif user == 1:
        return jsonify({"msg": 'invalid password'}), 400
    access_token = user.get_token()
    response = jsonify({'access_token': access_token})
    set_access_cookies(response, access_token)
    return response, 201


# get tasks
@app.route('/todo')
@jwt_required()
def get_todo():
    tasks = current_user.tasks
    response = {'username': current_user.username}
    for task in tasks:
        upd = {f'task №: {task.id}': f'descr: {task.description}'}
        response.update(upd)
    return response, 200


# add task
@app.route('/todo', methods=['POST'])
@jwt_required()
def add_todo():
    query_body = request.form
    if "description" not in query_body:
        return jsonify('invalid params'), 400

    user_id = current_user.id
    task = Task(**query_body)
    task.user_id = user_id
    task.save_in_database()
    return jsonify('added task №' + str(task.id)), 201


# delete task
@app.route('/todo/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    if id <= 0:
        return jsonify('invalid params'), 400

    task = Task.query.filter(Task.id == id).first()

    if task is None:
        return jsonify('task №' + str(id) + ' NOT FOUND'), 418

    # cannot delete somebody else's task
    user_id = current_user.id
    if task.user_id != user_id:
        return jsonify('invalid params'), 400

    task.delete_from_database()
    return jsonify('task №' + str(id) + ' DELETED'), 202


# update task
@app.route('/todo/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    queryBody = request.form
    if id <= 0 or 'description' not in queryBody:
        return jsonify('invalid params'), 400

    task = Task.query.filter(Task.id == id).first()
    user_id = current_user.id
    if task.user_id != user_id:
        return jsonify('invalid params'), 400

    if task is None:
        return jsonify('task №' + str(id) + ' NOT FOUND'), 418
    else:
        task.description = queryBody['description']
        task.save_in_database()
        return jsonify('task N' + str(id) + ' UPDATED'), 202


# -3 часа, ибо документацию фиг разберешь
@jwtManager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()
