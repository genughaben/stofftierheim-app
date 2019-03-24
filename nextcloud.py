def publish_to_nextcloud(self, filename_absolute):
    """ Publish a given file (by its absolute filename) to the nextcloud that is specified via envs """

    auth = HTTPBasicAuth(os.environ["NC_USERNAME"], os.environ["NC_PASSWORD"])
    url = os.environ["NC_URL"] + filename_absolute.rsplit('/', 1)[-1]
    files = {"file": open(filename_absolute, "rb")}
    response = requests.put(url, auth=auth, files=files)
    return response.status_code
