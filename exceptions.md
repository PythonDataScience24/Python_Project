We implemented a `try-except` block in the following function from `get_data.py`
```python
def download_file(url: str, save_path : str):
    """Downloads file from url locally to the specified path """

    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except OSError as e:
        print(f"Error saving {save_path}: {e}")
```
The function can be used to download files from a specified URL. Two general issues can occur in doing so. The first `except` statement catches exceptions raised when making the request for the URL. For instance if a misspelled URL is passed to the function an HTTPError is raised since the URL cannot be found. The second `except` statement catches exceptions raised when trying to write the file locally. For example if a user does not have write permissions to the directory. Overall these two clauses are used to provide better feedback to the user. Moreover, if such an error does occur, the entire program would not crash allowing for fallback mechanisms or cleanup operations.
