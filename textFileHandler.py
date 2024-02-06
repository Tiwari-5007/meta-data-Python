import paramiko
from dotenv import load_dotenv
import os
from logsHandler import logw
import utils as sendreq
import azureFileHandler as az
# Load environment variables from .env
load_dotenv()

remote_host = os.getenv("REMOTE_HOST")
remote_username = os.getenv("REMOTE_USERNAME")
remote_password = os.getenv("REMOTE_PASSWORD")
remote_file_path = os.getenv("REMOTE_FILE_PATH")

if not remote_host or not remote_username or not remote_password or not remote_file_path:
    logw("error", "Remote server details not found in config")
    exit()

ssh_client = None

def establish_ssh_connection():
    global ssh_client
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(remote_host, username=remote_username, password=remote_password)
    except Exception as e:
        logw("error", f"Failed to establish SSH connection: {str(e)}")

def read_remote_file():
    try:
        if not ssh_client:
            establish_ssh_connection()
        # Open an SFTP session
        sftp = ssh_client.open_sftp()

        # Read the remote file
        with sftp.open(remote_file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        # Clear the content of the remote file if data has been successfully read
        if lines:
            with sftp.open(remote_file_path, 'w') as file:
                file.write('')
        
        return lines
    except Exception as e:
        logw("error", f"Failed to read remote file: {str(e)}")
        return False

def getfile_detail(str):
    new_srt = str.split(" ")[1].split("##")
    return [new_srt[0].lstrip("\""), new_srt[1]]

def process_file_key_data(key):
    (monFileN, monFileP) = getfile_detail(key)
    if monFileN and monFileP:
        az.handle_data(monFileN, monFileP)
        sendreq.sendmetaData(key)
    else:
        logw("warning", f"Data not Found for either Monitor File Name: {monFileN} or Monitor File Path: {monFileP}")
