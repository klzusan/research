# 同一URL内での重複なしログを作成

import os

def main():
    merged_files, input_dir, output_dir = dir_init()

    for merged_file in merged_files:
        input_file_path = os.path.join(input_dir, merged_file)
        print(f"Processing {merged_file}")

        logs_with_dup = input_withDupFile(input_file_path)

        parse_and_output_dup(merged_file, logs_with_dup, output_dir)

def dir_init():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    root = os.path.dirname(parent_dir)
    input_dir = os.path.join(parent_dir, "merged_log", "with_dup")
    merged_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith("all.txt")]
    os.makedirs(f"{parent_dir}/merged_log/no_dup", exist_ok=True)
    output_dir = os.path.join(parent_dir, "merged_log", "no_dup")

    return merged_files, input_dir, output_dir

def input_withDupFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines

# 重複を解析し，重複のないログを出力
def parse_and_output_dup(input_file_name, logs_with_dup, output_dir):
    fileName = input_file_name.replace("_all", "_ndup")
    outPath = os.path.join(output_dir, fileName)

    i = 0
    logs_no_dup = []

    with open(outPath, 'w', encoding='utf-8') as outFile:
        while i < len(logs_with_dup):
            line = logs_with_dup[i]

            if line.startswith("URL: "):
                # 重複確認用のリストを初期化
                err_mesgs = []
                war_mesgs = []

                outFile.write(line)
                i += 1
                line = logs_with_dup[i]
                outFile.write(line) # Catを出力

                # Errを出力
                i += 1
                line = logs_with_dup[i]
                outFile.write(line)
                i += 1
                line = logs_with_dup[i]
                while line.startswith("(Err)"):
                    if line not in err_mesgs:
                        err_mesgs.append(line)
                        outFile.write(line)
                    i += 1
                    line = logs_with_dup[i]

                # Warを出力
                outFile.write(line)
                i += 1
                line = logs_with_dup[i]
                while line.startswith("(War)"):
                    if line not in war_mesgs:
                        war_mesgs.append(line)
                        outFile.write(line)
                    i += 1
                    line = logs_with_dup[i]

            if line.strip() == "":
                outFile.write(line)

            i += 1

if __name__ == "__main__":
    main()