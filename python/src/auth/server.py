import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

#config
server.config['MySQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MySQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MySQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MySQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')
# print(server.config['MySQL_HOST'])

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    
    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM users WHERE email = %s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True)
    else:
        return "Invalid Credentials", 401

@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(' ')[1]

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get('JWT_SECRET'),
            algorithm='HS256'
        )
    except:
        return "Invalid token", 401
    
    return decoded, 200


def createJWT(username, secret, authz):
    payload = {
        'username': username,
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'admin': authz
    }
    return jwt.encode(payload, secret, algorithm='HS256')



if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)