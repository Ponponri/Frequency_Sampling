from Sampling_frequency import Sampling_frequency
import argparse

def main(args):
    # Initialize
    fs = Sampling_frequency(args.k)
    # Compute
    fs.compute()
    # Show results
    fs.show()

if __name__ == '__main__':
    # Get the parameter k
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', default = 10, type = int)
    args = parser.parse_args()

    main(args)
