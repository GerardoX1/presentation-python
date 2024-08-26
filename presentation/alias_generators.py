def to_camel(string):
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def dict_to_camel(dictionary):
    result = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            value = dict_to_camel(value)
        words = key.split("_")
        key = words[0] + "".join(word.capitalize() for word in words[1:])
        result[key] = value
    return result
