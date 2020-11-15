if __name__ == '__main__':
    import distutils.util
    import os
    import sys

    build_lib = 'build/lib'
    build_lib_ext = os.path.join(
        'build', 'lib.%s-%s' % (distutils.util.get_platform(), sys.version[0:3])
    )
    sys.path.insert(0, build_lib)
    sys.path.insert(0, build_lib_ext)
    import test_appliance
    import test_yaml_ext

    test_appliance.run(test_yaml_ext)
