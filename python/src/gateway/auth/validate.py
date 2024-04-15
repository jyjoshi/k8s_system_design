import os, requests, logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def token(request):
    logging.warning("In Validate")
    if not "Authorization" in request.headers:
        logging.warning("No Authorization header in request headers")
        return None, ("Missing credentials", 401)
    
    token = request.headers["Authorization"]
    logging.warning(f"Token Received {token}")

    if not token:
        logging.warning("Token is empty")
        return None, ("Missing credentials", 401)
    
    response = requests.post(
        f"http://{os.environ['AUTH_SVC_ADDRESS']}/validate",
        headers={"Authorization": token}
    )
    logging.warning(f"Response received")

    if response.status_code == 200:
        logging.warning("Token is valid")
        return response.text, None
    else:
        logging.warning("Token is invalid")
        return None, (response.text, response.status_code)
    