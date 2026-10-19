import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, font
from pathlib import Path

# Main Window
root = tk.Tk()
root.title("Basic Text Editor")
root.geometry("1000x500")

# Text Area
currentFont = font.Font(family = "Serif", size = 16)
wrap_tkBoolVar = tk.BooleanVar(value = True)
caseSensitivity_tkBoolVar = tk.BooleanVar(value=False)
text = tk.Text(
	root,
	wrap = tk.WORD,
	font = currentFont
)
text.pack(expand = True, fill = tk.BOTH)


""" ----- Methods ----- """
def saveFile():
	filePath = filedialog.asksaveasfilename(
		defaultextension = ".txt",
		filetypes = [
			("Text Files", "*.txt *.c *.py *.java *.html *.json *.css *.js *.ipynb"),
			("All Files", "*.*")
		]
	)
	if not filePath: # user cancelled or entered nothing
		return False

	with open(filePath, "w") as file:
		file.write(text.get(1.0, "end-1c"))
		
	messagebox.showinfo("Success", "File Saved Successfully.")
	return True

def openFile():
	confirm = messagebox.askyesnocancel("Save Changes?", "Save Current Text or IT WILL BE LOST.\nDo you want to save your current changes before opening a new file?")
	# if user clicked 'Cancel
	# or if user clicked 'Yes' but then cancelled the save dialog,
	# stop the opening process
	if confirm is None or (confirm is True and not saveFile()): return

	filePath = filedialog.askopenfilename(
		defaultextension = ".txt",
		filetypes = [("Text Files", "*.txt *.c *.py *.java *.html *.json *.css *.js *.ipynb")]
	)
	
	if not filePath:
		messagebox.showinfo("Failure", "No File Selected.")
		return
	if not Path(filePath).exists():
		messagebox.showinfo("Failure", "Given File Path DOESN'T EXIST!")
		return

	with open(filePath, "r") as file:
		text.delete(1.0, tk.END)
		text.insert(tk.END, file.read())

def changeFontFamily(fam):
	currentFont.configure(family = fam)
	
def changeFontSize(sz):
	currentFont.configure(size = sz)

def toggleWrap():
	if wrap_tkBoolVar.get(): # i.e. if rootMenu/textFormatMenu/Wrap checkbox is checked
		text.config(wrap = tk.WORD)	
	else:
		text.config(wrap = tk.NONE)
	
def findInFile():
	# clear any highlights from a previous search
	text.tag_remove("match", "1.0", tk.END)
	
	match = simpledialog.askstring("Find Text", "Enter text to find:")
	if not match: # user cancelled or entered nothing
		return

	text.tag_config("match", background = "yellow", foreground = "black")
	startPosition = "1.0"
	no_of_matches = 0
	while True:
		startPosition = text.search(match, startPosition, stopindex = tk.END, nocase  = caseSensitivity_tkBoolVar.get())
		if not startPosition: # no more matches found
			break
		endPosition = f"{startPosition} + {len(match)}c" # is where the current match ends
		text.tag_add("match", startPosition, endPosition) # highlight current match
		startPosition = endPosition
		no_of_matches += 1
	if no_of_matches == 0:
		messagebox.showinfo("Find", f"'{match}' not found.")

""" ----- End of Methods ----- """


""" ----- Menu ----- """
rootMenu = tk.Menu(root)
root.config(menu = rootMenu)

# File Menu
fileMenu = tk.Menu(rootMenu, tearoff = 0)
rootMenu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Open File", command = openFile)
fileMenu.add_command(label = "Save File", command = saveFile)	
fileMenu.add_separator()
fileMenu.add_command(label = "Exit Program", command = root.quit)	

# Text Menu
textFormatMenu = tk.Menu(rootMenu, tearoff = 0)
rootMenu.add_cascade(label = "Text", menu = textFormatMenu)
textFormatMenu.add_command(label = "Find", command = findInFile)
textFormatMenu.add_checkbutton(
    label = "Ignore Case (Find)", 
    variable = caseSensitivity_tkBoolVar
)
textFormatMenu.add_separator()
textFormatMenu.add_checkbutton(
	label = "Word Wrap", 
	variable = wrap_tkBoolVar, 
	command = toggleWrap
)
textFormatMenu.add_separator()

# -> Font Family SubMenu
fontMenu = tk.Menu(textFormatMenu, tearoff = 0)
textFormatMenu.add_cascade(label = "Font Family", menu = fontMenu)
for f in ["Serif", "Sans-Serif", "Courier", "Arial", "Times New Roman", "Comic Sans"]:
	fontMenu.add_command(label = f, command=lambda custom_f=f: changeFontFamily(custom_f))

# -> Font Size SubMenu
sizeMenu = tk.Menu(textFormatMenu, tearoff = 0)
textFormatMenu.add_cascade(label = "Font Size", menu = sizeMenu)
for s in [10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40]:
	sizeMenu.add_command(label = str(s), command=lambda custom_s=s: changeFontSize(custom_s))

""" ----- End of Menu ----- """

root.mainloop()
