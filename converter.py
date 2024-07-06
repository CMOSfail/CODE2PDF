import os
import pdfkit
import pygments
from pygments import lexers, formatters
from datetime import datetime
import traceback
import json
import concurrent.futures
import threading
import subprocess
import sys
import urllib.request
import zipfile

lock = threading.Lock()

def install_wkhtmltopdf():
    url = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe"
    installer_path = os.path.join(os.getenv('TEMP'), "wkhtmltopdf-installer.exe")

    print("Downloading wkhtmltopdf...")
    urllib.request.urlretrieve(url, installer_path)

    print("Installing wkhtmltopdf...")
    subprocess.run([installer_path, "/silent", "/install"], check=True)

def check_wkhtmltopdf(config):
    wkhtmltopdf_path = config.get("pdfkit_path")
    if not wkhtmltopdf_path or not os.path.exists(wkhtmltopdf_path):
        print("wkhtmltopdf not found. Installing...")
        install_wkhtmltopdf()
        config["pdfkit_path"] = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

def convert_to_pdf(file_path, output_dir, log_file, config):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        lexer = lexers.get_lexer_for_filename(file_path)
        formatter = formatters.HtmlFormatter(full=True, linenos=True, cssclass="code", style='colorful')
        highlighted_code = pygments.highlight(file_content, lexer, formatter)

        # Create HTML content with header and footer
        file_name = os.path.basename(file_path)
        class_name = os.path.splitext(file_name)[0]
        file_type = file_path.split('.')[-1].upper()
        explanation = config["file_types"].get(file_type.lower(), "Code File")

        header = f"<div style='background:gray; color:white; padding:5px;'>{file_name} | {class_name} | {file_type} [{explanation}]</div>"
        footer = f"<div style='background:gray; color:white; padding:5px; text-align:center;'>CODE2PDF by Itamar Itzhaki | All Rights Reserved</div>"

        html_content = f"""
        <html>
        <head>
            <style>{formatter.get_style_defs('.code')}</style>
        </head>
        <body>
            {header}
            {highlighted_code}
            {footer}
        </body>
        </html>
        """

        # Save as PDF
        pdf_file_name = os.path.splitext(file_name)[0] + '.pdf'
        pdf_output_path = os.path.join(output_dir, pdf_file_name)
        
        config_path = config["pdfkit_path"]
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=config_path)
        pdfkit.from_string(html_content, pdf_output_path, configuration=pdfkit_config)

    except Exception as e:
        with lock:
            with open(log_file, 'a') as log:
                log.write(f"Error processing file {file_path}: {str(e)}\n")
                log.write(traceback.format_exc() + "\n")

def format_path(path):
    return os.path.normpath(path.strip('"').strip("'"))

def main():
    project_dir = input("Enter the project directory: ")
    output_dir = input("Enter the output directory: ")
    global config_path
    config_path = input("Enter the path to the config file: ")

    project_dir = format_path(project_dir)
    output_dir = format_path(output_dir)
    config_path = format_path(config_path)

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    check_wkhtmltopdf(config)

    timestamp = str(int(datetime.now().timestamp() * 1000))
    output_dir = os.path.join(output_dir, timestamp)
    log_file = os.path.join(output_dir, 'logs', f'{timestamp}.log')

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, 'w') as log:
        log.write(f"Starting conversion at {datetime.now()}\n")

    file_types = tuple(config["file_types"].keys())
    files_to_convert = []

    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(file_types):
                file_path = os.path.join(root, file)
                files_to_convert.append((file_path, output_dir, log_file, config))
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda p: convert_to_pdf(*p), files_to_convert)

    with open(log_file, 'a') as log:
        log.write(f"Finished conversion at {datetime.now()}\n")

if __name__ == "__main__":
    main()
