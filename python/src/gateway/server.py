import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
import logging
import sys

# Set up logging to console at debug level
handler = logging.StreamHandler(sys.stdout)  # Use stdout instead of the default stderr
handler.setLevel(logging.DEBUG)  # Set the log level you want to output
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


server = Flask(__name__)
mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

server.logger.addHandler(handler)
server.logger.setLevel(logging.DEBUG)

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        if 1 < len(request.files) < 1:
            return "Exactly one file must be uploaded", 400

        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return err
        
        return "File uploaded", 200
    else:
        return "Not authorized", 401

@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port = 8080, debug=True)
    
