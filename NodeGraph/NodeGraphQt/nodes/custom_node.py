from NodeGraphQt import Node
import os,json

class CustomNode(Node):
    """
    This is a example test node.
    """
    # set a unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set the initial default node name.
    NODE_NAME = 'Custom Node'

    def __init__(self):
        super(CustomNode, self).__init__()
        self.set_color(81, 54, 88)
        path_json="NodeGraphQt/nodes/jsonFile/CustomNode.json"
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
