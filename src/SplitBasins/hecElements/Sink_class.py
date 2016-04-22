from Element_class import Element

class Sink(Element):
    def __init__(self):
        super(Sink, self).__init__('Sink', None)

    @classmethod
    def readSink(cls, currentLine, basinsrc, basinsink):
        s = Sink()
        super(Sink, s).deserialize(currentLine, basinsrc)
        s.serialize(basinsink)
        return s
