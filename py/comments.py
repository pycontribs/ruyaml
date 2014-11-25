from __future__ import absolute_import
from __future__ import print_function

__all__ = ["CommentedSeq", "CommentedMap", "CommentedOrderedMap",
           "CommentedSet", 'comment_attrib']

"""
stuff to deal with comments on dict/list/ordereddict/set
"""

from collections import MutableSet

from .compat import ordereddict

comment_attrib = '_yaml_comment'


class Comment(object):
    # sys.getsize tested the Comment objects, __slots__ make them bigger
    # and adding self.end did not matter
    attrib = '_yaml_comment'

    def __init__(self):
        self.comment = None  # [post, [pre]]
        # map key (mapping/omap/dict) or index (sequence/list) to a  list of
        # dict: post_key, pre_key, post_value, pre_value
        # list: pre item, post item
        self._items = {}
        # self._start = [] # should not put these on first item
        self._end = []  # end of document comments

    def __str__(self):
        if self._end:
            end = ',\n  end=' + str(self._end)
        else:
            end = ''
        return "Comment(comment={0},\n  items={1}{2})".format(
            self.comment, self._items, end)

    @property
    def items(self):
        return self._items

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def start(self):
        return self._start

    @end.setter
    def start(self, value):
        self._start = value


# to distinguish key from None
def NoComment():
    pass


class CommentedBase(object):
    @property
    def ca(self):
        if not hasattr(self, Comment.attrib):
            setattr(self, Comment.attrib, Comment())
        return getattr(self, Comment.attrib)

    def yaml_end_comment_extend(self, comment, clear=False):
        if clear:
            self.ca.end = []
        self.ca.end.extend(comment)

    def yaml_key_comment_extend(self, key, comment, clear=False):
        l = self.ca._items.setdefault(key, [None, None, None, None])
        if clear or l[1] is None:
            if comment[1] is not None:
                assert isinstance(comment[1], list)
            l[1] = comment[1]
        else:
            l[1].extend(comment[0])
        l[0] = comment[0]

    def yaml_value_comment_extend(self, key, comment, clear=False):
        l = self.ca._items.setdefault(key, [None, None, None, None])
        if clear or l[3] is None:
            if comment[1] is not None:
                assert isinstance(comment[1], list)
            l[3] = comment[1]
        else:
            l[3].extend(comment[0])
        l[2] = comment[0]


class CommentedSeq(list, CommentedBase):
    __slots__ = [Comment.attrib, ]

    def _yaml_add_comment(self, comment, key=NoComment):
        if key is not NoComment:
            self.yaml_key_comment_extend(key, comment)
        else:
            self.ca.comment = comment


class CommentedMap(ordereddict, CommentedBase):
    __slots__ = [Comment.attrib, ]

    def _yaml_add_comment(self, comment, key=NoComment, value=NoComment):
        """values is set to key to indicate a value attachment of comment"""
        if key is not NoComment:
            self.yaml_key_comment_extend(key, comment)
        elif value is not NoComment:
            self.yaml_value_comment_extend(value, comment)
        else:
            self.ca.comment = comment


class CommentedOrderedMap(CommentedMap):
    __slots__ = [Comment.attrib, ]


class CommentedSet(MutableSet, CommentedMap):
    __slots__ = [Comment.attrib, 'odict']

    def __init__(self, values=None):
        self.odict = ordereddict()
        MutableSet.__init__(self)
        if values is not None:
            self |= values

    def add(self, value):
        """Add an element."""
        self.odict[value] = None

    def discard(self, value):
        """Remove an element.  Do not raise an exception if absent."""
        del self.odict[value]

    def __contains__(self, x):
        return x in self.odict

    def __iter__(self):
        for x in self.odict:
            yield x

    def __len__(self):
        return len(self.odict)

    def __repr__(self):
        return 'set({0!r})'.format(self.odict.keys())
