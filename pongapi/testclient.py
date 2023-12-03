import requests


resp = requests.get('http://localhost:5000/ping')
print (resp.status_code)
print(resp)


post_resp = requests.post('http://localhost:5000/ping', json={'name': 'joe', 'age': 30}
						  )


print(post_resp)