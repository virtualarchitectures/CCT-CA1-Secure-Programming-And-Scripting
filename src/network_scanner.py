import socket


def tcp_scan(ip, port):
    # Try connecting to a TCP port to determine if it is open.
    try:
        # Create an TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set a timeout for the connection attempt
            sock.settimeout(1)
            # Attempt to connect to the specified IP and port
            if sock.connect_ex((ip, port)) == 0:
                print(f"TCP Port {port} is open on {ip}")
    except Exception as e:
        print(f"Error scanning TCP port {port} on {ip}: {e}")


def udp_scan(ip, port):
    # Send a UDP packet to a port and check for response to infer if it might be open.
    try:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # Set a timeout to wait for a response
            sock.settimeout(1)
            # Send an empty UDP packet
            sock.sendto(b"", (ip, port))
            try:
                # Attempt to receive a response
                sock.recvfrom(1024)
                print(f"UDP Port {port} is open on {ip}")
            except socket.timeout:
                # If no response is received, the port may be open or filtered
                print(f"No response: UDP Port {port} on {ip} is open or filtered")
    except Exception as e:
        print(f"Error scanning UDP port {port} on {ip}: {e}")


def scan_ip(ip, ports):
    # Scan an IP address across a range of ports for TCP and UDP
    print(f"\nScanning IP: {ip}")
    for port in ports:
        # Check each port for open TCP ports
        tcp_scan(ip, port)
        # Check each port for open UDP ports
        udp_scan(ip, port)


def parse_ip_range(ip_range):
    # Parse a single IP or a range of IPs.
    # A range can be specified as follows: "192.168.1.1-10"
    if "-" in ip_range:
        # Split the input into the start and the end of the range
        start_ip, end_ip = ip_range.split("-")
        # Split the starting IP into octets
        start_octets = start_ip.split(".")
        # Convert the last segment of the range to an integer for looping
        end_last_octet = int(end_ip)

        # Build a list of IP addresses from the start to the end range
        base_ip = ".".join(start_octets[:3])
        return [
            f"{base_ip}.{i}" for i in range(int(start_octets[3]), end_last_octet + 1)
        ]

    # Return a single IP in list form
    return [ip_range]


if __name__ == "__main__":
    # User input for an IP or an IP range
    ip_input = input("Enter a single IP address or a contiguous IP address range: ")
    ports = list(range(1, 1025))  # Define the port range to scan (1-1024)

    # Generate list of IPs from the given input range
    ips = parse_ip_range(ip_input.strip())
    for ip in ips:
        scan_ip(ip, ports)  # Scan each IP address in the list
