import os
from my_app import utils
from my_app.app import app
from flask import jsonify, request, make_response


@app.route('/')
def home():
    """Create a Flask backend API for Whatsapp

        The Whatsapp API should contain the following views:
            1. GET messages between user1 and user 2
            2. POST a message from user1 to user2
            3. PATCH Edit the previous message from the user.
            4. Start chatting with a new user
        """
    return "Welcome to the WhatsApp API"

@app.route('/sign_up', methods=['POST'])
def sign_up():
    request_body = request.get_json()
    # check inputs: format should be correct and user should not already exist
    if 'username' not in request_body:
        return make_response(jsonify(error="The body must contain 'username' for sign up."), 400)
    username = request_body['username']

    if utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} already exists"), 400)

    # create a new directory for the user
    user_notes_folder = f'notes/{username}'
    try:
        os.makedirs(user_notes_folder)
        return make_response(jsonify(message='ok'), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)

@app.route('/get-message/<string:username>', methods=['GET'])
def get_message(username):
    # check input format
    request_body = request.get_json()
    user_notes_folder = f'notes/{username}'
    note_name = request['note_name']

    try:
        stored_file = open(f'{user_notes_folder}/{note_name}.txt', 'r')
        note_content = stored_file.read()
        stored_file.close()
        return make_response(jsonify(text=note_content), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)


@app.route('/modify-message/<string:username>', methods=['PUT'])
def modify_message(username):
    # take new text as input
    request_body = request.get_json()
    if 'text' not in request_body:
        return make_response(jsonify(error="The body must contain 'text' for modify note."), 400)
    user_notes_folder = f'notes/{username}'
    note_name = request['note_name']
    text = request_body['text']
    # update the file stored locally
    try:
        stored_file = open(f'{user_notes_folder}/{note_name}.txt', 'w')
        stored_file.write(text)
        stored_file.close()
        return make_response(jsonify(message='ok'), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)


