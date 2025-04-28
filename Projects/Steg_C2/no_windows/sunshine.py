import os
import requests
image_url = "https://erickumara1.github.io/images/super-innocent.png"
save_path = os.path.join(os.path.expanduser("~"), "Desktop", "innocent.png")
response = requests.get(image_url)
with open(save_path, "wb") as file:
    file.write(response.content)
