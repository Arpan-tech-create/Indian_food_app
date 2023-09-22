from flask import Flask,render_template,jsonify,request
import sqlite3


app = Flask(__name__,template_folder='templates')




@app.route('/')
def index():
    conn=sqlite3.connect('indian.db')
    cur=conn.cursor()
    cur.execute("select count(distinct course) as cnt from food")
    course=cur.fetchone()[0]
    print(course)

   

    
    cur.execute("select count(distinct ingredients) as st from food ")
    ingr=cur.fetchone()[0]
    print(ingr)

    cur.execute("select count(distinct name) as snm from food ")
    dish=cur.fetchone()[0]
    print(dish)

  

    cur.execute("select diet,count(*) as dt from food group by diet order by dt desc")
    diets=cur.fetchall()
    print("DIETS",diets)

    cur.execute("select flavor_profile,count(*) as fl from food where  flavor_profile !=-1 group by flavor_profile order by fl desc")
    flavr=cur.fetchall()
    print('flavors',flavr)

    cur.execute("select state,count(*) as st from food where state !=-1 group by state order by st desc limit 5")
    states=cur.fetchall()
    print("states",states)

    cur.execute("SELECT DISTINCT name, prep_time FROM food ")
    data = cur.fetchall()
    print("DISH_PREP",data)
    cur.close()
    conn.close

    return render_template('dashboard.html',course=course,ingr=ingr,dish=dish,diets=diets
    ,flavr=flavr,states=states,data=data)


@app.route('/update_counts_by_state/<string:ct>', methods=['GET'])
def update_counts_by_state(ct):
    conn = sqlite3.connect('indian.db')
    cur = conn.cursor()
    cur.execute("select count(distinct name) as snm from food where state=?", (ct,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)

@app.route('/update_flavor_by_state/<string:st>', methods=['GET'])
def update_flavor_by_state(st):
    conn = sqlite3.connect('indian.db')
    cur = conn.cursor()
    cur.execute("SELECT flavor_profile, COUNT(*) as fl FROM food WHERE state=? AND flavor_profile != -1 GROUP BY flavor_profile ORDER BY fl DESC", (st,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)

@app.route('/update_diet_by_state/<string:dt>', methods=['GET'])
def update_diet_by_state(dt):
    conn = sqlite3.connect('indian.db')
    cur = conn.cursor()
    cur.execute("SELECT diet, COUNT(*) as dt1 FROM food WHERE state=?  GROUP BY diet ORDER BY dt1 DESC", (dt,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)


@app.route('/update_prep_by_state/<string:prep>', methods=['GET'])
def update_prep_by_state(prep):
    conn = sqlite3.connect('indian.db')
    cur = conn.cursor()
    cur.execute("SELECT distinct name, prep_time  FROM food WHERE state=?", (prep,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)

app.run('0.0.0.0',debug=True)