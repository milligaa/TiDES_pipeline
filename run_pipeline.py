import requests
import os
import shutil
import logging
from pysnid.snid import SNIDReader
from source import M25_pipeline

logger = logging.getLogger(__name__)

SNID_URL=''
DASH_URL=''
NGSF_URL=''

def run_snid(spectrum:str):
    print(f"Running SNID on {spectrum}")

    payload = {"spectrum": spectrum}

    try:
        response = requests.post(
            SNID_URL,
            json=payload,
            timout=30
        )

        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

    return response.json()

def run_dash(spectrum:str, redshift:float):
    print(f"Running Dash on {spectrum}")

    payload = {"spectrum": spectrum, "redshift": redshift}

    try:
        response = requests.post(
                DASH_URL,
                json = payload,
                timeout=30
                )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

    return response.json()

def run_ngsf(spectrum:str, redshift:float):
    print(f"Running NGSF on {spectrum}")

    payload = {"spectrum": spectrum, "z": redshift}

    try:
        response = requests.post(
                NGSF_URL,
                json=payload,
                timeout=100
            )

        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

    return response.json()

def run_pipeline(spectrum:str):
    print(f"Running Pipeline on {spectrum}")

    snid_response = run_snid(spectrum)

    snidres = SNIDReader.from_filename(snid_response["data"]["file_path"])
    redshift = snidres.get_redshift(nfirst=1)

    dash_response = run_dash(spectrum, redshift)

    ngsf_response = run_ngsf(spectrum, redshift)

    paths = {
            "snid": snid_response["data"]["file_path"],
            "dash": dash_response["data"]["file_path"],
            "NGSF": ngsf_response["data"]["file_path"]
            }

    M25_pipeline.pipeline(paths, spectrum)
