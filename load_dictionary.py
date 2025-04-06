import aho_corasick
import requests
import io
import pandas as pd
import zipfile
import os

class Dictionary:
	def __init__(self):
		pass

	def normalize(self, string):
		if len(string) == 0:
			return []
		
		result = []
		for i in range(len(string)):
			char = string[i]
			# カタカナの範囲内かチェック
			if 'ァ' <= char <= 'ヿ':
				if char == "ヲ":
					result.append("オ")
				elif char == "・":
					continue  # スキップ
				elif char == "ヿ":
					result.append("コ")
					result.append("ト")
				else:
					result.append(char)
			else:
				# 処理の流れを中断せずに警告だけ表示
				print(f"想定していない文字: {string} の '{char}'")
		
		return result
	
	def download_sudachi(self, type="small"):
		match type:
			case "small":
				url = "http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict-raw/20250129/small_lex.zip"
				csv_path = "./data/small_lex.csv"
			case _:
				print("error")
				return
		
		# CSVファイルがすでに存在するか確認
		if os.path.exists(csv_path):
			print(f"{csv_path}はすでに存在します。ダウンロードをスキップします。")
			return
			
		# データディレクトリが存在しない場合は作成
		os.makedirs("./data", exist_ok=True)
		
		res = requests.get(url).content
		bytes_io = io.BytesIO(res)
		zip = zipfile.ZipFile(bytes_io)
		zip.extractall("./data/")
		print("辞書ファイルをダウンロードして解凍しました。")
	
	def load_dictionary(self, type="small"):
		import time
		
		match type:
			case "small":
				csv_path = "./data/small_lex.csv"
			case _:
				print("error")
				return
		
		if not os.path.exists(csv_path):
			print(f"{csv_path}が存在しません。辞書をダウンロードしてください。")
			return

		dictionary = aho_corasick.ACAutomaton()
		df = pd.read_csv(csv_path, encoding="utf-8", header=None)
		
		# 処理開始時間を記録
		start_time = time.time()
		total_items = len(df)
		print(f"辞書データの読み込みを開始します。合計 {total_items} 件のエントリを処理します。")
		
		for i in range(total_items):
			word = df.iloc[i][0]
			kana = self.normalize(list(df.iloc[i][11]))
			if kana:  # 空のリストでないことを確認
				dictionary.add(kana, word)
			
			# 1000件ごとに進捗を表示
			if (i + 1) % 1000 == 0 or i + 1 == total_items:
				elapsed_time = time.time() - start_time
				progress_percent = (i + 1) / total_items * 100
				print(f"進捗: {i + 1}/{total_items} ({progress_percent:.1f}%) 経過時間: {elapsed_time:.1f}秒")
				
		# 処理完了時間と合計所要時間を表示
		total_time = time.time() - start_time
		print(f"辞書データの処理が完了しました。所要時間: {total_time:.1f}秒")
		
		dictionary.set_failure_path()
		print("辞書を読み込みました。")
		return dictionary

if __name__ == "__main__":
	dic = Dictionary()
	dic.load_dictionary()