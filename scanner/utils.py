# scanner/utils.py

from urllib.parse import urljoin
import nmap, requests

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


class CVESearch(object):
    def __init__(self, base_url="https://cvepremium.circl.lu", proxies=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.headers.update(
            {
                "content-type": "application/json",
                "User-Agent": "PyCVESearch - python wrapper",
            }
        )

    def _http_get(self, api_call, query=None):
        if query is None:
            response = self.session.get(
                urljoin(self.base_url, "api/{}".format(api_call))
            )
        else:
            response = self.session.get(
                urljoin(self.base_url, "api/{}/{}".format(api_call, query))
            )
        return response


def get_cve_description(cve_id):
    # Strip leading and trailing whitespaces from the CVE ID
    cve_id = cve_id.strip()

    # Initialize CVESearch class
    cve_search = CVESearch()

    try:
        # Make a request to the CIRCL CVE Premium API
        response = cve_search._http_get("cve", cve_id)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract relevant information from the JSON response
            cve_info = response.json()
            return {
                'summary': cve_info.get("summary", "Description not available."),
                'cvss': cve_info.get('cvss', 'N/A'),
                'cvss3': cve_info.get('cvss3', 'N/A'),
                'Published': cve_info.get('Published', 'N/A'),
            }

    except requests.RequestException as e:
        print(f"Error fetching CVE description: {e}")

    # Return a placeholder dictionary if the request fails
    return {
        'summary': f"Description for CVE {cve_id} is not available.",
        'cvss': 'N/A',
        'cvss3': 'N/A',
        'Published': 'N/A',
    }
