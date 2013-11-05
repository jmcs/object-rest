import requests
import json


class Node(object):
    def __init__(self, url, suffix="", session=None):
        self.__url = url
        self.__session = session
        self.__props = {
            "method": "GET",
            "suffix": suffix
        }
        self.__children = dict()

    def __getattr__(self, name):
        if name not in self.__children:
            child_url = "{base_url}/{name}".format(base_url=self.__url, name=name)
            self.__children[name] = Node(child_url, self["suffix"], self.__session)
        return self.__children[name]

    def __getitem__(self, key):
        return self.__props[key]

    def __setitem__(self, key, value):
        self.__props[key] = value

    def __call__(self, __mode=None, **kwargs):
        mode = __mode if __mode else self["method"]
        url = self.__url + self["suffix"]

        if mode == "GET":
            method = self.__session.get
        elif mode == "POST":
            method = self.__session.post
        response = method(url, params=kwargs)
        try:
            return json.loads(response.content.decode('utf-8'))
        except ValueError:
            return response.text


class Service(Node):
    def __init__(self, url, suffix=""):
        session = requests.Session()
        session.headers = {'user-agent': 'jmcs\'s test rest module', }
        super(Service, self).__init__(url, suffix, requests.Session())

