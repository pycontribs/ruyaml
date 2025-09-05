version: 0.2
text: md
pdf: false
--- |
# Overview

`ruyaml` is a YAML 1.2 loader/dumper package for Python. It is a
derivative of Kirill Simonov\'s [PyYAML
3.11](https://bitbucket.org/xi/pyyaml).

`ruyaml` supports [YAML 1.2]() and has round-trip loaders and
dumpers. A round-trip is a YAML load-modify-save sequence and
ruyaml tries to preserve, among others:

-   comments
-   block style and key ordering are kept, so you can diff the
    round-tripped source
-   flow style sequences ( \'a: b, c, d\') (based on request and test by
    Anthony Sottile)
-   anchor names that are hand-crafted (i.e. not of the form`idNNN`)
-   [merges](http://yaml.org/type/merge.html) in dictionaries are
    preserved

This preservation is normally not broken unless you severely alter the
structure of a component (delete a key in a dict, remove list entries).
Reassigning values or replacing list items, etc., is fine.

For the specific 1.2 differences see
`yaml-1-2-support`{.interpreted-text role="ref"}

Although individual indentation of lines is not preserved, you can
specify separate indentation levels for mappings and sequences (counting
for sequences does **not** include the dash for a sequence element) and
specific offset of block sequence dashes within that indentation.

Although `ruyaml` still allows most of the PyYAML way of doing
things, adding features required a different API then the transient
nature of PyYAML\'s `Loader` and `Dumper`. Starting with `ruyaml`
version 0.15.0 this new API gets introduced. Old ways that get in the
way will be removed, after first generating warnings on use, then
generating an error. In general a warning in version 0.N.x will become
an error in 0.N+1.0

Many of the bugs filed against PyYAML, but that were never acted upon,
have been fixed in `ruyaml`
--- !inc-raw |
links.rydinc

