import copy

from ..services.oss import StorageService


def resolve_messages_urls(messages: list):
    new_messages = copy.deepcopy(messages)

    for msg in new_messages:
        if isinstance(msg['content'], str):
            continue

        content = msg['content'][0]
        if content['type'] != 'image_url':
            continue

        content['image_url']['url'] = StorageService.create_presign(
            content['image_url']['url'])

    print(new_messages)

    return new_messages
