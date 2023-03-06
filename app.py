sys.path.append("/app_repository/app.py")

# Import modules
import sys, subprocess, os, shutil, requests, datetime, random, string
from flask import Flask, request, render_template, make_response, send_file
from werkzeug.utils import secure_filename
from Bio import SeqIO
from io import StringIO

app = Flask(__name__)
app.config["APPLICATION_ROOT"] = "/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

# Index page
@app.route("/")
def index():
    return render_template("clustal.html")

@app.route("/run_clustalo", methods=["GET","POST"])
def run_clustalo():
    print(request.form) # for error testing
    if request.method == "POST":
        input_data, input_type = get_input_data(request)
        output_format = request.form.get("output_format")

        if output_format not in ['fasta', 'clu']:
            return "Invalid output format specified", 400

        if input_data is None:
            return "No input data found", 400
        elif input_type == "error":
            return input_data, 500

        input_file_path = write_input_to_file(input_data)
        cmd = build_command(input_file_path, output_format)

        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            return f"Error executing clustalo: {e.stderr}", 500

        output = read_output_file()
        download_link = f'<a href="/download">Download results</a>'
        return f"{download_link}<br><br>{output}", 200

# To download output file
@app.route("/download")
def download_output_file():
    try:
        files = os.listdir(".")
        output_files = [f for f in files if f.startswith("output_")]
        if len(output_files) == 0:
            return "Output file not found", 500
        latest_output_file = max(output_files)
        with open(latest_output_file, "rb") as f:
            data = f.read()
            response = make_response(data)
            response.headers.set("Content-Disposition", "attachment", filename=latest_output_file)
            response.headers.set("Content-Type", "text/plain")
            return response
    except FileNotFoundError as e:
        return f"Error reading output file: {e}", 500

# Get the input data from the form
def get_input_data(request):
    fasta_sequences = request.form.get("fasta_sequences")
    uniprot_ids = request.form.get("uniprotIds")
    
    if fasta_sequences is not None and fasta_sequences.strip():
        print("Reading input data from fasta_sequences")
        print(f"Input data from fasta_sequences: {fasta_sequences}")
        return fasta_sequences, "fasta"
    elif uniprot_ids is not None and uniprot_ids.strip():
        uniprot_ids = uniprot_ids.split(",")
        fasta_sequences = ""
        for uniprot_id in uniprot_ids:
            url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
            print(f"Requesting sequence data for Uniprot ID {uniprot_id} from {url}")
            response = requests.get(url)
            if response.ok:
                print(f"Received response from {url}")
                print(f"Response content: {response.content}")
                fasta_sequences += response.text
            else:
                error_msg = f"Error retrieving Uniprot sequence for ID {uniprot_id}"
                print(error_msg)
                return error_msg, "error"
        print(f"Input data from Uniprot IDs: {fasta_sequences}")
        return fasta_sequences, "fasta"
    elif "file_upload" in request.files:
        file = request.files["file_upload"]
        filename = secure_filename(file.filename)
        if filename.split(".")[-1] in ["txt", "fasta"]:
            file.save(filename)
            with open(filename, "r") as f:
                input_data = f.read()
            os.remove(filename)
            print(f"Input data from file upload: {input_data}")
            return input_data, "file_upload"
        else:
            return "Invalid file format", "error"
    else:
        return None, None

# Create an input file with the input
def write_input_to_file(input_data):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    file_name = f"input_{now}_{random_string}.txt"
    with open(file_name, "w") as f:
        f.write(input_data)
    return file_name

# Create a output file with the output
def build_command(input_file_path, output_format):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    output_file_name = f"output_{now}_{random_string}.txt"
    return f"clustalo -i {input_file_path} -o {output_file_name} --outfmt={output_format} --force"

# Display output
def read_output_file():
    try:
        files = os.listdir(".")
        output_files = [f for f in files if f.startswith("output_")]
        if len(output_files) == 0:
            return "Output file not found", 500
        latest_output_file = max(output_files)
        with open(latest_output_file, "r") as f:
            # read the file contents and replace newlines with "<br>"
            output = f.read().replace('\n', '<br>')

        # add a "white-space: pre;" style to the <p> tag to preserve white spaces
        return render_template("results.html", output=output, style="white-space: pre;")

    except FileNotFoundError as e:
        return f"Error reading output file: {e}", 500



if __name__ == "__main__":
    app.run(debug=True)
