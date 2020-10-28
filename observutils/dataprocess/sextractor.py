from astropy.io import ascii
import os

def sext2reg(infile, outfile, outformat="radec", dolabel=False, color='green', overwrite=False):
    """
    Converts cat file created by sextractor to a region file
    that can be loaded by ds9
    Inputs:
    infile (required): path to the input cat file
    outfile (required): path to save the output file
    outformat (optional): "radec" or "pix" (for pixel positons), defaults to radec
    dolabel (optional): whether or not to label the objects, defaults to False
    color (optional): Color for markings in ds9, default green
    overwrite (optional): Whether to allow code to overwrite the output file if it already
        exists. Defaults to False
    
    """
    
    try:
        data = ascii.read(infile)
    except:
        print("Error: Could not read input file")
        return
    
    if os.path.exists(outfile) and not overwrite:
        print("Error: Specificed output file already exists")
        return
    
    with open(outfile, 'w') as output:
        output.write('global color={}\n'.format(color))
        if outformat=="radec":
            template = "j2000;ellipse({},{},{},{},{})\n"
            keys = ['ALPHA_J2000', 'DELTA_J2000']
        elif outformat=="pix":
            template = "image;ellipse({},{},{},{},{})\n"
            keys = ['X_IMAGE', 'Y_IMAGE']
        else:
            print("Error: Invalid output format specified")
            print("Supported output types are \"radec\" and \"pix\" ")
            return
        
        col_names = data.colnames
        for key in keys:
            if key not in col_names:
                print("Error, input format {} specifed but"\
                      " data does not contain necessary information".format(outformat))
                return
        
        keys_common = ['A_WORLD', 'B_WORLD', 'THETA_J2000']
        for line in data:
            rfac = line['KRON_RADIUS'] / 3600 / 20
            common_factors = [rfac*360*60, rfac*360*60, 1]
            vals_un = [line[key] for key in keys]
            vals_common = [line[key] * common_factors[index] for index,key in enumerate(keys_common)]
            vals_un.extend(vals_common)
            output.write(template.format(*vals_un))
                