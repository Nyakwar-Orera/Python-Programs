import sys
import socket
import struct
import random

# DNS server details
DNS_SERVER = '8.8.8.8'
DNS_PORT = 53

def build_dns_query(hostname):
    # DNS header fields
    ID = random.randint(0, 65535)  # Generate a random ID
    QR = 0
    OPCODE = 0
    AA = 0
    RD = 1
    QDCOUNT = 1

    # DNS question section fields
    QNAME = b''
    for label in hostname.split('.'):
        QNAME += struct.pack('B', len(label)) + label.encode()
    QNAME += b'\x00'  # Terminating null label
    QTYPE = 1  # A record
    QCLASS = 1  # IN class

    # Construct the DNS query message
    dns_query = struct.pack('!HHHHHH', ID, (QR << 15) | (OPCODE << 11) | (AA << 10) | (RD << 8) | QDCOUNT, 0, 0, 0, 0)
    dns_query += QNAME + struct.pack('!HH', QTYPE, QCLASS)

    return dns_query, QNAME


def send_dns_query(query):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_socket.sendto(query, (DNS_SERVER, DNS_PORT))
        client_socket.settimeout(5)  # Set socket timeout to 5 seconds

        attempts = 0
        while attempts < 3:
            try:
                response, server_address = client_socket.recvfrom(4096)
                return response
            except socket.timeout:
                attempts += 1
                print(f"DNS response not received (attempt {attempts} of 3)...")
        
        print("Error: No response from the DNS server after multiple attempts.")

    finally:
        client_socket.close()


def parse_domain_name(response, offset):
    domain_name = ""
    while True:
        length = response[offset]
        if length == 0:
            break
        elif length >= 192:
            pointer = struct.unpack('!H', response[offset:offset + 2])[0]
            offset = (pointer ^ (1 << 14))  # Follow pointer
        else:
            offset += 1
            label = response[offset:offset + length].decode()
            domain_name += label + "."
            offset += length

    return domain_name.rstrip(".")
def process_dns_response(response, QNAME):
    if response:
        print("DNS response received.")
        print("Processing DNS response...")
        print("-" * 79)

        if len(response) < 12:
            print("Error: Invalid DNS response.")
            return

        header = struct.unpack('!6H', response[:12])
        if len(header) < 6:
            print("Error: Invalid DNS header.")
            return

        print("----------------------------------------------------------------------------")
        print(f"header.ID = {header[0]}")
        print(f"header.QR = {(header[1] >> 15) & 1}")
        print(f"header.OPCODE = {(header[1] >> 11) & 15}")
        # Print other header fields...

        qname = QNAME.decode()
        print(f"question.QNAME = {qname}")
        # Print question.QTYPE and question.QCLASS...

        answer_count = header[5]
        authority_count = header[6] if len(header) >= 7 else 0
        additional_count = header[7] if len(header) >= 8 else 0
        offset = 12 + len(QNAME)

        # Print answer section
        print("Answer Section:")
        for _ in range(answer_count):
            name, rtype, rclass, ttl, rdlength = struct.unpack('!HHHLH', response[offset:offset + 12])
            offset += 12
            rdata = response[offset:offset + rdlength]

            if rtype == 1:  # A record
                ip_address = socket.inet_ntoa(rdata)
                print(f"answer.NAME = {parse_domain_name(response, name)}")
                print(f"answer.TYPE = {rtype}")
                # Print other answer fields...
                print(f"answer.RDATA = {ip_address}")

            offset += rdlength

        # Print authority section
        print("Authority Section:")
        for _ in range(authority_count):
            name, rtype, rclass, ttl, rdlength = struct.unpack('!HHHLH', response[offset:offset + 12])
            offset += 12
            rdata = response[offset:offset + rdlength]

            # Parse and print authority RR fields
            authority_name = parse_domain_name(response, name)
            print(f"authority.NAME = {authority_name}")
            print(f"authority.TYPE = {rtype}")
            # Print other authority fields...

            offset += rdlength

        # Print additional section
        print("Additional Section:")
        for _ in range(additional_count):
            name, rtype, rclass, ttl, rdlength = struct.unpack('!HHHLH', response[offset:offset + 12])
            offset += 12
            rdata = response[offset:offset + rdlength]

            # Parse and print additional RR fields
            additional_name = parse_domain_name(response, name)
            print(f"additional.NAME = {additional_name}")
            print(f"additional.TYPE = {rtype}")
            # Print other additional fields...

            offset += rdlength

        print("-" * 79)

# Main code
if len(sys.argv) != 2:
    print("Usage: python dns_client.py <hostname>")
    sys.exit(1)

hostname = sys.argv[1]
query, QNAME = build_dns_query(hostname)

print("Preparing DNS query...")
print("Contacting DNS server...")
print("Sending DNS query...")

response = send_dns_query(query)

print("DNS response received (attempt 1 of 3)")
process_dns_response(response, QNAME)
