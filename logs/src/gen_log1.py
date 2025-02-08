# 重複ありログを生成

import os
import re

def main():
    browsers = ['chrome', 'edge', 'firefox']
    
    for browser in browsers:
        print(browser)

        input_folder, output_file , url_file = dir_init(browser)
        print(f"input: {input_folder}, output: {output_file}")

        merge_logs(input_folder, output_file, url_file, browser)

    print("Completed.")

        

# ディレクトリ関連初期設定
def dir_init(browser):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    root = os.path.dirname(parent_dir)
    input_folder = os.path.join(parent_dir, browser, "raw")
    os.makedirs(f"{parent_dir}/merged_log/with_dup", exist_ok=True)
    output_file_name = os.path.join(parent_dir, "merged_log", "with_dup", f"{browser}_merged_all.txt")
    url_file = os.path.join(root, "category.txt")

    return input_folder, output_file_name, url_file

# ファイルをマージ
def merge_logs(input_folder, output_file, url_file, browser):
    try:
        # URLとカテゴリの辞書を作成
        url_to_category = {}
        with open(url_file, 'r', encoding='utf-8') as urls:
            lines = urls.readlines()
            for i in range(0, len(lines), 3):  # 3行ごとに処理
                if lines[i].startswith("URL:") and lines[i+1].startswith("Category:"):
                    url = lines[i].strip().replace("URL:", "").strip()
                    category = lines[i+1].strip().replace("Category:", "").strip()
                    url_to_category[url] = category

        # 重複ありログファイルの生成
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filename in sorted(os.listdir(input_folder)):
                if filename.endswith('.txt'):
                    # ファイル名からURLを取得
                    url = filename.replace('.txt', '')
                    print(f"Processing {url}...")

                    # URLを出力
                    outfile.write(f"URL: {url}\n")

                    # カテゴリを出力
                    category = url_to_category.get(url, "Unknown Category")
                    outfile.write(f"Cat: {category}\n")

                    # 個別のrawファイルから内容を読み取りlineに記憶
                    file_path = os.path.join(input_folder, filename)
                    lines = input_rawFile(file_path)

                    # エラーログを抽出
                    type = "error"
                    outfile.write("Err:\n")
                    if browser == "chrome":
                        error_logs = parse_lines(lines, type)
                    elif browser == "edge":
                        error_logs = parse_lines(lines, type)
                    elif browser == "firefox":
                        error_logs = parse_firefox(lines, type)

                    # エラーログからメッセージを抽出
                    if browser == "chrome":
                        error_mesgs = get_text(error_logs)
                    elif browser == "edge":
                        error_mesgs = get_text(error_logs)
                    elif browser == "firefox":
                        error_mesgs = get_text_firefox(error_logs)

                    # 書き出し
                    for single_mesg in error_mesgs:
                        outfile.write("(Err)")
                        outfile.write(single_mesg)

                    # ワーニングログを抽出
                    type = "warning"
                    outfile.write("War:\n")
                    if browser == "chrome":
                        warning_logs = parse_lines(lines, type)
                    elif browser == "edge":
                        warning_logs = parse_lines(lines, type)
                    elif browser == "firefox":
                        warning_logs = parse_firefox(lines, type)

                    # ワーニングログからメッセージを抽出
                    if browser == "chrome":
                        warning_mesgs = get_text(warning_logs)
                    elif browser == "edge":
                        warning_mesgs = get_text(warning_logs)
                    elif browser == "firefox":
                        warning_mesgs = get_text_firefox(warning_logs)

                    # 書き出し
                    for single_mesg in warning_mesgs:
                        outfile.write("(War)")
                        outfile.write(single_mesg)

                    outfile.write("\n")


    except Exception as e:
        print(f"An error occurred: {e}")

# rawファイルを読み込み，その内容を返す
def input_rawFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines

# ログを解析し，typeが一致すればlogsとして保存 (chrome, edge)
def parse_lines(lines, type):
    i = 0
    debug_msg = 0
    single_log = []
    logs = []
    while i < len(lines):
        line = lines[i]

        if "[DEBUG]" in line and "{" in line and get_indent_lev(line) == 0:
            # start of mesg
            single_log = []
            debug_msg = 1
        elif debug_msg == 1 and "}" in line and get_indent_lev(line) == 0:
            # end of mesg
            single_log.append(line)
            # single_log.append("\n")
            j = 0
            while j < len(single_log):
                if type == "error":
                    if "\"level\": \"error\"" in single_log[j]:
                        logs.append(single_log)
                        break
                elif type == "warning":
                    if "\"level\": \"warning\"" in single_log[j]:
                        logs.append(single_log)
                        break
                j += 1
            debug_msg = 0
        elif get_indent_lev(line) == 0:
            # other mesg
            debug_msg = 0

        if debug_msg == 1:
            # single_logに一行追加
            single_log.append(line)
            
        i += 1

    return logs

# ログを解析し，typeが一致すればlogsとして保存 (firefox)
def parse_firefox(lines, type):
    logs = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if type == "error":
            if ("console." in line and "error" in line) or ("JavaScript " in line and "error" in line):
                logs.append(line)
                logs.append("\n")
        elif type == "warning":
            if ("console." in line and "warn" in line) or ("JavaScript " in line and "warning" in line):
                logs.append(line)
                logs.append("\n")

        i += 1

    return logs

# ログからテキストのみを抽出（chrome, edge）
def get_text(logs_of_a_browser):
    i = 0
    error_mesgs = []

    while i < len(logs_of_a_browser):
        lines = logs_of_a_browser[i]
        for line in lines:

            if "\"text\":" in line:
                text = line.lstrip(" ").replace("\"text\": \"", "").replace("\",\n", "\n")
                mesg = re.sub(r"http[s]?://[^\s']+", "REPLACED_URL", text)
                error_mesgs.append(mesg)

        i += 1

    return error_mesgs

# ログからテキストのみを抽出（firefox）
def get_text_firefox(logs_of_a_browser):
    i = 0
    error_mesgs = []
    while i < len(logs_of_a_browser):
        line = logs_of_a_browser[i]

        if "error: " in line or "warn" in line:
            if line.startswith("console.error: "):
                text = line.replace("console.error: ", "")
            elif line.startswith("console.warn: "):
                text = line.replace("console.warn: ", "")
            elif line.startswith("JavaScript error: "):
                text = line.replace("JavaScript error: ", "")
            elif line.startswith("JavaScript warning: "):
                text = line.replace("JavaScript warning: ", "")

            temp = re.sub(r'^.*?: ', '', text)
            mesg = re.sub(r"http[s]?://[^\s']+", "REPLACED_URL", temp)
            error_mesgs.append(mesg)

        i += 1

    return error_mesgs

# 引数の種類のメッセージかどうかを判定
# def check_mesgType(type):

# 渡された行のインデントレベルを返す
def get_indent_lev(line):
    return len(line) - len(line.lstrip())

if __name__ == "__main__":
    main()