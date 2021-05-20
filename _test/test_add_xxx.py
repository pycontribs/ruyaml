# coding: utf-8

import re

import pytest  # NOQA

from .roundtrip import dedent, round_trip_dump  # NOQA


# from PyYAML docs
class Dice(tuple):
    def __new__(cls, a, b):
        return tuple.__new__(cls, [a, b])

    def __repr__(self):
        return 'Dice(%s,%s)' % self


def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)


def dice_representer(dumper, data):
    return dumper.represent_scalar('!dice', '{}d{}'.format(*data))


def test_dice_constructor():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    ruyaml.add_constructor('!dice', dice_constructor)
    data = yaml.load('initial hit points: !dice 8d4')
    assert str(data) == "{'initial hit points': Dice(8,4)}"


def test_dice_constructor_with_loader():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    ruyaml.add_constructor('!dice', dice_constructor, Loader=ruyaml.Loader)
    data = yaml.load('initial hit points: !dice 8d4')
    assert str(data) == "{'initial hit points': Dice(8,4)}"


def test_dice_representer():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    yaml.default_flow_style = False
    ruyaml.add_representer(Dice, dice_representer)
    # ruyaml 0.15.8+ no longer forces quotes tagged scalars
    buf = ruyaml.compat.StringIO()
    yaml.dump(dict(gold=Dice(10, 6)), buf)
    assert buf.getvalue() == 'gold: !dice 10d6\n'


def test_dice_implicit_resolver():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    yaml.default_flow_style = False
    pattern = re.compile(r'^\d+d\d+$')
    ruyaml.add_implicit_resolver('!dice', pattern)
    buf = ruyaml.compat.StringIO()
    yaml.dump(dict(treasure=Dice(10, 20)), buf)
    assert buf.getvalue() == 'treasure: 10d20\n'
    assert yaml.load('damage: 5d10') == dict(damage=Dice(5, 10))


class Obj1(dict):
    def __init__(self, suffix):
        self._suffix = suffix
        self._node = None

    def add_node(self, n):
        self._node = n

    def __repr__(self):
        return 'Obj1(%s->%s)' % (self._suffix, self.items())

    def dump(self):
        return repr(self._node)


class YAMLObj1(object):
    yaml_tag = '!obj:'

    @classmethod
    def from_yaml(cls, loader, suffix, node):
        import ruyaml  # NOQA

        obj1 = Obj1(suffix)
        if isinstance(node, ruyaml.MappingNode):
            obj1.add_node(loader.construct_mapping(node))
        else:
            raise NotImplementedError
        return obj1

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag + data._suffix, data.dump())


def test_yaml_obj():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    ruyaml.add_representer(Obj1, YAMLObj1.to_yaml)
    ruyaml.add_multi_constructor(YAMLObj1.yaml_tag, YAMLObj1.from_yaml)
    x = yaml.load('!obj:x.2\na: 1')
    print(x)
    buf = ruyaml.compat.StringIO()
    yaml.dump(x, buf)
    assert buf.getvalue() == """!obj:x.2 "{'a': 1}"\n"""


def test_yaml_obj_with_loader_and_dumper():
    import ruyaml  # NOQA

    yaml = ruyaml.YAML(typ='unsafe', pure=True)
    ruyaml.add_representer(Obj1, YAMLObj1.to_yaml, Dumper=ruyaml.Dumper)
    ruyaml.add_multi_constructor(
        YAMLObj1.yaml_tag, YAMLObj1.from_yaml, Loader=ruyaml.Loader
    )
    x = yaml.load('!obj:x.2\na: 1')
    # x = ruyaml.load('!obj:x.2\na: 1')
    print(x)
    buf = ruyaml.compat.StringIO()
    yaml.dump(x, buf)
    assert buf.getvalue() == """!obj:x.2 "{'a': 1}"\n"""


# ToDo use nullege to search add_multi_representer and add_path_resolver
# and add some test code

# Issue 127 reported by Tommy Wang


def test_issue_127():
    import ruyaml  # NOQA

    class Ref(ruyaml.YAMLObject):
        yaml_constructor = ruyaml.RoundTripConstructor
        yaml_representer = ruyaml.RoundTripRepresenter
        yaml_tag = '!Ref'

        def __init__(self, logical_id):
            self.logical_id = logical_id

        @classmethod
        def from_yaml(cls, loader, node):
            return cls(loader.construct_scalar(node))

        @classmethod
        def to_yaml(cls, dumper, data):
            if isinstance(data.logical_id, ruyaml.scalarstring.ScalarString):
                style = data.logical_id.style  # ruyaml>0.15.8
            else:
                style = None
            return dumper.represent_scalar(cls.yaml_tag, data.logical_id, style=style)

    document = dedent(
        """\
    AList:
      - !Ref One
      - !Ref 'Two'
      - !Ref
        Two and a half
    BList: [!Ref Three, !Ref "Four"]
    CList:
      - Five Six
      - 'Seven Eight'
    """
    )
    yaml = ruyaml.YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = None
    yaml.indent(sequence=4, offset=2)
    data = yaml.load(document)
    buf = ruyaml.compat.StringIO()
    yaml.dump(data, buf)
    assert buf.getvalue() == document.replace('\n    Two and', ' Two and')
