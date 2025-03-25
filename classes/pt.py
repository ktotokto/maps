class PtList:
    def __init__(self, styles):
        self.list_coord = [styles]

    def add_pt(self, coordinates):
        self.list_coord.insert(0, coordinates)