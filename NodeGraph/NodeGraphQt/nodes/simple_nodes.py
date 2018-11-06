from NodeGraphQt import Node
import os,json

class FooNode(Node):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # set a unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set the initial default node name.
    NODE_NAME = 'Foo Node'

    def __init__(self):
        super(FooNode, self).__init__()
        # set the node color.
        #self.set_color(2, 67, 81)
        path_json="NodeGraphQt/nodes/jsonFile/FooNode.json"
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


class BarNode(Node):
    """
    A node class with 3 inputs and 3 outputs.
    """

    # set unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set initial default node name.
    NODE_NAME = 'Bar Node'

    def __init__(self):
        super(BarNode, self).__init__()
        path_json="NodeGraphQt/nodes/jsonFile/BarNode.json"
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
