# coding: utf-8

"""
testing of YAML.register_class and @yaml_object
"""

from roundtrip import YAML


class User0:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class User1:
    yaml_tag = u'!user'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(
            cls.yaml_tag, u'{.name}-{.age}'.format(node, node)
        )

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(*node.value.split('-'))


class TestRegisterClass:
    def test_register_0_rt(self):
        yaml = YAML()
        yaml.register_class(User0)
        ys = """
        - !User0
          name: Anthon
          age: 18
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys, unordered_lines=True)

    def test_register_0_safe(self):
        # default_flow_style = None
        yaml = YAML(typ='safe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_0_unsafe(self):
        # default_flow_style = None
        yaml = YAML(typ='unsafe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_rt(self):
        yaml = YAML()
        yaml.register_class(User1)
        ys = """
        - !user Anthon-18
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_safe(self):
        yaml = YAML(typ='safe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_unsafe(self):
        yaml = YAML(typ='unsafe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)


class TestDecorator:
    def test_decorator_implicit(self):
        from ruyaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User2:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        ys = """
        - !User2
          name: Anthon
          age: 18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys, unordered_lines=True)

    def test_decorator_explicit(self):
        from ruyaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User3:
            yaml_tag = u'!USER'

            def __init__(self, name, age):
                self.name = name
                self.age = age

            @classmethod
            def to_yaml(cls, representer, node):
                return representer.represent_scalar(
                    cls.yaml_tag, u'{.name}-{.age}'.format(node, node)
                )

            @classmethod
            def from_yaml(cls, constructor, node):
                return cls(*node.value.split('-'))

        ys = """
        - !USER Anthon-18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys)
