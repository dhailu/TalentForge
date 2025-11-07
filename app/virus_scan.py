import os
import clamd
from dotenv import load_dotenv
load_dotenv()

CLAMD_HOST = os.getenv("CLAMD_HOST", "clamav")
CLAMD_PORT = int(os.getenv("CLAMD_PORT", "3310"))

def scan_file(file_path):
    """Return (is_clean:bool, result:str)"""
    try:
        cd = clamd.ClamdNetworkSocket(host=CLAMD_HOST, port=CLAMD_PORT)
        res = cd.scan(file_path)
        # res is dict: {filename: ('OK' or 'FOUND', ...)}
        if not res:
            return True, "no-result"
        for k, v in res.items():
            status = v[0]
            if status == "OK":
                return True, "OK"
            else:
                return False, status
    except Exception as e:
        # If clamav unavailable, fail-safe: return False to force human review
        return False, f"clamd-error:{e}"
