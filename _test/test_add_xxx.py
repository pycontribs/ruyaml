# coding: utf-8

import re

import pytest  # NOQA
from roundtrip import dedent


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
    return dumper.represent_scalar(u'!dice', u'{}d{}'.format(*data))


def test_dice_constructor():
    import ruyaml  # NOQA

    ruyaml.add_constructor(u'!dice', dice_constructor)
    data = ruyaml.load('initial hit points: !dice 8d4', Loader=ruyaml.Loader)
    assert str(data) == "{'initial hit points': Dice(8,4)}"


def test_dice_constructor_with_loader():
    import ruyaml  # NOQA

    ruyaml.add_constructor(u'!dice', dice_constructor, Loader=ruyaml.Loader)
    data = ruyaml.load('initial hit points: !dice 8d4', Loader=ruyaml.Loader)
    assert str(data) == "{'initial hit points': Dice(8,4)}"


def test_dice_representer():
    import ruyaml  # NOQA

    ruyaml.add_representer(Dice, dice_representer)
    # ruyaml 0.15.8+ no longer forces quotes tagged scalars
    assert (
        ruyaml.dump(dict(gold=Dice(10, 6)), default_flow_style=False)
        == 'gold: !dice 10d6\n'
    )


def test_dice_implicit_resolver():
    import ruyaml  # NOQA

    pattern = re.compile(r'^\d+d\d+$')
    ruyaml.add_implicit_resolver(u'!dice', pattern)
    assert (
        ruyaml.dump(dict(treasure=Dice(10, 20)), default_flow_style=False)
        == 'treasure: 10d20\n'
    )
    assert ruyaml.load('damage: 5d10', Loader=ruyaml.Loader) == dict(damage=Dice(5, 10))


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


class YAMLObj1:
    yaml_tag = u'!obj:'

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

    ruyaml.add_representer(Obj1, YAMLObj1.to_yaml)
    ruyaml.add_multi_constructor(YAMLObj1.yaml_tag, YAMLObj1.from_yaml)
    x = ruyaml.load('!obj:x.2\na: 1', Loader=ruyaml.Loader)
    print(x)
    assert ruyaml.dump(x) == """!obj:x.2 "{'a': 1}"\n"""


def test_yaml_obj_with_loader_and_dumper():
    import ruyaml  # NOQA

    ruyaml.add_representer(Obj1, YAMLObj1.to_yaml, Dumper=ruyaml.Dumper)
    ruyaml.add_multi_constructor(
        YAMLObj1.yaml_tag, YAMLObj1.from_yaml, Loader=ruyaml.Loader
    )
    x = ruyaml.load('!obj:x.2\na: 1', Loader=ruyaml.Loader)
    # x = ruyaml.load('!obj:x.2\na: 1')
    print(x)
    assert ruyaml.dump(x) == """!obj:x.2 "{'a': 1}"\n"""


# ToDo use nullege to search add_multi_representer and add_path_resolver
# and add some test code

# Issue 127 reported by Tommy Wang


def test_issue_127():
    import ruyaml  # NOQA

    class Ref(ruyaml.YAMLObject):
        yaml_constructor = ruyaml.RoundTripConstructor
        yaml_representer = ruyaml.RoundTripRepresenter
        yaml_tag = u'!Ref'

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
    data = ruyaml.round_trip_load(document, preserve_quotes=True)
    assert ruyaml.round_trip_dump(
        data, indent=4, block_seq_indent=2
    ) == document.replace('\n    Two and', ' Two and')
