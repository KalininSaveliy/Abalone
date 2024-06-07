import requests
import numpy as np


def check(cond, test_name):
    if cond:
        print(f"{test_name}\t OK")
    else:
        print(f"{test_name}\t Wrong")


def test_hello(url):
    response = requests.get(url + "/hello")
    check(response.text == "Hello there\n", "Hello test")


def test_bye(url):
    data = {"age": 17, "name": "Saveliy"}
    response = requests.post(url + "/bye", json=data)
    cond = response.json() == f"Bye {data['name']}, have a nice day\n"
    check(cond, "Bye test")


def test_predict(url):
    data = [{'Sex': 'I',
            'Length': 0.4300000071525574,
            'Diameter': 0.3449999988079071,
            'Height': 0.10499999672174454,
            'Whole weight': 0.44699999690055847,
            'Whole weight.1': 0.19599999487400055,
            'Whole weight.2': 0.08250000327825546,
            'Shell weight': 0.11999999731779099,
            },
            {'Sex': 'F',
            'Length': 0.574999988079071,
            'Diameter': 0.42500001192092896,
            'Height': 0.12999999523162842,
            'Whole weight': 0.9204999804496765,
            'Whole weight.1': 0.4034999907016754,
            'Whole weight.2': 0.16899999976158142,
            'Shell weight': 0.25,
            }]
    y = [7.78581437, 9.63371893]
    cond = True
    for i, obj in enumerate(data):
        response = requests.post(url + '/predict', json=obj)
        cond = np.allclose(response.json(), y[i]) and cond
    check(cond, "Predict test")


if __name__ == "__main__":
    url = "http://127.0.0.1:666"
    # url = "http://192.168.1.6:666"
    test_hello(url)
    test_bye(url)
    test_predict(url)
