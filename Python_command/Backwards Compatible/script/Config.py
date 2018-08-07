import argparse
import BC_ParseYW as Linear
import BC_SPParseYW as SP


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-L','--Linear',help="Generate Linear YW model",action="store_true")
    parser.add_argument('-SP','--SerialParallel',help="Generate Serial-Parallel YW model",action="store_true")
    args=parser.parse_args()
    if args.Linear:
        Linear.main()
    elif args.SerialParallel:
        SP.main()


if __name__=='__main__':
    main()
