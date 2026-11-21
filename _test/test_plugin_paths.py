import os
from types import SimpleNamespace
from typing import Any

from ruyaml import YAML, main


def test_explicit_plugin_path_is_imported(monkeypatch: Any) -> None:
    seen = []
    plugin = SimpleNamespace(typ='rt', init_typ=lambda yaml: None)
    monkeypatch.setattr(YAML, 'official_plug_ins', lambda self: [])
    monkeypatch.setattr(main, 'import_module', lambda name: seen.append(name) or plugin)
    YAML(plug_ins=[os.path.join('sample', 'plugin')])
    assert seen == ['sample.plugin']


def test_official_plugin_paths_are_discovered(monkeypatch: Any) -> None:
    plugin = os.path.join(os.path.dirname(main.__file__), 'sample', '__plug_in__.py')
    monkeypatch.setattr(main.glob, 'glob', lambda pattern: [plugin])
    yaml = YAML.__new__(YAML)
    assert yaml.official_plug_ins() == [os.path.join('ruyaml', 'sample', '__plug_in__')]
