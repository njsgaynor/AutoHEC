<h1>Splitting subbasins: part of the AutoHEC package</h1>
<p>Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016).<br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0,and 
HEC-DSSVue 2.0.1</em><br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Creators: Nicole JS Gaynor, ISWS</em></p>


<h4>Purpose</h4>
<p>This program was built to split subbasins in the HEC-HMS model into a
developed portion and an undeveloped portion. The developed portion routes
through a reservoir. Then the reservoir and the undeveloped portion of the 
subbasin route through a shared junction. Output from this file includes 
a pickle file that stores the subbasin name, storage-outflow table name, 
the maximum release rate in cfs/acre for the reservoir, and the area of 
the subbasin. This data is then used in the AutoHEC package to create 
rating curves for each reservoir for a second HEC-HMS run.</p>


<h4>How to run code that splits basins independent of running models</h4>
<p><ol><li>Modify *_hecConfig.py to find the files that need to be modified and to
reflect the characteristics of the future subbasins (must be named 
hecConfig.py, not one of the *hecConfig.py files). This will only run
for a single subsubwatershed. <strong>When preparing the bank station 
elevations file, do not include Node Names in the table (under
Options menu in the Profile Output Table of HEC-RAS).</strong>
</li><li>Open Windows Command Prompt.
</li><li>Change to directory containing runInitHMS.cmd (AutoHEC/src/WeRunFirst) 
directory ("dir" lists directory contents and "cd" changes directory).
</li><li>Type "runInitHMS.cmd" into the Windows command line and press Enter.
Output will be saved to output.txt.</li></ol></p>


<h4>Structure of subbasin splitting code</h4>
<h6>runInitHMS.cmd</h6>
<p><ul><li>description: Windows command-line script that runs InitHMS.py
and outputs to InitHMSout.txt; **may need to edit python path**
</li><li>depends on: InitHMS.py</li></ul></p>

<h6>InitHMS.py [driver script]</h6>
<p><ul><li>description: drives the process of splitting subbasins in the
specified (sub)watershed; this is the main script for the pre-
processing of data for HEC-HMS and HEC-RAS model runs
</li><li>depends on: contents of hecElements, Subwatershed_class, 
Tablenames_class, SBDict_class
</li><li>UpdatePdataFile(pd, pdatasink): not currently used.
</li><li>readBasinFile(ws): reads the input *.basin file, splits subbasins
(and does related tasks via imported modules, and writes updated
*.basin file
</li><li>modMetFile(metFile, metData, hmsPath, sbList): adds the new
subbasins to the relevant *.met file
</li><li>main(config): drives the workflow</li></ul></p>

<h6>Subwatershed_class.py</h6>
<p><ul><li>description: dictionary class that stores subwatershed
characteristics, with _keys pre-defined for watershed name, 
subwatershed name, *.basin input file, *.basin output file,
*.pdata file, *.dss file, % redevelopment, curve number, and
release rate
</li><li>depends on: None
</li><li>getKeys: returns keys for instances
</li><li>__init__(config): instantiates Subwatershed with keys in _keys;
assigns value of None to pre-defined keys. Calls functions to
add real values to keys from config file.
</li><li>chooseWatershed: assigns values to watershed and subwatershed
keys; both currently set to None
</li><li>setFilenames(config): assigns values of *.basin input file,
*.basin output file, *.pdata file, and *.dss file
</li><li>setParams(config): assigns % redevelopment, curve number,
and release rate to appropriate keys</li></ul></p>

<h6>SBDict_class.py</h6>
<p><ul><li>description: dictionary class that contains
subbasin_name:release rate pairs
</li><li>depends on: None
</li><li>__init__: instantiates basic dictionary
</li><li>add(x): adds x to the dictionary, where x is a {"key":value} pair
</li><li>remove(x): deletes item with key x from the dictionary
</li><li>getKeys: returns the keys in the dictionary
</li><li>getValues: returns the values in the dictionary
</li><li>writeSbPairs(sbOut): writes entire dictionary to JSON file
specified in sbOut</li></ul></p>

<h6>TableNames_class.py</h6>
<p><ul><li>description: list class that contains a list of lists,
where the sublist includes subbasin name, table name,
subbasin area, and release rate
</li><li>depends on: None
</li><li>__init__: instantiates basic list
</li><li>append(x): adds x to the end of the list
</li><li>remove(x): finds x and removes it from the list
</li><li>writeTableFile(tableOut): writes table to JSON file tableOut</li></ul></p>

<h6>hecElements/Property_class.py</h6>
<p><ul><li>description: dictionary class that contains 
property_name:property_value pairs, which are the basis for named
properties in the Elements class (and its child classes)
</li><li>depends on: None
</li><li>__init__(name): instantiates dictionary with key set to name and
value set to None
</li><li>newProperty(name, value) [classmethod]: instantiates new Property
with key of name and value of value
</li><li>getValue: returns value of Property instance
</li><li>getAsFloat: returns value as float; error if cannot be converted
</li><li>getAsString: returns value as string; error if cannot be converted
</li><li>getName: returns key of Property instance
</li><li>setName(name): sets key to name</li></ul></p>

<h6>hecElements/Element_class.py</h6>
<p><ul><li>description: list class that contains Property instances; parent
class for types of elements in *.basin HEC-HMS files
</li><li>depends on: Property_class
</li><li>__init__(category, identifier): instantiates Element with category
and identifier set to input values
</li><li>getIdentifer: returns value of identifer
</li><li>setIdentifer(identifier): sets identifier property to input
</li><li>getCategory: returns value of category
</li><li>setCategory(category): sets category property to input
</li><li>deserialize(currentLine, infile): reads a single element from *.basin
input file starting at line currentLine
</li><li>serialize(outfile): writes a single element to *.basin output file
</li><li>add(x): adds Property x to an Element instance
</li><li>remove(x): removes Property x from an Element instance; returns error
if property does not exit in Element instance</li></ul></p>

<h6>hecElements/Basin_class.py</h6>
<p><ul><li>description: list class that contains Property instances for Basin
items in *.basin HEC-HMS files
</li><li>depends on: Element_class
</li><li>__init__: instantiates an Element with category "Basin"
</li><li>readBasin(currentLine, basinsrc, basinsink) [classmethod]: reads a
single Basin element from *.basin input file and writes it to 
*.basin output file; returns Basin instance.</li></ul></p>

<h6>hecElements/Subbasin_class.py</h6>
<p><ul><li>description: list class that contains Property instances for
Subbasin items in *.basin HEC-HMS files
</li><li>depends on: Element_class, Property_class, Junction_class, 
Reservoir_class, copy
</li><li>__init__: instantiates an Element with category "Subbasin" and 
Properties for area, downstream, curve number, percent impervious
area, canvas x, canvas y, canopy, release rate, and percent
redevelopment; Property values set to None
</li><li>readSubbasin(currentLine, basinsrc, basinsink) [classmethod]: reads
a single Subbasin element from *.basin input file. Calls functions
that divide the subbasin, add a reservoir, and add a junction.
Assigns values as appropriate to pre-defined Properties.
Writes Subbasin element to *.basin output file; returns Subbasin
instance with Properties updated to reflect subbasin division, new 
subbasin, and name of storage-outflow table for new subbasin.
</li><li>add(x): adds Property x to instance of Subbasin, using pre-defined
Property if available; error if x is not an instance of Property.
</li><li>remove(x): removes x from instance of Subbasin or assigns value of
None if it is a pre-defined Property; returns error if not found.
</li><li>divideSubbasin(basinsink, redevel, curvenum, rlsrate): Divides 
subbasin based on percent redevelopment with new subbasin occupying
the portion that is redeveloped and old subbasin area reduced to the
remainder. Calls functions to create new Subbasin, Junction, and 
Reservoir instances. Routes new subbasin through Reservoir to
Junction and old subbasin directly to Junction so that measurements
at Junction are for entire subbasin (new + old). Sets release rate
and redevelopment percent of new subbasin.
</li><li>newSubbasin(s, basinsink, redevel, curvenum) [classmethod]: copies
Subbasin s to new instance of Subbasin. Sets properties to reflect
characteristics of redeveloped area. Writes new subbasin to *.basin
output file. Returns Subbasin instance of new subbasin.</li></ul></p>

<h6>hecElements/Junction_class.py</h6>
<p><ul><li>description: list class that contains Property instances for
Junction items in *.basin HEC-HMS files
</li><li>depends on: Element_class, Property_class
</li><li>__init__: instantiates an Element with category "Junction" and 
Property for downstream; Property value set to None
</li><li>readJunction(currentLine, basinsrc, basinsink) [classmethod]: reads
a single Junction element from *.basin input file. Writes Junction
element to *.basin output file; returns Junction instance.
</li><li>add(x): adds Property x to instance of Junction, using pre-defined
Property if available; error if x is not an instance of Property.
</li><li>remove(x): removes x from instance of Junction or assigns value of
None if it is a pre-defined Property; returns error if not found.
</li><li>newJunction(s, basinsink) [classmethod]: instantiates new Junction
and sets properties as appropriate based on those in Subbasin s.
Writes Junction element to *.basin output file. Returns instance
of Junction.</li></ul></p>

<h6>hecElements/Reservoir_class.py</h6>
<p><ul><li>description: list class that contains Property instances for
Reservoir items in *.basin HEC-HMS files
</li><li>depends on: Element_class, Property_class
</li><li>__init__: instantiates an Element with category "Reservoir" and 
Properties for downstream and storage-outflow table; Property values
set to None.
</li><li>readReservoir(currentLine, basinsrc, basinsink, redevel, rlsrate)
[classmethod]: reads a single Reservoir element from *.basin input
file. Writes Reservoir element to *.basin output file; returns 
instance of Reservoir.
</li><li>add(x): adds Property x to instance of Reservoir, using pre-defined
Property if available; error if x is not an instance of Property.
</li><li>remove(x): removes x from instance of Reservoir or assigns value of
None if it is a pre-defined Property; returns error if not found.
</li><li>newReservoir(s, basinsink) [classmethod]: instantiates new Reservoir
and sets properties as appropriate based on those in Subbasin s. Sets
storage-outflow table name based on subbasin name, % redevelopment,
and release rate. Writes Reservoir element to *.basin output file.
Returns instance of Reservoir.</li></ul></p>

<h6>hecElements/Reach_class.py</h6>
<p><ul><li>description: list class that contains Property instances for
Reach items in *.basin HEC-HMS files
</li><li>depends on: Element_class, Property_class
</li><li>__init__: instantiates an Element with category "Reach" and 
Property for downstream; Property value set to None.
</li><li>readReach(currentLine, basinsrc, basinsink) [classmethod]: reads a 
single Reach element from *.basin input file. Writes Reach
element to *.basin output file; returns instance of Reach.
</li><li>add(x): adds Property x to instance of Reach, using pre-defined
Property if available; error if x is not an instance of Property.
</li><li>remove(x): removes x from instance of Reach or assigns value of
None if it is a pre-defined Property; returns error if not found.</li></ul></p>

<h6>Diversion_class.py</h6>
<p><ul><li>description: list class that contains Property instances for
Diversion items in *.basin HEC-HMS files
</li><li>depends on: Element_class, Property_class
</li><li>__init__: instantiates an Element with category "Diversion" and 
Properties for downstream and divert to; Property values set to None.
</li><li>readDiversion(currentLine, basinsrc, basinsink) [classmethod]: reads a 
single Diversion element from *.basin input file. Writes Diversion
element to *.basin output file; returns instance of Diversion.
</li><li>add(x): adds Property x to instance of Diversion, using pre-defined
Property if available; error if x is not an instance of Property.
</li><li>remove(x): removes x from instance of Diversion or assigns value of
None if it is a pre-defined Property; returns error if not found.</li></ul></p>

<h6>hecElements/Sink_class.py</h6>
<p><ul><li>description: list class that contains Property instances for Sink
items in *.basin HEC-HMS files
</li><li>depends on: Element_class
</li><li>__init__: instantiates an Element with category "Sink"
</li><li>readSink(currentLine, basinsrc, basinsink) [classmethod]: reads a
single Sink element from *.basin input file and writes it to 
*.basin output file; returns instance of Sink.</li></ul></p>

<h6>hecElements/BasinSchema_class.py</h6>
<p><ul><li>description: list class that contains Property instances for Basin
Schematic Properties items in *.basin HEC-HMS files
</li><li>depends on: Element_class
</li><li>__init__: instantiates an Element with category "Basin Schematic
Properties"
</li><li>readBasinSchema(currentLine, basinsrc, basinsink) [classmethod]:
reads a single Basin Schematic Properties element from *.basin input
file and writes it to *.basin output file; returns instance of
BasinSchema.</li></ul></p>

<h6>hecElements/Pdata_class.py</h6>
<p><ul><li>description: provides the properties of a Table that will be
added to the *.pdata file
</li><li>depends on: Element_class, Property_class, datetime.datetime,
calendar
</li><li>__init__: instantiates new Element item with category "Table";
Properties for DSS file that contains the storage-outflow table
and the path to the table within the DSS file.
</li><li>newPdata(soname, pdatasink, dssfile) [classmethod]: instantiates
new Pdata; creates and adds all Properties for new entry in *.pdata
file. Writes instance to *.pdata file.</li></ul></p>
	