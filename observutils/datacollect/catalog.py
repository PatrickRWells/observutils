import os

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

    def __init__(self, data, metadata, **kwargs):
        self.data = data
        self.meta = metadata

    def toFile(self, fname, format='pickle'):
        """
        Writes the catalog data to a file to be used later.
        ---------------
        params:
        fname: string, output file name
        format: output format, currently only pickle is supported
        
        """
        if format == 'pickle':
            import pickle
            pickle.dump(self, open(fname, 'wb'))

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

    try:
        import pickle
        data = pickle.load(open(fname, 'rb'))
    except:
        print("Error: Currently only pickled data is supported")

    if type(data) != type(catalogData(None, None)):
        print("Error: file {} does not contain catalog data".format(fname))
    else:
        return data