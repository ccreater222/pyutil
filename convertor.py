
def cookie_str_to_setcookie(cookie_str: str)-> str:
    cookies = cookie_str.split("; ")
    result = ""
    for cookie in cookies:
        key, value = cookie.split("=")
        result += f"Set-Cookie: {key}={value}\r\n"
    return result