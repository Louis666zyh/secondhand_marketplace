import os
import django
import requests

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondhand_marketplace.settings')
django.setup()

# 导入模型
from apps.users.models import User
from apps.products.models import Product, Category
from apps.transactions.models import Transaction


# 准备测试数据
def setup_test_data():
    # 创建或获取 admin 用户（seller 和 buyer）
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_superuser': True,
            'is_staff': True,
            'is_approved': False
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()

    # 创建或获取普通用户（buyer）
    buyer_user, created = User.objects.get_or_create(
        username='buyer',
        defaults={
            'email': 'buyer@example.com',
            'first_name': 'Buyer',
            'last_name': 'User',
            'is_approved': False
        }
    )
    if created:
        buyer_user.set_password('buyer123')
        buyer_user.save()

    # 创建或获取 Category
    category, _ = Category.objects.get_or_create(name="Test Category")

    # 创建或获取 Product
    product, _ = Product.objects.get_or_create(
        name="Test Product",
        defaults={
            'price': 99.99,
            'status': 'available',
            'category': category,
            'seller': admin_user,
            'is_approved': False
        }
    )

    # 创建或获取 Transaction
    transaction, _ = Transaction.objects.get_or_create(
        product=product,
        buyer=buyer_user,
        defaults={
            'status': 'pending',
            'total_price': 99.99  # 确保与 product.price 一致
        }
    )


BASE_URL = "http://127.0.0.1:8000/api/admin/"
ADMIN_USERNAME = "Ciciyizi"
ADMIN_PASSWORD = "ly2002216"


def get_admin_token(username, password):
    url = "http://127.0.0.1:8000/api/users/login/"
    data = {"username_or_email": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("✅ Admin login successful:", response.json())
        return response.json().get("access")
    else:
        print("❌ Admin login failed:", response.status_code, response.json())
        return None


def test_approve_user(token, user_id):
    url = f"{BASE_URL}users/{user_id}/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"is_approved": True}
    print(f"Testing approve user for user_id={user_id} with data={data}")
    response = requests.patch(url, json=data, headers=headers)
    try:
        print(f"User approval: {response.status_code} {response.json()}")
    except ValueError as e:
        print(f"❌ User approval failed: {response.status_code} {response.text}")


def test_approve_product(token, product_id):
    url = f"{BASE_URL}products/{product_id}/approve/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"is_approved": True}
    print(f"Testing approve product for product_id={product_id} with data={data}")
    response = requests.patch(url, json=data, headers=headers)
    try:
        print(f"Product approval: {response.status_code} {response.json()}")
    except ValueError as e:
        print(f"❌ Product approval failed: {response.status_code} {response.text}")


def test_update_transaction_status(token, transaction_id, status):
    url = f"{BASE_URL}transactions/{transaction_id}/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"status": status}
    print(f"Testing transaction status update for transaction_id={transaction_id} with data={data}")
    response = requests.patch(url, json=data, headers=headers)
    try:
        print(f"Transaction status update: {response.status_code} {response.json()}")
    except ValueError as e:
        print(f"❌ Transaction status update failed: {response.status_code} {response.text}")


if __name__ == "__main__":
    # 准备测试数据
    setup_test_data()

    token = get_admin_token(ADMIN_USERNAME, ADMIN_PASSWORD)
    if token:
        # 获取 admin 用户的 id
        admin_user = User.objects.get(username='admin')
        test_approve_user(token, user_id=admin_user.id)

        # 获取产品的 id
        test_product = Product.objects.get(name="Test Product")
        test_approve_product(token, product_id=test_product.id)

        # 获取交易的 id
        test_transaction = Transaction.objects.get(status="pending")
        test_update_transaction_status(token, transaction_id=test_transaction.id, status="shipped")
    else:
        print("❌ Token retrieval failed, tests aborted!")