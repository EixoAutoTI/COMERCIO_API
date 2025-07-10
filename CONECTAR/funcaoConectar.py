import sqlite3

def conectar():
    return sqlite3.connect("appEcho.db")  # banco no mesmo diretório