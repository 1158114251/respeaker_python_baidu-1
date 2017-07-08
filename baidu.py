import logging
import time
import os
import json
from threading import Thread, Event
from respeaker import Microphone
from respeaker.baidu_speech_api import BaiduVoiceApi               

# get a APIKey and SecretKey from http://yuyin.baidu.com/
APP_KEY = ''
SECRET_KEY = ''      


def task(quit_event):                                                         
    mic = Microphone(quit_event=quit_event)                                   
    baidu = BaiduVoiceApi(appkey=APP_KEY,secretkey=SECRET_KEY)                                        

    while not quit_event.is_set():
        if mic.wakeup('respeaker'):        
            print('Wake up')               
            data = mic.listen()            
            try:                      
                text = baidu.server_api(data)
                if text:
		    text = json.loads(text)
                    print('Recognized %s' % text['result'][0])
            except Exception as e:               
                print(e.message)                 

def main():                                                              
    logging.basicConfig(level=logging.DEBUG)                                                           
    quit_event = Event()        
    thread = Thread(target=task, args=(quit_event,))
    thread.start()                          
    while True:                             
        try:                                
            time.sleep(1)                           
        except KeyboardInterrupt:                   
            print('Quit')                           
            quit_event.set()
            break        
    thread.join()                

if __name__ == '__main__':       
    main()
