# scanner/views.py

import requests, os
import concurrent.futures
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ScanForm
from .models import WebsiteScan
import threading, nmap, subprocess, os
from scapy.all import ARP, Ether, srp
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .utils import get_cve_description, live_host_scan
from urllib.parse import urljoin, urldefrag
from threading import Thread
from django.contrib.auth.decorators import login_required


def generate_pdf(scan_results):
    pdf_filename = 'scan_results.pdf'
    
    # Create a PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Set up styles for paragraphs
    styles = getSampleStyleSheet()
    body_style = styles["BodyText"]
    
    # Create a list to hold all the paragraphs
    content = []
    
    # Add a title to the PDF
    content.append(Paragraph("Live Host Scan Results", styles["Title"]))
    
    # Add content for each scan result
    for result in scan_results:
        ip_text = f"IP: {result['ip']}, Status: {result['status']}"
        
        # Check if open_ports is present in the result
        if 'open_ports' in result:
            open_ports_text = f"Open Ports: {', '.join(map(str, result['open_ports']))}"
            content.append(Paragraph(ip_text, body_style))
            content.append(Paragraph(open_ports_text, body_style))
        else:
            # If open_ports is not present, just add the IP and status
            content.append(Paragraph(ip_text, body_style))
        
        # Add a separator line between results
        content.append(Paragraph("<br/><hr/><br/>", body_style))
    
    # Build the PDF document with the content
    doc.build(content)
    
    return pdf_filename



def index(request):
    return render(request, 'index.html')



def scan(request):
    ip = request.POST['ip']

    # Perform the live host scan in a separate thread
    scan_results = live_host_scan(ip)

    print("Scan Results:", scan_results)


    # Store scan_results in the session
    request.session['scan_results'] = scan_results

    # Generate PDF using the scan results
    pdf_filename = generate_pdf(scan_results)

    return render(request, 'scan_in_progress.html', {'pdf_filename': pdf_filename})



def download(request):
    # Retrieve scan_results from the session
    scan_results = request.session.get('scan_results', [])

    # Generate PDF using the scan results
    pdf_filename = generate_pdf(scan_results)

    # Clear scan_results from the session (optional, depending on your requirements)
    request.session.pop('scan_results', None)

    # Return the PDF file as a response
    with open(pdf_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    return response



def cve_descriptor(request):
    if request.method == 'POST':
        cve_id = request.POST.get('cve_id')

        # Get CVE description
        cve_description = get_cve_description(cve_id)

        return render(request, 'cve_descriptor_results.html', {'cve_id': cve_id, 'cve_description': cve_description})

    return render(request, 'cve_descriptor_form.html')  # Display the form to input the CVE ID



def run_scan(ip_address):
    command = f'nmap -sT -sV -T5 -Pn --script vulners {ip_address}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()


def generate_pdf_report(scan_results_list):
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'pdf_reports')
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    pdf_filename = os.path.join(pdf_directory, 'scan_report.pdf')
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    style_heading = styles['Heading1']
    style_normal = styles['Normal']
    
    content = []
    content.append(Paragraph("Scan Report", style_heading))
    content.append(Spacer(1, 12))

    for result in scan_results_list:
        content.append(Paragraph(result, style_normal))
        content.append(Spacer(1, 6))

    doc.build(content)
    return pdf_filename


def scan_tool(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        scan_results, _ = run_scan(ip_address)
        pdf_filename = generate_pdf_report(scan_results.split('\n'))
        pdf_url = f"{settings.MEDIA_URL}pdf_reports/{os.path.basename(pdf_filename)}"
        return render(request, 'scan_tool.html', {'pdf_url': pdf_url})
    return render(request, 'scan_tool.html')



def download_pdf(request):
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'pdf_reports')
    pdf_file_path = os.path.join(pdf_directory, 'scan_report.pdf')
    
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="scan_report.pdf"'
            return response
    else:
        return HttpResponse("PDF file not found.", status=404)
    


# def scan_subdomains(request):
#     if request.method == 'POST':
#         domain_name = request.POST.get('domain_url', '')
#         if domain_name:
#             subdomains = enumerate_subdomains(domain_name)
#             return render(request, 'subdomain_results.html', {'subdomains': subdomains})
#     return render(request, 'scan_subdomains.html')

# def enumerate_subdomains(domain_name):
#     try:
#         # Run dnsrecon command to enumerate subdomains
#         command = f'dnsrecon -d {domain_name} -t std'
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         stdout, stderr = process.communicate()
#         subdomains = stdout.decode().splitlines()
#         return subdomains
#     except Exception as e:
#         return [str(e)]





# def scan_directory(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find all links in the page
#     links = [a.get('href') for a in soup.find_all('a')]

#     # Filter out None values and links that are not to directories
#     directories = [link for link in links if link and link.endswith('/')]

#     return directories


# def scan_directory(url):
#     # Make a GET request
#     try:
#         response = requests.get(url)
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return []

#     # Check if the request was successful
#     if response.status_code != 200:
#         print(f"Failed to access {url}")
#         return []

#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find all links in the page
#     links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

#     # Filter out links that are not to directories
#     directories = [urljoin(url, link) for link in links if link.endswith('/')]

#     return directories




def scan_directory(url, directory):
    dir_url = urljoin(url, directory.strip().rstrip('/')) + '/'

    # Make a GET request
    try:
        response = requests.get(dir_url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Successfully accessed {dir_url}")



def scan_directories(url, directories):
    threads = []
    for directory in directories:
        thread = Thread(target=scan_directory, args=(url, directory))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()



def scan_directory_fast(base_url):
    # Open the file
    with open('static/common.txt', 'r') as file:
        directories = file.read().splitlines()

    # Find all directories in the list
    found_directories = []

    # Use a ThreadPoolExecutor to make requests in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(requests.get, urljoin(base_url, directory.strip())): directory for directory in directories}
        for future in concurrent.futures.as_completed(future_to_url):
            directory = future_to_url[future]
            try:
                response = future.result()
            except Exception as exc:
                print(f'{base_url}/{directory} generated an exception: {exc}')
            else:
                if response.status_code == 200:
                    print(f"Successfully accessed {base_url}/{directory}")
                    found_directories.append(f"{base_url}/{directory}")

    return found_directories



def scan_form_view(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            # Call the scan_directory function and store the results
            directories = scan_directory_fast(website_url)
            results = '\n'.join(directories)
            # Create a new WebsiteScan object and save it
            scan_result = WebsiteScan(website_url=website_url, results=results)
            scan_result.save()
            # Redirect to the result page
            return redirect('scan_result', result_id=scan_result.id)
    else:
        form = ScanForm()
    return render(request, 'scanner_form.html', {'form': form})



def scan_result_view(request, result_id):
    result = get_object_or_404(WebsiteScan, pk=result_id)  # Change class name to WebsiteScan
    return render(request, 'scan_result.html', {'result': result})


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("signin")
    else:
        return redirect("signin")