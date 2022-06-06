import json
from secrets import get_secret_image_gallery

json_string = get_secret_image_gallery()
print(json.loads(json_string))
