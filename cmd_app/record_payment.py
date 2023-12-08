from .utils import intro_and_choose_account

def record_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Awesome. Let's record a payment.")
    return True
