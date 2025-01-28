from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    name = request.form['playerName']
    position = request.form['playerPosition']
    age = int(request.form['playerAge'])
    weight = float(request.form['playerWeight'])
    height = float(request.form['playerHeight'])

    
    import warnings
    warnings.filterwarnings('ignore')

    import numpy as np
    import pandas as pd
    import seaborn as sns

    df=pd.read_csv("C:\\Users\\adity\\OneDrive\\Desktop\\Desktop Apps\\python\\datascience\\project.csv")
    df.rename({"calories/very active pal":"cals"},axis=1,inplace=True)
    for i in range (0,50):
      df["protein"][i]=df["protein"][i]*7
      df["fat"][i]=df['cals'][i]*0.244
      if(df["position"][i])=="gk":
        df["carbs"][i]=df["weight"][i]*(3.9*7.5)
      elif(df["position"][i])=="def":
        df["carbs"][i]=df["weight"][i]*(4.3*7.5)
      elif(df["position"][i])=="mid":
        df["carbs"][i]=df["weight"][i]*(5.65*7.5)
      elif(df["position"][i])=="wb":
        df["carbs"][i]=df["weight"][i]*(5.6*7.5)
      elif(df["position"][i])=="fwd":
        df["carbs"][i]=df["weight"][i]*(5.7*7.5)
    df.drop("vitamin minerals",axis=1,inplace=True)
    df=df.replace(to_replace="gk",value=1)
    df=df.replace(to_replace="def",value=2)
    df=df.replace(to_replace="wb",value=3)
    df=df.replace(to_replace="mid",value=4)
    df=df.replace(to_replace="fwd",value=5)

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

    x=df[["position","age","weight","height"]]
    y=df[["carbs","protein","fat"]]

    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.25)
    randomforestmodel=RandomForestRegressor(n_estimators=100,random_state=42)
    randomforestmodel.fit(x_train,y_train)
    y_pred=randomforestmodel.predict(x_test)

    new_data=pd.DataFrame({"position":[position],"age":[age],"weight":[weight],"height":[height]})

    new_data=new_data.replace(to_replace="gk",value=1)
    new_data=new_data.replace(to_replace="def",value=2)
    new_data=new_data.replace(to_replace="wb",value=3)
    new_data=new_data.replace(to_replace="mid",value=4)
    new_data=new_data.replace(to_replace="fwd",value=5)

    new_pred=randomforestmodel.predict(new_data)
    prediction=new_pred.tolist()
    carbs=prediction[0][0]
    prot=prediction[0][1]
    fats=prediction[0][2]

    
    carbs_grams = carbs / 4
    protein_grams = prot / 4
    fat_grams = fats / 9

    
    result = {
        "name": name,
        "carbs": round(carbs),
        "carbs_grams": round(carbs_grams),
        "protein": round(prot),
        "protein_grams": round(protein_grams),
        "fat": round(fats),
        "fat_grams": round(fat_grams),
        "total_calories": round(carbs+prot+fats)
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)




