import json
import os
def reorder_and_update_json_fields(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Define the new order of fields
                new_data = {
                    'IsVisible': data.get('IsVisible'),
                    'Icon': data.get('Icon'),
                    'UsageDescription': data.get('UsageDescription'),
                    'ChinesePromptTemplate': data.get('ChinesePromptTemplate', ''),
                    'EnglishPromptTemplate': '',  # New field with empty string
                    'Inputs': data.get('Inputs')
                }

                # Write the updated data back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)

reorder_and_update_json_fields(directory='config/菜单配置')