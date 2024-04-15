import os, requests

def login(request):
    print("In acess module")
    auth = request.authorization
    print("auth", auth)
    print('type(auth)', type(auth))
    if not auth:
        return None, ("Missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ['AUTH_SVC_ADDRESS']}/login",
        auth=basicAuth
    )
    print('response', response)
    print('type(response)', type(response))

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    