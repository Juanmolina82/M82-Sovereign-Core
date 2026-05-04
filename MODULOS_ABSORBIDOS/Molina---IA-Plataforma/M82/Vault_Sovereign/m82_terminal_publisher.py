import requests
import os

def publish_to_linkedin():
    # El token se debe configurar en el entorno de Termux para seguridad
    access_token = os.getenv('LINKEDIN_TOKEN')
    author_id = os.getenv('LINKEDIN_PERSON_ID') # Tu URN de LinkedIn

    if not access_token:
        print("\033[1;31m[ERROR] Falta LINKEDIN_TOKEN en Termux.\033[0m")
        return

    url = "https://api.linkedin.com/v2/ugcPosts"
    
    with open("M82_Final_Logistics_Audit.txt", "r") as f:
        content = f.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_data = {
        "author": f"urn:li:person:{author_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"M82 Sovereign Update:\n\n{content}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code == 201:
        print("\033[1;32m[SUCCESS] Post eyectado desde la terminal Termux.\033[0m")
    else:
        print(f"\033[1;31m[FAILED] Error {response.status_code}: {response.text}\033[0m")

if __name__ == "__main__":
    publish_to_linkedin()
