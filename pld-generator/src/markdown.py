def title(string, priority=1, prefix=""):
    return f"{prefix}{'#' * priority} {string}" + string 

def dotted_list(array: list):
    return '\n'.join([f"- {elem}" for elem in array])

def citation(string):
    return f"> {string}"

def bold(string):
    return f"**{string}**"
