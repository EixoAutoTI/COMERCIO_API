import sqlite3

def conectar():
    return sqlite3.connect("BlibliComicsLiv.db")  # banco no mesmo diretório