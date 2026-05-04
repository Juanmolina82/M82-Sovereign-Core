import requests, json, datetime, os
T_FILE = "m82_token.json"
POSTS = {
    "9AM": "Strategic Resilience: Anchoring global infrastructure in Democracy and Legal Certainty. #M82 #MOLINAHOLDINGS #USA",
    "3PM": "Market Architecture: Strengthening the Rule of Law across Tennessee, NY, Miami, and Caracas. #M82 #MOLINAHOLDINGS",
    "8PM": "The Shift to Tangible Value: Global stability is architected through infrastructure and institutional rigour. From the strategic enforcement of logistics to the evolution of enterprise AI, we focus on the assets that define sovereignty. Expanding our Hedge Fund footprint from NY and Miami to Tennessee and Caracas. We stand with the architects of the West. #M82 #MOLINAHOLDINGS #USA #HedgeFunds #InfrastructureSovereignty"
}

def transmit():
    try:
        if not os.path.exists(T_FILE): return
        with open(T_FILE, "r") as f:
            token = json.load(f)["access_token"]
        u_info = requests.get("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {token}"}).json()
        author_urn = f"urn:li:person:{u_info['sub']}"
        h = datetime.datetime.now().hour
        txt = POSTS["9AM"] if 5 <= h < 12 else POSTS["3PM"] if 12 <= h < 18 else POSTS["8PM"]
        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": txt},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"}
        r = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=payload)
        if r.status_code == 201:
            print("[M82 SUCCESS] Manifiesto Institucional de Wall Street transmitido.")
        else:
            print(f"[M82 ERROR] {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    transmit()
