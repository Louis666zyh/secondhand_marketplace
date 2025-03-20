import pydot
from django.apps import apps
import os

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondhand_marketplace.settings')
import django
django.setup()

# 创建Graphviz图
graph = pydot.Dot(graph_type='digraph', rankdir='TP', fontsize='10')

# 获取所有模型
models = apps.get_models()

# 存储已经处理过的表，避免重复
processed_tables = set()

# 遍历所有模型，添加节点（表）
for model in models:
    table_name = model._meta.db_table
    if table_name in processed_tables:
        continue
    processed_tables.add(table_name)

    # 构建表的标签，包含字段信息
    label = f"{{ {table_name} |"
    fields = model._meta.get_fields()
    for field in fields:
        if not field.is_relation:  # 只显示非关系字段
            field_type = field.get_internal_type()
            label += f"{field.name}: {field_type}\\l"
    label += "}"

    # 创建节点
    node = pydot.Node(table_name, label=label, shape="record", style="filled", fillcolor="lightgrey")
    graph.add_node(node)

# 遍历模型，添加边（关系）
for model in models:
    table_name = model._meta.db_table
    for field in model._meta.get_fields():
        # 检查外键或多对多关系
        if field.is_relation and field.related_model:
            related_table = field.related_model._meta.db_table
            # 创建边，标注关系类型
            if field.many_to_many:
                edge_label = "many-to-many"
            elif field.one_to_one:
                edge_label = "one-to-one"
            else:
                edge_label = "one-to-many"
            edge = pydot.Edge(table_name, related_table, label=edge_label, color="blue")
            graph.add_edge(edge)

# 保存ER图为PNG文件
output_file = "er_diagram.png"
graph.write_png(output_file)
print(f"ER图已生成：{output_file}")