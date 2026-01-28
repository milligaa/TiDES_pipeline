from astropy.table import Table
from astropy.io import ascii
import argparse

def DASH(spectrum, redshift, filesave_path, dash_class=None):

    print(f'Beginning DASH classification for {spectrum}')

    class_dict = {'Ia':['Ia-norm', 'Ia-91T', 'Ia-91bg'],
                      'Ibc':['Ib-norm', 'Ib-pec', 'Ic-norm', 'Ic-broad', 'IIb', 'Ib', 'Ic', 'Ibn', 'Ic-pec'],
                      'II':['IIP', 'II-pec', 'IIL', 'IIn', 'II'],
                      'SL':[],
                      'Non':[],
                      'other':['Ia-pec', 'Ia-02cx', 'Ia-csm']}
    begin=spectrum.rfind('/')
    spec_name = []
    spec_name.append(spectrum[begin+1:])

    spec_fit = []
    spec_fit.append(spectrum)
    z_fit = []
    z_fit.append(float(redshift))

    best_class = []
    best_prob = []
    Ia_prob = []
    Ibc_prob = []
    II_prob = []
    SL_prob = []
    Non_prob = []
    Other_prob = []

    # Classify all spectra
    #classification = astrodash.Classify(spec_fit, z_fit, classifyHost=False, knownZ=True, smooth=6, rlapScores = True)
    #bestFits, Redshifts, bestTypes, rlapFlag, matchesFlag, redshiftErrs = classification.list_best_matches(n=100)

    dash_table = Table.read(dash_class, format='ascii')

    for i in dash_table['bestFits']:
        prob_dict = {'Ia':0, 'Ibc':0, 'II':0, 'SL':0, 'Non':0, 'other':0}
        for j in i:
            sn_class = j[1]
            sn_prob = j[3]
            for key, _ in class_dict.items():
                if sn_class in class_dict[key]:
                    prob_dict[key]+=float(sn_prob)
                else:
                    continue

        best_class.append(max(prob_dict, key=prob_dict.get))
        best_prob.append(max(prob_dict.values()) / sum(prob_dict.values()))
        Ia_prob.append(prob_dict['Ia'] / sum(prob_dict.values()))
        Ibc_prob.append(prob_dict['Ibc'] / sum(prob_dict.values()))
        II_prob.append(prob_dict['II'] / sum(prob_dict.values()))
        SL_prob.append(prob_dict['SL'] / sum(prob_dict.values()))
        Non_prob.append(prob_dict['Non'] / sum(prob_dict.values()))
        Other_prob.append(prob_dict['other'] / sum(prob_dict.values()))

    comb_table = Table()
    comb_table['spectrum'] = spec_name
    comb_table['pred_z'] = dash_table['Redshifts']
    comb_table['Best_class'] = best_class
    comb_table['Best_prob'] = best_prob
    comb_table['Ia_prob'] = Ia_prob
    comb_table['Ibc_prob'] = Ibc_prob
    comb_table['II_prob'] = II_prob
    comb_table['SL_prob'] = SL_prob
    comb_table['Non_prob'] = Non_prob
    comb_table['Other_prob'] = Other_prob
    comb_table['Classifier'] = ['DASH']

    #ascii.write(comb_table, 'config/DASH_interim.csv', overwrite = True, format = 'csv')

    print('Dash classification complete, probably')
    return comb_table

def parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-s",
        "--spectrum",
        default=None,
        help="path to spectrum to classify",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="path to save file of results",
    )

    parser.add_argument(
        "-r",
        "--redshift",
        default=None,
        help="redshift for classification",
    )

    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    DASH(args.spectrum, args.redshift, args.output)
