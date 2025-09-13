import socket
import threading  # To handle multiple clients at the same time
import json


users = {
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3"
}


votes = {
    "Alice": 0,
    "Bob": 0,
    "Charlie": 0
}

# Keep track of users who have already voted
voted_users = set()

# A lock ensures that multiple threads (clients) do not update votes at the same time
lock = threading.Lock()

def handle_client(conn, addr):
  try:
        # Send welcome message and ask for username
        conn.send("Welcome to the Voting System!\nEnter username: ".encode())
        username = conn.recv(1024).decode().strip()  # Receive username from client

        # Ask for password
        conn.send("Enter password: ".encode())
        password = conn.recv(1024).decode().strip()  # Receive password

         # Authentication check
        if username not in users or users[username] != password:
            conn.send("Authentication Failed. Disconnecting...".encode())
            conn.close()  # Close connection if authentication fails
            return
         
        # Check if user has already voted
        if username in voted_users:
            conn.send("You have already voted. Disconnecting...".encode())
            conn.close()
            return

        # Send voting options
        options = "Vote for a candidate:\n" + "\n".join(votes.keys()) + "\nYour choice: "
        conn.send(options.encode())

    
        # Receive vote choice from client
        choice = conn.recv(1024).decode().strip()


       # Validate vote
        if choice not in votes:
            conn.send("Invalid choice. Disconnecting...".encode())
            conn.close()
            return

        # Safely update vote count using a lock
        with lock:
            votes[choice] += 1
            voted_users.add(username)

       # Confirm vote to user
        conn.send(f"Thank you for voting for {choice}!\n".encode())

        # Print server-side log
        print(f"{username} voted for {choice}")

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        conn.close()
    finally:
        conn.close()  # Ensure the connection is always closed

def main():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 12345      # Port number for the server

    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))  # Bind socket to IP and port
    server.listen(5)  # Listen for incoming connections (max 5 queued)
    print(f"Server listening on {host}:{port}...")


    # Infinite loop to accept new clients
    while True:
        conn, addr = server.accept()  # Accept new connection
        print(f"New connection from {addr}")

        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()

