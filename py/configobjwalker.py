

def configobj_walker(cfg):
    """
    walks over a ConfigObj (INI file with comments) generating
    corresponding YAML output (including comments
    """
    from configobj import ConfigObj
    assert isinstance(cfg, ConfigObj)
    for c in cfg.initial_comment:
        if c.strip():
            yield c
    for s in _walk_section(cfg):
        if s.strip():
            yield s
    for c in cfg.final_comment:
        if c.strip():
            yield c


def _walk_section(s, level=0):
    from configobj import Section
    assert isinstance(s, Section)
    indent = '  ' * level
    for name in s.scalars:
        for c in s.comments[name]:
            yield indent + c.strip()
        line = '{0}{1}: {2}'.format(indent, name, s[name])
        c = s.inline_comments[name]
        if c:
            line += ' ' + c
        yield line
    for name in s.sections:
        for c in s.comments[name]:
            yield indent + c.strip()
        line = '{0}{1}:'.format(indent, name)
        c = s.inline_comments[name]
        if c:
            line += ' ' + c
        yield line
        for val in _walk_section(s[name], level=level+1):
            yield val
