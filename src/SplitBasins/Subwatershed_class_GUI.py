import javax.swing as swing
import java.awt as awt

class Subwatershed(dict):

    # List of required keys for Subwatershed dict item
    _keys = ['watershed', 'subwatershed', 'basinin', 'basinout', 'pdatafile', 'dssfile', 'redevelopment', 'curvenumber',
             'releaserate']

    @classmethod
    def getKeys(cls):
        return cls._keys

    def __init__(self):
        # Initialize this instance to None, then get properties from user
        for key in self._keys:
            self[key] = None
        self.chooseWatershed()
        self.getFilenames()
        self.getParams()

    def chooseWatershed(self):
        # GUI to choose the watershed and subwatershed
        self['watershed'] = None
        self['subwatershed'] = None

    def getFilenames(self):
#        default_path = 'C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek/Stony_V1.0/' \
#                       'HydrologicModels/ExistingConditions/LucasDitch/LUDT_DesignRuns'
        default_path = 'C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src/HEC-HMSModels/LucasDitch/LUDT_DesignRuns'
        # GUI to get filename of *.basin file for reading - this is from the source version
        basinchoice = swing.JFileChooser(default_path)  #FileFilter="basin"
        #        filter = swing.JFileChooser.FileNameExtensionFilter("*.basin files",["basin"])
        #        basinin.addChoosableFileFilter(filter)
        basinchoice.setDialogTitle('Choose the source *.basin file (old version)')
        #        basinchoice.SetFileFilter(FileNameExtensionFilter('*.basin files', 'basin'))
        basinfile = basinchoice.showOpenDialog(None)
        self['basinin'] = str(basinchoice.selectedFile)

        # GUI to get filename of *.basin file for writing - this is for the new version
        basinchoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the sink *.basin file (new version)')
        basinfile = basinchoice.showOpenDialog(None)
        self['basinout'] = str(basinchoice.selectedFile)

        # GUI to get filename of the *.pdata file - this is for the new version
        pdatachoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the *.pdata file (new version)')
        pdatafile = pdatachoice.showOpenDialog(None)
        self['pdatafile'] = str(pdatachoice.selectedFile)

        # GUI to get filename of the *.dss file - this is for the new version
        dsschoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the *.dss file (new version)')
        dssfile = dsschoice.showOpenDialog(None)
        self['dssfile'] = str(dsschoice.selectedFile)

    def setParams(self, rd, cn, rr, frame):
        # Save the future conditions parameters to the current instance of Subwatershed
        self['redevelopment'] = float(15) #rd.text #float(rd.text)
        self['curvenumber'] = float(88) #cn.text #float(cn.text)
        self['releaserate'] = float(0.15) #rr.text #float(rr.text)
        print('setParams')
        frame.dispose()
    #        self.initElements()
    #        readBasinFile(self['basinin'], self['basinout'])

    def getParams(self):
        # GUI to get future % of subbasin redeveloped, curve number, and release rate
        # Initialize window for UI
        frame = swing.JFrame("Set conditions of redeveloped portion of subbasin", layout=awt.BorderLayout())
        frame.setDefaultCloseOperation(swing.JFrame.EXIT_ON_CLOSE)

        # Create panel that includes three text entry fields for % redeveloped, curve number, and release rate
        futureparams = swing.JPanel(layout=awt.GridLayout(3,2))
        inbutton = swing.JPanel()
        futureparams.add(swing.JLabel('Percent Redevelopment '))
        rd = swing.JTextField('', 5)
        futureparams.add(rd)
        futureparams.add(swing.JLabel('Future Curve Number '))
        cn = swing.JTextField('', 5)
        futureparams.add(cn)
        futureparams.add(swing.JLabel('Release Rate '))
        rr = swing.JTextField('', 5)
        futureparams.add(rr)

        # Create panel for button that stores the values entered
        setButton = swing.JButton('Set parameters', actionPerformed=(lambda x: self.setParams(rd, cn, rr, frame)))
        self.setParams(rd, cn, rr, frame)

        # Add panels to the window and make the window visible
        frame.add(futureparams, awt.BorderLayout.NORTH)
        inbutton.add(setButton)
        frame.add(inbutton, awt.BorderLayout.SOUTH)
        #        setButton.addMouseListener(awt.event.MouseListener.mouseClicked(self, self.setParams(rd, cn, rr, frame)))
        frame.pack()
#        frame.setVisible(True)
