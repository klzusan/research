import os, re

# リストインデックス
CAT = 0
NUM = 1
NET = 2
JAV = 3
SEC = 4
PER = 5
DEP = 6
OTH = 7
UNK = 8

def main():
    page_cat_path, mes_cat_path, with_dup_path = dir_init()

    page_cat_ori = input_text(page_cat_path)
    mes_cat_ori = input_text(mes_cat_path)
    files = get_allFilesName(with_dup_path, "all.txt")

    # 3つのブラウザのコンソールログテキストを読み込む
    log = [] # [debug message, log_text]
    for f in files:
        temp = [f"DEBUG: {f} below.\n"]
        log_path = os.path.join(with_dup_path, f)
        log_text = input_text(log_path)
        temp.append(log_text)
        log.append(temp)

    page_cat, mes_cat, mesgs = ex_cat(page_cat_ori, mes_cat_ori)

    list = count(page_cat, mes_cat, log, mesgs)

    print_res(list)

def get_allFilesName(path, end=None):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (end is None or f.endswith(end))]

    return files

def dir_init():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src
    parent_dir = os.path.dirname(current_dir) # logs
    root = os.path.dirname(parent_dir) # research

    page_cat_path = os.path.join(root, "category.txt")
    mes_cat_path = os.path.join(parent_dir, "merged_log", "only_mesg", "err_cat.txt")
    with_dup_path = os.path.join(parent_dir, "merged_log", "with_dup")

    return page_cat_path, mes_cat_path, with_dup_path

def input_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines

def print_res(list):
    i = 0
    while i < len(list):
        print(f"Category: {list[i][CAT]}", end="")
        print(f": {list[i][NUM]} * 3 pages")
        print(f"NET: {list[i][NET]}", end=", ")
        print(f"JAV: {list[i][JAV]}", end=", ")
        print(f"SEC: {list[i][SEC]}", end=", ")
        print(f"PER: {list[i][PER]}", end=", ")
        print(f"DUP: {list[i][DEP]}", end=", ")
        print(f"OTH: {list[i][OTH]}", end=", ")
        print(f"unk: {list[i][UNK]}")

        print()
        i += 1


def ex_cat(page_cat_ori, mes_cat_ori):
    page_cat = []
    for line in page_cat_ori:
        if "CAT:" in line:
            temp = line[4:]
            cat_kind = temp.replace("\n", "")
            if not any(cat_kind == item[0] for item in page_cat):
                page_cat.append([cat_kind, 1])
            else:
                for item in page_cat:
                    if item[0] == cat_kind:
                        item[1] += 1
                        break

    mesgs = [] # [[mes, cat]]
    mes_cat = [] # [cat]
    i = 0
    while i < len(mes_cat_ori):
        line = mes_cat_ori[i]
        
        if "MES: " in line:
            mes = line[5:]
            i += 1
            line = mes_cat_ori[i]
            temp = line[5:]
            cat_kind = temp.replace("\n", "")
            mesgs.append([mes, cat_kind])

            temp = cat_kind.replace("\n", "")
            if temp not in mes_cat:
                mes_cat.append(temp)

        i += 1

    page_cat.sort()
    mes_cat.sort()
    mesgs.sort()

    return page_cat, mes_cat, mesgs

def count(page_cat, mes_cat, log, mesgs):
    # mesgs: [[message, error type]]
    
    list = [] # [page_cat, page_cat_num, Network, JavaScript, Security, Performance, Deplication, Other, unknown]
    for pc in page_cat:
        if not any(pc[CAT] == item[CAT] for item in list):
            pc_temp = pc + [0, 0, 0, 0, 0, 0, 0]
            list.append(pc_temp)

    # カウント
    i = 0 # ブラウザインデックス
    while i < len(log):
        deb = log[i][0]
        mes = log[i][1]
        j = 0 # ログラインインデックス

        while j < len(mes):
            # 各ブラウザのall.txtを走査
            log_line = mes[j]
            if log_line.startswith("URL:"):
                url = log_line[5:].replace("\n", "")
                j += 1
                log_line = mes[j]
                cat_of_url = log_line[5:].replace("\n", "")
                j += 1
                log_line = mes[j]

                while log_line.strip() != "":
                    for m in mesgs:
                        # 注目しているログメッセージをログ集から見つけたとき
                        if log_line.replace("\n", "") == m[0].replace("\n", ""):
                            # cat_of_urlと一致するpage_catであるlistのm[1]のタイプのカウントをインクリメント
                            cat_of_mes = m[1].replace("\n", "")
                            if cat_of_mes == "Network Error":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[NET] += 1
                            elif cat_of_mes == "JavaScript Error":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[JAV] += 1
                            elif cat_of_mes == "Security Error":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[SEC] += 1
                            elif cat_of_mes == "Performance Warn":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[PER] += 1
                            elif cat_of_mes == "Deprecation Warn":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[DEP] += 1
                            elif cat_of_mes == "Other":
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[OTH] += 1
                            else:
                                for l in list:
                                    if l[CAT] == cat_of_url:
                                        l[UNK] += 1
                            break

                    j += 1
                    log_line = mes[j]


            j += 1

        i += 1

    return list
    
    

if __name__ == "__main__":
    main()