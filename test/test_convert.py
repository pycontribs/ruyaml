
from ruamel.yaml.convert.html import HTML2YAML
from textwrap import dedent

class Bin:
    pass

class TestH2Y:
    sample1 = dedent("""\
        text:
        - |-
          This is an example text, spanning multiple lines, and it has embedded elements
          like
        - a:
          - .attribute:
              p: value
          - this
        - and
        - b: this
        - '.  There is also a list:'
        - quote:
          - text:
            - |-
              The text of the quote, spanning multiple lines, and it has
                      embedded elements like
            - c:
              - .attribute:
                  p: value
              - this
            - and
            - b: this
          - author: The Author of this quote
        - Text continues here.
        """)


    def test_00(self):
        b = Bin()
        b.strip = True
        h2y = HTML2YAML(b)
        d = h2y.html_to_data(dedent("""\
        <text>
        This is an example text, spanning multiple lines, and it has embedded elements
        like <a p="value">this</a> and <b>this</b>.  There is also a list:
             <quote>
                <text>The text of the quote, spanning multiple lines, and it has
                embedded elements like <c p="value">this</c> and <b>this</b></text>
                <author>The Author of this quote</author>
            </quote>
        Text continues here.
        </text>
        """))
        if 'html' in d:
            d = d['html']['body']
        res = h2y.data_to_yaml(d)
        assert res == self.sample1


    def XXtest_01(self):
        y2h = YAML2HTML(b)
        d = y2h.yaml_to_data(self.sample1)
