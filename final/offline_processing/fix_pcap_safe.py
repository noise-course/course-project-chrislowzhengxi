from scapy.all import PcapReader, PcapWriter
import os

print("Starting conversion with timestamp sanitization...")
count = 0
# Start at a safe, valid epoch time (e.g., Year 2020)
SAFE_TIME = 1600000000.0 

with PcapWriter("traffic_fixed.pcap", append=True, sync=True) as writer:
    for pkt in PcapReader("traffic.pcapng"):
        # Force the timestamp to be a standard float
        try:
            ts = float(pkt.time)
            # Check if timestamp is too big (Year 2106+) or negative
            if ts < 0 or ts > 4000000000:
                raise ValueError("Timestamp out of range")
            pkt.time = ts
        except:
            # If invalid, invalid type, or out of range, use a fake sequential time
            pkt.time = SAFE_TIME + (count * 0.001)
             
        writer.write(pkt)
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} packets...", end='\r')

print(f"\nSuccess! Converted {count} packets to traffic_fixed.pcap")
