import aho_corasick
import requests
import io
import pandas as pd

class Dictionary:
	def __init__(self):
		pass

	def normalize(self, string):
		if len(string) == 0:
			return ""
		i = 0
		while i < len(string):
			if string[i] < "ァ" or string[i] > "ヿ":
				print("想定していない文字:", string)
				break
			match string[i]:
				case "ヲ":
					string[i] = "オ"
				case "・":
					del string[i]
				case "ヿ":
					string[i] = "コ"
					string.insert(i + 1, "ト")
					i += 1
	
	def download_sudachi(self, type="small"):
		match type:
			case "small":
				url = "http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict-raw/20250129/small_lex.zip"
			case _:
				print("error")
				return
		res = requests.get(url).content
		df = pd.read_csv(io.StringIO(res.decode("utf-8")), header=0, index_col=0)
			

if __name__ == "__main__":
	dictionary = aho_corasick.ACAutomaton()