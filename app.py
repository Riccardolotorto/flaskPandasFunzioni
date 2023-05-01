from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("https://github.com/tommella90/milano-housing-price/blob/main/milano_housing_02_2_23.xlsx?raw=true")

@app.route('/')
def home():
    q = list(set(df["neighborhood"].dropna()))
    q.sort()
    return render_template("home.html", lista = q)

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

@app.route('/esercizio4', methods = ["GET"])
def esercizio4():
    zona = request.args.get("zona")
    dfZona = df[df["neighborhood"].str.contains(zona, na = False)]
    prezzo_medio = round(dfZona["price"].mean(), 0)
    return render_template("risultato.html", prezzo = prezzo_medio)

@app.route('/esercizio5')
def esercizio5():
    dfPrezzi = df.groupby("neighborhood")[["price"]].mean().sort_values("price", ascending = False).reset_index().dropna().to_html()
    return render_template("risultato.html", tabella = dfPrezzi)

@app.route('/esercizio6', methods = ["GET"])
def esercizio6():
    tasso = float(request.args.get("tasso"))
    def conversione(euro, tasso):
        return euro * tasso
    d = df.groupby("neighborhood")[["price"]].mean().sort_values("price", ascending = False).reset_index().dropna()
    dfAltraValuta = conversione(d[["price"]].dropna(), tasso)
    dfAltraValutaTesti = d[["neighborhood"]].dropna()
    dff = [dfAltraValutaTesti, dfAltraValuta]
    result = pd.concat(dff, axis = 1).to_html()
    return render_template("risultato.html", tabella = result)

@app.route('/variante', methods = ["GET"])
def variante():
    zona2 = request.args.getlist("zona2")
    prezzi = []
    for z in zona2:
        dfZonaCheck = df[df["neighborhood"].str.contains(z, na = False)]
        prezzi.append(round(dfZonaCheck["price"].mean(), 0))
    return render_template("risultato.html", lista = prezzi)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)