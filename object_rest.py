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
        For example abc.def would correspond to the URLS abc/def.
        An '_' prefix can be used to access some URLs that would be otherwise be invalid like
        numbers.

        :param name: Node name
        :type name: str
        :return: Node
        :rtype: Node
        """
        name = name.lstrip('_')
        return self.__get_child(name)

    def __setitem__(self, key, value):
        """
        PUT on child node with a dict syntax

        :param key: Child name
        :param value: Value to store
        """
        self.__setattr__(key, value)

    def __getitem__(self, name):
        """
        Access child node using dict like syntax for node names that can't be fetched as an
        attribute like numbers, names with dots or reserved attributes like __method

        :param name: Node name
        :type name: str
        :return: Node
        :rtype: Node
        """
        return self.__get_child(name)

    def __setattr__(self, key, value):
        """
        Put object

        :param key: Node name
        :type key: str
        :param value: Object Value
        :type value: dict
        :return: None
        """

        if key.startswith('_Node__'):  # if it's a private variable
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

    def __get_child(self, name):
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


class Service(Node):

    @staticmethod
    def __parse_documentation(fname):
        #todo: catch errors
        config = defaultdict(list)
        with open(fname) as cfg_file:
                for i, line in enumerate(cfg_file):
                    if i == 0 and line.startswith('URL:'):
                        _, url = line.split(':', maxsplit=1)
                        config['URL'] = url.strip()
                        continue
                    if not line or line[0].isspace():
                        continue
                    method, url = line.split()
                    config[url].append(method)
        return config

    def __init__(self, url=None, documentation=None):
        #todo: allow defining only the documentation and extract the url from it
        session = requests.Session()
        session.headers = {'user-agent': 'object_rest.py', }
        doc = Service.__parse_documentation(documentation) if documentation else {}
        url = url if url else doc['URL']
        super(Service, self).__init__(url, requests.Session(), doc)

