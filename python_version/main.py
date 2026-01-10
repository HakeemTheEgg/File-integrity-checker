import argparse

def compute_hash(file_path, algorithm="sha256"):
    f = open(file_path, "rb")
    #implement the algorithm using haslib here

parser = argparse.ArgumentParser(description="Compute the hash of a file.")
parser.add_argument("file", type=str, help="Path to the file to hash")
parser.add_argument("-a", type=str, help="Algortithm to use")

args = parser.parse_args()


