from Property_class import Property

class Element(list):
    def __init__(self, category, identifier):
        # Initialize a generic Element with a category/name and an identifier/ID
        self.setCategory(category)
        self.setIdentifier(identifier)

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def getCategory(self):
        return self.category

    def setCategory(self, category):
        self.category = category

    def deserialize(self, currentLine, infile):
        lineList = currentLine.strip('\n').strip().split(': ')
        try:
            self.setIdentifier(lineList[1])
        except IndexError:
            print(lineList)
            self.setIdentifier('')
        # Read a single line and add the info to a new Property of an Element child class as long it is not an 'End:'
        # line. This is intended to be used only in the child classes in super() or overridden in the child class.
        currentLine = infile.readline()
        while not currentLine.startswith('End:'):
            if not currentLine == '\n':
#                p = Property(None)
                lineList = currentLine.strip('\n').strip().split(': ')
                p = Property(lineList[0])
                try:
                    p.setValue(lineList[1])
                except IndexError:
                    p.setValue('')
                self.__class__.add(self, p)
                currentLine = infile.readline()
            else:
                currentLine = infile.readline()

    def serialize(self, outfile):
        # Print Element object to file and then print 'End:'
        if(not self.getIdentifier() == ''):
            outfile.write(self.getCategory() + ': ' + self.getIdentifier() + '\n')
        else:
            outfile.write(self.getCategory() + ':\n')
        for line in self:
            if(line.getName() == ''):
                outfile.write('\n')
            elif(line.getName() == 'Release Rate'):
                pass
            elif(self.getCategory() == 'Reservoir' and line.getName() == 'Downstream'):

                outfile.write('     ' + line.getName() + ': ' + line.getAsString() + '\n\n')
            elif(not line.getAsString() == ''):
                outfile.write('     ' + line.getName() + ': ' + line.getAsString() + '\n')
            elif(line.getName().startswith('End')):
                outfile.write('     ' + line.getName() + '\n')
            else:
                outfile.write('     ' + line.getName() + ':\n')
        outfile.write('End:\n\n')

    def add(self, a):
        # Adds a Property object to current instance of Element
        super(Element, self).append(a)

    def remove(self, a):
        # Removes a Property object from current instance of Element
        try:
            super(Element, self).remove(a)
        except LookupError:
            print("Property not found.")
