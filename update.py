import os
import time
from modules.token import Token
from collections import deque
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
app_acess = os.getenv("app_acess")
refresh_token = os.getenv("refresh_token")

token_rd = Token(app_acess, refresh_token, client_id, client_secret)
token_rd.get_new_token_with_refresh()


LIMIT = 120
INTERVAL = 60
count_segmentations = 0
request_timestamps = deque()


def show_response(data_response):
    try:
        name_contact = data_contact["name"]
        email_contact = data_contact["email"]
        if "job_title" in data_contact:
            job_title_contact = data_contact["job_title"]
        else:
            job_title_contact = "vazio"
            print(
                f"{name_contact} - {email_contact} -  {job_title_contact} | Time: {current_time} \n"
            )

    except:
        print(data_contact)

print("SEGMENTACAO \n")
segmentations = token_rd.make_request("https://api.rd.services/platform/segmentations/")

for segmentation in segmentations["segmentations"]:
    count_segmentations += 1
    print(f'{count_segmentations} - {segmentation['id']} - {segmentation['name']}')

    print("CONTATOS\n")
    contacts = token_rd.make_request(segmentation["links"][0]["href"])

    for _contact in contacts["contacts"]:
        current_time = time.time()

        while request_timestamps and current_time - request_timestamps[0] > INTERVAL:
            request_timestamps.popleft()

        if len(request_timestamps) < LIMIT:
            data_contact = token_rd.make_request(
                f'https://api.rd.services/platform/contacts/email:{_contact['email']}'
            )
            show_response(data_contact)
            request_timestamps.append(current_time)

        else:
            sleep_time = INTERVAL - (current_time - request_timestamps[0])
            time.sleep(sleep_time)

            current_time = time.time()

            data_contact = token_rd.make_request(
                f'https://api.rd.services/platform/contacts/email:{_contact['email']}'
            )
            show_response(data_contact)
            request_timestamps.append(current_time)

    print(" ")

print("Programa encerrado")
