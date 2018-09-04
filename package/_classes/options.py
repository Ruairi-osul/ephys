'''Options class for storing configuration information'''

import json
import os

class Options:
    '''Options class to store configuration choices'''

    def __init__(self, *args, **kwargs):
        for dictionary in args:
            try:
                assert isinstance(dictionary, dict)
            except AssertionError:
                raise ValueError('Non Dictionary passed as positional argument to options')
            for key in dictionary:
                setattr(self, key, dictionary[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.parent_dir = self.parent_dir()
        

    def parent_dir(self):
        try:
            assert hasattr(self, "continuous_dir")
        except AssertionError:
            raise ValueError('Error calculating parent directory. "continuous_dir" attribute not present')
        return os.path.dirname(self.continuous_dir)

    def __str__(self):
        attrs = [i for i in self.__dict__.keys() if i[:1] != '_']
        out = ('Items in Options:')
        for i in attrs:
            out = '\n\t'.join([out, i])
        return out


def options_from_args(args):
    '''Takes argparse.Namespace object and returns Options object'''

    if ',' in args.recordings:
        args.recordings = args.recordings.split(',')

    options = vars(args)
    if ('reference_method' in options.keys()) and options['reference_method'] is None:
        options['reference_method'] == '' 
    options = dict(filter(lambda x: x[1] is not None, options.items()))

    with open(args.config_file) as file:
        options.update(json.loads(file.read()))

    return Options(options)
