import sqlite3
import pyautogui
from tkinter import *
from tkinter import messagebox

class app(object):
	"""rummy score counter app"""
	def __init__(self):
		self.bg = '#081828'
		self.fg = '#FFFFFF'
		self.font = 16
		self.height = 120
		self.width  = 250

		self.labels = []
		self.entries = []
		self.players = pyautogui.prompt(text='enter the player names seperated by comma(",")', title='players' , default='').split(",")
		self.root = Tk()
		self.db_init()
		self.app()
		self.root.mainloop()

	def db_init(self):
		self.db = sqlite3.connect('scores.db')
		self.cur = self.db.cursor()
		querry = "CREATE TABLE SCORES"
		querry+='('
		for player in self.players:
			querry+=player+' int,'

		querry= querry[:-1]+')'
		try:
			self.cur.execute("DROP TABLE SCORES")
		except:
			pass
		self.cur.execute(querry)

	def insert(self):
		try:
			scores = [int(entry.get()) for entry in self.entries]
			querry = "INSERT INTO SCORES VALUES"
			querry+='('
			for i in range(len(self.players)):
				querry+='?,'

			querry= querry[:-1]+')'

			self.cur.execute(querry,scores)
			self.db.commit()
			self.clear()
		except:
			messagebox.showerror("error","insert a valid integer")

	def view(self):
		self.player_scores = [0 for i in self.players]
		self.cur.execute("SELECT * FROM SCORES")
		for rounds in self.cur.fetchall():
			for player_score in rounds:
				self.player_scores[rounds.index(player_score)]+=player_score

		t = ""
		for i in range(len(self.players)):
			t+=self.players[i]+' : '+str(self.player_scores[i])+'\n'
		messagebox.showinfo('scores',t)

	def clear(self):
		for entry in self.entries:
			entry.delete(0,END)

	def add_players(self):
		row = 0
		column = 0
		width = min([len(i) for i in self.players])

		for player in self.players:
			self.labels.append(Label(self.root,text=player,bg=self.bg,fg=self.fg,font=self.font))
			self.entries.append(Entry(self.root,width=width,bg=self.bg,fg=self.fg,font=self.font))

		for i in range(len(self.players)):
			if i%3==0 and i!=0:
				row+=2
				column=0
				self.height+=60
			self.labels[i].grid(row=row,column=column,padx=10,pady=5)
			self.entries[i].grid(row=row+1,column=column,padx=10,pady=5)

			column+=1

		self.btn_insert = Button(self.root,text='insert',bg=self.bg,fg=self.fg,font=self.font,command=self.insert)
		self.btn_view = Button(self.root,text='view',bg=self.bg,fg=self.fg,font=self.font,command=self.view)
		self.btn_clear = Button(self.root,text='clear',bg=self.bg,fg=self.fg,font=self.font,command=self.db_init)

		self.btn_insert.grid(row=row+2,column=0,padx=10,pady=5)
		self.btn_view.grid(row=row+2,column=1,padx=10,pady=5)
		self.btn_clear.grid(row=row+2,column=2,padx=10,pady=5)

	def app(self):
		self.root.geometry(f"{self.width}x{self.height}")
		self.root.config(bg=self.bg)
		self.root.title('rummy score counter')
		self.add_players()




app()