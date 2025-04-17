import os
import json
import requests
import logging
from typing import List, Dict, Any
from urllib.parse import urljoin

def get_cve_data(api_url: str, cve_id: str) -> Dict[str, Any]:
    """
    Fetch CVE data from the API.
    """
    try:
        response = requests.get(urljoin(api_url, cve_id))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching CVE data: {e}")
        return {}

def parse_cve_data(cve_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse CVE data to extract relevant information.
    """
    cve_list = []
    for item in cve_data.get("CVE_Items", []):
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        description = item["cve"]["description"]["description_data"][0]["value"]
        cvss_score = item["impact"].get("baseMetricV3", {}).get("cvssV3", {}).get("baseScore", 0)
        cve_list.append({
            "cve_id": cve_id,
            "description": description,
            "cvss_score": cvss_score
        })
    return cve_list

def save_cve_data(cve_list: List[Dict[str, Any]], output_file: str) -> None:
    """
    Save CVE data to a JSON file.
    """
    with open(output_file, 'w') as f:
        json.dump(cve_list, f, indent=4)
    logging.info(f"CVE data saved to {output_file}")

def load_cve_data(input_file: str) -> List[Dict[str, Any]]:
    """
    Load CVE data from a JSON file.
    """
    if not os.path.exists(input_file):
        logging.error(f"Input file {input_file} does not exist.")
        return []
    
    with open(input_file, 'r') as f:
        cve_list = json.load(f)
    logging.info(f"CVE data loaded from {input_file}")
    return cve_list

def filter_cve_data(cve_list: List[Dict[str, Any]], min_cvss_score: float) -> List[Dict[str, Any]]:
    """
    Filter CVE data based on CVSS score.
    """
    filtered_cve_list = [cve for cve in cve_list if cve["cvss_score"] >= min_cvss_score]
    logging.info(f"Filtered CVE data to {len(filtered_cve_list)} items with CVSS score >= {min_cvss_score}")
    return filtered_cve_list

def perform_cve_scan(api_url: str, cve_id: str, output_file: str, min_cvss_score: float) -> None:
    """
    Perform a CVE scan by fetching, parsing, filtering, and saving CVE data.
    """
    # Fetch CVE data from the API
    cve_data = get_cve_data(api_url, cve_id)
    
    # Parse the CVE data
    cve_list = parse_cve_data(cve_data)
    
    # Filter the CVE data based on CVSS score
    filtered_cve_list = filter_cve_data(cve_list, min_cvss_score)
    
    # Save the filtered CVE data to a JSON file
    save_cve_data(filtered_cve_list, output_file)
    
    return filtered_cve_list

if __name__ == "__main__":
    
    # Example usage
    logging.basicConfig(level=logging.INFO)
    API_URL = "https://services.nvd.nist.gov/rest/json/cve/2.0/"
    CVE_ID = "CVE-2023-12345"  # Example CVE ID
    OUTPUT_FILE = "cve_data.json"
    MIN_CVSS_SCORE = 7.0
    
    perform_cve_scan(API_URL, CVE_ID, OUTPUT_FILE, MIN_CVSS_SCORE)
    # Load and display the saved CVE data