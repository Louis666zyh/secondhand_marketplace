import requests

BASE_URL = "http://127.0.0.1:8000/api/"
ADMIN_USERNAME = "Ciciyizi"
ADMIN_PASSWORD = "ly2002216"

def get_token():
    """Retrieve authentication token"""
    response = requests.post(BASE_URL + "users/login/", json={"username_or_email": ADMIN_USERNAME, "password": ADMIN_PASSWORD})
    return response.json().get("access")

def post_review(token, product_id, rating, comment):
    """Post a review for a product"""
    url = BASE_URL + "reviews/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"product": product_id, "rating": rating, "comment": comment}

    response = requests.post(url, json=data, headers=headers)
    print("✅ Post Review Response:", response.status_code, response.json())

def get_reviews(product_id):
    """Retrieve reviews for a product"""
    url = BASE_URL + f"reviews/?product={product_id}"
    response = requests.get(url)
    print("✅ Get Reviews Response:", response.status_code, response.json())

if __name__ == "__main__":
    token = get_token()
    if token:
        post_review(token, product_id=1, rating=5, comment="Great product!")
        get_reviews(product_id=1)
