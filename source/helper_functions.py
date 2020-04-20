import requests
from os import path

def GetFileFromUrl(url, fpath):
    if(not path.exists(fpath)):
        print("Downloading dataset to local file...")
        # Download from URL into a file-like object
        uf = requests.get(url)

        # Write to disk file
        f = open(fpath, 'wb')
        f.write(uf.content)
        f.close()
