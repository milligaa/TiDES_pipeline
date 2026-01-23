#this program takes the results from superfit and concatenates the best result from each into a single csv file

from astropy.io import ascii
from astropy.table import Table
import glob
from scipy import stats
import argparse
import numpy as np

def concatenate(csv_path, save_path):
    #load all the csv files
    csv_files = []
    csv_files.append(csv_path)
    print(csv_path)

    final_res_table = Table()
    spectrum = []
    pred_z = []
    best_class = []
    best_prob = []
    Ia_prob = []
    Ibc_prob = []
    II_prob = []
    SL_prob = []
    Non_prob = []
    Other_prob = []
    best_classes = []

    class_dict = {'Ia':['Ia 91T-like', 'Ia-norm', 'Ia 91bg-like', 'Ia 99aa-like'],
                      'Ibc':['Ibn', 'Ib', 'Ic', 'Ic-BL', 'Ic-pec','IIb', 'IIb-flash'],
                      'II':['II', 'II-flash', 'IIn'],
                      'SL':['SLSN-II', 'SLSN-IIn', 'SLSN-I', 'SLSN-Ib', 'SLSN-IIb'],
                      'Non':['TDE H', 'TDE He', 'TDE H+He', 'FBOT', 'ILRT'],
                      'other':['Ia 02es-like', 'Ia-02cx like', 'Ia-CSM-(ambigious)', 'Ia-pec',
                               'Ia-CSM', 'Ia-rapid', 'Ca-Ia', 'super_chandra',  'SN - Imposter', 'computed', 'Ca-Ib']}

    for i in range(len(csv_files)):
        table = Table.read(csv_files[i], format = 'csv', delimiter = ',')
        mask = (table['CHI2/dof'] != -np.inf)

        table = table[mask]
        spec = str(table['SPECTRUM'][0])
        spectrum.append(spec)
        pred_z.append(table['Z'][0])
        smag = int(spec.find('Smag'))
        gmag = int(spec.find('Gmag'))
        texp = int(spec.find('texp'))
        z = int(spec.find('z'))

        
        prob_dict = {'Ia':0, 'Ibc':0, 'II':0, 'SL':0, 'Non':0, 'other':0}

        max_chi = max(table['CHI2/dof'])
        min_chi = min(table['CHI2/dof'])
        best_c = str(table['SN'][0])
        str_no = best_c.find('/')
        best_c = best_c[:str_no]

        if len(table) <= 9:
            ran = len(table)
        else:
            ran = 9

        for j in range(ran):
            sn_class_full = table[j][2]
            slash = sn_class_full.find('/')
            sn_class = sn_class_full[:slash]
            try:
                sn_dof = int(table[j][11] / table[j][12])
                sn_chi = table[j][11]
                sn_prob =stats.chi2.cdf(sn_chi, 1)
                # sn_prob = ((max_chi - sn_chi) / (max_chi - min_chi)) ** 2
            except ValueError:
                sn_prob = 0

            for key, _ in class_dict.items():
                if sn_class in class_dict[key]:
                    prob_dict[key]+=float(sn_prob)
                else:
                    continue

            # print(prob_dict)
        
        Ia_prob.append(prob_dict['Ia']/ sum(prob_dict.values()))
        Ibc_prob.append(prob_dict['Ibc']/ sum(prob_dict.values()))
        II_prob.append(prob_dict['II']/ sum(prob_dict.values()))
        SL_prob.append(prob_dict['SL']/ sum(prob_dict.values()))
        Non_prob.append(prob_dict['Non']/ sum(prob_dict.values()))
        Other_prob.append(prob_dict['other']/ sum(prob_dict.values()))


        best_class.append(max(prob_dict, key=prob_dict.get))
        best_prob.append(max(prob_dict.values()) / sum(prob_dict.values()))
        best_classes.append(best_c)

        # print(best_class, best_prob)

    variables = [spectrum,pred_z,best_class,best_prob,
                 Ia_prob,Ibc_prob,II_prob,SL_prob,Non_prob,Other_prob, ['NGSF']]
    variable_strs = ['spectrum','pred_z','Best_class','Best_prob','Ia_prob',
                     'Ibc_prob','II_prob','SL_prob','Non_prob','Other_prob', 'Classifier']
    
    for i in range(len(variables)):
        final_res_table[variable_strs[i]] = variables[i]

    ascii.write(final_res_table, save_path, format='csv', overwrite=True)

    print('NGSF_output.py Complete!')


def parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--csvpath",
        default=None,
        help="path to csv files to concatenate",
    )

    parser.add_argument(
        "-s",
        "--savepath",
        default=None,
        help="path to save concatenated file of results",
    )

    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    concatenate(args.csvpath, args.savepath)
