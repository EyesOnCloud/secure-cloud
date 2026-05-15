"""
Report Generator Module
Uses PyYAML for config parsing and lxml for XML report output.
Both packages have known CVEs in the versions pinned in requirements.txt.
"""

import yaml
import lxml.etree as ET
from datetime import datetime


def generate_report(report_type: str, period: str, config: dict) -> dict:
    """
    Generate a financial report.

    Uses PyYAML to parse report configuration.
    CVE NOTE: PyYAML 5.3.1 is vulnerable to CVE-2022-1471 —
    yaml.load() without Loader allows arbitrary Python object instantiation.
    This code uses yaml.safe_load() as a partial mitigation, but the
    package version itself is still flagged by scanners.
    """

    # Default report configuration
    default_config_yaml = """
    format: json
    include_charts: false
    decimal_places: 2
    currency: USD
    """

    # Parse configuration — safe_load used here but package version still vulnerable
    try:
        report_config = yaml.safe_load(default_config_yaml)
        if config:
            user_config = yaml.safe_load(str(config))
            if isinstance(user_config, dict):
                report_config.update(user_config)
    except yaml.YAMLError as e:
        report_config = {"format": "json"}

    # Sample financial data
    data = {
        "Q1-2024": {"revenue": 4250000, "expenses": 3100000, "profit": 1150000},
        "Q2-2024": {"revenue": 4800000, "expenses": 3400000, "profit": 1400000},
        "Q3-2024": {"revenue": 5100000, "expenses": 3600000, "profit": 1500000},
        "Q4-2024": {"revenue": 5500000, "expenses": 3900000, "profit": 1600000},
    }

    period_data = data.get(period, data["Q1-2024"])

    if report_type == "xml":
        # Generate XML report using lxml
        # CVE NOTE: lxml 4.6.3 is vulnerable to CVE-2022-2309 (null bytes in paths)
        root = ET.Element("FinancialReport")
        ET.SubElement(root, "Period").text = period
        ET.SubElement(root, "GeneratedAt").text = datetime.utcnow().isoformat()
        for key, value in period_data.items():
            elem = ET.SubElement(root, key.capitalize())
            elem.text = str(value)
        xml_string = ET.tostring(root, pretty_print=True).decode()
        return {"format": "xml", "report": xml_string, "period": period}

    return {
        "format": "json",
        "period": period,
        "report_type": report_type,
        "generated_at": datetime.utcnow().isoformat(),
        "data": period_data,
        "currency": report_config.get("currency", "USD")
    }
