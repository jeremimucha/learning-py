# Implementation:
# A Tree of Nodes
# FirstTag - start of the document
# ChildNode - state that decides to which state to switch
# OpenTag - new opening tag found
# CloseTag - closing tag found
# Text - contents of the tag we're currently in
from xml_parser_states import Node, ChildNode, OpenTag, CloseTag, TextNode, FirstTag


class Parser:

    def __init__(self, parse_string):
        self.parse_string = parse_string
        self.root = None
        self.current_node = None

        self.state = FirstTag()

    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)

    def start(self):
        self.process(self.parse_string)


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as file:
        contents = file.read()
        p = Parser(contents)
        p.start()

        nodes = [p.root]
        while nodes:
            node = nodes.pop(0)
            print(node)
            nodes = node.children + nodes
