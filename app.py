from flask import Flask, url_for, request, redirect
from flask import render_template
from mysql import connector

app = Flask(__name__)
db = connector.connect(
    host    = "localhost",
    user    = "root",
    passwd  = "",
    database= "ucs"
)

@app.route('/')
def halaman_utama():
    return render_template('base.html')

@app.route('/profil')
def profil():
    return render_template('new.html')

@app.route('/menu', methods=['get'])
def menu():
    cur = db.cursor()
    cur.execute("select * from daftar_minuman union select * from daftar_makanan")
    res = cur.fetchall()
    cur.close()
    return render_template('coba.html', hasil=res)


@app.route('/where')
def where():
    return render_template('where.html')

@app.route('/pesan', methods=['post'])
def pesan():
    nama = request.form['nama']
    makanan = request.form['makanan']
    minuman = request.form['minuman']
    cur = db.cursor()
    cur.execute('INSERT INTO customer (nama, makanan, minuman) VALUES (%s, %s, %s)', (nama, makanan, minuman))
    db.commit()
    return redirect(url_for('tampil'))

@app.route('/tampil')
def tampil():
    cur = db.cursor()
    cur.execute("select * from customer")
    res = cur.fetchall()
    cur.close()
    return render_template('ne.html', hasil=res)

@app.route('/hapus/<nama>', methods=['get'])
def hapus(nama):
    cur = db.cursor()
    cur.execute("DELETE from customer where nama=%s", (nama,))
    db.commit()
    return redirect(url_for('cancel'))

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run()