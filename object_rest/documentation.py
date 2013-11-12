from collections import defaultdict


class Page(object):
    def __init__(self):
        self.methods = []
        self.description = ''

    @property
    def default_method(self):
        """
        Returns first defined access method if present on configuration or 'GET' otherwise
        :return: Default method
        :rtype: str
        """
        return self.methods[0] if self.methods else 'GET'


class Documentation(object):
    """
    Object to hold all the service documentation
    """

    def __init__(self, fname=None):
        self.config = defaultdict(Page)  # Service Documentation
        self.params = dict()  # General service configuration
        if fname:
            self.parse(fname)

    def __getitem__(self, path):
        """
        Returns documentation for path, with helpful defaults.

        :param path: Path
        :return: Documentation for path
        :rtype: namedtuple
        """

        page = self.config[path]
        return page

    def parse(self, fname):
        if not fname:
            #If there is no config file return with empty config
            return
        with open(fname) as cfg_file:
            for line in cfg_file:
                if not line.strip():  # if line is empty we can ignore it
                    continue
                if line.startswith(':'):  # it's a parameter
                    key, value = line[1:].split(':', maxsplit=1)
                    self.params[key] = value.strip()
                    continue

                if not line[0].isspace():  # if the first char isn't whitespace then it should
                # be rule
                    method, url = line.split()
                    self.config[url].methods.append(method)
                else:
                    self.config[url].description += line.strip()


def help(node):
    """
    Prints Node help
    :param node: Node to inspect
    """
    # We need to access to the private property to get the documentation
    page = node._Node__doc_page
    print(page.description)