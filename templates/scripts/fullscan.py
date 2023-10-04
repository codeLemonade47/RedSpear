import subprocess

from .checksum import check
from .ctpdf import convert_to_pdf

def fullscan_script(ip, user_name, function_name):

    command = ["nmap", "-PS", f"{ip}"]

    p = subprocess.run(command, capture_output=True, encoding="utf-8")
    output = p.stdout.split("\n")[1:]

    if check():
        ip = str(ip).split(",")[0]
        convert_to_pdf(output, user_name, function_name)

    else:
        exit(1)