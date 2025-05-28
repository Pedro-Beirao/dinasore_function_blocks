import os
import base64
import datetime

class IMAGE_SAVER:

    def __init__(self):
        pass

    def schedule(self, event_input_name, event_input_value, data, path):

        if event_input_name == 'INIT':
            print("Image processor initialized.")
            return [event_input_value, None, []]  

        elif event_input_name == 'SAVE':

            if data is None:
                status="No image data received"
                print(status)
                return [None, event_input_value, status]

            if path is None:
                status="Error in specifying path"
                print(status)
                return [None, event_input_value, status]

           
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
            os.makedirs(path, exist_ok=True)
            full_path = os.path.join(path, filename)
            
            with open(full_path, "wb") as f:
                f.write(base64.b64decode(data))

            print(f"Image saved to {full_path}")
            status=f"Saved: {filename}"
            
            return [None, event_input_value, status] 
