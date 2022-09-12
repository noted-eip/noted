def title(string:str, priority:int = 1, prefix:str = "") -> str:
    return f"{prefix}{'#' * priority} {string}" 

def dotted_list(array:list) -> str:
    return '\n'.join([f"- {elem}" for elem in array])

def unchecked_list(array:list) -> str:
    return '\n'.join([f"- [ ] {elem}" for elem in array])

def citation(string:str) -> str:
    return f"> {string}"

def bold(string:str) -> str:
    return f"**{string}**"

def separator() -> str:
    return '---'

