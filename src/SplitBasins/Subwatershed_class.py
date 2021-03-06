class Subwatershed(dict):

    # List of required keys for Subwatershed dict item
    _keys = ['watershed', 'subwatershed', 'basinin', 'basinout', 'pdatafile', 'dssfile', 'redevelopment', 'curvenumber',
             'releaserate']

    @classmethod
    def getKeys(cls):
        return cls._keys

    def __init__(self, config):
        # Initialize this instance to None, then get properties from user
        for key in self._keys:
            self[key] = None
        self.chooseWatershed()
        self.setFilenames(config)
        self.setParams(config)

    def chooseWatershed(self):
        # GUI to choose the watershed and subwatershed
        self['watershed'] = None
        self['subwatershed'] = None

    def setFilenames(self, config):
        self['basinin'] = str(config.basinin)
        self['basinout'] = str(config.basinout)
        self['pdatafile'] = str(config.pdatafile)
        self['dssfile'] = str(config.dssfile)

    def setParams(self, config):
        # Save the future conditions parameters to the current instance of Subwatershed
        self['redevelopment'] = float(config.redevelopment)
        self['redevelopmentalt'] = float(config.redevelopmentalt)
        self['redevelopmentalt2'] = float(config.redevelopmentalt2)
        self['curvenumber'] = float(config.curvenumber)
        self['releaserate'] = float(config.releaserate)
        self['releaseratealt'] = float(config.releaseratealt)
        self['releaseratealt2'] = float(config.releaseratealt2)
        self['canopyrate'] = float(config.canopyrate)
        self['canopyalt'] = float(config.canopyalt)
