from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

@app.route('/')  # The root/Index of the server
def home():
    #TODO: Return a string that will be displayed on the home page
    return '''<span style='text-align:center'>
                <h1>Welcome to the users database</h1>
                <h3>Authorized Users Only</h3><hr/>
            </span>'''

@app.route('/revise')  # domain/revise route
def edit_request():
    username = request.args.get('username')  # URL is of form http://domain/revise?username=x
    auth = request.args.get('auth')  # URL is of form http://domain/revise?username=x&auth=value

    #TODO: Implement the logic to handle the request
    # create the control flow to handle the request
    if not username:# if the username is not provided, return an error message
        return jsonify({"error": "Username is required"}), 400
    # if the username is provided but the auth is not, return the user record
    record = access_row(username)
    # if the username and auth are provided, update the user record and return the updated record
    if record is None:
        return jsonify({"error": "User not found"}), 404
    # if the username is not found, return an error message
    if auth is None:
        return jsonify({
            "user_id": record[0],
            "username": record[1],
            "password": record[2],
            "auth_level": record[3]
        })
    # do not forget to return the response as a JSON object
    else:
        update_auth(username, auth)
        updated_record = access_row(username)
        return jsonify({
            "user_id": updated_record[0],
            "username": updated_record[1],
            "password": updated_record[2],
            "auth_level": updated_record[3]
        })



def access_row(person):
    #TODO: update the database connection and query to return the user record
    conn = sqlite3.connect('people.db')  # TO-DO: Change '' to the database name inside quotes, Hint: the name ends with .db
    cursor = conn.cursor()  # Get cursor
    cursor.execute("SELECT * FROM users WHERE username = ?", (person,))  # Read SQL
    user_record = cursor.fetchone()  # Get row
    conn.close()  # Release resources
    return user_record  # Got a record


def update_auth(person, auth):  # Delegate the updating to this function
    #TODO: update the database connection and query to update the user record
    conn = sqlite3.connect('people.db')  # TO-DO: Change '' to the database name inside quotes, Hint: the name ends with .db
    cursor = conn.cursor()  # Get cursor
    result = cursor.execute('''UPDATE users SET auth_level=? WHERE username = ?''', (auth, person))
    conn.commit()  # Make changes permanent
    conn.close()  # Release resources
    return result

if __name__ == '__main__':
    app.run(debug=True)

