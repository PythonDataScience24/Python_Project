import os
import requests

def download_file(url: str, save_path : str):
    """Downloads file from url locally to the specified path """

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


if __name__ == "__main__":

    URL_NAME = "https://datasets.imdbws.com/name.basics.tsv.gz"
    PATH_NAME = "./data/name.basics.tsv.gz"
    URL_CREW = "https://datasets.imdbws.com/title.crew.tsv.gz"
    PATH_CREW = "./data/title.crew.tsv.gz"
    URL_TITLE = "https://datasets.imdbws.com/title.basics.tsv.gz"
    PATH_TITLE = "./data/title.basics.tsv.gz"

    download_file(URL_NAME, PATH_NAME)
    download_file(URL_CREW, PATH_CREW)
    download_file(URL_TITLE, PATH_TITLE)