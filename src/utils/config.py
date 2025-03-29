from os import getenv

proxies = {"http":      getenv("HTTP_PROXY"),
           "https":     getenv("HTTPS_PROXY")
           }