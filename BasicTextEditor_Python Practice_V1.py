import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, font
from pathlib import Path

# Main Window Settings
root = tk.Tk()
root.title("Basic Text Editor")
root.geometry("1000x500")

# Text and Text Area Settings
currentFont = font.Font(
	family = "Serif",
	size = 16
)
text = tk.Text(
	root,
	wrap = tk.WORD,
	font = currentFont,
	undo = True
)
text.pack(
	expand = True,
	fill = tk.BOTH
)
wrap_tkBoolVar = tk.BooleanVar(value = True)
caseSensitivity_tkBoolVar = tk.BooleanVar(value = False)
def check4UnsavedChanges(event = None):
	if text.edit_modified():
		root.title("Basic Text Editor * (Unsaved Changes)")
text.bind("<<Modified>>", check4UnsavedChanges)


""" ----- Methods ----- """
def saveFile():
	filePath = filedialog.asksaveasfilename(
		defaultextension = ".txt",
		filetypes = [
			("Text Files", "*.txt *.c *.py *.java *.html *.json *.css *.js *.ipynb"),
			("All Files", "*.*")
		]
	)
	if not filePath:
		return False
	with open(filePath, "w") as file:
		file.write(text.get(1.0, "end-1c"))
	messagebox.showinfo("Success", "File Saved Successfully.")
 
	text.bind("<<Modified>>", "") # to avoid the reset echo loop bug in tkinter
	text.edit_modified(False) 
	root.title("Basic Text Editor")
	text.bind("<<Modified>>", check4UnsavedChanges)

	return True

def openFile():
	if text.edit_modified():
		confirm = messagebox.askyesnocancel(
			"Save Changes?",
			"Save Current Text or IT WILL BE LOST.\nDo you want to save your current changes before opening a new file?"
		)
		# if user clicked 'Cancel' or if user clicked 'Yes' but then cancelled the save dialog, stop the opening process
		if confirm is None or confirm and not saveFile():
			return

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

	text.bind("<<Modified>>", "") # to avoid the reset echo loop bug in tkinter
	text.edit_modified(False) 
	root.title("Basic Text Editor")
	text.bind("<<Modified>>", check4UnsavedChanges) 

def safeExit():
	if not text.edit_modified():
		return root.destroy()
	save = messagebox.askyesnocancel(
		"Unsaved Changes", 
		"You have unsaved changes. Do you want to save them before exiting?"
	)
	if save is True:
		if saveFile():
			root.destroy()
	elif save is False:
		root.destroy()

def changeFontFamily(fam):
	currentFont.configure(family = fam)
	
def changeFontSize(sz):
	currentFont.configure(size = sz)

def toggleWrap():
	if wrap_tkBoolVar.get(): # i.e. if rootMenu/textFormatMenu/Wrap checkbox is checked
		text.config(wrap = tk.WORD)	
	else:
		text.config(wrap = tk.NONE)

def removeHighlights():
	text.tag_remove("match", "1.0", tk.END)
	
def findInFile():
	removeHighlights()
	match = simpledialog.askstring("Find Text", "Enter text to find:")
	if not match:
		return

	text.tag_config("match", background = "yellow", foreground = "black")
	startPosition = "1.0"
	no_of_matches = 0
	while True:
		startPosition = text.search(match, startPosition, stopindex = tk.END, nocase = caseSensitivity_tkBoolVar.get())
		if not startPosition: # no more matches found
			break
		endPosition = f"{startPosition} + {len(match)}c" # is where the current match ends
		text.tag_add("match", startPosition, endPosition) # highlight current match
		startPosition = endPosition
		no_of_matches += 1
	if no_of_matches == 0:
		messagebox.showinfo("Find", f"'{match}' not found.")
		return
	else:
		messagebox.showinfo("Find", f"'{no_of_matches}' matches found.")

def replaceAllInFile():
	target = simpledialog.askstring("Replace Text", "Enter text to find:")
	if not target: # if user cancels prompt or if input is empty
		return
	replacement = simpledialog.askstring("Replace Text", f"Replace '{target}' with:")
	if replacement is None: # only if user cancels prompt specifically; allows empty input (for deletion of all {target}s)
		return
	
	text.edit_separator() # treat the bulk replacement as a single undo action if needed
	startPosition = "1.0"
	no_of_replacements = 0
	while True:
		startPosition = text.search(target, startPosition, stopindex = tk.END, nocase = caseSensitivity_tkBoolVar.get())
		if not startPosition:
			break
		endPosition = f"{startPosition} + {len(target)}c"
		text.delete(startPosition, endPosition)
		text.insert(startPosition, replacement)
		startPosition = f"{startPosition} + {len(replacement)}c"
		no_of_replacements += 1
	if no_of_replacements == 0:
		messagebox.showinfo("Replace", f"'{target}' not found.")
	else:
		messagebox.showinfo("Replace", f"Successfully replaced {no_of_replacements} occurrence(s).")

""" ----- End of Methods ----- """


""" ----- Menu ----- """
rootMenu = tk.Menu(root)
root.config(menu = rootMenu)

# File Menu
fileMenu = tk.Menu(rootMenu, tearoff = 0)
rootMenu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Open File (Ctrl + O)", command = openFile)
fileMenu.add_command(label = "Save File (Ctrl + S)", command = saveFile)	
fileMenu.add_separator()
fileMenu.add_command(label = "Exit Program", command = safeExit)	

# Text Menu
textFormatMenu = tk.Menu(rootMenu, tearoff = 0)
rootMenu.add_cascade(label = "Text", menu = textFormatMenu)
textFormatMenu.add_command(label = "Find (Ctrl + F)", command = findInFile)
textFormatMenu.add_command(label = "Replace (Ctrl + R)", command = replaceAllInFile)
textFormatMenu.add_checkbutton(
	label = "[?] Ignore Case in 'Find'/'Replace' ?", 
	variable = caseSensitivity_tkBoolVar
)
textFormatMenu.add_command(label = "Remove Highlights (Ctrl + H)", command = removeHighlights)
textFormatMenu.add_separator()
textFormatMenu.add_checkbutton(
	label = "[?] Word Wrap ?", 
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

""" ----- Keyboard Bindings ----- """
import sys # Mac uses 'Command' & Windows/Linux use 'Control'
PLATFORM_MODIFIER = "Command" if sys.platform == "darwin" else "Control"
def keyBind(event):
	match event.keysym.lower(): # to bypass Caps Lock
		case "s": saveFile()
		case "o": openFile()
		case "f": findInFile()
		case "r": replaceAllInFile()
		case "h": removeHighlights()
		case _: return None
	return "break" # intercepts matched shortcuts only
root.bind(f"<{PLATFORM_MODIFIER}-KeyPress>", keyBind)
""" ----- End of Keyboard Bindings ----- """

root.protocol("WM_DELETE_WINDOW", safeExit)
root.mainloop()