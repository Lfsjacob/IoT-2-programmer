from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure 
import extract_db_data
import api_data
import rpi_data
from time import sleep
from multiprocessing import Process

app = Flask(__name__)



def prognose_graf():
    datapunkter = 288
    række, date, time, udledning = extract_db_data.CO2_Prognose(datapunkter)
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3) 
    ax.plot(time, udledning, linestyle = "dashed", c="#F11", linewidth="0.5")
    linje_x = [1, datapunkter]
    linje_y = [60, 60]
    ax.plot(linje_x, linje_y, c="#00FF00", linestyle ="dashed", linewidth="0.5")
    ax.text(linje_x[0] -1, linje_y[0] -1, "Grøn strøm", rotation=90)
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel("CO2-udledning (g/kWh)")
    ax.tick_params(axis='x', which='both', rotation=40)

    n = 12
    x_ticks = ax.get_xticks()
    for i in range(len(x_ticks)):
        if i % n != 0:
            ax.get_xaxis().get_major_ticks()[i].set_visible(False)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    sleep(1)
    return data


def strømforbrug_graf():
    tidspunkter, strømforbrug = extract_db_data.strømforbrug()
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.plot(tidspunkter, strømforbrug, linestyle = "dashed", marker='o', c="#F11", linewidth="0.5")
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel("W/h")
    ax.tick_params(axis='x', which='both', rotation=40)
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    sleep(1)
    return data


def display_strømtype():
    strømtype_rpi = rpi_data.get_rpi_data("type")
    return strømtype_rpi

@app.route("/")
def home():
    prognose = prognose_graf()
    strømforbrug = strømforbrug_graf()
    strømtype = display_strømtype()
    #batteriniveau = batteriniveau()
    return render_template("index.html", prognose = prognose, strømforbrug = strømforbrug, strømtype = strømtype)



def kør_nu():
    app.run(debug=True, host='0.0.0.0') 

p1 = Process(target=kør_nu)
p1.start()
p2 = Process(target=api_data.log)
p2.start()
p3 = Process(target = rpi_data.log)
p3.start()