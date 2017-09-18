import requests
from urllib.request import urlretrieve as urlr

def get_image_url(album_name, offset=0, size=0):
    return get_all_image_urls(album_name, size)[offset]

def get_all_image_urls(album_name, size=0):
    r = requests.get("http://api.spotify.com/v1/search?q=" + album_name + "&type=album")
    r = r.json()
    r = r["albums"]["items"]
    if len(r) == 0:
        print("no albums found for " + album_name)
    return list(map(lambda x : x.replace("https:","http:"), [i["images"][size]["url"] for i in r]))

def download_image(image_url, folder="./img/", file_name=""):
    if file_name == "":
        file_name = image_url.split("/")[-1]
    if not (folder.endswith("/") or folder == ""):
            folder += "/"
    urlr(image_url, folder + file_name)

def download_all(input_file="albums.txt", folder="./img/"):
    with open(input_file) as f:
        for line in f.readlines():
            name = " ".join(line.split(" ")[:-1])
            offset = 0
            if line.split(" ")[-1] != "0":
                offset = int(line.split(" ")[-1])
            url = get_image_url(name,offset,0)
            download_image(url, folder, file_name=name + ".jpg")
