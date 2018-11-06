from NodeGraphQt import Node
import os,json

class TextNode(Node):
    """
    A example of a node with a added text input.
    """

    # set unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set initial default node name.
    NODE_NAME = 'Text node'

    def __init__(self):
        super(TextNode, self).__init__()
        path_json="NodeGraphQt/nodes/jsonFile/Inputtextnode.json"
        if os.path.isfile(path_json):
            with open(path_json) as file:
                dict_all = json.loads(file.read())
            #print dict_all
            inputlen=len(dict_all["input"])
            outputlen=len(dict_all["output"])
            for i in range(inputlen):
                self.add_input(dict_all["input"][i])
            for i in range(outputlen):
                self.add_output(dict_all["output"][i])
