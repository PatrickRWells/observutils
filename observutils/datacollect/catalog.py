import os
from astropy.table import Table
from astropy.io import  fits


class catalog:
    def __init__(self, url):
        self.url = url
    def search(self):
        """
        Search the catalog
        """
        pass

class catalogData:
    """
    Basic container class for data returned from a catalog query.
    Can write to file

    """

    def __init__(self, data, metadata, format='astropy', **kwargs):
        self.data = data
        self.meta = metadata
        self.format = format

    def toFile(self, fname, outformat='fits', savemeta=False):
        """
        Writes the catalog data to a file to be used later.
        ---------------
        params:
        fname: string, output file name
        format: output format, currently fits or pickle
        
        """
        if not savemeta:
            if outformat == 'pickle':
                import pickle
                pickle.dump(self, open(fname, 'wb'))

            if outformat == 'fits':
                hdus = []
                primary = fits.PrimaryHDU()
                primary.header['OBUTILS'] = True
                primary.header['META'] = savemeta
                primary.header['FORMAT'] = self.format
                hdus.append(primary)    
                if self.format == 'astropy':
                    data_hdu = fits.table_to_hdu(self.data)
                    hdus.append(data_hdu)
            
                output = fits.HDUList(hdus)
                if fname.endswith('fits'):
                    output.writeto(fname)
                else:
                    output.writeto('.'.join([fname, 'fits']))



def openCatalogData(fname, **kwargs):
    """
    Open catalog data that was previous written to file
    -------------------
    params:
    fname: name  of file
    
    """
    if not os.path.exists(fname):
        print("ERROR: file {} does not exist".format(fname))
        return

    if fname.endswith('.fits'):
        raw_data = fits.open(fname)
        try:
            isCatalogData = raw_data[0].header['OBUTILS']
        except:
            print("Error: file does not contain catalog data")
        data = catalogData(Table(raw_data[1].data), None, 'astropy')

    else:
        try:
            import pickle
            data = pickle.load(open(fname, 'rb'))
        except:
            print("Error: Unable to read file {}".format(fname))

    if type(data) != type(catalogData(None, None)):
        print("Error: file {} does not contain catalog data".format(fname))
    else:
        return data