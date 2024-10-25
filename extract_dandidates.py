import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

# 出力するCSVファイルのパス
output_csv = r"C:\candidates\candidates.csv"

# CSVのヘッダー
headers = [
    "Party", "Name_Kana", "Name_Kanji", "Status", "Age",
    "Election_Count", "Profession", "Constituency", "Image_URL", "Profile_URL"
]

# ベースURL
BASE_URL = "https://www.nhk.or.jp/senkyo/database/shugiin/party_list/"

# 対象のHTMLファイルリスト
html_files = [
    "list1.html", "list195.html", "list187.html", "list3.html",
    "list4.html", "list197.html", "list212.html", "list5.html",
    "list227.html", "list243.html", "list245.html", "list29.html",
    "list-1.html"
]

# WebDriverのオプション設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # ヘッドレスモード（ブラウザを表示しない）
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# WebDriverのサービスを開始（webdriver-managerを使用）
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# CSVファイルを書き込みモードで開く（Shift_JISエンコーディング）
with open(output_csv, mode='w', encoding='cp932', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # ヘッダーを書き込む

    # 各HTMLファイルを処理
    for html_file in html_files:
        url = BASE_URL + html_file
        print(f"Processing URL: {url}")  # デバッグ用出力
        try:
            driver.get(url)
            time.sleep(3)  # ページが完全にロードされるまで待機（必要に応じて調整）
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue  # 次のファイルに進む

        # Seleniumで要素を取得
        try:
            candidates = driver.find_elements(By.CLASS_NAME, "partylist-candidate")
            print(f"Found {len(candidates)} candidates in {html_file}")  # デバッグ用出力
        except Exception as e:
            print(f"Error finding candidates in {url}: {e}")
            continue

        for candidate in candidates:
            try:
                # パーティ名
                party = candidate.find_element(By.CLASS_NAME, "partylist-candidate__prtyNm").text.strip()
                print(f"Party: {party}")  # デバッグ用出力

                # 名前（カナ）
                name_kana = candidate.find_element(By.CLASS_NAME, "partylist-candidate__khNmKana").text.strip()
                print(f"Name Kana: {name_kana}")  # デバッグ用出力

                # 名前（漢字）
                name_kanji = candidate.find_element(By.CLASS_NAME, "partylist-candidate__khNmKnj").text.strip()
                print(f"Name Kanji: {name_kanji}")  # デバッグ用出力

                # ステータス（例: 新, 前）
                try:
                    status = candidate.find_element(By.CLASS_NAME, "partylist-candidate__zmsk").text.strip()
                except:
                    status = ""
                print(f"Status: {status}")  # デバッグ用出力

                # 年齢
                try:
                    age = candidate.find_element(By.CLASS_NAME, "partylist-candidate__age").text.strip()
                except:
                    age = ""
                print(f"Age: {age}")  # デバッグ用出力

                # 当選回数（存在する場合）
                try:
                    election_count = candidate.find_element(By.CLASS_NAME, "partylist-candidate__tsKaisu").text.strip()
                except:
                    election_count = ""
                print(f"Election Count: {election_count}")  # デバッグ用出力

                # 職業
                try:
                    prof = candidate.find_element(By.CLASS_NAME, "partylist-candidate__prof").text.strip()
                except:
                    prof = ""
                print(f"Profession: {prof}")  # デバッグ用出力

                # 選挙区
                try:
                    constituency_element = candidate.find_element(By.CLASS_NAME, "partylist-candidate__senk")
                    # <br class="sp-only"> をスペースに置き換える
                    constituency_html = constituency_element.get_attribute('innerHTML').replace('<br class="sp-only">', ' ').strip()
                    constituency = BeautifulSoup(constituency_html, 'html.parser').get_text(separator=" ", strip=True)
                except:
                    constituency = ""
                print(f"Constituency: {constituency}")  # デバッグ用出力

                # 画像URL（フルURLに変換）
                try:
                    img_src = candidate.find_element(By.TAG_NAME, "img").get_attribute("src")
                    image_url = img_src if img_src.startswith("http") else "https://www.nhk.or.jp" + img_src
                except:
                    image_url = ""
                print(f"Image URL: {image_url}")  # デバッグ用出力

                # プロフィールURL（フルURLに変換）
                try:
                    profile_href = candidate.find_element(By.CLASS_NAME, "partylist-candidate__senk").get_attribute("href")
                    profile_url = profile_href if profile_href.startswith("http") else "https://www.nhk.or.jp" + profile_href
                except:
                    profile_url = ""
                print(f"Profile URL: {profile_url}")  # デバッグ用出力

                # CSVに書き込む行
                row = [
                    party,
                    name_kana,
                    name_kanji,
                    status,
                    age,
                    election_count,
                    prof,
                    constituency,
                    image_url,
                    profile_url
                ]

                writer.writerow(row)

            except Exception as e:
                print(f"Error parsing candidate in {url}: {e}")
                continue  # 次の候補者に進む

print(f"データの抽出が完了しました。出力ファイル: {output_csv}")

# WebDriverを閉じる
driver.quit()
