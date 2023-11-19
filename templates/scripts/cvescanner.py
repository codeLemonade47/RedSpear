'''from urllib.parse import urljoin
import requests

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
    
    def browse(self, param=None):
        data = self._http_get("browse", query=param)
        return data.json()
    
    def search(self, param):
        data = self._http_get("search, query=param")
        return data.json()
    
    def id(self, param):
        data = self._http_get("cve", query=param)
        return data.json()
    
    def last(self):
        data = self._http_get("last")
        return data.json()
    
    def dbinfo(self):
        data = self._http_get("dbInfo")
        return data.json()
    
    def cpe22(self, param):
        data = self._http_get("cpe2.2", query=param)
        return data
    
    def cpe23(self, param):
        data = self._http_get("cpe2.3", query=param)
        return data
    
    def cvefor(self, param):
        data = self._http_get("cvefor", query=param)
        return data.json()
    
    def cve_search(cve_id):
        cve = CVESearch()
        pre_result = cve.id(cve_id)
        if len(pre_result) > 2:
            result = {
                "cve_id": pre_result["id"],
                "cvss": pre_result["cvss"] if "cvss" in pre_result else "Unknown",
                "complexity": pre_result["access"]["complexity"]
                if "access" in pre_result
                else "Unknown",
                "summary": pre_result["summary"],
                "published": pre_result["Published"],
                "modified": pre_result["Modified"],
                "capec": [
                    pre_result["capec"][i]["name"] for i in range(len(pre_result["capec"]))
                ]
                if "capec" in pre_result
                else "Unknown",
            }
            return result
        else:
            return None'''