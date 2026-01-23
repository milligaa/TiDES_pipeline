#open the various results files from a SNID run and save the relevant information from them
import argparse


def concatenate(pto, pts, sp):
    import glob
    import numpy as np
    from astropy.table import Table
    from astropy.io import ascii
    import math

    #need to get the spectra that were used to create the results, so any where the fit failed and didn't produce any output are known
    spectra = []
    spectra.append(pts)
    spectra_names = []
    for a in range(len(spectra)):
        begin = spectra[a].rfind('/')
        end = spectra[a].find('.txt')
        spectra_names.append(spectra[a][begin+1:end])

    output_files = glob.glob(pto+'*.output')
    output_names = []
    for b in range(len(output_files)):
        begin = output_files[b].find(pto) + len(pto)
        end = output_files[b].find('_snid')
        output_names.append(output_files[b][begin:end])

    #now perform the extraction, for each spectrum name check that an equivalent output exists and extract info
    #if it doesn't append a null value into every column

    best_class = []
    best_prob = []
    Ia_prob = []
    Ibc_prob = []
    II_prob = []
    SL_prob = []
    Non_prob = []
    Other_prob = []

    class_dict = {'Ia':['Ia','Ia-norm' ,'Ia-91T'  ,'Ia-91bg', 'Ia-99aa'],
                      'Ibc':['Ib', 'Ib-pec', 'Ib-norm','Ic', 'Ic-norm', 'Ic-pec',
                      'Ic-broad', 'IIb', 'Ib/c', 'SN Ibn', 'SN Icn', 'SN Ic-BL', 'Ibn'],
                      'II':['II', 'IIL', 'IIP', 'II-pec', 'IIn'],
                      'SL':['SLSN-II', 'SLSN-IIn', 'SLSN-I', 'SLSN-Ib', 'SLSN-IIb'],
                      'Non':['TDE', 'Ca-rich', 'ILRT'],
                      'other':['Gal', 'None', 'Other', 'other', 'NotSN', 'AGN', 'LBV', 'M-star', 'QSO',
                      'C-star', 'LRN', 'Ia-csm'  ,'Ia-pec' ,'Ia-02cx']}


    #need to define this somehow so it works
    file_line_search_str = 'placeholder'
    filename = str(pto) + str(output_names[0]) + '_snid.output'
    with open(filename) as f:
        file = f.readlines()

    for i in range(100):
        if 'sn type lap rlap z zerr' in file[i]:
            index_begin = i
        elif 'Forced initial redshift' in file[i]:
            line = file[i].split()
            redshift=line[-1]
        else:
            continue

    file_line_search_str = file[index_begin]
    for c in range(len(spectra_names)):

        try:
            index = output_names.index(spectra_names[c])
            #open the file by construncting the filename from the output name
            filename = str(pto) + str(output_names[index]) + '_snid.output'
            
            with open(filename) as f:
                file = f.readlines()

            prob_dict = {'Ia':0, 'Ibc':0, 'II':0, 'SL':0, 'Non':0, 'other':0}
            
            #file is open, search for line at start of results and get index, first three results are the three subsequent indexes
            res_begin_index = file.index(file_line_search_str)
            
            for i in range(len(file) - (res_begin_index+1)):
                    result = file[res_begin_index + 1 + i].split()
                    if len(result) == 10:
                        sn_class = result[2]
                        lap = result[3]
                        rlap = result[4]
                        r = float(rlap) / float(lap)
                        prob = math.erf(r)
                        for key, _ in class_dict.items():
                            if sn_class in class_dict[key]:
                                prob_dict[key]+=float(prob)
                            else:
                                continue
                    else:
                        break
                
            best_class.append(max(prob_dict, key=prob_dict.get))
            best_prob.append(max(prob_dict.values()) / sum(prob_dict.values()))
            Ia_prob.append(prob_dict['Ia'] / sum(prob_dict.values()))
            Ibc_prob.append(prob_dict['Ibc'] / sum(prob_dict.values()))
            II_prob.append(prob_dict['II'] / sum(prob_dict.values()))
            SL_prob.append(prob_dict['SL'] / sum(prob_dict.values()))
            Non_prob.append(prob_dict['Non'] / sum(prob_dict.values()))
            Other_prob.append(prob_dict['other'] / sum(prob_dict.values()))
        
        
        except Exception as e:
            print(e)
            best_class.append('other')
            best_prob.append(1)
            Ia_prob.append(0)
            Ibc_prob.append(0)
            II_prob.append(0)
            SL_prob.append(0)
            Non_prob.append(0)
            Other_prob.append(0)
        

    #now save the results
    saving_table = Table()
    saving_table['spectrum'] = spectra_names
    saving_table['pred_z'] = redshift
    saving_table['Best_class'] = best_class
    saving_table['Best_prob'] = best_prob
    saving_table['Ia_prob'] = Ia_prob
    saving_table['Ibc_prob'] = Ibc_prob
    saving_table['II_prob'] = II_prob
    saving_table['SL_prob'] = SL_prob
    saving_table['Non_prob'] = Non_prob
    saving_table['Other_prob'] = Other_prob
    saving_table['Classifier'] = ['SNID']

    ascii.write(saving_table, sp, format='csv', delimiter = ',', overwrite=True)

def parser():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--outputs",
        default=None,
        help="path to outout files from classification",
    )

    parser.add_argument(
        "-s",
        "--save",
        default=None,
        help="path to save results",
    )

    parser.add_argument(
        "-p",
        "--spectra",
        default=None,
        help="path to spectra used",
    )
    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    # print(args)
    concatenate(args.outputs, args.spectra, args.save)