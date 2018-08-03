# coding: utf-8

from __future__ import print_function

import pytest  # NOQA

from roundtrip import save_and_run  # NOQA


def test_monster(tmpdir):
    program_src = u'''\
    import ruamel.yaml
    from textwrap import dedent

    class Monster(ruamel.yaml.YAMLObject):
        yaml_tag = u'!Monster'

        def __init__(self, name, hp, ac, attacks):
            self.name = name
            self.hp = hp
            self.ac = ac
            self.attacks = attacks

        def __repr__(self):
            return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
                self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

    data = ruamel.yaml.load(dedent("""\\
        --- !Monster
        name: Cave spider
        hp: [2,6]    # 2d6
        ac: 16
        attacks: [BITE, HURT]
    """), Loader=ruamel.yaml.Loader)
    # normal dump, keys will be sorted
    assert ruamel.yaml.dump(data) == dedent("""\\
        !Monster
        ac: 16
        attacks: [BITE, HURT]
        hp: [2, 6]
        name: Cave spider
    """)
    '''
    assert save_and_run(program_src, tmpdir) == 0
