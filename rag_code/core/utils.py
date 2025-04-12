import os, json, re


ENCODING = "UTF-8"
WRITE_JSON_PATTERN = r'\[\n\s+([-0-9eE\.,\s]+)\n\s+\]'


def file_exists(file_path: str) :
    if file_path == None or len(file_path) == 0 :
        return False

    if os.path.exists(file_path) and os.path.isfile(file_path) :
        return True

    return False


def make_parent(file_path: str) :
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def file_open(file_path: str, encoding=ENCODING, mode='r') :
    if mode.find('w') != -1 or mode.find('a') != -1 :
        make_parent(file_path)
    
    return open(file_path, mode, encoding=encoding)


def load_json_file_to_dict(in_file_path: str, encoding=ENCODING) :
    try :
        if file_exists(in_file_path) :
            file = file_open(in_file_path, encoding, 'r')

            # 파일을 읽을 때는, load() 호출
            json_dict = json.load(file)

            return json_dict

    except Exception as e :
        print("### error utils.load_json_file_to_dict()", e)
        return None

    return None


def write_json_file(input, out_file_path: str, encoding=ENCODING) :
    try :
        json_str = json_to_str(input)
        json_str = re.sub(WRITE_JSON_PATTERN, lambda m: "[" + " ".join(m.group(1).split()) + "]", json_str)

        file = file_open(out_file_path, encoding, 'w')
        file.write(json_str)
        file.close()

        print(f'utils.write_json_file() out_file_path : {out_file_path}, data size : {len(input)}')
        return True

    except Exception as e :
        print("### error utils.write_json_file()", e)
        return False


def json_to_str(input, indent=4) :
    try :
        return json.dumps(input, ensure_ascii=False, indent=indent)

    except Exception as e :
        print("### error utils.json_to_str()", e)
        return ""


def add_str_list_int(in_dict: dict, key_list: list, value: int) :
    if in_dict != None :
        for i in range(len(key_list)) :
            key = str(key_list[i])
            add_str_int(in_dict, key, value)


def add_str_int(in_dict: dict, key: str, value: int) :
    if in_dict != None :
        if key in in_dict :
            value_prev = int(in_dict[key])
            in_dict[key] = value_prev + value
        else :
            in_dict[key] = value


'''
    key를 기준으로 정렬
        - is_reverse = False : 오름 차순
        - is_reverse = True : 내림 차순
'''
def sorted_dict_key(in_dict: dict, is_reverse=False) :
    return dict(sorted(in_dict.items(), key=lambda item:item[0], reverse=is_reverse))

'''
    value를 기준으로 정렬
        - is_reverse = False : 오름 차순
        - is_reverse = True : 내림 차순
'''
def sorted_dict_value(in_dict: dict, is_reverse=False) :
    return dict(sorted(in_dict.items(), key=lambda item:item[1], reverse=is_reverse))

'''
    key를 기준으로 오름 차순 정렬, value를 기준으로 내림 차순 정렬
'''
def sorted_dict(in_dict: dict) :
    return sorted_dict_value(sorted_dict_key(in_dict, False), True)