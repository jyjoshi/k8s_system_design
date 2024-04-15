import jwt, datetime, os, pymysql, logging, sys
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# config
db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'db': 'auth',
    'port': int(os.environ.get('MYSQL_PORT', 3306))  # Ensure it defaults to 3306 if not specified
}


def get_db_connection():
    return pymysql.connect(**db_config)

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    
    # check db for username and password
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            res = cur.execute(
                "SELECT email, password FROM user WHERE email = %s", (auth.username,)
            )

            if res > 0:
                user_row = cur.fetchone()
                email = user_row[0]
                password = user_row[1]
                if auth.username != email or auth.password != password:
                    return "Invalid credentials", 401
                else:
                    return "Authorization: Bearer "+createJWT(auth.username, os.environ.get('JWT_SECRET'), True)
            else:
                return "Invalid Credentials", 401
    finally:
        conn.close()

@server.route('/validate', methods=['POST'])
def validate():
    logging.warning("In Validate")
    # logging.warning("Request headers Authorization:", request.headers["Authorization"])
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(' ')[1]
    logging.warning(f"Token Received {encoded_jwt}")

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get('JWT_SECRET'),
            algorithm='HS256'
        )
    except Exception as e:
        logging.warning(f"Error: {e}")
        logging.warning("Some issue in decoding")
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