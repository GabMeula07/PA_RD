import os
import time
from modules.token import Token
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
app_acess = os.getenv('app_acess')
refresh_token = os.getenv('refresh_token')

token_rd = Token(app_acess, refresh_token, client_id, client_secret)
token_rd.get_new_token_with_refresh()


print("SEGMENTACAO \n")
segmentations = token_rd.make_request('https://api.rd.services/platform/segmentations/')

start = time.time()
limit = 118
interval = 60

count_segmentations = 0 
count_contacts = 0
for segmentation in segmentations['segmentations']:
    count_segmentations += 1
    print(f'{count_segmentations} - {segmentation['id']} - {segmentation['name']}')
    print('CONTATOS\n')
    contacts = token_rd.make_request(segmentation['links'][0]['href'])
    
   
    
    
    for _contact in contacts['contacts']:
       
        if count_contacts >= limit:
            exec_time = time.time() - start
            if exec_time < interval:
                sleep_time = interval - exec_time
                print('Calma meu patrão')
                time.sleep(sleep_time)
            
            count_contacts = 0 
            start = time.time()
        
        data_contact = token_rd.make_request(f'https://api.rd.services/platform/contacts/email:{_contact['email']}')
        try: 
            name_contact = data_contact['name']
            email_contact = data_contact['email']
            if 'job_title' in data_contact:
                job_title_contact = data_contact['job_title']
            else:
                job_title_contact = 'vazio'
            print(f'{count_contacts} - {name_contact} - {email_contact} -  {job_title_contact} | Time: {time.time() - start:.3f}s \n')
            count_contacts += 1
        except:
            print(data_contact)
    
    
        
    print(' ')
    
    