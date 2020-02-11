import urllib2;
import multiprocessing;
import time;
import re;
import textwrap;

import Tkinter,tkFileDialog
from Tkinter import *
import ttk
from ttkthemes import ThemedStyle
import Tkinter as tk
import tkFont

from bs4 import BeautifulSoup;


class Application(Frame):

	def createWidgets(self):

		self.table_count = 0;

		self.italicFont = tkFont.Font(size = '12', slant = 'italic');
		self.defaultFont = tkFont.Font(size = '12', slant = 'roman');

		self.allObjects = [];
		self.allTextAreas = [];


		#Displays at the top
		self.applicationTitle = Label(self, text = "SCP Database", background='#424242', fg='white', font = ('Courier', 15, 'bold'));
		self.applicationTitle.grid(columnspan=1, row=0, column=6);
		self.allObjects.append(self.applicationTitle);


		#Field and Label for entering new SCP Data Retrieval Request
		self.scpRequestLabel = Label(self, text = "SCP Entry Request:", background='#424242', fg='white', font = ('Courier', 11, 'bold'));
		self.scpRequestLabel.grid(columnspan = 1, row = 1, column = 5, sticky = E);
		#-----#
		self.scpRequestEntry = Entry(self, width = 10);
		self.scpRequestEntry.grid(columnspan = 1, row = 1, column = 6, sticky = EW);
		self.scpRequestEntry.bind('<Return>', lambda x : self.load_scp_data(self.scpRequestEntry.get()) );
		self.scpRequestEntry.focus();
		self.allTextAreas.append(self.scpRequestEntry);


		#Field for displaying SCP data
		self.scpDataDisplay = Text(self, wrap = WORD, width = 75, height = 50, padx = 18);
		self.scpDataDisplay.grid(columnspan = 5, rowspan = 11, row = 2, column = 2, sticky = 'NESW');
		self.scpDataDisplay.config(state=DISABLED);
		#Scrollbar for scpDataDisplay
		self.displayScroll = ttk.Scrollbar(self, command = self.scpDataDisplay.yview);
		self.displayScroll.place(in_ = self.scpDataDisplay, relx = 1.0, x = -18, relheight = 1, bordermode = 'outside')
		self.scpDataDisplay['yscrollcommand'] = self.displayScroll.set;


		#Field for displaying Links
		self.scpLinkDisplay = Listbox(self, width = 75, selectmode = SINGLE, font = ('Courier', 12));
		self.scpLinkDisplay.grid(columnspan = 3, rowspan = 2, row = 3, column = 7, sticky = 'EWNS', padx = 50);
		#self.scpLinkDisplay.config(state=DISABLED);
		#Scrollbar for scpLinkDisplay
		self.linkScroll = ttk.Scrollbar(self, command = self.scpLinkDisplay.yview);
		self.linkScroll.place(in_ = self.scpLinkDisplay, relx = 1.0, x = -18, relheight = 1, bordermode = 'outside')
		self.scpLinkDisplay['yscrollcommand'] = self.linkScroll.set;
		#Label for scpLinkDisplay
		self.linkLabel = Label(self, text = 'External Links:', background='#424242', fg='white', font = ('Courier', 15, 'bold'));
		self.linkLabel.place(in_ = self.scpLinkDisplay, rely = 0.0, y = -15*3)


		#Field for displaying SCP Images
		self.scpImageDisplay = Listbox(self, selectmode = SINGLE, font = ('Courier', 12));
		self.scpImageDisplay.grid(columnspan = 3, rowspan = 2, row = 7, column = 7, sticky = 'EWNS', padx = 50);
		#Scrollbar for scpImageDisplay
		self.imageScroll = ttk.Scrollbar(self, command = self.scpImageDisplay.yview);
		self.imageScroll.place(in_ = self.scpImageDisplay, relx = 1.0, x = -18, relheight = 1, bordermode = 'outside')
		self.scpImageDisplay['yscrollcommand'] = self.imageScroll.set;
		#Label for scpImageDisplay
		self.imageLabel = Label(self, text = 'Images:', background='#424242', fg='white', font = ('Courier', 15, 'bold'));
		self.imageLabel.place(in_ = self.scpImageDisplay, rely = 0.0, y = -15*3)


		#Field for displaying SCP Footnotes
		self.scpFootnoteDisplay = Listbox(self, selectmode = SINGLE, font = ('Courier', 12));
		self.scpFootnoteDisplay.grid(columnspan = 3, rowspan = 2, row = 11, column = 7, sticky = 'EW', padx = 50);
		#Scrollbar for scpFootnoteDisplay
		self.footnoteScroll = ttk.Scrollbar(self, command = self.scpFootnoteDisplay.yview);
		self.footnoteScroll.place(in_ = self.scpFootnoteDisplay, relx = 1.0, x = -18, relheight = 1, bordermode = 'outside')
		self.scpFootnoteDisplay['yscrollcommand'] = self.footnoteScroll.set;
		#Label for scpFootnoteDisplay
		self.footnoteLabel = Label(self, text = 'Footnotes:', background='#424242', fg='white', font = ('Courier', 15, 'bold'));
		self.footnoteLabel.place(in_ = self.scpFootnoteDisplay, rely = 0.0, y = -15*3)


		#Font options
		self.scpDataDisplay.tag_configure('italic', font=('Times', 12, 'italic'), lmargin1 = 15, lmargin2 = 15);
		self.scpDataDisplay.tag_configure('italic-bold', font=('Times', 12, 'italic', 'bold'), lmargin1 = 15, lmargin2 = 15);
		self.scpDataDisplay.tag_configure('bold', font=('Times', 13, 'bold'), spacing3 = 15, spacing1 = 15);
		self.scpDataDisplay.tag_configure('bold-default', font=('Times', 13, 'bold'), lmargin1 = 15, lmargin2 = 15);
		self.scpDataDisplay.tag_configure('link-default', font=('Courier', 12), lmargin1 = 15, lmargin2 = 15, foreground = 'cyan');
		self.scpDataDisplay.tag_configure('link-italic', font=('Courier', 12, 'italic'), lmargin1 = 15, lmargin2 = 15, foreground = 'cyan');
		self.scpDataDisplay.tag_configure('footnote', offset = 4, font=('Courier', 8), lmargin1 = 15, lmargin2 = 15, foreground = 'cyan');
		self.scpDataDisplay.tag_configure('footnote-italic', offset = 4, font=('Courier', 8, 'italic'), lmargin1 = 15, lmargin2 = 15, foreground = 'cyan');
		self.scpDataDisplay.tag_configure('strike-through', font=('Courier', 12, 'overstrike'), lmargin1 = 15, lmargin2 = 15);
		self.scpDataDisplay.tag_configure('list', font=('Courier', 12), lmargin1 = 35, lmargin2 = 55);
		self.scpDataDisplay.tag_configure('default', font=('Courier', 12), lmargin1 = 15, lmargin2 = 15);

		self.allTextAreas.append(self.scpDataDisplay);
		self.allTextAreas.append(self.scpLinkDisplay);
		self.allTextAreas.append(self.scpImageDisplay);
		self.allTextAreas.append(self.scpFootnoteDisplay);

		#Button for submitting SCP Data Retrieval Request
		self.REQUEST = Button(self, font = ('Courier', 11, 'bold'));
		self.REQUEST["text"] = "REQUEST";
		self.REQUEST["command"] = lambda : self.load_scp_data(self.scpRequestEntry.get()); #lambda very important here
		self.REQUEST.grid(row=1, column=7, sticky = W, padx = 5)
		self.REQUEST.config(width="8")
		self.allObjects.append(self.REQUEST)

		#Button for submitting SCP Data Retrieval Request
		self.LINK_REQUEST = Button(self, font = ('Courier', 11, 'bold'));
		self.LINK_REQUEST["text"] = "REQUEST";
		self.LINK_REQUEST["command"] = lambda : self.load_scp_data(self.scpRequestEntry.get()); #lambda very important here
		self.LINK_REQUEST.place(in_ = self.scpLinkDisplay, relx = 1.0, rely = 1.0, x = -81, bordermode = 'outside')
		self.LINK_REQUEST.config(width="8")
		self.allObjects.append(self.LINK_REQUEST)

		#Button for submitting SCP Data Retrieval Request
		self.IMAGE_REQUEST = Button(self, font = ('Courier', 11, 'bold'));
		self.IMAGE_REQUEST["text"] = "REQUEST";
		self.IMAGE_REQUEST["command"] = lambda : self.load_scp_data(self.scpRequestEntry.get()); #lambda very important here
		self.IMAGE_REQUEST.place(in_ = self.scpImageDisplay, relx = 1.0, rely = 1.0, x = -81, bordermode = 'outside')
		self.IMAGE_REQUEST.config(width="8")
		self.allObjects.append(self.IMAGE_REQUEST)

		#Quit button, quits the application
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["command"] =  self.quit
		self.QUIT.grid(columnspan = 2, rowspan=2, row=13, column=6)
		self.QUIT.config(width="15", height = "2")
		self.allObjects.append(self.QUIT)

		#Button for going to next SCP
		self.NEXT = Button(self)
		self.NEXT["text"] = " > "
		self.NEXT["command"] =  lambda : self.load_scp_data(int(self.scpRequestEntry.get()) + 1);
		self.NEXT.grid(rowspan = 3, row=6, column=10)
		self.NEXT.config(width="15", height="2")
		self.allObjects.append(self.NEXT)

		#Button for going to previous SCP
		self.PREV = Button(self)
		self.PREV["text"] = " < "
		self.PREV["command"] =  lambda : self.load_scp_data(int(self.scpRequestEntry.get()) - 1);
		self.PREV.grid(rowspan = 3, row=6, column=1)
		self.PREV.config(width="15", height="2");
		self.allObjects.append(self.PREV)


###################################################################################################################################
#Data Retrieval and Processing
###################################################################################################################################	
	


	def createTable(self, entry):
		entry = entry.encode('utf-8');

		#These are just a headache I don't want to deal with in grids.
		entry = re.sub('<strong>|</strong>', '', entry);

		#Attempting to strikethrough regular text. . .
		strikes = re.findall('(?<=<span style=\"text-decoration: line-through;\">)[\s|\S]*?(?=</span>)', entry);
		for strike in strikes:
			
			replacement_txt = ''
			for char in strike:
				replacement_txt = replacement_txt + char + u'\u0335';

			entry = re.sub('<span style=\"text-decoration: line-through;\">' + strike + '</span>', replacement_txt, entry);
			entry = entry.encode('utf-8');

		#Initialize Treeview, showing only headings and not the label of each row
		data_table = ttk.Treeview(self.scpDataDisplay, show = 'headings', selectmode = 'none');

		#Grabbing all the rows
		table_rows = re.findall('(?<=<tr>)[\s|\S]*?(?=</tr>)', entry);
		del table_rows[0]; #Removing headers from the list

		#Separating the individual cell data into a list for each row.
		max_row_height = 0;
		for i, row in enumerate(table_rows):

			table_rows[i] = re.findall('(?<=<td>)[\s|\S]*?(?=</td>)', row);

			for j, cell in enumerate(table_rows[i]):
				cell = cell.decode('utf-8')
				table_rows[i][j] = ''.join(textwrap.fill(cell, 30));
				table_rows[i][j] = table_rows[i][j].encode('utf-8');

				if table_rows[i][j].count('\n') > max_row_height:
					max_row_height = table_rows[i][j].count('\n');

			data_table.insert('', END, values=table_rows[i])

		#Grabbing the headers
		table_headers = re.findall('(?<=<th>)[\s|\S]*?(?=</th>)', entry);

		#Setting treeview headers
		data_table["columns"] = table_headers;

		#Here we can take into account if there were table headers absent
		if not table_headers:
			for i in range(0, len(table_rows[0])):
				table_headers.append('');
			data_table["columns"] = table_headers;
		else:
			for header in table_headers:
				data_table.heading(column=header, text = header);


		#Changing style of the grid to match rest of app
		ttk.Style().configure('Table' + str(self.table_count) + '.Treeview', rowheight = max_row_height*20, fieldbackground = '#232323', background = '#232323', foreground = '#42ff58');
		data_table["style"] = 'Table' + str(self.table_count) + '.Treeview'; 
		#Changing height of table to match how many rows there are.
		data_table["height"] = len(table_rows)

		self.scpDataDisplay.window_create(INSERT, window=data_table);
		self.scpDataDisplay.insert(END, '\n\n')
		self.table_count += 1;




	def load_scp_data(self, scp_entry):
		try:
			#Declaring URL
			scp_entry = str(scp_entry);

			#If it's a standard SCP entry, include the scp- prefix otherwise it should be treated as supporting material.
			if re.findall('^[\d]+$', scp_entry):
				scp_entry = '/scp-' + scp_entry;

			masterURL = "http://www.scp-wiki.net" + scp_entry;

			#Requesting access as a user-agent that is not a web drone, and also pulling the info
			url_request = urllib2.Request( masterURL, headers = {"User-Agent": "Mozilla/5.0"} );

			print('Retrieval Request Approved, Standby. . .')

			print('\nNow retrieving data regarding: ' + scp_entry + '\n');

			page_contents = BeautifulSoup( urllib2.urlopen(url_request) );

			#print(page_contents);

			print('Classified Information Retrieved, Standby. . .' + '\n');

			juicy_bits = page_contents.find(id='page-content');
			#print(juicy_bits);
			#Troubleshooting
			#print(page_contents);

			juicy_bits = str(juicy_bits);
			juicy_bits = re.sub('<div class=\"footer[\s|\S]*?</div>', '', juicy_bits);

			try:
				scp_display_no = re.findall( '(?<=<strong>Item #:</strong> SCP-)[^<]*', juicy_bits )[0];
				scp_class = re.findall( '(?<=<strong>Object Class:</strong> ).*', juicy_bits )[0];
			except IndexError:
				print('WARNING: This is not a traditionally styled page.')

			filtered_bits = re.findall( '<blockquote>[\s|\S]*?</blockquote>|<p>[\s|\S]*?</p>|<ul>[\s|\S]*?</ul>|<table[\s|\S]*?>[\s|\S]*?</table>', juicy_bits);

			#print(juicy_bits);
			# for i in filtered_bits:
			# 	print(i + '\n');

			#Clearing the display window
			self.scpDataDisplay.config(state = NORMAL);
			self.scpDataDisplay.delete('1.0', END);

			links = [];
			footnotes = re.findall('(?<=WIKIDOT\.page\.utils\.scrollToReference\(\'footnoteref-\d\'\)\">\d</a>\.)[\s|\S]*?(?=</div>)', juicy_bits);
			
			for data in filtered_bits:

				style_check_string = data;
				#print(data + '\n')
				data = re.sub('<p>', '\n', data);
				data = re.sub('<br/>|<em>', '', data);
				#print(data + '\n');
				data = re.sub('<sup[\s|\S]*?>', '', data);
				data = re.sub('</sup>', '', data);
				#print(data + '\n');

				table_flag = False;

				if re.findall('</table>', data):
					table_flag = True;
				else:
					substrings = re.findall('<(?!/)[\s|\S]*?>[^<]*?</[\s|\S]*?>', data);

					substrings_iter = re.finditer('<(?!/)[\s|\S]*?>[^<]*?</[\s|\S]*?>', data);
					substrings_iter = [[m.start(0), m.end(0)] for m in substrings_iter]
					#print(substrings_iter[0][0])
					#print(substrings);

				ordered_data = [];
				ordered_data = [];

				#print('\nSubstrings:' + str(substrings));
				#print('Substring Length:' + str(len(substrings)));
				
				#Parser for html lines, pretty nifty and prob needs to be reworked into something simpler.
				if substrings_iter and table_flag == False:
					
					for i, string in enumerate(substrings_iter):
								
						if len(substrings_iter) > i+1:

							first_start_pos = substrings_iter[i][0];
							first_end_pos = substrings_iter[i][1];
							second_start_pos = substrings_iter[i+1][0];
							
							#If there is no ordered data yet, we need to account for the possiblity of text before the first substring
							if not ordered_data:
								ordered_data.append(data[0:first_start_pos]);
								ordered_data.append(data[first_start_pos:first_end_pos]);
								ordered_data.append(data[first_end_pos:second_start_pos]);
							else:
								ordered_data.append(data[first_start_pos:first_end_pos]);
								ordered_data.append(data[first_end_pos:second_start_pos]);
						else: #This is to handle if there is only one single tag to account for
							first_start_pos = substrings_iter[i][0];
							first_end_pos = substrings_iter[i][1];

							if not ordered_data:
								ordered_data.append(data[0:first_start_pos]);
								ordered_data.append(data[first_start_pos:first_end_pos]);
								ordered_data.append(data[first_end_pos:]);
							else:
								ordered_data.append(data[first_start_pos:first_end_pos]);
								ordered_data.append(data[first_end_pos:]);
					
				else:
					ordered_data.append(data);

				#print ordered_data;

				#print(ordered_data);
				# print('\n')
				#Printing the ordered data into the UI
				for i, entry in enumerate(ordered_data):
					entry.decode('utf-8')
					#print('\nstart\n' + entry + '\nend')
					#Removing em tags here prevents problems
					entry = re.sub('<em>|</em>', '', entry);
					#Removing all link tags, as we should be recording those before this loop
					#entry = re.sub('<a[\s|\S]*?>|</a>', '', entry);
					#Replacing </ul> and </li> with linebreaks, for readability, also removing <ul> and replacing <li> with bulletpoint
					entry = re.sub('</ul>', '\n', entry);
					entry = re.sub('<ul>', '', entry);
					entry = re.sub('<li>', u'\u2022 ', entry.decode('utf-8'));
					#Replacing &lt; and &gt; with corresponding symbols
					entry = re.sub('&lt;', '<', entry);
					entry = re.sub('&gt;', '>', entry);

					#print(entry.encode('utf-8'));
					#This takes care of data that is needing to be displayed in italics
					if re.findall('<blockquote>', style_check_string):

						#Replacing paragraph end tags with newlines for readability
						entry = re.sub('</p>', '\n', entry);
						#Removing blockquotes, we don't need them anymore
						entry = re.sub('<blockquote>|</blockquote>', '', entry);

						#Conditionals for bold text, strikethrough text, and default text
						if re.findall('<strong>', entry):

							#Handling nested <strong>'s
							if i > 0 and re.findall('^\n$', ordered_data[i-1]):
								entry = re.sub('</strong>', '\n', entry);
								entry = re.sub('<strong>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'italic-bold');
							else:
								entry = re.sub('</strong>', '', entry);
								entry = re.sub('<strong>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'italic-bold');

						elif re.findall('<span style="text-decoration: line-through;">', entry):

							entry = re.sub('<span style="text-decoration: line-through;">|</span>', '', entry);
							self.scpDataDisplay.insert(END, entry, 'strike-through');

						elif re.findall('</li>', entry):

							entry = re.sub('</li>', '\n', entry);
							self.scpDataDisplay.insert(END, entry, 'list');

						elif re.findall('</a>', entry):

							if re.findall('class="footnoteref"|class = "footnoteref"', entry):

								entry = re.sub('<a[\s|\S]*?>|</a>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'footnote-italic');

							else:

								link_url = re.findall('(?<=href=\")[\s|\S]*?(?=\")', entry);
								links.append(link_url[0]);
								entry = re.sub('<a[\s|\S]*?>|</a>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'link-italic');

						else:

							self.scpDataDisplay.insert(END, entry, 'italic');
					
					elif table_flag == True:

						self.createTable(entry);

					else:

						#Replacing paragraph end tags with newlines for readability
						entry = re.sub('</p>', '\n\n', entry);

						#Conditionals for bold text, strikethrough text, and default text
						#Bold
						if re.findall('<strong>', entry):
							
							#Handling nested <strong>'s
							if i > 0 and re.findall('^\n$', ordered_data[i-1]):
								entry = re.sub('</strong>', '\n', entry);
								entry = re.sub('<strong>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'bold');
							else:
								entry = re.sub('</strong>', '', entry);
								entry = re.sub('<strong>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'bold-default');

						#Strikethrough
						elif re.findall('<span style="text-decoration: line-through;"', entry):

							entry = re.sub('<span style="text-decoration: line-through;">|</span>', '', entry);
							self.scpDataDisplay.insert(END, entry, 'strike-through');

						#Lists
						elif re.findall('</li>', entry):

							entry = re.sub('</li>', '\n', entry);
							self.scpDataDisplay.insert(END, entry, 'list');

						elif re.findall('</a>', entry):

							if re.findall('class="footnoteref"|class = "footnoteref"', entry):

								entry = re.sub('<a[\s|\S]*?>|</a>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'footnote');

							else:

								link_url = re.findall('(?<=href=\")[\s|\S]*?(?=\")', entry);
								links.append(link_url[0]);
								entry = re.sub('<a[\s|\S]*?>|</a>', '', entry);
								self.scpDataDisplay.insert(END, entry, 'link-default');

						#Default
						else:

							self.scpDataDisplay.insert(END, entry, 'default');

			self.scpDataDisplay.config(state = DISABLED);

			try:
				self.scpRequestEntry.delete(0, END);
				self.scpRequestEntry.insert(END, scp_display_no);
			except UnboundLocalError:
				print('An incorrect format has been submitted into the request bar.')


			self.scpLinkDisplay.delete(0, END);
			for link in links:
				self.scpLinkDisplay.insert(END, link);

			print(footnotes)
			self.scpLinkDisplay.delete(0, END);
			for i, footnote in enumerate(footnotes):
				self.scpFootnoteDisplay.insert(END, str(i+1) + ':' + footnote);

			return;
		except urllib2.HTTPError:
			print('Request for SCP data retrieval denied!\nPrepare for involuntary amnesitic administration.');
			return;

###################################################################################################################################
#INIT function, very important
###################################################################################################################################

	def __init__(self, master=None):
		Frame.__init__(self, master, background='#424242')
		#self.style = ThemedStyle(self)
		#self.style.set_theme('black')
		color = '#424242'
		self.pack()
		self.createWidgets()
		for wid in self.allObjects:
			wid.configure(background = color)
			wid.configure(foreground = 'white')
		for wid in self.allTextAreas:
			wid.configure(background = '#232323')
			wid.configure(foreground = '#42ff58')

root = Tk()
root.title('SCPDB')
app = Application(master=root)
app.mainloop()
root.destroy()

# user_input = input('Retrieval Request: ');

# while user_input != 'exit':
# 	load_scp_data(user_input);

# 	user_input = input('Retrieval Request: ');

