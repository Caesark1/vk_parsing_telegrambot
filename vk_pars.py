import requests
import csv
from bs4 import BeautifulSoup as bs



def get_posts():
	token = "dfd15cc6dfd15cc6dfd15cc60adfa2703bddfd1dfd15cc680cbf567979b94961e37478b"
	version = 5.118
	global domain
	domain = input("Введите ссылку на группу(пример:yvkurse): ")
	#Если хотите сразу указать группу в переменную domain можете вместо инпута сразу указать группу пример: domain = "yvkurse"
	all_posts = []
	response = requests.get("https://api.vk.com/method/wall.get", params = {
																	"access_token": token,
																	"v": version,
																	"domain": domain,
																	"count": 100})
	data = response.json()["response"]["items"]
	all_posts.extend(data)
	return all_posts

def file_writter(data):
	with open(f"{domain}.csv", "w",encoding="UTF-8") as file:
		posts = csv.writer(file, delimiter = ";")
		posts.writerow(("text", "url"))
		for post in data:
			try:
				if post["attachments"][0]["type"] == "video":
					img_url = post["attachments"][0]["video"]["image"][-1]["url"]
				elif post["attachments"][0]["type"] == "link":
					img_url = post["attachments"][0]["link"]["photo"]["sizes"][-1]["url"]
				elif post["attachments"][0]["type"] == "photo":
					images = post["attachments"]
					list_image = []
					for image in images:
						list_image.append(image["photo"]["sizes"][-1]["url"])
					convert = str(list_image)
					img_url = convert.replace("[", "").replace("]", "")
				else:
					img_url = "No photo"
			except:
				pass
			posts.writerow((post["text"],img_url))

all_posts = get_posts()
file_writter(all_posts)

