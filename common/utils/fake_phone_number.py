import random


def fake_phone_number():
    code = "+37529"
    random_number = ''.join([str(num) for num in random.sample(range(0, 10), 7)])
    return f"{code}{random_number}"
