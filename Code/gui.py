from tkinter import *
from PIL import Image, ImageTk
import sys, os, json
from IR_query_finder import run_query

class Application(Frame):
	def __init__(self, master=None):
		master.minsize(width=1200, height=1200)
		master.maxsize(width=1200, height=1200)
		super().__init__(master)
		self.pack()
		self.create_widgets(master)
		self.what_dir_to_look_in='Test_Set'
		self.int_to_filename = None
		with open(os.path.join(os.getcwd(),r"ind_to_paths.json"), 'r') as fp:
			self.int_to_filename = json.load(fp)

	def create_widgets(self,master):

		master.title("3DANK M3M3Z 5YOU M8")
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)
		
		self.lbl = Label(self, text="Search for your favourite memes here!", font = ("Times New Roman",32))
		self.lbl.grid(sticky=W, pady=4, padx=5)

		self.main_frame = Frame(self,width=1100, height=1100, bg="#666666")

		self.main_frame.img_frame = Frame(self,bg="#3FADA8")
		# self.self.main_frame.img_frame.pack(side="bottom")
		self.main_frame.img_frame.grid(row=2, column=0, columnspan=5, rowspan=4, padx=5, pady=5,sticky=E+W+S+N)

		self.main_frame.textbox = Text(self,height = 2,width=100, bg="#808b96",fg="black",relief = SUNKEN,
							  undo = True, wrap = WORD,
							  font = ("Times New Roman",32))
		self.main_frame.textbox.grid(row=1, column=0, columnspan=3)

		# self.textbox.tag_configure("center", justify='center')
		# self.textbox.tag_add("center", 1.0, "end")
		# self.self.main_frame.textbox.pack(side="top")

		self.main_frame.search = Button(self,text="Search", fg="white",bg = "#333333",width=10, height=3, font = ("Times New Roman",16),
							  command=self.load_query_result)
		self.main_frame.search.grid(row=1, column=3)
		# self.main_frame.search.pack(fill= "both",side="top")

		self.main_frame.quit = Button(self, text="Quit", fg="white", bg = "#333333",width=10, height=3, font = ("Times New Roman",16),
							  command=root.destroy)
		self.main_frame.quit.grid(row=1, column=4)
		# self.main_frame.quit.pack(fill= "both",side="top")
		self.default_txt = StringVar()

		self.image_label = Label(self.main_frame.img_frame, justify = CENTER,image=None,bg="#3FADA8")
		self.image_label.image = None
		# self.default_txt.set("No results to show")
		self.image_label.pack()

		self.label_images = []

		for i in range(25):
				self.label_images.append(Label(self.main_frame.img_frame,image=None,bg="#3FADA8"))
				self.label_images[i].image = None

	def load_query_result(self):
		# print("hi there, everyone!")
		query = self.main_frame.textbox.get(1.0, END)
		query = query.strip('\n')
		print("Query: ", query)
		res = run_query(query)
		res = list(res)
		print("Result: ", res)
		if(len(res)==0):
			self.image_label.configure(image = None)
			# self.default_txt.set("No results to show")
			# self.image_label.configure(textvariable=self.default_txt) # Why this is not getting set a second time???
			self.image_label.image = None
		else:

			# top_meme = str(res[0])
			# meme_name = self.int_to_filename[top_meme].split(".")[0] + ".jpg"
			# print(meme_name)
			# image = Image.open(os.path.join(os.getcwd(),self.what_dir_to_look_in,meme_name))
			# resized = image.resize((500, 500),Image.ANTIALIAS)
			# photo = ImageTk.PhotoImage(resized)
			# self.image_label.configure(image = photo)
			# self.image_label.image = photo # keep a reference!
			
			res = res[:25]
			# print(res)
			meme_names = [] 
			for file in res:
				img_name = self.int_to_filename[str(file[0])]
				img_filename = img_name.split(".")[0].split("/")[1]
				img_filename = img_filename.strip("_img")
				# print(img_filename)
				img_filename = img_filename + ".jpg"
				meme_names.append(img_filename)
			# print(meme_names)
			images = [Image.open(os.path.join(os.getcwd(),self.what_dir_to_look_in,meme)) for meme in meme_names]
			images = [image.resize((198, 198),Image.ANTIALIAS) for image in images]
			photos = [ImageTk.PhotoImage(resized) for resized in images]

			for i in range(25):
				self.label_images[i].configure(image='',bg="#3FADA8")
				self.label_images[i].image = ''

			xlen = 56
			ylen = 10
			
			for i in range(len(res)):
				self.label_images[i] = Label(self.main_frame.img_frame, image=photos[i])
				self.label_images[i].image = photos[i]
				# print(xlen,",",ylen)
				self.label_images[i].place(x=xlen, y=ylen, width=images[i].size[0], height=images[i].size[1])
				if xlen > 800:
					ylen = ylen + 216
					xlen = 56
				else:
					xlen = xlen + 216

root = Tk()
app = Application(master=root)
app.mainloop()