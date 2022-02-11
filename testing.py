import os
import arionpaylib
client = arionpaylib.initialize_client()
arionpaylib.create_asset(client, 'arioneft', 1000)
print("Done")

