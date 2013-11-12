from collections import defaultdict
import fnmatch


class Rule(object):
    def __init__(self, method="GET", path=None):
        self.method = method
        self.path = path
        self.description = ""


class Documentation(object):
    """
    Object to hold all the service documentation
    """

    def __init__(self, fname=None):
        self.params = dict()  # General service configuration
        self.rules = self.parse(fname)


    def __getitem__(self, path):
        """
        Returns documentation for path, with helpful defaults.
        If there is more than one rule for a path the first one is returned.
        If there is no rule for a path a default rule is returned.

        :param path: Path
        :return: Documentation for path
        :rtype: namedtuple
        """
        for rule in self.rules:
            if fnmatch.fnmatch(path, rule.path):
                return rule

        return Rule(method="GET", path=path)

    def parse(self, fname):
        if not fname:
            #If there is no config file return with empty config
            return []

        rules = []

        with open(fname) as cfg_file:
            for line in cfg_file:
                if not line.strip():  # if line is empty we can ignore it
                    continue
                if line.startswith(":"):  # it's a parameter
                    key, value = line[1:].split(':', maxsplit=1)
                    self.params[key] = value.strip()
                    continue

                if not line[0].isspace():
                    # if the first char isn't whitespace then it should be the start of a rule

                    method, url = line.split()
                    page = Rule(method, url)
                    rules.append(page)
                else:
                    page.description += line.strip()
        return rules

def help(node):
    """
    Prints Node help
    :param node: Node to inspect
    """
    # We need to access to the private property to get the documentation
    page = node._Node__doc_page
    print(page.description)

#TODO: Optional parts of the url on documentation (like reddit API)
#TODO: add header parameter