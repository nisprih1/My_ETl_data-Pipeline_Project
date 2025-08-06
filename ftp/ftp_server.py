import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_USER = "Harsh"
FTP_PASS = "12345"
FTP_PORT = 2121
FTP_DIR = "data"  

os.makedirs(FTP_DIR, exist_ok=True)

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASS, FTP_DIR, perm="elradfmwMT")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", FTP_PORT), handler)
    print(f"FTP server started at ftp://127.0.0.1:{FTP_PORT}")
    print(f"User: {FTP_USER} |  Pass: {FTP_PASS}")
    print(f"Shared folder: {FTP_DIR}")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()
