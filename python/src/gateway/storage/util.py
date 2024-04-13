import pika, json

def upload(f, fs, channel, access):

    try:
        fid = fs.put(f) # Get file id for successful upload
    except Exception as err:
        return "Internal server error: " 
    
    message = {
        'video_fid': str(fid),
        'mp3_fid': None,
        'username': access['username']
    }

    try:
        channel.basic_publish(
            exchange='', # Using the default exchange
            routing_key='video', # Name of the q as we are using default exchange
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )            
        )
    
    except:
        fs.delete(fid)
        return "Internal server error", 500
    