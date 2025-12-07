'''
Google Gemini Prompt: Here are the results of
`strings offline_processing/traffic.pcapng | head -n 100` and 
`tshark -r offline_processing/traffic.pcapng -T fields -e frame.comment | head -n 20`. 

Please write a Python script that uses TShark to extract the source IP addresses 
and the embedded labels from the pcapng file located at `offline_processing/traffic.pcapng`.
The script should save the extracted data into a CSV file named `labels_extracted.csv` with 
two columns: `tshark_ip` for the source IP addresses and `raw_label` for the embedded labels.
'''




import subprocess
import pandas as pd
import os

# Path to your found file
pcap_file = "offline_processing/traffic.pcapng"

print(f"🚀 Running TShark on {pcap_file}...")
print("   Extracting: Source IP and Packet Comments (Labels)...")

# TShark Command:
# -n: No name resolution (prevents DNS crash/loops)
# -Y "ip": Only IPv4 packets (matches your nprint -4 flag)
# -T fields: Output specific fields
# -e ip.src: The Source IP (to check alignment)
# -e frame.comment: The embedded label
command = [
    "tshark", "-n", "-r", pcap_file,
    "-Y", "ip",  # Filter to match nprint's IPv4 extraction
    "-T", "fields",
    "-e", "ip.src",
    "-e", "frame.comment",
    "-E", "separator=,",  # CSV format
    "-E", "quote=d"       # Quote values
]

# Run tshark and save to CSV
with open("labels_extracted.csv", "w") as outfile:
    # Write header
    outfile.write("tshark_ip,raw_label\n")
    outfile.flush()
    
    # Run command and pipe output to file
    subprocess.run(command, stdout=outfile, stderr=subprocess.DEVNULL)

print(" Extraction complete. Checking file...")

# Load and inspect
try:
    df = pd.read_csv("labels_extracted.csv")
    print(f"   Rows captured: {len(df)}")
    print("   Sample Data:")
    print(df.head())
    
    # Check if we have labels
    if df['raw_label'].notnull().sum() > 0:
        print("\n Success! Labels found.")
    else:
        print("\n Warning: No labels found in 'frame.comment'.")
        print("   The field name might be different (e.g., pcap_comment).")
except Exception as e:
    print(f" Error reading CSV: {e}")
