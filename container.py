class Dima1():
    def __init__(self, value):
        self.value = value

    def print(self):
        print('dima1:', self.value)


class Dima2():
    def __init__(self, value, value2='2'):
        self.value = value
        self.value2 = value2

    def print(self):
        print('dima2:', self.value, self.value2)


class Resolver():
    def __init__(self, config):
        self.config = config

    def resolve(self, key, default=None):
        if key not in self.config:
           return None

        obj = self.config[key]

        if isinstance(obj, type):
            args = {}
            for var in obj.__init__.__code__.co_varnames:
                if var != 'self':
                    val = self.resolve(var, default=default)
                    if val:
                        args[var] = val

            return obj(**args)
        else:
            return obj


resolver = Resolver({
    'dima': Dima1,
    'value': 'x'
})

dima = resolver.resolve('dima')

dima.print()


