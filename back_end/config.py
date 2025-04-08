# Retreive Access Token for Outlook
# import os
# from dotenv import load_dotenv
# import msal 

# # Azure AD App registration details
# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET') 
# TENANT_ID = os.getenv('TENANT_ID')
# # Scope for client credentials flow: Mail.ReadWrite, Mail.Send, User.Read
# SCOPES = ["https://graph.microsoft.com/.default"]

# def get_access_token():
#     # Create an MSAL app object for Confidential Client Application
#     app = msal.ConfidentialClientApplication(
#         CLIENT_ID,
#         authority=f"https://login.microsoftonline.com/{TENANT_ID}",
#         client_credential=CLIENT_SECRET  
#     )

#     # Requesting the token using client credentials flow
#     result = app.acquire_token_for_client(scopes=SCOPES)

#     if "access_token" in result:
#         access_token = result["access_token"]
#         print("Access token obtained successfully!")
#         return access_token
#     print("Error obtaining access token")
#     print(result.get("error"))
#     print(result.get("error_description"))
#     return None


import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")