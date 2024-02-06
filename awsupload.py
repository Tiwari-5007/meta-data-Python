import logs as lg
import sys
import datetime
import boto3

def upload_to_aws_s3():
    now = str(datetime.datetime.now()).split('.')[0]
    lg.logw("info", f"{now}#################################### S3 Upload file Start #########################################")

    voice_file = sys.argv[1]
    upload_filename = voice_file.split('/')[-1]

    aws_access_key = 'AKIAVV6ZJBA2C5MTVZ3V'
    aws_secret_key = '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'
    bucket_name = 'cz-test-001'

    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        with open(voice_file, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, upload_filename)

        res_msg = f"Upload successful: {voice_file}"
        lg.logw("info", f"{now} {res_msg}")
        print(f"true##{res_msg}")

    except Exception as e:
        lg.logw("info", f"{now} Upload Failed for: {voice_file} and Error is: - {e}")
        print(f"false##{e}")

upload_to_aws_s3()
