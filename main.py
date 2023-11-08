import requests
import json
import functions_framework


def dict_to_yaml(d, indent=0):
    yaml_str = ""
    for key, value in d.items():
        yaml_str += ' ' * indent + f' *{str(key)}*' + ": "
        if isinstance(value, dict):
            yaml_str += "\n" + dict_to_yaml(value, indent+2)
        elif isinstance(value, list):
            yaml_str += "\n"
            for item in value:
                yaml_str += ' ' * (indent+2) + "- " + str(item) + "\n"
        else:
            yaml_str += str(value) + "\n"
    return yaml_str


def format_payload(payload, indent=0):
    lines = []
    indent_str = ' ' * indent
    if isinstance(payload, dict):
        for key, value in payload.items():
            lines.append(f'{indent_str}*{key}*:')
            if isinstance(value, dict):
                lines.extend(format_payload(value, indent + 4))
            elif isinstance(value, list):
                lines.extend(format_payload(value, indent + 4))
            else:
                lines.append(f'{indent_str}  {value}')
    elif isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                for subkey, subvalue in item.items():
                    lines.append(f'{indent_str}  - *{subkey}*: {subvalue}')
            else:
                lines.append(f'{indent_str}- {item}')
    else:
        lines.append(f'{indent_str}{payload}')
    return '\n'.join(lines)

def send_to_chat(message, chat_webhook_url):
    headers = {'Content-type': 'application/json'}
    data = {"text": message}
    response = requests.post(chat_webhook_url, headers=headers, data=json.dumps(data))
    return response

@functions_framework.http
def process_notification(request):
    data = request.get_json()
    chat_webhook_url = request.args.get('chat_webhook_url')

    if not chat_webhook_url:
        return "No chat_webhook_url provided", 400

    message = formatted_message = dict_to_yaml(data)
    response = send_to_chat(message, chat_webhook_url)

    return f"Message sent to Google Chats with status code: {response.status_code}"
