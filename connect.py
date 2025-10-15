import requests
import json

response = requests.get("https://jsonplaceholder.typicode.com/posts")

# Let's print the status code
print(response.status_code)  # 200 means success!

# Now, let's print the data
print(json.dumps(response.json(), indent=4))
