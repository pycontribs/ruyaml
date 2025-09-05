# coding: utf-8

import sys
import pytest  # type:ignore  # NOQA

last_to_warn = (0, 17, 40)


@pytest.mark.skipif(sys.version_info < (3, 7) or sys.version_info >= (3, 9),  # type: ignore
                    reason='collections not available?')
def test_collections_deprecation() -> None:
    with pytest.warns(DeprecationWarning):
        from collections import Hashable  # type: ignore  # NOQA


class TestFunctionDeprecation:
    def test_deprecation_scan(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            with pytest.warns(PendingDeprecationWarning):
                data = ruyaml.load('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.load('a: 42')  # NOQA

    def test_deprecation_parse(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            data = ruyaml.parse('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_compose(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            with pytest.warns(PendingDeprecationWarning):
                data = ruyaml.compose('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_compose_all(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            data = ruyaml.compose_all('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_load(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            with pytest.warns(PendingDeprecationWarning):
                data = ruyaml.load('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_load_all(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            data = ruyaml.load_all('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_safe_load(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            with pytest.warns(PendingDeprecationWarning):
                data = ruyaml.safe_load('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA

    def test_deprecation_round_trip_load(self) -> None:
        import ruyaml

        if ruyaml.version_info <= last_to_warn:
            with pytest.warns(PendingDeprecationWarning):
                data = ruyaml.round_trip_load('a: 42')  # NOQA
        else:
            with pytest.raises(AttributeError):
                data = ruyaml.parse('a: 42')  # NOQA


class TestYamlTyp:
    def test_unsafe_deprecation(self) -> None:
        import ruyaml

        if ruyaml.version_info < (0, 18, 0):
            yaml = ruyaml.YAML(typ='unsafe')
        else:
            with pytest.warns(PendingDeprecationWarning):
                #   with pytest.raises(SystemExit):
                yaml = ruyaml.YAML(typ='unsafe')  # NOQA

    def test_full_load_error(self) -> None:
        import ruyaml

        yaml = ruyaml.YAML(typ='full', pure=True)
        with pytest.raises(ruyaml.error.YAMLError):
            yaml.load('a: b')
        yaml = ruyaml.YAML(typ='full')  # C scanner/loader
        with pytest.raises(ruyaml.error.YAMLError):
            yaml.load('a: b')

    def test_full_rt(self) -> None:
        import os
        import io
        import ruyaml

        yaml = ruyaml.YAML(typ='full', pure=True)
        buf = io.BytesIO()
        yaml.dump([{'fun': os.system}], buf)
        print(buf.getvalue())
        yaml = ruyaml.YAML()
        data = yaml.load(buf.getvalue())
        print(data)
        ts = data[0]['fun']
        assert 'posix.system' in str(ts.tag)
