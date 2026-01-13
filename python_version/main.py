import argparse
import hashlib, json
from os import scandir
import os

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
                if not results:
                    results[entry.name]= "File could not be processed"
                
            elif entry.is_dir():
                results.update(hash_directory(entry.path, algorithm))#recursiion fur subdirectories
        return results
    except PermissionError:
        print(f"Permission denied: {path}")
        return results
    
def simple_printer(results):#function to print the results in a simple format
    for filename, filehash in results.items():
        print(f"{filename}: {filehash}")

def print_json(results, output_file):#function to print the results in JSON format
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON file: {e}")

def general_printer(args, results):#function to choose the output format
    if args.output == 'json':
        print_json(results, args.output_file)
    elif args.output == 'simple':
        simple_printer(results)

if __name__ == "__main__": #entry point to verify that the script is being run directly
        parser = argparse.ArgumentParser(description="Compute the hash of a file.")
        parser.add_argument("file", type=str, help="Path to the file to hash")
        parser.add_argument("-a", type=str, default="sha256", help="Algorithm to use")
        parser.add_argument("--output", choices=["json", "simple"], default="simple", help="Output in JSON format")
        parser.add_argument("--output_file", type=str, default="hashes.json", help="Output file for JSON format")
        
        args = parser.parse_args()
        
        if os.path.isdir(args.file):
            results = hash_directory(args.file, args.a)
            if not results:
                print("no files processed")
                
        elif os.path.isfile(args.file):
            file_hash = compute_hash(args.file, args.a)
            results = {os.path.basename(args.file): file_hash}
        
        general_printer(args, results)






    