import uuid

def hex_uuid():
    id = uuid.uuid4()
    return id.hex