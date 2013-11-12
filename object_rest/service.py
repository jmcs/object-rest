import requests
import json
import urllib.parse
from object_rest.documentation import Documentation


class Node(object):
    def __init__(self, url, session=None, documentation={}):
        self.__children = dict()
        self.__url = url
        self.__session = session
        self.__path = urllib.parse.urlparse(url).path

        #Documentation related stuff
        self.__documentation = documentation  # full_documentation
        self.__doc_page = documentation[self.__path]  # 'page' relative to this path

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
        self.__put(key, value)

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
        PUT on key by attribute

        :param key: Node name
        :type key: str
        :param value: Object Value
        :type value: dict
        :return: None
        """
        if not key.startswith('_Node__'):
            key = key.lstrip('_')
        self.__put(key, value)

    def __call__(self, __method=None, **kwargs):

        # if method is not specified use the default from the documentation file
        # or GET if it's not documented
        __method = __method if __method else self.__doc_page.default_method

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

    def __put(self, key, value):
        """
        Send PUT request to key with value

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


class Service(Node):
    def __init__(self, url=None, documentation=None):
        session = requests.Session()
        session.headers = {'user-agent': 'object_rest.py', }
        doc = Documentation(documentation)
        try:
            url = url if url else doc.params['URL']
        except KeyError:
            raise TypeError('No URL defined')
        super(Service, self).__init__(url, requests.Session(), doc)


        #todo: move everything to folder, separate documentation and service
        #TODO: Add documentation to the method (implies replacing simple method in the list with a dict)
        #TODO: Optional parts of the url on documentation (like reddit API)