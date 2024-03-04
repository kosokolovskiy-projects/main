from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_files import list_files

import os
import shutil
import subprocess
import argparse

SCOPES = ['https://www.googleapis.com/auth/drive']

cred_name_file = 'replace_path_to_credentials'

def upload_new_variant(username, subject, var_name, is_file=0):
    creds = None
    if os.path.exists('access_files/token.json'):
        creds = Credentials.from_authorized_user_file('access_files/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_name_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('access_files/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    CONVERT_SUBJECT = {'math': 'M_', 'inf': 'I_'}
    CONVERT_MIMETYPE = {0: 'application/pdf', 1: 'application/zip'}
    CONVERT_DOC_TYPE = {0: 'Variant', 1: 'Files'}

    num_var = list_files(username, CONVERT_DOC_TYPE[is_file], CONVERT_SUBJECT[subject])
    print(num_var, len(num_var))
    if subject == 'math':
        code = ['replace_folder_name']
    elif subject in 'inf':
        code = ['replace_folder_name']

    if is_file:
        file_name = f'{CONVERT_SUBJECT[subject]}F_var_{len(num_var) + 1}_{var_name}_{username}.{CONVERT_MIMETYPE[is_file][-3:]}'
    else:
        file_name = f'{CONVERT_SUBJECT[subject]}var_{len(num_var) + 1}_{var_name}_{username}.{CONVERT_MIMETYPE[is_file][-3:]}'

    shutil.copyfile(f'variants/{subject}_{username}/{var_name}.{CONVERT_MIMETYPE[is_file][-3:]}', f'variants/{subject}_{username}/{file_name}')

    file_metadata = {
        'name': f'{file_name}',
        'parents': code
    }

    try:
        media = MediaFileUpload(f'replace_path/to/variants/{subject}_{username}/{var_name}.{CONVERT_MIMETYPE[is_file][-3:]}', mimetype=CONVERT_MIMETYPE[is_file])
    except Exception:
        media = MediaFileUpload(f'replace_path/to/variants/{subject}/{var_name}.{CONVERT_MIMETYPE[is_file][-3:]}', mimetype=CONVERT_MIMETYPE[is_file])


    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'New file ID: {file.get("id")}')

    anyone_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file.get('id'), body=anyone_permission).execute()
    print('New file is now accessible to anyone with the link.')


parser = argparse.ArgumentParser(description='Upload a PDF to Google Drive and make it public.')
parser.add_argument('-u', '--username', help='The username to construct the PDF filename')
parser.add_argument('-s', '--subject', help='inf or math')
parser.add_argument('-n', '--varname', help='the name of variant')
parser.add_argument('-i', '--isfile', help='is it a file or not', type=int)

args = parser.parse_args()

upload_new_variant(args.username, args.subject, args.varname, args.isfile)



