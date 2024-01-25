# Importation des modules nécessaires
import flask  # Flask pour créer un serveur web.
from flask_cors import CORS  # Gestion des requêtes cross-origin (CORS).
import sqlite3  # Interaction avec la base de données SQLite.

# Création de l'application Flask
app = flask.Flask(__name__, template_folder='views')
CORS(app)

# Fonction pour déterminer l'emoji en fonction de la température
def determiner_pictogramme(temperature):
    # Si la température est égale ou supérieure à 20, renvoie un emoji soleil, sinon un emoji neige.
    if temperature >= 20:
        return '☀️'
    else:
        return '❄️'

# Route pour créer un compte utilisateur
@app.route('/api/signup', methods=['POST'])
def signup():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    pseudo = data.get('pseudo')
    mot_de_passe = data.get('mot_de_passe')
    confirmation_mot_de_passe = data.get('confirmation_mot_de_passe')

    # Vérifier que les mots de passe correspondent
    if mot_de_passe != confirmation_mot_de_passe:
        return flask.jsonify({"message": "Les mots de passe ne correspondent pas"}), 400

    # Vérifier si l'utilisateur existe déjà
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs WHERE pseudo = ?', (pseudo,))
    existing_user = cursor.fetchone()

    if existing_user:
        return flask.jsonify({"message": "L'utilisateur existe déjà"}), 400

    # Ajouter l'utilisateur à la base de données
    cursor.execute('INSERT INTO utilisateurs (pseudo, mot_de_passe) VALUES (?, ?)', (pseudo, mot_de_passe))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Compte utilisateur créé avec succès"}), 201

# Route pour ajouter un relevé
@app.route('/api/releves', methods=['POST'])
def ajouter_releve():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    humidite = data.get('humidite')
    temperature = data.get('temperature')
    pression = data.get('pression')
    date_releve = data.get('date_releve')
    id_sonde = data.get('id_sonde')

    connection = sqlite3.connect("baseDeDonnee.db")
    cursor = connection.cursor()

    # Insertion du relevé dans la base de données
    cursor.execute('INSERT INTO releves (id_sonde, temperature, humidite, pression, date_releve) VALUES (?,?,?,?,?)',
                   (id_sonde, temperature, humidite, pression, date_releve))
    connection.commit()
    connection.close()

    return flask.jsonify({"message": "Relevé bien ajouté"})

# Route pour récupérer tous les relevés
@app.route('/api/releves/', methods=['GET'])
def recuperer_releves():
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Sélectionner tous les relevés de la base de données
    cursor.execute('SELECT * FROM releves')
    releves = cursor.fetchall()
    conn.close()

    liste_releves = []

    # Transformation des relevés en format JSON
    for releve in releves:
        dico = {'id_releve': releve[0],
                'id_sonde': releve[1],
                'temperature': releve[2],
                'humidite': releve[3],
                'pression': releve[4],
                'date_releve': releve[5]}
        liste_releves.append(dico)

    return flask.jsonify(liste_releves)

# Route pour récupérer les relevés d'une sonde spécifique
@app.route('/api/releves/<int:id_sonde>', methods=['GET'])
def recuperer_releves_sonde(id_sonde):
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Sélectionner les relevés spécifiques d'une sonde dans la base de données
    cursor.execute('SELECT * FROM releves WHERE id_sonde = ?', (id_sonde,))
    releves = cursor.fetchall()
    conn.close()

    liste_releves = []

    # Transformation des relevés en format JSON
    for releve in releves:
        dico = {'id_releve': releve[0],
                'id_sonde': releve[1],
                'temperature': releve[2],
                'humidite': releve[3],
                'pression': releve[4],
                'date_releve': releve[5]}
        liste_releves.append(dico)

    return flask.jsonify(liste_releves)

# Route pour ajouter une sonde
@app.route('/api/ajouter-sonde', methods=['POST'])
def ajouter_sonde():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    nom = data.get('nom')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Insertion de la sonde dans la base de données
    cursor.execute('INSERT INTO sondes (nom) VALUES (?)', (nom,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien ajoutée"})

# Route pour supprimer une sonde
@app.route('/api/supprimer-sonde', methods=['POST'])
def supprimer_sonde():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Suppression de la sonde de la base de données
    cursor.execute('DELETE FROM sondes WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien supprimée"})

# Route pour activer une sonde
@app.route('/api/activer-sonde', methods=['POST'])
def activer_sonde():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Activation de la sonde dans la base de données
    cursor.execute('UPDATE sondes SET etat = 1 WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien activée"})

# Route pour désactiver une sonde
@app.route('/api/desactiver-sonde', methods=['POST'])
def desactiver_sonde():
    data = flask.request.get_json()  # Récupère les données JSON de la requête.
    id_sonde = data.get('id_sonde')

    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Désactivation de la sonde dans la base de données
    cursor.execute('UPDATE sondes SET etat = 0 WHERE id_sonde = ?', (id_sonde,))
    conn.commit()
    conn.close()

    return flask.jsonify({"message": "Sonde bien désactivée"})

# Route pour récupérer toutes les données pour une sonde spécifique (utilisateur)
@app.route('/api/user/recup-toutes-les-donnees', methods=['GET'])
def recuperer_toutes_les_donnees():
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Sélectionner tous les relevés dans la base de données
    cursor.execute('SELECT * FROM releves')
    releves = cursor.fetchall()

    # Sélectionner les relevés spécifiques d'une seule sonde dans la base de données
    cursor.execute('SELECT * FROM releves WHERE id_sonde = ?', (id_sonde,))
    releves = cursor.fetchall()

    conn.close()

    liste_releves = []

    # Transformation des relevés en format JSON
    for releve in releves:
        dico = {'id_releve': releve[0],
                'id_sonde': releve[1],
                'temperature': releve[2],
                'humidite': releve[3],
                'pression': releve[4],
                'date_releve': releve[5],
                'pictogramme': determiner_pictogramme(releve[2])}
        liste_releves.append(dico)

    return flask.jsonify(liste_releves)

# Route pour récupérer toutes les données pour un administrateur
@app.route('/api/admin/recup-toutes-les-donnees', methods=['GET'])
def recuperer_toutes_les_donnees_admin():
    conn = sqlite3.connect("baseDeDonnee.db")
    cursor = conn.cursor()

    # Sélectionner tous les relevés dans la base de données
    cursor.execute('SELECT * FROM releves')
    releves = cursor.fetchall()
    conn.close()

    liste_releves = []

    # Transformation des relevés en format JSON
    for releve in releves:
        dico = {'id_releve': releve[0],
                'id_sonde': releve[1],
                'temperature': releve[2],
                'humidite': releve[3],
                'pression': releve[4],
                'date_releve': releve[5],
                'pictogramme': determiner_pictogramme(releve[2])}
        liste_releves.append(dico)

    return flask.jsonify(liste_releves)

# Exécution de l'application Flask
if __name__ == '__main__':
    app.run(host="192.168.124.128", debug=True)
