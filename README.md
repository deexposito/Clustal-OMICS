# Clustal-OMICS
This repository contains a developed web-application for doing Clustal-Omega multiple sequences alignment using Python and Flask. <p>
The html page consists of a description and user-manual to work with the application, a form to introduce the input either as a pasted multi fasta sequence, using Uniprot IDs or uploading a file. <p>
When submitting the input, the user gets redirected to a results.html page that displays the result of the multiple sequence alignment and provides a link to download it as a file.

## Installation
1) Clone the repository:<p>
```
git clone https://github.com/dexposito98/Clustal_Omega_WebApplication
```

2) Install the required packages: <p>
```
pip install -r requirements.txt
```

3) Go to the app folder and start the application
```
python app.py
```

## Usage
1) Open a web browser and navigate to http://localhost:5000/.
2) Read the instructions and enter the input you want to align in the correct format.
3) Select the output format.
4) Click the "Run Clustal-OMICS" button to perform the alignment.
5) Wait for the alignment to finish.
6) Visualize and download the aligned sequences.

## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request. You can also submit bug reports or feature requests by opening an issue.

## Credits
This project was created by Denis Expósito.
