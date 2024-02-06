import subprocess
import os
import mixing as ms
from dotenv import load_dotenv
from logsHandler import logw

# Load environment variables from .env
load_dotenv()

python_env = os.getenv("PY_ENV")

# take path/ upload file path from Config

def upload_data_azure(file_path,file_name):
    # command = ["/Czentrix/apps/erp_python/venv37/bin/python", "/home/bhanu/azureupload.py", f"{file_path}{file_name}"]
    #command = [python_env, "/home/bhanu/azureupload.py", f"{file_path}{file_name}"]
    command = [python_env, "/home/bhanu/awsupload.py", f"{file_path}{file_name}"]
    logw("info", f"Executing Command: {command}")
    result     = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout_str = result.stdout
    stderr_str = result.stderr
    resList    = stdout_str.split("##")
    if result.returncode == 0:
        if resList[0] == "false":
            listRes = resList[1].splitlines()[0].strip()
            return f"false##{listRes}"

        return f"true##File Successfully Uploaded"
    else:
        error_message = f"There Was Some error uploading the File. Stdout: {stdout_str}, Stderr: {stderr_str}"
        return f"false##{error_message}"


def handle_data(file_name,file_path):
    ext = file_name.split(".")[1]
    if ext == "wav":
        logw("info",f"Checking for file: {file_path + file_name}")
        if os.path.exists(file_path + file_name):
            logw("info",f"File {file_path + file_name} found successfully")
            logw("info",f"Initiating Data Upload to Azure for fileName {file_path + file_name}")
            data_uploaded = upload_data_azure(file_path, file_name)
            if data_uploaded.split("##")[0] == "false":
                # print({"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
                logw("error",{"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
                # Return the above json in the loger
            else:
                # print({"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
                logw("info",{"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
                # Return the above json in the loger
        else:
            inFile = file_name.split(".")[0] + "-in.wav"
            otFile = file_name.split(".")[0] + "-out.wav"
            logw("info",f"File {file_name} Not found, Checking for {inFile} and {otFile}")
            if os.path.exists(file_path + inFile) and os.path.exists(file_path + otFile):
                logw("info",f"File {inFile} and {otFile} found successfully")
                logw("info",f"Initiating Mixing for {inFile} and {otFile}")
                mix = ms.mix_audio_files(file_path + inFile, file_path + otFile, file_path + file_name)
                if mix:
                    logw("info",f"Mix Successful")
                    logw("info",f"Initiating Data Upload to Azure for fileName {file_path + file_name}")
                    data_uploaded = upload_data_azure(file_path, file_name)
                    if data_uploaded.split("##")[0] == "false":
                        # print({"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
                        logw("error",{"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
                    else:
                        # print({"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
                        logw("info",{"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
                else:
                    # print({"Status": "Failure", "Msg": 'There was some error in mixing the files'})
                    logw("error",{"Status": "Failure", "Msg": 'There was some error in mixing the files'})
            else:
                # print({"Status": "Failure", "Msg": 'In/Out WAV file not found'})
                logw("warning",{"Status": "Failure", "Msg": '{inFile}/{otFile} WAV file not found'})
    elif ext == "mp3":
        logw("info",f"Checking for file: {file_path + file_name}")
        if os.path.exists(file_path + file_name):
            logw("info",f"Initiating Data Upload to Azure for file Name: {file_path + file_name}")
            data_uploaded = upload_data_azure(file_path, file_name)
            if data_uploaded.split("##")[0] == "false":
                # print({"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
                logw("error",{"Status": "FAILURE", "Msg": f"{data_uploaded.split('##')[1]}"})
            else:
                # print({"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
                logw("info",{"Status": "SUCCESS", "Msg": f"{data_uploaded.split('##')[1]}"})
        else:
            logw("error",{"Status": "Failure", "Msg": f"File {file_name} Not Exists at location {file_path}"})
