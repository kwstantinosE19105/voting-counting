import socket  # For network communication

def main():
    # Ask user to input server IP
    host = input("Enter server IP (e.g., 127.0.0.1): ").strip()
    port = 12345  # Port should match the server's port

    # Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))  # Connect to the server

    while True:
        # Receive data from server
        data = client.recv(1024).decode()
        if not data:
            break  # Exit if server closes connection

        # Print server messages to the console
        print(data, end="")

        # Check if server is asking for input
        if "username" in data.lower() or "password" in data.lower() or "your choice" in data.lower():
            msg = input()  # Take input from user
            client.send(msg.encode())  # Send input to server

    client.close()  # Close the connection when done

if __name__ == "__main__":
    main()
