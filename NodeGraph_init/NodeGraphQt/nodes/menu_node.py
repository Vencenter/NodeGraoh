from NodeGraphQt import Node
import os,json

class DropdownMenuNode(Node):
    """
    A example of a node with a added menu and a few input & outputs.
    """

    # set unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set initial default node name.
    NODE_NAME = 'Menu node'

    def __init__(self):
        super(DropdownMenuNode, self).__init__()
        path_json="NodeGraphQt/nodes/jsonFile/menu.json"
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
