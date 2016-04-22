from Element_class import Element


class Basin(Element):
    def __init__(self):
        super(Basin, self).__init__('Basin', None)

    @classmethod
    def readBasin(cls, currentLine, basinsrc, basinsink):
        b = Basin()
        super(Basin, b).deserialize(currentLine, basinsrc)
        b.serialize(basinsink)
        return b
