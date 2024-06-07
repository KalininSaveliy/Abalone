from flask import Flask, request, jsonify
from catboost import CatBoostRegressor
import numpy as np
import pandas as pd


app = Flask('SavieryFlaskShit')


@app.route('/', methods=["GET"])
def empty() -> str:
    return "route func"


@app.route('/hello', methods=["GET"])
def hello() -> str:
    return "Hello there\n"


@app.route('/bye', methods=["POST"])
def bye() -> str:
    data = request.get_json()
    answer = f"Bye {data['name']}, have a nice day\n"
    return jsonify(answer)


model = CatBoostRegressor()
model.load_model("model.cbm")

def add_new_cols(data: pd.DataFrame) -> pd.DataFrame:
    new_cols = {'Meat_per'     : {'t': 'num', 'fun': lambda df: df['Whole weight.1'].divide(df['Whole weight'])},
                'Square'       : {'t': 'num', 'fun': lambda df: df['Length'] * df['Diameter']},
                'Mass_div_sq'  : {'t': 'num', 'fun': lambda df: df['Whole weight.1'].divide(df['Square'])},
                'Volume'       : {'t': 'num', 'fun': lambda df: df['Square'] * df['Height']},
                'Shell_density': {'t': 'num', 'fun': lambda df: df['Shell weight'].divide(df['Volume'])},
                'e'            : {'t': 'num', 'fun': lambda df: np.sqrt(1 - (df['Diameter']**2).divide(df['Length']**2))}  # эксцентриситет
                }
    cols = list(data.columns)
    new_data = data
    for col, val in new_cols.items():
        if col not in cols:
            new_data[col] = val['fun'](data)
    return new_data

def inference(obj: dict) -> float:
    data = pd.DataFrame({k: [val] for k, val in obj.items()})
    data = add_new_cols(data)   
    pred = model.predict(data)
    return pred[0]

@app.route("/predict", methods=["POST"])
def predict():
    pred = inference(request.get_json())
    print(pred)
    return jsonify(float(pred))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="666", debug=False)
