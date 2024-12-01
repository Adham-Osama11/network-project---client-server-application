import socket
import random
import time


def simulate_dhcp_client(client_id, server_host="127.0.0.1", server_port=12345):
    """Simulates a single DHCP client."""
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)  # Set timeout for responses

    try:
        # Simulate DHCP DISCOVER
        print(f"Client {client_id}: Sending DHCP_DISCOVER...")
        client_socket.sendto(f"DHCP_DISCOVER:{client_id}".encode('utf-8'), (server_host, server_port))

        # Receive DHCP OFFER
        response, server_address = client_socket.recvfrom(1024)
        offer = response.decode('utf-8')
        print(f"Client {client_id}: Received: {offer}")

        if offer.startswith("DHCP_OFFER"):
            offered_ip = offer.split(":")[1]

            # Simulate DHCP REQUEST
            print(f"Client {client_id}: Sending DHCP_REQUEST...")
            client_socket.sendto(f"DHCP_REQUEST:{client_id}".encode('utf-8'), server_address)

            # Receive DHCP ACK or NAK
            ack_response, _ = client_socket.recvfrom(1024)
            print(f"Client {client_id}: Received: {ack_response.decode('utf-8')}")
        else:
            print(f"Client {client_id}: No offer received.")
    except socket.timeout:
        print(f"Client {client_id}: No response from DHCP server.")
    finally:
        client_socket.close()


def start_multiple_clients(num_clients, server_host="127.0.0.1", server_port=12345):
    """Simulates multiple DHCP clients."""
    for client_id in range(1, num_clients + 1):
        simulate_dhcp_client(client_id, server_host, server_port)
        time.sleep(random.uniform(0.5, 2))  # Random delay between clients


if __name__ == "__main__":
    # Start simulation with multiple clients
    start_multiple_clients(num_clients=6)
