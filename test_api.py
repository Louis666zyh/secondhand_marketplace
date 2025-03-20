# test_api.py
import os
import django
from django.core.files import File
from django.contrib.auth import get_user_model

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondhand_marketplace.settings')

# 配置 Django
django.setup()

# 获取 User 模型
User = get_user_model()

# 查找用户名为 Unitedkingdom 的用户
try:
    user = User.objects.get(username='Unitedkingdom')
    print(f"找到用户: {user.username}")
except User.DoesNotExist:
    print("用户 Unitedkingdom 不存在，请先创建该用户")
    exit()

# 头像文件的路径
avatar_path = r"C:\Users\Louis\Desktop\微信截图_20250320155940.png"

# 确保文件存在
if not os.path.exists(avatar_path):
    print(f"文件 {avatar_path} 不存在，请检查路径")
    exit()

# 打开文件并上传
with open(avatar_path, 'rb') as f:
    # 如果用户已有头像，先删除旧头像
    if user.avatar:
        user.avatar.delete(save=False)  # 删除旧文件，但不保存用户对象
        print("已删除旧头像")

    # 上传新头像
    user.avatar.save(
        os.path.basename(avatar_path),  # 文件名
        File(f),  # 文件对象
        save=True  # 保存用户对象
    )
    print(f"头像已上传，路径: {user.avatar.path}")
    print(f"头像 URL: {user.avatar.url}")