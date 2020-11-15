from __future__ import absolute_import, print_function

import datetime
import pprint

import ruyaml

try:
    set
except NameError:
    from sets import Set as set  # NOQA

import ruyaml.tokens


def cmp(a, b):
    return (a > b) - (a < b)


def execute(code):
    global value
    exec(code)
    return value


def _make_objects():
    global MyLoader, MyDumper, MyTestClass1, MyTestClass2, MyTestClass3
    global YAMLobject1, YAMLobject2, AnObject, AnInstance, AState, ACustomState
    global InitArgs, InitArgsWithState
    global NewArgs, NewArgsWithState, Reduce, ReduceWithState, MyInt, MyList, MyDict
    global FixedOffset, today, execute

    class MyLoader(ruyaml.Loader):
        pass

    class MyDumper(ruyaml.Dumper):
        pass

    class MyTestClass1:
        def __init__(self, x, y=0, z=0):
            self.x = x
            self.y = y
            self.z = z

        def __eq__(self, other):
            if isinstance(other, MyTestClass1):
                return self.__class__, self.__dict__ == other.__class__, other.__dict__
            else:
                return False

    def construct1(constructor, node):
        mapping = constructor.construct_mapping(node)
        return MyTestClass1(**mapping)

    def represent1(representer, native):
        return representer.represent_mapping('!tag1', native.__dict__)

    ruyaml.add_constructor('!tag1', construct1, Loader=MyLoader)
    ruyaml.add_representer(MyTestClass1, represent1, Dumper=MyDumper)

    class MyTestClass2(MyTestClass1, ruyaml.YAMLObject):
        ruyaml.loader = MyLoader
        ruyaml.dumper = MyDumper
        ruyaml.tag = '!tag2'

        def from_yaml(cls, constructor, node):
            x = constructor.construct_yaml_int(node)
            return cls(x=x)

        from_yaml = classmethod(from_yaml)

        def to_yaml(cls, representer, native):
            return representer.represent_scalar(cls.yaml_tag, str(native.x))

        to_yaml = classmethod(to_yaml)

    class MyTestClass3(MyTestClass2):
        ruyaml.tag = '!tag3'

        def from_yaml(cls, constructor, node):
            mapping = constructor.construct_mapping(node)
            if '=' in mapping:
                x = mapping['=']
                del mapping['=']
                mapping['x'] = x
            return cls(**mapping)

        from_yaml = classmethod(from_yaml)

        def to_yaml(cls, representer, native):
            return representer.represent_mapping(cls.yaml_tag, native.__dict__)

        to_yaml = classmethod(to_yaml)

    class YAMLobject1(ruyaml.YAMLObject):
        ruyaml.loader = MyLoader
        ruyaml.dumper = MyDumper
        ruyaml.tag = '!foo'

        def __init__(self, my_parameter=None, my_another_parameter=None):
            self.my_parameter = my_parameter
            self.my_another_parameter = my_another_parameter

        def __eq__(self, other):
            if isinstance(other, YAMLobject1):
                return self.__class__, self.__dict__ == other.__class__, other.__dict__
            else:
                return False

    class YAMLobject2(ruyaml.YAMLObject):
        ruyaml.loader = MyLoader
        ruyaml.dumper = MyDumper
        ruyaml.tag = '!bar'

        def __init__(self, foo=1, bar=2, baz=3):
            self.foo = foo
            self.bar = bar
            self.baz = baz

        def __getstate__(self):
            return {1: self.foo, 2: self.bar, 3: self.baz}

        def __setstate__(self, state):
            self.foo = state[1]
            self.bar = state[2]
            self.baz = state[3]

        def __eq__(self, other):
            if isinstance(other, YAMLobject2):
                return self.__class__, self.__dict__ == other.__class__, other.__dict__
            else:
                return False

    class AnObject:
        def __new__(cls, foo=None, bar=None, baz=None):
            self = object.__new__(cls)
            self.foo = foo
            self.bar = bar
            self.baz = baz
            return self

        def __cmp__(self, other):
            return cmp(
                (type(self), self.foo, self.bar, self.baz),  # NOQA
                (type(other), other.foo, other.bar, other.baz),
            )

        def __eq__(self, other):
            return type(self) is type(other) and (self.foo, self.bar, self.baz) == (
                other.foo,
                other.bar,
                other.baz,
            )

    class AnInstance:
        def __init__(self, foo=None, bar=None, baz=None):
            self.foo = foo
            self.bar = bar
            self.baz = baz

        def __cmp__(self, other):
            return cmp(
                (type(self), self.foo, self.bar, self.baz),  # NOQA
                (type(other), other.foo, other.bar, other.baz),
            )

        def __eq__(self, other):
            return type(self) is type(other) and (self.foo, self.bar, self.baz) == (
                other.foo,
                other.bar,
                other.baz,
            )

    class AState(AnInstance):
        def __getstate__(self):
            return {'_foo': self.foo, '_bar': self.bar, '_baz': self.baz}

        def __setstate__(self, state):
            self.foo = state['_foo']
            self.bar = state['_bar']
            self.baz = state['_baz']

    class ACustomState(AnInstance):
        def __getstate__(self):
            return (self.foo, self.bar, self.baz)

        def __setstate__(self, state):
            self.foo, self.bar, self.baz = state

    # class InitArgs(AnInstance):
    #     def __getinitargs__(self):
    #         return (self.foo, self.bar, self.baz)
    #     def __getstate__(self):
    #         return {}

    # class InitArgsWithState(AnInstance):
    #     def __getinitargs__(self):
    #         return (self.foo, self.bar)
    #     def __getstate__(self):
    #         return self.baz
    #     def __setstate__(self, state):
    #         self.baz = state

    class NewArgs(AnObject):
        def __getnewargs__(self):
            return (self.foo, self.bar, self.baz)

        def __getstate__(self):
            return {}

    class NewArgsWithState(AnObject):
        def __getnewargs__(self):
            return (self.foo, self.bar)

        def __getstate__(self):
            return self.baz

        def __setstate__(self, state):
            self.baz = state

    InitArgs = NewArgs

    InitArgsWithState = NewArgsWithState

    class Reduce(AnObject):
        def __reduce__(self):
            return self.__class__, (self.foo, self.bar, self.baz)

    class ReduceWithState(AnObject):
        def __reduce__(self):
            return self.__class__, (self.foo, self.bar), self.baz

        def __setstate__(self, state):
            self.baz = state

    class MyInt(int):
        def __eq__(self, other):
            return type(self) is type(other) and int(self) == int(other)

    class MyList(list):
        def __init__(self, n=1):
            self.extend([None] * n)

        def __eq__(self, other):
            return type(self) is type(other) and list(self) == list(other)

    class MyDict(dict):
        def __init__(self, n=1):
            for k in range(n):
                self[k] = None

        def __eq__(self, other):
            return type(self) is type(other) and dict(self) == dict(other)

    class FixedOffset(datetime.tzinfo):
        def __init__(self, offset, name):
            self.__offset = datetime.timedelta(minutes=offset)
            self.__name = name

        def utcoffset(self, dt):
            return self.__offset

        def tzname(self, dt):
            return self.__name

        def dst(self, dt):
            return datetime.timedelta(0)

    today = datetime.date.today()


try:
    from ruamel.ordereddict import ordereddict
except ImportError:
    from collections import OrderedDict

    # to get the right name import ... as ordereddict doesn't do that

    class ordereddict(OrderedDict):
        pass


def _load_code(expression):
    return eval(expression, globals())


def _serialize_value(data):
    if isinstance(data, list):
        return '[%s]' % ', '.join(map(_serialize_value, data))
    elif isinstance(data, dict):
        items = []
        for key, value in data.items():
            key = _serialize_value(key)
            value = _serialize_value(value)
            items.append('%s: %s' % (key, value))
        items.sort()
        return '{%s}' % ', '.join(items)
    elif isinstance(data, datetime.datetime):
        return repr(data.utctimetuple())
    elif isinstance(data, float) and data != data:
        return '?'
    else:
        return str(data)


def test_constructor_types(data_filename, code_filename, verbose=False):
    _make_objects()
    native1 = None
    native2 = None
    try:
        with open(data_filename, 'rb') as fp0:
            native1 = list(ruyaml.load_all(fp0, Loader=MyLoader))
        if len(native1) == 1:
            native1 = native1[0]
        with open(code_filename, 'rb') as fp0:
            native2 = _load_code(fp0.read())
        try:
            if native1 == native2:
                return
        except TypeError:
            pass
        # print('native1', native1)
        if verbose:
            print('SERIALIZED NATIVE1:')
            print(_serialize_value(native1))
            print('SERIALIZED NATIVE2:')
            print(_serialize_value(native2))
        assert _serialize_value(native1) == _serialize_value(native2), (
            native1,
            native2,
        )
    finally:
        if verbose:
            print('NATIVE1:')
            pprint.pprint(native1)
            print('NATIVE2:')
            pprint.pprint(native2)


test_constructor_types.unittest = ['.data', '.code']


def test_roundtrip_data(code_filename, roundtrip_filename, verbose=False):
    _make_objects()
    with open(code_filename, 'rb') as fp0:
        value1 = fp0.read()
    native2 = list(ruyaml.load_all(value1, Loader=MyLoader))
    if len(native2) == 1:
        native2 = native2[0]
    try:
        value2 = ruyaml.dump(
            native2,
            Dumper=MyDumper,
            default_flow_style=False,
            allow_unicode=True,
            encoding='utf-8',
        )
        # value2 += x
        if verbose:
            print('SERIALIZED NATIVE1:')
            print(value1)
            print('SERIALIZED NATIVE2:')
            print(value2)
        assert value1 == value2, (value1, value2)
    finally:
        if verbose:
            print('NATIVE2:')
            pprint.pprint(native2)


test_roundtrip_data.unittest = ['.data', '.roundtrip']


if __name__ == '__main__':
    import sys

    import test_constructor  # NOQA

    sys.modules['test_constructor'] = sys.modules['__main__']
    import test_appliance

    test_appliance.run(globals())
