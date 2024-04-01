def parse_mindmap(data, parent_id='', node_count=[0]):
    """
    递归解析简化的思维导图 JSON 数据，为每个节点添加唯一的 id。
    使用单元素列表 node_count 作为可变对象以在递归调用中保持状态。

    :param data: 包含标签和子节点的字典。
    :param parent_id: 父节点的 id，用于构建当前节点的唯一 id。
    :param node_count: 用于生成唯一 id 的计数器，以列表形式传递以在递归调用中保持更新。
    :return: 解析后的节点数据，包含为每个节点分配的唯一 id。
    """
    # 如果是字典，处理单个节点
    if isinstance(data, dict):
        # 构建节点的唯一 id
        node_id = f"{parent_id}-{node_count[0]}" if parent_id else str(node_count[0])
        data['id'] = node_id
        node_count[0] += 1

        # 如果有子节点，递归处理子节点
        if 'children' in data:
            children = data['children']
            for child in children:
                parse_mindmap(child, node_id, node_count)
    return data

