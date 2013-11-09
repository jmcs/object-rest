from collections import defaultdict
import requests
import json
import urllib.parse

class Node(object):
    def __init__(self, url, session=None, documentation={}):
        self.__url = url
        self.__session = session
        self.__path = urllib.parse.urlparse(url).path
        self.__documentation = documentation
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
            self.__children[name] = Node(child_url, self.__session, self.__documentation)
        return self.__children[name]

    def __getitem__(self, name):
        """
        Access child node using dict like syntax for node names that can't be fetched as an
        attribute like numbers or reserved attributes likes __method

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

        #todo add __set_key__
        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            child_url = "{base_url}/{name}".format(base_url=self.__url, name=key)
            self.__session.put(child_url, params=value)

    def __call__(self, __method=None, **kwargs):
        #When the method isn't specified
        if not __method:
            if self.__path in self.__documentation:
                #When not specified we use the first documented method
                __method = self.__documentation[self.__path][0]
            else:
                __method = "GET"
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

    @staticmethod
    def __parse_documentation(fname):
        #todo: catch errors
        config = defaultdict(list)
        with open(fname) as cfg_file:
                for line in cfg_file:
                    if not line or line[0].isspace():
                        continue
                    method, url = line.split()
                    config[url].append(method)
        return config

    def __init__(self, url, documentation=None):
        #todo: allow defining only the documentation and extract the url from it
        session = requests.Session()
        session.headers = {'user-agent': 'object_rest.py', }
        doc = Service.__parse_documentation(documentation) if documentation else {}
        super(Service, self).__init__(url, requests.Session(), doc)

