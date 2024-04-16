import pika, json, logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def upload(f, fs, channel, access):
    print("Inside upload function in util.py module in storage package")

    try:
        fid = fs.put(f) # Get file id for successful upload
    except Exception as err:
        return f"Internal server error: {err}", 500 
    logging.warning(f"Uploaded file with id: {str(fid)}")
    
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
    
    except Exception as e:
        logging.error(f"Error publishing message to queue: {e}")
        fs.delete(fid)
        return f"Internal server error: {e}", 500
    