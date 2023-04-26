from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("https://github.com/tommella90/milano-housing-price/blob/main/milano_housing_02_2_23.xlsx?raw=true")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/esercizio1', methods = ["GET"])
def esercizio1():
    quartiere = request.args.get("quartiere")
    df1 = df[df["neighborhood"].str.contains(quartiere, na = False)].to_html()
    return render_template("risultato.html", tabella = df1)

@app.route('/esercizio2')
def esercizio2():
    quartieri = list(set(df["neighborhood"].dropna()))
    quartieri.sort()
    return render_template("risultato.html", lista = quartieri)

@app.route('/esercizio3')
def esercizio3():
    dfquartieri = df[["neighborhood"]].drop_duplicates().sort_values(by="neighborhood").dropna().to_html()
    return render_template("risultato.html", tabella = dfquartieri)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)