def filter_and_convert_to_intergers(data):
    return [int(x) for c in data if isinstance(x, (int, float))]
data=[1,2,3,'4','5','test',5.6]
filtered_integers=filter_and_convert_to_intergers(data)
print("Filterd integers: ",filtered_integers)