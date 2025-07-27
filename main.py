#%%
%load_ext autoreload
%autoreload 2 
#%%
from ScannerNotifier import *

#%%
notifier_obj = Notifier("config.json")
#%%
notifier_obj.getUserID(updateconfig=True)

#%%
notifier_obj.sendMessage(['algo aconteceu comigo','fodasse'])
#%%
