# ENCS3320 - Computer Networks Project #1

## Overview

This project aims to enhance understanding of fundamental networking concepts, socket programming, and web server development. The tasks are designed to give hands-on experience with protocols like TCP, UDP, and HTTP, along with tools for network troubleshooting and analysis.

### Key Objectives:
- **Network Commands & Troubleshooting**: Understand basic network commands (`ipconfig`, `ping`, `tracert`, `telnet`, `nslookup`) and use **Wireshark** for packet analysis.
- **Web Server Programming**: Implement a web server with socket programming, handling HTML pages and dynamic redirection.
- **UDP Trivia Game**: Design and implement a multiplayer trivia game using **UDP** to demonstrate client-server communication in real-time.

## Project Tasks

### Task 1: Network Commands and Wireshark
- **Objective**: Understand and use fundamental network commands and packet analysis.
- **Concepts**:
  - **ipconfig**: Displays network configuration details like IP addresses and DNS.
  - **ping**: Tests connectivity between devices over the network.
  - **tracert**: Traces the route of packets to a specified destination.
  - **telnet**: Allows remote access to a server via text-based interface.
  - **nslookup**: Resolves DNS queries to fetch IP addresses for domain names.
  - **Wireshark**: A packet sniffer used to capture network traffic, especially DNS queries and responses.
- **Task Details**:
  - Run network commands and analyze outputs.
  - Use **Wireshark** to capture DNS queries and analyze the packet data.

### Task 2: Web Server Implementation
- **Objective**: Develop a basic web server using socket programming to serve HTML pages and handle HTTP requests.
- **Concepts**:
  - **Socket Programming**: Create server and client sockets using the Python `socket` library.
  - **HTTP Protocol**: Implement HTTP request/response handling, status codes (e.g., 200 OK, 404 Not Found), and dynamic content delivery.
  - **HTML/CSS**: Develop and serve HTML pages styled using CSS.
- **Task Details**:
  - Implement a server that listens on port **5698**.
  - Serve the following pages:
    - **main_en.html**: Team details, project description, and links to resources.
    - **supporting_material_en.html**: Image/video request form with redirection.
    - **Arabic versions**: Provide translated versions of the pages.
  - Implement error handling for invalid URLs (404 error page).
  - Handle **GET** requests, print request details, and serve appropriate content based on requested URL.

### Task 3: UDP Client-Server Trivia Game
- **Objective**: Implement a multiplayer trivia game using **UDP** sockets for communication between clients and server.
- **Concepts**:
  - **UDP (User Datagram Protocol)**: A connectionless protocol for sending datagrams between client and server.
  - **Socket Communication**: Use `UDP` sockets for fast, stateless communication between clients and server.
  - **Concurrency**: Handle multiple clients, broadcasting questions, and collecting answers.
- **Task Details**:
  - The **server** manages client connections, broadcasts trivia questions, collects answers, and calculates scores.
  - The **client** sends answers to the server and listens for updates (e.g., next question, score).
  - Implement features like round management, score tracking, and winner announcements.
  - The game will be played interactively, with the server managing the flow of questions and answers.

## Technologies Used
- **Programming Languages**: Python (for Task 2), Java (for Task 3), Bash (for Task 1)
- **Networking Protocols**: TCP, UDP, HTTP
- **Web Technologies**: HTML, CSS
- **Tools**: Wireshark (for packet analysis), GitHub (for version control)



