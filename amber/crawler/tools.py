
# smbc entry types
SMBC_FILE = 8L
SMBC_DIR = 7L
SMBC_SERVICE = 3L

def item_type(entry):
    return 'file' if entry.smbc_type == SMBC_FILE else 'dir'

def is_service(entry):
    return entry.smbc_type == SMBC_SERVICE


def percent_encode(string):
    encode_table = {
                    '!': '%21',
                    '&': '%26',
                    '?': '%3F',
                    '%': '%25',
                    '~': '%7E',
                    '[': '%5B',
                    ']': '%5D',
                   }
    result = ''
    for i in range(len(string)):
        if string[i] in encode_table:
            result += encode_table[string[i]]
        else:
            result += string[i]
    return result



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
