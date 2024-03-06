# scanner/utils.py

import nmap

def live_host_scan(ip):
    nm = nmap.PortScanner()
    
    # Set the scan speed to -T5
    nm.scan(hosts=ip, arguments='-p- -T3')

    scan_results = []
    for host in nm.all_hosts():
        result = {
            'ip': host,
            'status': nm[host]['status']['state'],
            'open_ports': [],
        }

        # Check if 'tcp' key is present in the dictionary
        if 'tcp' in nm[host]:
            result['open_ports'] = list(nm[host]['tcp'].keys())

        scan_results.append(result)

    return scan_results
