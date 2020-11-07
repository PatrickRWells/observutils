
A set of utilities used when preparing for and processing astronomical observations.

## Installation

    git clone https://github.com/PatrickRWells/observutils.git
    cd observutils
    pip install -e .

It is recommended you install in development mode (-e) since the code is being updated frequently. 

Currently this package includes only two real functionalities.

## Querying the PAN-STARRS1 catalog

    from observutils.datacollect import panstarrs
    client = panstarrs.client()
    searchdata = client.regionsearch(ra=ra, dec=dec,radius=radius)
 
The default unit for the radius is arcmins, but this can be changed by passing one of (deg, min, sec) to the 'unit' parameter
You can choose whether to search the mean, stacked, or detection catalogs by passing one of (mean, stack, detection) to the 'table' parameter
Defaults to data release 2, this can be changed with release="dr1". The output format can either be an astropy table (default) or a pandas dataframe (outformat='pandas')

The client returns a basic container class. The search results themsleves are contained in `searchdata.data` and metadata is contained in `searchdata.meta`. The metadata contains information about all the columns in the search results. 

If you want to get a particular set of columns, you can pass them as a list (`columns=listofcolumns`). Without this argument, returns a set of defaults. For information about available columns, see http://archive.stsci.edu/panstarrs/help/columns.html

Once you have the catalog data object, you can write it to file with `searchdata.toFile(fname=filename)`. This data can be reloaded with the following:

    from observutils.datacollect import catalog
    searchdata = catalog.openCatalogData(fname)

Currently, data is written to file using the pickle module, which means the file is not human-readable. In the future, I may add options to output to other datatypes (i.e. csv)

## Converting source extractor data to ds9 region file

The package comes with a script to convert sextractor ouptuts to a ds9 region file. Once the package has been installed, this can be done with:

    sext2reg infile outfile [-f/--format radec OR pix]

Default output format uses ra and dec for position data, but can also use pixel positions.
