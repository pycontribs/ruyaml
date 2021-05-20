# coding: utf-8

try:
    import numpy
except:  # NOQA
    numpy = None


def Xtest_numpy():
    import ruyaml

    if numpy is None:
        return
    data = numpy.arange(10)
    print('data', type(data), data)

    yaml_str = ruyaml.dump(data)
    datb = ruyaml.load(yaml_str)
    print('datb', type(datb), datb)

    print('\nYAML', yaml_str)
    assert data == datb
