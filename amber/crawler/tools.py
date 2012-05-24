


def get_name(path):
    return os.path.split(path)[1]

def get_extension(path):
    split = get_name(path).split('.')
    if len(split) > 1: return split[-1].lower()


def get_unic_id(path, size, change_time):
    name = get_name(path)
    unic_str = name + u':' + str(size) + ':' + change_time.isoformat()
    bin_string = hashlib.md5(unic_str.encode('utf8')).digest()
    return binary.Binary(bin_string, binary.MD5_SUBTYPE)
