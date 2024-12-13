import socket
import os
from urllib.parse import urlparse, parse_qs

PORT = 5698
ADDR = ('', PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

HEADER = 4096
FORMAT = 'utf-8'
LOCAL_DIRECTORY = os.getcwd()

FILES = {
    "/": ("text/html", open('main_en.html', 'r', encoding=FORMAT).read()),
    "/en": ("text/html", open('main_en.html', 'r', encoding=FORMAT).read()),
    "/index.html": ("text/html", open('main_en.html', 'r', encoding=FORMAT).read()),
    "/main_en.html": ("text/html", open('main_en.html', 'r', encoding=FORMAT).read()),
    "/ar": ("text/html", open('main_ar.html', 'r', encoding=FORMAT).read()),
    "/main_ar.html": ("text/html", open('main_ar.html', 'r', encoding=FORMAT).read()),
    "/style.css": ("text/css", open('style.css', 'r', encoding=FORMAT).read()),
    "/404.css": ("text/css", open('404.css', 'r', encoding=FORMAT).read()),
    "/fotTopic.css": ("text/css", open('fotTopic.css', 'r', encoding=FORMAT).read()),
    "/member.css": ("text/css", open('member.css', 'r', encoding=FORMAT).read()),
    "/Structure_of_the_Internet.jpg": ("image/jpeg", open('Structure_of_the_Internet.jpg', 'rb').read()),
    "/AccessingWebPage.jpg": ("image/jpeg", open('AccessingWebPage.jpg', 'rb').read()),
    "/mohammad.png": ("image/png", open('mohammad.png', 'rb').read()),
    "/toqa.png": ("image/png", open('toqa.png', 'rb').read()),
    "/omar.png": ("image/png", open('omar.png', 'rb').read()),
    "/mohammadInfo.html": ("text/html", open('mohammadInfo.html', 'r', encoding=FORMAT).read()),
    "/toqaInfo.html": ("text/html", open('toqaInfo.html', 'r', encoding=FORMAT).read()),
    "/omarInfo.html": ("text/html", open('omarInfo.html', 'r', encoding=FORMAT).read()),
    "/mohammadInfo_ar.html": ("text/html", open('mohammadInfo_ar.html', 'r', encoding=FORMAT).read()),
    "/toqaInfo_ar.html": ("text/html", open('toqaInfo_ar.html', 'r', encoding=FORMAT).read()),
    "/omarInfo_ar.html": ("text/html", open('omarInfo_ar.html', 'r', encoding=FORMAT).read()),
    "/supporting_material_en.html": ("text/html", open('supporting_material_en.html', 'r', encoding=FORMAT).read()),
    "/supporting_material_ar.html": ("text/html", open('supporting_material_ar.html', 'r', encoding=FORMAT).read()),
}

notFoundPage = open('notFound.html', 'r', encoding=FORMAT).read()

def handle_request(conn):
    try:
        request = conn.recv(HEADER).decode(FORMAT)

       
        
        print("[FULL REQUEST] Received the following HTTP request:")
        print(request)
        print("-" * 50)


        msg = request.splitlines()[0]
        resource = msg.split(' ')[1]
        print(f"[REQUEST LINE] {msg}")
        print(f"[RESOURCE REQUESTED] {resource}")


        parsed_url = urlparse(resource)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        print(f"[DEBUG] Full Request: {request}")
        print(f"[DEBUG] Parsed URL - Path: {path}, Query Params: {query_params}")

        

        if path in FILES:
            content_type, content = FILES[path]
            response_headers = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Connection: close\r\n\r\n"
            )
            conn.sendall(response_headers.encode(FORMAT))
            conn.sendall(content if isinstance(content, bytes) else content.encode(FORMAT))
            print("[RESPONSE END] Resource served successfully.")
            return

        if path in ["/search_supporting_material", "/supporting_material_ar"]:
            print(f"[DEBUG] Path matched: {path}")  
            
            if "filename" in query_params:
                filename = query_params["filename"][0] 
                print(f"[DEBUG] Filename: {filename}")

                file_path = os.path.join(LOCAL_DIRECTORY, filename)

                if os.path.exists(file_path):
                    extension = os.path.splitext(filename)[1].lower()
                    if extension in ['.jpg', '.jpeg']:
                        content_type = "image/jpeg"
                    elif extension in ['.png', '.gif']:
                        content_type = "image/png"
                    elif extension in ['.mp4', '.avi', '.mov', '.mkv']:
                        content_type = "video/mp4"
                    else:
                        return handle_404(conn)

                    with open(file_path, 'rb') as f:
                        content = f.read()
                    response_headers = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {content_type}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    conn.sendall(response_headers.encode(FORMAT))
                    conn.sendall(content)
                    return
                else:
                    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        redirect_url = f"https://www.google.com/search?q={filename}&tbm=isch"
                        print(f"[SEARCH REDIRECT] Redirecting to Google search for image: {query_params}")

                    elif filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        redirect_url = f"https://www.youtube.com/results?search_query={filename}"
                        print(f"[SEARCH REDIRECT] Redirecting to YouTube search for video: {query_params}")

                    else:
                        return handle_404(conn)  

                    response_headers = (
                        f"HTTP/1.1 307 Temporary Redirect\r\n"
                        f"Location: {redirect_url}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    conn.sendall(response_headers.encode(FORMAT))
                    print(f"[REDIRECT] Redirected to {redirect_url}")
                    print("[RESPONSE END] Redirect response sent successfully.")
                    return

        handle_404(conn)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print("[CONNECTION CLOSED] Connection with the client has been closed.")


def handle_404(conn):
    notFoundForClient = notFoundPage.replace("{{client_ip}}", conn.getpeername()[0])
    notFoundForClient = notFoundForClient.replace("{{client_port}}", str(conn.getpeername()[1]))
    
    response_headers = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        "Connection: close\r\n\r\n"
    )
    conn.sendall(response_headers.encode(FORMAT))
    conn.sendall(notFoundForClient.encode(FORMAT))
    print(f"[NOT FOUND] Resource not found")
    print("[RESPONSE END] 404 response sent successfully.")

def start():
    SERVER.listen()
    print(f"[LISTENING] Server is listening on port {PORT}")
    while True:
        conn, addr = SERVER.accept()
        print(f"[CONNECTION] New connection from {addr}")
        handle_request(conn)

print("[STARTING] Server is starting...")
start()
