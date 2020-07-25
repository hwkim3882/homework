professor_wizards = [
    {'name': '덤블도어', 'age': 116},
    {'name': '맥고나걸', 'age': 85},
    {'name': '스네이프', 'age': 60},
]

def get_age(name, wizards):
    for wizard in wizards:
        if wizard['name'] == name:
            return wizard['age']
    return 'no name'

print(get_age('맥고나걸', professor_wizards))