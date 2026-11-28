import copy

from ..services.oss import StorageService


def resolve_messages_urls(messages: list) -> list[dict]:
    new_messages = []

    for msg in messages:
        content = copy.deepcopy(msg.content)

        if isinstance(content, list):
            for item in content:
                if item.get("type") != "image_url":
                    continue

                item["image_url"]["url"] = StorageService.get_cached_url(
                    item["image_url"]["url"]
                )

        new_messages.append({
            "role": msg.role,
            "content": content,
        })

    return new_messages
