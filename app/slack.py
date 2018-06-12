import requests

def send_file_to_slack(token,channels,file):
    from urllib import request, parse
    url = 'https://slack.com/api/files.upload'
    my_file = {
            'file' : (file,open(file,'rb'),'txt')
    }

    payload={
            "filename":file,
            "token":token,
            "channels":[channels]
    }

    r = requests.post(url,params=payload,files=my_file)
