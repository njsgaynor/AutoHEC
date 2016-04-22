from Element_class import Element

class BasinSchema(Element):
    def __init__(self):
        super(BasinSchema, self).__init__('Basin Schematic Properties', None)

    @classmethod
    def readBasinSchema(cls, currentLine, basinsrc, basinsink):
        b = BasinSchema()
        super(BasinSchema, b).deserialize(currentLine, basinsrc)
        b.serialize(basinsink)
        return b
