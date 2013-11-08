import configparser
import requests
import json


class Node(object):
    def __init__(self, url, session=None):
        self.__url = url
        self.__session = session
        self.__children = dict()

    def __getattr__(self, name):
        """
        Get child node as attribute.
        For example abc.def would correspond to the url abc/def

        :param name: Node name
        :type name: str
        :return: Node
        :rtype: Node
        """
        if name not in self.__children:
            child_url = "{base_url}/{name}".format(base_url=self.__url, name=name)
            self.__children[name] = Node(child_url, self.__session)
        return self.__children[name]

    def __getitem__(self, name):
        """
        Access child node using dict like syntax for node names that can't be fetched as an attribute
        like numbers or reserved attributes likes __method

        :param name: Node name
        :type name: str
        :return: Node
        :rtype: Node
        """
        return self.__getattr__(name)

    def __setattr__(self, key, value):
        """
        Put object

        :param key: Node name
        :type key: str
        :param value: Object Value
        :type value: dict
        :return: None
        """
        if key.startswith('_Node__'):
            self.__dict__[key] = value
        else:
            child_url = "{base_url}/{name}".format(base_url=self.__url, name=key)
            self.__session.put(child_url, params=value)

    def __call__(self, __method="GET", **kwargs):
        if __method == "GET":
            method = self.__session.get
        elif __method == "POST":
            method = self.__session.post
        response = method(self.__url, params=kwargs)
        try:
            return json.loads(response.content.decode('utf-8'))
        except ValueError:
            return response.text


class Service(Node):
    def __init__(self, url):
        session = requests.Session()
        session.headers = {'user-agent': 'jmcs\'s test rest module', }
        super(Service, self).__init__(url, requests.Session())

