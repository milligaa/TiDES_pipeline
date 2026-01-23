from qmostetc import Spectrum
from astropy.table import Table, vstack
import astropy.units as u
from astropy.io import ascii
import argparse

def rband_mag(spectrum):

    spec=Table.read(spectrum, format = 'ascii.no_header', delimiter = ' ')
    lam = spec['col1'] 
    intens = spec['col2']

    wavelength = lam * u.nm / 10
    photon_flux = intens * u.erg / (u.cm ** 2 * u.s * u.angstrom)

    spec_obj = Spectrum(wavelength, photon_flux)
    spec_mag = spec_obj.get_mag(u.ABmag, 'LSST_LSST.r')

    print(spec_mag)

    if spec_mag <= 21.8*u.ABmag:
        return True
    else:
        return False

def pipeline(config_path, spec):

    dash_res = Table.read(config_path+'/DASH_interim.csv', format='csv', delimiter=',')
    ngsf_res = Table.read(config_path+'/NGSF_interim.csv', format='csv', delimiter=',')
    snid_res = Table.read(config_path+'/SNID_interim.csv', format='csv', delimiter=',')

    combined_results = vstack([dash_res,ngsf_res,snid_res])
    ascii.write(combined_results, 'results/'+str(snid_res['spectrum'][0])+'.csv', 
                format='csv', delimiter=',', overwrite=True)
    
    pipeline_class = 'Placeholder'
    if dash_res['Best_class'][0] in ['Ia', 'II']:
        if ngsf_res['Best_class'][0] == dash_res['Best_class'][0]:
            pipeline_class = ngsf_res['Best_class'][0]
        else:
            pass
    elif rband_mag(spec) == True:
        pipeline_class = ngsf_res['Best_class'][0]
    else:
        pipeline_class = 'Other'

    print('---------------------------------------------------------')
    print('!! Milligan+25 TiDES Automated Classification pipeline !!')
    print(f'Transient Classification is: {pipeline_class}')
    print('Might be worth checking though!!!')
    print('---------------------------------------------------------')

def parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--configpath",
        default=None,
        help="path to config folder with interim results",
    )

    parser.add_argument(
        "-s",
        "--specpath",
        default=None,
        help="path to spectrum, needed for mag check",
    )

    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    pipeline(args.configpath, args.specpath)