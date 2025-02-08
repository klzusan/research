# URL関係なしの重複なしログを作成

import os

# 重複なしログリスト
err_logs = []
war_logs = []

def main():
    merged_files, input_dir, output_dir = dir_init()

    for merged_file in merged_files:
        input_file_path = os.path.join(input_dir, merged_file)
        print(f"Processing {merged_file}")

        logs_with_dup = input_withDupFile(input_file_path)

        get_only_mesg(logs_with_dup)

    output_mesgFile(output_dir)

    

def dir_init():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    root = os.path.dirname(parent_dir)
    input_dir = os.path.join(parent_dir, "merged_log", "with_dup")
    merged_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith("all.txt")]
    os.makedirs(f"{parent_dir}/merged_log/only_mesg", exist_ok=True)
    output_dir = os.path.join(parent_dir, "merged_log", "only_mesg")

    return merged_files, input_dir, output_dir

def input_withDupFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines

# 重複なしログを生成
def get_only_mesg(logs_with_dup):
    i = 0
    while i < len(logs_with_dup):
        line = logs_with_dup[i]

        if line.startswith("(Err)"):
            if line not in err_logs:
                err_logs.append(line)
        elif line.startswith("(War)"):
            if line not in war_logs:
                war_logs.append(line)

        i += 1

# only_err.txtとonly_war.txtを出力
def output_mesgFile(output_dir):
    errPath = os.path.join(output_dir, "only_err.txt")
    warPath = os.path.join(output_dir, "only_war.txt")

    # only_err.txtを出力
    with open(errPath, 'w', encoding='utf-8') as errFile:
        for single_log in sorted(err_logs):
            errFile.write(single_log)

    # only_war.txtを出力
    with open(warPath, 'w', encoding='utf-8') as warFile:
        for single_log in sorted(war_logs):
            warFile.write(single_log)

if __name__ == "__main__":
    main()