from collections import defaultdict
import fnmatch
import json


class Rule(object):
    def __init__(self, method="GET", path=None, default_parameters={}):
        self.method = method
        self.path = path
        self.description = []
        self.defaults = default_parameters
        self.parameters = dict()

    def __str__(self):
        s = "{method} {path}\n".format(method=self.method, path=self.path)
        for key, value in self.parameters.items():
            s += "    :{key}: {value}\n".format(key=key, value=value)
        for line in self.description:
            s += "    {line}\n".format(line=line)
        return s


class Documentation(object):
    """
    Object to hold all the service documentation
    """

    def __init__(self, fname=None):
        self.rules, self.params = self.parse(fname)


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

        return Rule(method="GET", path=path, default_parameters=self.params)

    def rules_for_path(self, path):
        """
        Return all the rules that match a path
        """
        return [rule for rule in self.rules if fnmatch.fnmatch(path, rule.path)]

    def parse(self, fname):

        rules = []
        parameters = {}

        if not fname:
            #If there is no config file return with empty rule set and parameters
            return rules, parameters

        with open(fname) as cfg_file:
            for line in cfg_file:
                if not line.strip():  # if line is empty we can ignore it
                    continue
                if line.startswith(":"):  # it's a parameter
                    key, value = Documentation._parse_param(line)
                    parameters[key] = value
                    continue

                if not line[0].isspace():
                    # if the first char isn't whitespace then it should be the start of a rule

                    method, url = line.split()
                    page = Rule(method=method, path=url, default_parameters=parameters)
                    rules.append(page)
                else:
                    line = line.strip()
                    if line.startswith(":"):  # it's a local parameter
                        key, value = Documentation._parse_param(line)
                        page.parameters[key] = value
                    else:
                        page.description.append(line)
        return rules, parameters

    @staticmethod
    def _parse_param(line):
            json_params = ['HEADER']  # this parameters have json values

            line = line[1:]  # discard the first ":"
            key, value = line.split(':', maxsplit=1)
            key = key.upper()  # headers should be case insensitive

            if key in json_params:
                value = json.loads(value)
            else:
                value = value.strip()

            return key, value
def help(node):
    """
    Prints Node help
    :param node: Node to inspect
    :type node: object_rest.Node
    """
    # We need to access to the private property to get the documentation
    documentation = node._Node__documentation
    path = node._Node__path
    rules = documentation.rules_for_path(path)
    for rule in rules:
        print(rule)

#TODO: add header parameter