import sqlite3

def lisa():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    enimi = input("Sisesta nimi: ")
    pnimi = input("Sisesta perenimi: ")
    email = input("Sisesta email: ")
    amark = input("Sisesta automark: ")
    amudel = input("Sisesta automudel: ")
    aaasta = int(input("Sisesta auto aasta: "))
    ahind = float(input("Sisesta auto hind: "))
    a.execute('INSERT INTO ktonisson (enimi, pnimi, email, amark, amudel, aaasta, ahind) VALUES (?, ?, ?, ?, ?, ?, ?)', (enimi, pnimi, email, amark, amudel, aaasta, ahind))
    yhendus.commit()
    yhendus.close()
def kuvaread():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    a.execute("SELECT * FROM ktonisson WHERE aaasta<2000 LIMIT 20")
    siuu = a.fetchall()
    for rida in siuu:
        print(rida)
    yhendus.close()
def kustuta():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    k = input("Sisesta ID mille tahad kustutada: ")
    a.execute("DELETE FROM ktonisson WHERE id = ?", (k,))
    print("Kustutatud ID:",k)
    yhendus.commit()
    yhendus.close()
def kesk():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    a.execute("SELECT AVG(aaasta) FROM ktonisson")
    avg_aasta = a.fetchone()[0]
    print("Keskmine autode aasta:", avg_aasta)
    a.execute("SELECT MAX(ahind) FROM ktonisson")
    max_hind = a.fetchone()[0]
    print("Kõige kallim hind:", max_hind)
    yhendus.close()
def kallid_autod():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    a.execute("SELECT * FROM ktonisson WHERE ahind>70000 ORDER BY pnimi LIMIT 5")
    mjau = a.fetchall()
    for rida in mjau:
        print(rida)
    yhendus.close()
   
def uusauto():
    yhendus = sqlite3.connect ("epood_ktonisson.db")
    a = yhendus.cursor()
    sql = "SELECT amark, amudel FROM ktonisson ORDER BY aaasta DESC LIMIT 5"
    a.execute(sql)
    results = a.fetchall()
    print("5 kõige uuemat automarki koos mudelitega: ")
    for row in results:
        print(row[0], row[1])
    yhendus.close()
   
   
   
def menu():
         while True:
                    print("Tee valik\n1. Lisa\n2. Kuva vanad autod\n3. Kustuta\n4. Keskmine ja kallis\n5. Kallid autod \n6. 5 kõige uuemat autot\n0. exit")
                    algus = int(input("Sisesta nr: "))
                    if algus == 1:
                        lisa()
                    elif algus == 2:
                        kuvaread()
                    elif algus == 3:
                        kustuta()
                    elif algus == 4:
                        kesk()
                    elif algus == 5:
                        kallid_autod()
                    elif algus == 6:
                        uusauto()
                       
                   
                       
                   
       
if __name__ == '__main__':
            menu()