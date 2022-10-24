from constants import HEADER_LEN
def pad(text: str) -> str:
    return text+(HEADER_LEN-len(text))*"\0"
