import json
import requests

class Notifier():
    """_summary_
    Simple telegram bot class
    """
    def __init__(self, config_path: str):
        """_summary_

        Args:
            config_path (str, optional): Path to .json configuration file
        """
        self.config_path = config_path
        with open(config_path) as file:
            data = json.load(file)
            try:
                self.API_KEY = data['API_KEY']
            except:
                print(f"Não há API_KEY em {config_path}")

            try:
                self.CHAT_ID = data['CHAT_ID']
            except:
                self.CHAT_ID = []

    def getUserID(self,updateconfig = False):
        """_summary_
        Search for new bot interactions and store its CHAT_ID. 

        Args:
            updateconfig (bool, optional): If True, new CHAT_ID entries will be automatically added to .json configuration file. Defaults to False.
        """
        url = f"https://api.telegram.org/bot{self.API_KEY}/getUpdates"
        response = requests.get(url).json()
        for result in response['result']:
            ID = str(result['message']['chat']['id'])
            if ID not in self.CHAT_ID:
                self.CHAT_ID.append(ID)
        
        if updateconfig:
            with open(self.config_path,'r') as file:
                data = json.load(file)
            
            data['CHAT_ID'] = self.CHAT_ID
            with open(self.config_path, 'w') as file:
                json.dump(data, fp=file,indent=4)

            

    
    def sendMessage(self, input):
        """_summary_

        Args:
            input (str, list): Broadcast message or list of messages CHAT_ID list
        """
        url = f"https://api.telegram.org/bot{self.API_KEY}/sendMessage"
        for CHAT_ID in self.CHAT_ID:
            if isinstance(input,list): # Múltiplas mensagens
                for msg in input:
                    response = requests.post(url,
                                data={
                                    "chat_id":CHAT_ID,
                                    "text": msg
                                    },
                                headers={
                                    "Content-Type":"application/x-www-form-urlencoded"
                                    }
                                )
            else: # Mensagem única
                response = requests.post(url,
                            data={
                                "chat_id":CHAT_ID,
                                "text": input
                                },
                            headers={
                                "Content-Type":"application/x-www-form-urlencoded"
                                }
                            )
                # print(f"Request made\n{url}\n{CHAT_ID}")
                # print(f"{response}")
                # print("-"*20)
