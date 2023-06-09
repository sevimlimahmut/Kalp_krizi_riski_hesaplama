from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score

views = Blueprint('views', __name__)

data=pd.read_csv(r"C:\Users\Mahmut Sevimli\Desktop\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\healthcare-dataset-stroke-data4.csv")

data.head()

kategorik=["gender","hypertension","heart_disease","ever_married","work_type","Residence_type","smoking_status","stroke"]
data_kat=data.loc[:,kategorik]
data_kat

sayisal=["id","age","avg_glucose_level","bmi","stroke"]
data_sayisal=data.loc[:,sayisal]
data_sayisal.head()

sns.pairplot(data_sayisal,hue="stroke",diag_kind="kde")

data1=data.copy()
data1

data1=pd.get_dummies(data1,columns=kategorik[:-1],drop_first=True)
data1.head()

x=data1.drop(["stroke"],axis=1)
y=data1[["stroke"]]
x
y

scaler=StandardScaler()
x[sayisal[:-1]]=scaler.fit_transform(x[sayisal[:-1]])
x

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.429,random_state=5)

logreg=LogisticRegression()

logreg.fit(xtrain,ytrain)

ypred_prob=logreg.predict_proba(xtest)
ypred_prob

xtest

ypred=np.argmax(ypred_prob,axis=1)
ypred

print("Test Accuracy",accuracy_score(ypred,ytest))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        cinsiyet = request.form.get('cinsiyet')
        yas = request.form.get('yas')
        hipertans = request.form.get('hipertans')
        kalp = request.form.get('galp')
        evlilik = request.form.get('meric')
        calismatipi = request.form.get('worktype')
        yasam = request.form.get('yasam')
        glikoz = request.form.get('Glikoz')
        bmi = request.form.get('BMI')
        sigara = request.form.get('smoke')

        #hesaplama kısmı---
        new_data = pd.DataFrame([[ cinsiyet, yas, hipertans, kalp, evlilik, calismatipi, yasam, glikoz, bmi, sigara ]],
                                    columns=[ 'gender', 'age', 'hypertension', 'heart_disease',
                                            'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level',
                                            'bmi', 'smoking_status'])

        # Apply one-hot encoding to categorical variables
        new_data = pd.get_dummies(new_data, columns=kategorik[:-1], drop_first=True)

        # Check if the columns in new_data match the columns in x
        missing_columns = set(x.columns) - set(new_data.columns)
        for col in missing_columns:
            new_data[col] = 0  # Add missing columns and set them to 0

        # Reorder columns to match the order in x
        new_data = new_data[x.columns]

        # Scale the numerical variables
        new_data[sayisal[:-1]] = scaler.transform(new_data[sayisal[:-1]])

        # Predict the outcome for the new data
        ypred_prob = logreg.predict_proba(new_data)
        ypred_prob_percent = ypred_prob[:, 1] * 100  # Sadece 1'lerin olasılıklarını alıp yüzde olarak ifade ediyoruz

        #print(ypred_prob_percent)
        #---
        
        sonuc=float(ypred_prob_percent)

        if(sonuc<50):
            flash('Kalp Krizi Geçirme İhtimaliniz: % ' + str(sonuc) + '\n', category='success')
        else:
            flash('Kalp Krizi Geçirme İhtimaliniz: % ' + str(sonuc) + '  Lütfen Bir Doktora Görününüz...', category='success')

        
    return render_template("home.html", user=current_user)


def sonucgoster():

    cinsiyet = 'Male'
    yas = 75
    hipertans = 1
    kalp = 1
    evlilik = 'Yes'
    calismatipi = 'Private'
    yasam = 'Rural'
    glikoz = 70.09
    bmi = 27.4
    sigara = 'never smoked'
    
    veriler = {
        'cinsiyet': cinsiyet,
        'yas': yas,
        'hipertans': hipertans,
        'kalp': kalp,
        'evlilik': evlilik,
        'calismatipi': calismatipi,
        'yasam': yasam,
        'glikoz': glikoz,
        'bmi': bmi,
        'sigara': sigara

    }

    return veriler

def verileri_yaz():
    # Verileri dosyaya yazma
    with open('veriler.txt', 'w') as file:
        file.write("cinsiyet: " + "Male" + "\n")
        file.write("yas: " + str(75) + "\n")
        file.write("hipertans: " + str(1) + "\n")
        file.write("kalp: " + str(1) + "\n")
        file.write("evlilik: " + "Yes" + "\n")
        file.write("calismatipi: " + "Private" + "\n")
        file.write("yasam: " + "Rural" + "\n")
        file.write("glikoz: " + str(70.09) + "\n")
        file.write("bmi: " + str(27.4) + "\n")
        file.write("sigara: " + "never smoked" + "\n")

    print("Veriler dosyaya yazildi.")
    file.close()

def sonucu_oku():
    # Verileri filedan okuma
    with open('veriler.txt', 'r') as file:
        satirlar = file.readlines()
    cinsiyet = satirlar[0].split(":")[1].strip()
    yas = int(satirlar[1].split(":")[1])
    hipertans = int(satirlar[2].split(":")[1])
    kalp = int(satirlar[3].split(":")[1])
    evlilik = satirlar[4].split(":")[1].strip()
    calismatipi = satirlar[5].split(":")[1].strip()
    yasam = satirlar[6].split(":")[1].strip()
    glikoz = float(satirlar[7].split(":")[1])
    bmi = float(satirlar[8].split(":")[1])
    sigara = satirlar[9].split(":")[1].strip()
    #Risk_Orani = int(satirlar[10].split(":")[1])

    print("cinsiyet:", cinsiyet)
    print("yas:", yas)
    print("hipertans:", hipertans)
    print("kalp:", kalp)
    print("evlilik:", evlilik)
    print("calismatipi:", calismatipi)
    print("yasam:", yasam)
    print("glikoz:", glikoz)
    print("bmi:", bmi)
    print("sigara:", sigara)
    #print("Risk_Orani: ", Risk_Orani)

    file.close()

def sonuc_yaz(x):
    # Algoritma çalıştırılıp sonuç elde edildi
    sonuc = x

    # Sonucu dosyaya yazma
    with open('veriler.txt', 'w') as file:
        file.write("Sonuc: " + str(sonuc) + "\n")

    print("Sonuc dosyaya yazildi.")

    file.close()

def hesapla():
    
    # Verileri filedan okuma
    with open('veriler.txt', 'r') as file:
        satirlar = file.readlines()
    cinsiyet = satirlar[0].split(":")[1].strip()
    yas = int(satirlar[1].split(":")[1])
    hipertans = int(satirlar[2].split(":")[1])
    kalp = int(satirlar[3].split(":")[1])
    evlilik = satirlar[4].split(":")[1].strip()
    calismatipi = satirlar[5].split(":")[1].strip()
    yasam = satirlar[6].split(":")[1].strip()
    glikoz = float(satirlar[7].split(":")[1])
    bmi = float(satirlar[8].split(":")[1])
    sigara = satirlar[9].split(":")[1].strip()

    print("cinsiyet:", cinsiyet)
    print("yas:", yas)
    print("hipertans:", hipertans)
    print("kalp:", kalp)
    print("evlilik:", evlilik)
    print("calismatipi:", calismatipi)
    print("yasam:", yasam)
    print("glikoz:", glikoz)
    print("bmi:", bmi)
    print("sigara:", sigara)

    file.close()
    # Preprocess the new data
    

    #sonuc_yaz(ypred_prob_percent)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
