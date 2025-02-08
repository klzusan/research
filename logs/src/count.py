# メッセージの出現回数をカウント

import os

# リストインデックス
SUM = 0
CHR = 1
FIR = 2
EDG = 3
MES = 4

def main():
    only_mesg_dir, with_dup_dir, output_dir = dir_init()
    only_err, only_war = get_mesg_text(only_mesg_dir)

    # カウント用のリストを準備
    l_err = prepare_list(only_err)
    l_war = prepare_list(only_war)

    # 各メッセージの出現回数をカウント
    count(l_err, with_dup_dir)
    count(l_war, with_dup_dir)

    # リストを出力
    output(l_err, l_war, output_dir)
   

def dir_init():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src
    parent_dir = os.path.dirname(current_dir) # logs
    only_mesg_dir = os.path.join(parent_dir, "merged_log", "only_mesg") # input1
    with_dup_dir = os.path.join(parent_dir, "merged_log", "with_dup") # input2
    os.makedirs(f"{parent_dir}/merged_log/only_mesg", exist_ok=True)
    output_dir = os.path.join(parent_dir, "merged_log", "only_mesg")
    
    return only_mesg_dir, with_dup_dir, output_dir

def get_merged_fname(with_dup_dir):
    meregd_files = [f for f in os.listdir(with_dup_dir) if os.path.isfile(os.path.join(with_dup_dir, f)) and f.endswith("all.txt")]

    return meregd_files

def get_mesg_fname(only_mesg_dir):
    mesg_files = [f for f in os.listdir(only_mesg_dir) if os.path.isfile(os.path.join(only_mesg_dir, f)) and f.startswith("only_") and f.endswith(".txt")]

    return mesg_files

# merged_all.txtの内容を取得しリストとして返す
def get_merged_contents(with_dup_dir, merged_fname):
    contents = []
    path = os.path.join(with_dup_dir, merged_fname)
    with open(path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    return contents


def get_mesg_text(only_mesg_dir):
    only_err = []
    only_war = []
    for mesg_file in get_mesg_fname(only_mesg_dir):
        path = os.path.join(only_mesg_dir, mesg_file)

        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if mesg_file == "only_err.txt":
            only_err = lines
        elif mesg_file == "only_war.txt":
            only_war = lines

    return only_err, only_war

# [合計出現回数, chromeでの出現回数, firefoxでの出現回数, edgeでの出現回数, メッセージ,] の形のリストを作成
def prepare_list(mesgs):
    list = []
    for mesg in mesgs:
        list.append([0, 0, 0, 0, mesg])

    return list

# 各メッセージの出現回数をカウント
def count(list, with_dup_dir):
    merged_files = get_merged_fname(with_dup_dir)

    for file in merged_files:
        contents = get_merged_contents(with_dup_dir, file)

        for l in list:
            for c in contents:
                if l[MES] in c:
                    if "chrome" in file:
                        l[CHR] += 1
                    elif "firefox" in file:
                        l[FIR] += 1
                    elif "edge" in file:
                        l[EDG] += 1

    for l in list:
        l[SUM] = l[CHR] + l[FIR] + l[EDG]

# リストを出力
def output(l_err, l_war, output_dir):
    path_err = os.path.join(output_dir, "count_err.txt")
    path_war = os.path.join(output_dir, "count_war.txt")
    path = path_err, path_war
    for p in path:
        if "count_err.txt" in p:
            l_sorted = sorted(l_err, key=lambda x: (x[0], x[4]), reverse=True)
        elif "count_war.txt" in p:
            l_sorted = sorted(l_war, key=lambda x: (x[0], x[4]), reverse=True)

        with open(p, 'w', encoding='utf-8') as file:
            for L in l_sorted:
                print(L)
                i = 0
                for l in L:
                    match i:
                        case 0:
                            # 合計（SUM）の出力
                            file.write("[")
                            file.write(str(l))
                        case 1:
                            # 合計（CHR）の出力
                            file.write(", ")
                            file.write(str(l))
                        case 2:
                            # 合計（CHR）の出力
                            file.write(", ")
                            file.write(str(l))
                        case 3: 
                            # 合計（EDG）の出力
                            file.write(", ")
                            file.write(str(l))
                            file.write("] ")
                        case 4:
                            # メッセージの出力
                            file.write(l.rstrip("\n"))
                    i += 1

                file.write("\n")

if __name__ == "__main__":
    main()