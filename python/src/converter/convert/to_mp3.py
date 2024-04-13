import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # Empty temp file
    tf = tempfile.NamedTemporaryFile() # Creates a tempfile in temp direct with a name

    # Video Contents
    out = fs_videos.get(ObjectId(message['video_fid']))

    # add video contents to empty file
    tf.write(out.read())

    # Create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close() # Automatically deletes the temp file on closing

    # write autio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # Save file to mongo
    f = open(tf_path, 'rb')
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close() 
    os.remove(tf_path) # The file was created using write_audiofile so needs to be manually deleted unlike the temp file we used before

    message["mp3_fid"] = str(fid)

    # put the message on the mp3 q
    try:
        channel.basic_publish(
            exchange='', # Using the default exchange
            routing_key=os.environ.get("MP3_QUEUE"), # Name of the q taken from env variable
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )            
        )
    except Exception as err:
        fs_mp3s.delete(fid) # Delete the file from the fs_mp3s if the publish fails
        return "Failed to Publish to MP3 Queue"
    
