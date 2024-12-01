import socket

# Simulated pool of IP addresses
IP_POOL = ["192.168.1.100", "192.168.1.101", "192.168.1.102", "192.168.1.103"]

# Mapping of clients to assigned IPs
assigned_ips = {}


def start_dhcp_server(host="127.0.0.1", port=12345):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"DHCP Server running on {host}:{port}")

    while True:
        # Receive a DHCP request from the client
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Received '{message}' from {client_address}")

        # Parse the message
        if message.startswith("DHCP_DISCOVER"):
            client_id = message.split(":")[1] if ":" in message else "Unknown"

            # Check if any IPs are available
            if IP_POOL:
                ip_to_assign = IP_POOL.pop(0)  # Assign the first available IP
                assigned_ips[client_id] = ip_to_assign
                response = f"DHCP_OFFER:{ip_to_assign}"
                print(f"Offered IP {ip_to_assign} to {client_id} ({client_address})")
            else:
                response = "DHCP_NAK:No available IPs"

        elif message.startswith("DHCP_REQUEST"):
            client_id = message.split(":")[1] if ":" in message else "Unknown"
            if client_id in assigned_ips:
                response = f"DHCP_ACK:{assigned_ips[client_id]}"
                print(f"Acknowledged IP {assigned_ips[client_id]} for {client_id} ({client_address})")
            else:
                response = "DHCP_NAK:No IP assigned yet"

        else:
            response = "DHCP_ERROR:Unknown request"

        # Send response back to the client
        server_socket.sendto(response.encode('utf-8'), client_address)


if __name__ == "__main__":
    start_dhcp_server()
