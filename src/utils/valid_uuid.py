import uuid


def is_valid_uuid(uuid_str: str) -> bool:
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False
