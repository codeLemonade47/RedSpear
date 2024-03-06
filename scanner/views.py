# scanner/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import ScanResult
from django.http import JsonResponse
import threading
import nmap
from scapy.all import ARP, Ether, srp
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .utils import live_host_scan
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph


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
