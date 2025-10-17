import json

# some JSON
json_data = '{"name": "Luc Do", "age": 26, "city": "Ho Chi Minh"}'

data = json.loads(json_data)
age = data["age"]
name = data["name"]
city = data["city"]

print(f"Name: {name}, Age: {age}, City: {city}")
