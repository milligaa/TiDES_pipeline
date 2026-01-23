import argparse
import glob
import json

def create_jsons(path, redshift):
    print('running create_many.py')

    spectrum = glob.glob((path+'spectra/*'))

    #load parameters file data
    with open(path+'config/parameters.json', 'r') as file:
        data = json.load(file)
        data["object_to_fit"] = spectrum[0]
        data["use_exact_z"] = 1
        data["z_exact"] = float(redshift)
        data['saving_results_path'] = path
        data["error_spectrum"] = 'sg'
        data["lower_lam"] = 4000
        data["upper_lam"] = 8500
        data["show_plot"] = 0

    new_json_str = str(path+'config/parameters.json')

    with open(new_json_str, 'w') as f:
        json.dump(data, f, indent=4)

    print('create_NGSF_json.py complete')

def parser():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-p",
        "--path",
        default=None,
        help="path to files to classify",
    )

    parser.add_argument(
        "-r",
        "--redshift",
        default=None,
        help="redshift to use",
    )

    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    create_jsons(args.path, args.redshift)
