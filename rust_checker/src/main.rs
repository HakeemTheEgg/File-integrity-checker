use std::fmt::Error;
use std:io;

//declaration
fn compute_file_hash(file_path: &str) -> Error<String, std::fmt::Error>{
    
}
fn main() {
    let a = println!("Hello, world!");
    compute_file_hash();
}


//definitions
fn compute_file_hash(file_path: &str) -> Error<String, f64>{//function to compute file hash

    let mut file = std::fs::File::open(file_path)
        .map_err(|e| format!("Failed to open file: {}", e))?;//opens file or returns error

}
// i have nothing to add but i want to test git changes
