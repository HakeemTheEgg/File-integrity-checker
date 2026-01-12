import argparse
import hashlib, json
from os import scandir

def compute_hash(file_path, algorithm="sha256"):
    hash_obj = hashlib.new(algorithm)
    supported_algorithms = hashlib.algorithms_available
    if algorithm not in supported_algorithms:# checks if the specified algorithm is supported
         print(f"unsupported algorithm. select from: {', '.join(supported_algorithms)}")
    try:
        with open(file_path, "rb") as f: #pens the file in binary mode and reads it in chunks
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
def hash_directory(path, algorithm="sha256",skip_hidden=True):#function to hash files in a directory
    results = {}
    try:
        for entry in scandir(path):
            if skip_hidden and entry.name.startswith('.'):
                continue
            if entry.is_file():
                results[entry.name]= compute_hash(entry.path, algorithm)
            elif entry.is_dir():
                results.update(hash_directory(entry.path, algorithm))#recursiion fur subdirectories
        return results
    except PermissionError:
        print(f"Permission denied: {path}")
        return results
    


if __name__ == "__main__": #entry point to verify that the script is being run directly
        parser = argparse.ArgumentParser(description="Compute the hash of a file.")
        parser.add_argument("file", type=str, help="Path to the file to hash")
        parser.add_argument("-a", type=str, default="sha256", help="Algorithm to use")
        parser.add_argument()
        
        args = parser.parse_args()
        result = compute_hash(args.file, args.a if args.a else "sha256")#calls the compute_hash function, generates and stores the hash
        if result:
            print(f"The hash for {args.file.upper()} is: {result}")





    


def print_json(results):#function to print the results in JSON format
    