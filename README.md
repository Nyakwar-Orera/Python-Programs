DNS Client
This project is a DNS client implemented in Python that can query a DNS server for domain name to IP address translation. It allows the user to provide a hostname as a command-line argument and retrieves the corresponding IP addresses using the DNS protocol.

Features
Reads a hostname provided as a command-line argument.
Prepares a DNS query message adhering to the DNS protocol specifications.
Sends the DNS query message to a DNS server using UDP socket communication.
Receives and processes the DNS server's response.
Extracts and displays the IP addresses from the response.

Requirements
Python 3.x
Network connectivity to communicate with DNS server
Necessary permissions to create UDP sockets and send/receive data
Usage

Clone this repository or download the dns.py file.
Open a terminal or command prompt.
Navigate to the directory where the dns.py file is located.
Run the following command, replacing <hostname> with the desired hostname to query:

command prompt
py dns.py <hostname>
Example:

Copy code
python dns.py gmu.edu
The script will send a DNS query for the provided hostname to a DNS server (by default, Google Public DNS). It will then display the corresponding IP addresses in the response.

Notes
This DNS client currently supports querying a single hostname at a time.
The DNS server used in this implementation is Google Public DNS (8.8.8.8) by default. You can modify the DNS_SERVER variable in the code to use a different DNS server if desired.

The DNS query message adheres to the DNS protocol specifications, including the construction of the header, question section, and conversion to hexadecimal representation.
The DNS response parsing in this implementation focuses on extracting IPv4 addresses (A type records) from the answer section of the response. Additional parsing logic can be added to handle other types of records if needed.
Make sure you have the necessary network connectivity and permissions to run the DNS client.