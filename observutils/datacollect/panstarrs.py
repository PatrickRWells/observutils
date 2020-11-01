from observutils.datacollect.catalog import catalog
import requests
from astropy.table import Table
import numpy as np

class panstarrsClient(catalog):
    """
    Client for communicating with the Panstarrs catalog
    Much of this code is originally borrowed from a
    jupyter notebook made available by STScI.
    See https://outerspace.stsci.edu/display/PANSTARRS/How+to+retrieve+and+use+PS1+data
    """
    def __init__(self):
        super().__init__(url='https://catalogs.mast.stsci.edu/api/v0.1/panstarrs')
    
    def regionSearch(self, ra, dec, radius, r_unit = 'sec', table="mean",release="dr2",format="json",columns=None,
            verbose=False, **kwargs):
        """Do a search in a region
        
        Parameters
        ----------
        ra (float): (degrees) J2000 Right Ascension
        dec (float): (degrees) J2000 Declination
        radius (float): (degrees) Search radius (<= 0.5 degrees)
        r_unit (string): deg, min (arcmin) or sec (arcsec). Defaults to sec
        table (string): mean, stack, or detection
        release (string): dr1 or dr2
        format: csv, votable, json
        columns: list of column names to include (None means use defaults)
        baseurl: base URL for the request
        verbose: print info about request
        **kw: other parameters (e.g., 'nDetections.min':2)
        """
        
        data = kwargs.copy()
        data['ra'] = ra
        data['dec'] = dec
        data['radius'] = self.parseRadius(radius, r_unit)
        return self.search(table=table,release=release,format=format,columns=columns,
                        verbose=verbose, **data)

    def parseRadius(self, radius, r_unit='sec'):

        if r_unit not in ('deg', 'min', 'sec'):
            print("Error in search: Units of radius must be one of"\
                " deg, min, sec")

        if r_unit == 'deg':
            print("Searching in radius of {} degrees".format(radius))
            rad_parse = radius
        
        else:
            rad_parse = radius/60.0
            if r_unit == 'sec':
                rad_parse /= 60.0
        print('Searching in radius of {} {} = {} degrees'.format(radius, r_unit, round(rad_parse, 5)))

        return rad_parse
       

    def search(self, table="mean",release="dr2",format="json",columns=None,
                verbose=False, **kwargs):
        """Do a general search of the PS1 catalog (possibly without ra/dec/radius)
        
        Parameters
        ----------
        table (string): mean, stack, or detection
        release (string): dr1 or dr2
        format: csv, votable, json
        columns: list of column names to include (None means use defaults)
        baseurl: base URL for the request
        verbose: print info about request
        **kwargs: other parameters (e.g., 'nDetections.min':2).  Note this is required!
        """
        
        data = kwargs.copy()
        if not data:
            raise ValueError("You must specify some parameters for search")
        self.checkvalid(table,release)
        if format not in ("csv","votable","json"):
            raise ValueError("Bad value for format")

        url = "{}/{}/{}.{}".format(self.url, release, table, format)
        if columns:
            # check that column values are legal
            # create a dictionary to speed this up
            dcols = {}
            for col in self.metadata(table,release)['name']:
                dcols[col.lower()] = 1
            badcols = []
            for col in columns:
                if col.lower().strip() not in dcols:
                    badcols.append(col)
            if badcols:
                raise ValueError('Some columns not found in table: {}'.format(', '.join(badcols)))
            # two different ways to specify a list of column values in the API
            # data['columns'] = columns
            data['columns'] = '[{}]'.format(','.join(columns))

        # either get or post works
        r = requests.get(url, params=data)

        if verbose:
            print(r.url)
        r.raise_for_status()
        if format == "json":
            output = self.parseReturn(r.json(), **kwargs)
            return output
        else:
            return r.text
    

    def parseReturn(self, data, dtype='json', outformat='astropy', **kwargs):
        obj_data = data['data']
        col_names = [item['name'] for item in data['info']]
        if outformat == 'pandas':
            from pandas import DataFrame
            obj_frame = DataFrame(data=obj_data, columns=col_names)
            info_frame = DataFrame.from_dict(data['info'])
        
        elif outformat == 'astropy':
            obj_frame = Table(data=np.array(obj_data), names=col_names)
            info_frame = Table(data['info'])

        else:
            print('Error: Unknown format for data output')
            exit()

        return (obj_frame, info_frame)

    def checkvalid(self, table,release):
        """Checks if this combination of table and release is acceptable
        
        Raises a VelueError exception if there is problem
        """
        
        releaselist = ("dr1", "dr2")
        if release not in ("dr1","dr2"):
            raise ValueError("Bad value for release (must be one of {})".format(', '.join(releaselist)))
        if release=="dr1":
            tablelist = ("mean", "stack")
        else:
            tablelist = ("mean", "stack", "detection")
        if table not in tablelist:
            raise ValueError("Bad value for table (for {} must be one of {})".format(release, ", ".join(tablelist)))

  
    def metadata(self, table="mean",release="dr2"):
        """Return metadata for the specified catalog and table
        
        Parameters
        ----------
        table (string): mean, stack, or detection
        release (string): dr1 or dr2
        baseurl: base URL for the request
        
        Returns an astropy table with columns name, type, description
        """
        
        self.checkvalid(table,release)
        url = "{baseurl}/{release}/{table}/metadata".format(self.url, release, table, )
        r = requests.get(url)
        r.raise_for_status()
        v = r.json()
        # convert to astropy table
        tab = Table(rows=[(x['name'],x['type'],x['description']) for x in v],
                names=('name','type','description'))
        return tab

            


if __name__ == '__main__':
    client = panstarrsClient()
    data = client.regionSearch(ra=13.4349, dec=-20.2091, radius=5)
    print(type(data))