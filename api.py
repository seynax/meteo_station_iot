import flask
from flask_cors import CORS
import sqlite3

app = flask.Flask(__name__, template_folder='views')
CORS(app)  


@app.route('/api/releves', methods=['POST'])
def ajouter_releve():
    data = flask.request.get_json()
    humidite = data.get('humidite')
    temperature = data.get('temperature')
    pression = data.get('pression')
    date_releve = data.get('date_releve')
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO releves (id_sonde, temperature, humidite, pression, date_releve) VALUES (?,?,?,?,?)',
                   (id_sonde, temperature, humidite, pression, date_releve))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Relevé bien ajouté"})

@app.route('/api/releves/', methods=['GET'])
def recuperer_releves():
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM releves')
    releves = cursor.fetchall()
    conn.close()

    liste_releves = []

    for releve in releves:
        dico = {'id_releve': releve[0],
                'id_sonde': releve[1],
                'temperature': releve[2],
                'humidite': releve[3],
                'pression': releve[4],
                'date_releve': releve[5]}
        liste_releves.append(dico)

    return flask.jsonify(liste_releves)

@app.route('/api/ajouter-sonde', methods=['POST'])
def ajouter_sonde():
    data = flask.request.get_json()
    nom = data.get('nom')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sondes (nom) VALUES (?)', (nom,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien ajoutée"})

@app.route('/api/supprimer-sonde', methods=['POST'])
def supprimer_sonde():
    data = flask.request.get_json()
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sondes WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien supprimée"})

@app.route('/api/activer-sonde', methods=['POST'])
def activer_sonde():
    data = flask.request.get_json()
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE sondes SET etat = 1 WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien activée"})

@app.route('/api/desactiver-sonde', methods=['POST'])
def desactiver_sonde():
    data = flask.request.get_json()
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE sondes SET etat = 0 WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde désactivée"})

if __name__ == '__main__':
    app.run(debug=True)
