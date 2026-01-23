import argparse


def get_z(snid_out):

    filename = snid_out
    with open(filename) as f:
        file = f.readlines()

    for i in range(100):
        if 'zuser' in file[i]:
            line = file[i].split()
            redshift=line[-1]
        else:
            continue

    return redshift

def parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-s",
        "--snidout",
        default=None,
        help="path to the SNID output file",
    )

    return parser

if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    print(get_z(args.snidout))

