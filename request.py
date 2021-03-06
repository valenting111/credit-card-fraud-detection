import requests
import json

root_url = "http://localhost:8000/"

test_input_fraud = {"features": {'Time': 472.0,
                                 'V1': -3.0435406239976,
                                 'V2': -3.15730712090228,
                                 'V3': 1.08846277997285,
                                 'V4': 2.2886436183814,
                                 'V5': 1.35980512966107,
                                 'V6': -1.06482252298131,
                                 'V7': 0.325574266158614,
                                 'V8': -0.0677936531906277,
                                 'V9': -0.270952836226548,
                                 'V10': -0.838586564582682,
                                 'V11': -0.414575448285725,
                                 'V12': -0.503140859566824,
                                 'V13': 0.676501544635863,
                                 'V14': -1.69202893305906,
                                 'V15': 2.00063483909015,
                                 'V16': 0.666779695901966,
                                 'V17': 0.599717413841732,
                                 'V18': 1.72532100745514,
                                 'V19': 0.283344830149495,
                                 'V20': 2.10233879259444,
                                 'V21': 0.661695924845707,
                                 'V22': 0.435477208966341,
                                 'V23': 1.37596574254306,
                                 'V24': -0.293803152734021,
                                 'V25': 0.279798031841214,
                                 'V26': -0.145361714815161,
                                 'V27': -0.252773122530705,
                                 'V28': 0.0357642251788156,
                                 'Amount': 529.0},
                    "name": "Customer 10"}


response_body1 = requests.get(root_url)

print(response_body1.text)

response_body2 = requests.get(root_url + "testing_out_stuff/val111/24")

print(response_body2.text)

response_body3 = requests.post(root_url + "/predict", json=test_input_fraud)

print(response_body3.text)

with open('test_data.json') as json_file:
    data = json.load(json_file)

response_body4 = requests.post(root_url + "/predict", json=data)
print(response_body4.text)
