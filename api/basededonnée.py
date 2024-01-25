import sqlite3

connection = sqlite3.connect('baseDeDonnee.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        mot_de_passe TEXT NOT NULL,
        etat_user INTEGER DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sondes (
        id_sonde INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        IMEI_sonde varchar(15),        
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

cursor.execute("""INSERT INTO releves(id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)""", (1 , 25.5, 60.0, 1013.25))

cursor.execute("""INSERT INTO releves(id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)""", (1, 26.3, 68.3, 1012.90))


cursor.execute("INSERT INTO releves (id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)", (1 , 25.0, 60.0, 1013.80))


cursor.execute("INSERT INTO releves (id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)", (1 , 26.7, 62.3, 1011.15))


cursor.execute("INSERT INTO releves (id_sonde, temperature, humidite, pression) VALUES (?, ?, ?, ?)", (1 , 25.5, 75.0, 1012.75))


connection.commit()
connection.close()












