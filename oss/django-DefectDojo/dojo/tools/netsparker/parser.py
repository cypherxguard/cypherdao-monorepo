import datetime
import json

import html2text
from cvss import parser as cvss_parser
from dateutil import parser as date_parser

from dojo.models import Endpoint, Finding


class NetsparkerParser:
    def get_scan_types(self):
        return ["Netsparker Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Netsparker Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Netsparker JSON format."

    def get_findings(self, filename, test):
        tree = filename.read()
        try:
            data = json.loads(str(tree, "utf-8-sig"))
        except Exception:
            data = json.loads(tree)
        dupes = {}
        try:
            if "UTC" in data["Generated"]:
                scan_date = datetime.datetime.strptime(
                    data["Generated"].split(" ")[0], "%d/%m/%Y",
                ).date()
            else:
                scan_date = datetime.datetime.strptime(
                    data["Generated"], "%d/%m/%Y %H:%M %p",
                ).date()
        except ValueError:
            try:
                scan_date = date_parser.parse(data["Generated"])
            except date_parser.ParserError:
                scan_date = None

        for item in data["Vulnerabilities"]:
            title = item["Name"]
            findingdetail = html2text.html2text(item.get("Description", ""))
            if "Cwe" in item["Classification"]:
                try:
                    cwe = int(item["Classification"]["Cwe"].split(",")[0])
                except Exception:
                    cwe = None
            else:
                cwe = None
            sev = item["Severity"]
            if sev not in {"Info", "Low", "Medium", "High", "Critical"}:
                sev = "Info"
            mitigation = html2text.html2text(item.get("RemedialProcedure", ""))
            references = html2text.html2text(item.get("RemedyReferences", ""))
            url = item["Url"]
            impact = html2text.html2text(item.get("Impact", ""))
            dupe_key = title
            request = item["HttpRequest"].get("Content", None)
            response = item["HttpResponse"].get("Content", None)

            finding = Finding(
                title=title,
                test=test,
                description=findingdetail,
                severity=sev.title(),
                mitigation=mitigation,
                impact=impact,
                date=scan_date,
                references=references,
                cwe=cwe,
                static_finding=True,
            )
            state = item.get("State", None)
            if state == "FalsePositive":
                finding.active = False
                finding.verified = False
                finding.false_p = True
                finding.mitigated = None
                finding.is_mitigated = False
            elif state == "AcceptedRisk":
                finding.risk_accepted = True

            if item["Classification"] is not None:
                if item["Classification"].get("Cvss") is not None and item["Classification"].get("Cvss").get("Vector") is not None:
                    cvss_objects = cvss_parser.parse_cvss_from_text(
                        item["Classification"]["Cvss"]["Vector"],
                    )
                    if len(cvss_objects) > 0:
                        finding.cvssv3 = cvss_objects[0].clean_vector()
                elif item["Classification"].get("Cvss31") is not None and item["Classification"].get("Cvss31").get("Vector") is not None:
                    cvss_objects = cvss_parser.parse_cvss_from_text(
                        item["Classification"]["Cvss31"]["Vector"],
                    )
                    if len(cvss_objects) > 0:
                        finding.cvssv3 = cvss_objects[0].clean_vector()
            finding.unsaved_req_resp = [{"req": str(request), "resp": str(response)}]
            finding.unsaved_endpoints = [Endpoint.from_uri(url)]

            if dupe_key in dupes:
                find = dupes[dupe_key]
                find.unsaved_req_resp.extend(finding.unsaved_req_resp)
                find.unsaved_endpoints.extend(finding.unsaved_endpoints)
            else:
                dupes[dupe_key] = finding

        return list(dupes.values())
