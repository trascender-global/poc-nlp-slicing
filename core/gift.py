import json
import urllib.request

api_key = "aGty0E20nTJDkXtfvcWSJkd6oEi4ZIww"


def gif_url(text):
    texto = "+".join(text.split())
    path = f"http://api.giphy.com/v1/gifs/search?q={texto}&api_key={api_key}&limit=5"
    with urllib.request.urlopen(path) as url:
        s = url.read().decode('utf8')
        data = json.loads(s)

    url_gif = data["data"][0]["images"]["downsized_large"]["url"]
    return url_gif
