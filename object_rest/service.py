import requests
import json
from object_rest.documentation import Documentation


class Node(object):
    def __init__(self, host, path, session=None, documentation={}):
        self.__children = dict()
        self.__host = host
        self.__url = host + path
        self.__session = session
        self.__path = path

        #Documentation related stuff
        self.__documentation = documentation  # full_documentation
        self.__doc_page = documentation[path]  # "page" relative to this path

    def __getattr__(self, name):
        """
        Get child node as attribute.
        For example abc.def would correspond to the URLS abc/def.
        An "_" prefix can be used to access some URLs that would be otherwise be invalid like
        numbers.

        :param name: Node name
        :type name: str
        :return: Node
        :rtype: Node
        """
        name = name.lstrip("_")
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
        if not key.startswith("_Node__"):
            key = key.lstrip("_")
        self.__put(key, value)

    def __call__(self, __method=None, **kwargs):

        rule = self.__doc_page

        # if method is not specified use the default from the documentation file
        # or GET if it's not documented
        __method = __method if __method else rule.method

        if __method == "GET":
            method = self.__session.get
        elif __method == "POST":
            method = self.__session.post

        headers = rule.parameters["HEADERS"] if "HEADERS" in rule.parameters else {}
        response = method(self.__url, params=kwargs, headers=headers)

        try:
            return json.loads(response.content.decode("utf-8"))
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
            child_path = "/".join([self.__path, name])
            self.__children[name] = Node(host=self.__host,
                                         path=child_path,
                                         session=self.__session,
                                         documentation=self.__documentation, )
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

        if key.startswith("_Node__"):  # if it"s a private variable
            self.__dict__[key] = value
        else:
            child_url = "{base_url}/{name}".format(base_url=self.__url, name=key)
            self.__session.put(child_url, params=value)


class Service(Node):
    def __init__(self, host=None, documentation=None):
        session = requests.Session()
        session.headers = {"user-agent": "object_rest.py", }
        doc = Documentation(documentation)
        try:
            host = host if host else doc.params["URL"]
        except KeyError:
            raise TypeError("No URL defined")
        super(Service, self).__init__(host=host,
                                      path="",
                                      session=requests.Session(),
                                      documentation=doc)


#TODO: Error handling