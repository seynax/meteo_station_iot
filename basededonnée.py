import sqlite3

connection = sqlite3.connect('baseDeDonnee.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        mot_de_passe TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sondes (
        id_sonde INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        etat INTEGER DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS releves (
        id_releve INTEGER PRIMARY KEY AUTOINCREMENT,
        id_sonde INTEGER,
        temperature REAL,
        humidite REAL,
        pression REAL,
        date_releve DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (id_sonde) REFERENCES sondes(id_sonde)
    )
''')

cursor.execute("INSERT INTO sondes (nom, etat) VALUES (?, ?)", ("Sonde", 1))

cursor.execute("INSERT INTO releves (id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)", (0 , 25.5, 60.0, 1013.25))


connection.commit()
connection.close()












