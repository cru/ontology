#from django.db import models
#from mptt.models import MPTTModel, TreeForeignKey
import xml.etree.ElementTree as ET 


def add_children_ICD10(xml_root, ICD10_root):
	i = 0
	for child in xml_root:
		i = i + 1
		#print child.tag 
		#print "i = ", i 
		if (child.tag == 'inclusionTerm'):
			#print 'There are inclusions term(s) for:', xml_root.find('name')
			# add the inclusion terms to ICD10 node
			# .findall('note') finds all the inclusion terms for the node and stores them as a list
			incl_terms = child.findall('note')
			i = 0
			# for each term in the list add the term to the ICD10 node's inclusion terms
			for term in incl_terms:
				i = i+1
				#print "i: ",i,"term: ",term.text
				#print incl_term
				ICD10_root.add_inclusion_term(term.text)

		elif (child.tag == 'excludes1'):
			#print 'There are exclude 1 term(s) for:', xml_root.find('name')
			# add exclusion 1 terms to ICD10 node
			excl_terms = child.findall('note')
			#print excl_term
			i = 0
			for term in excl_terms:
				i = i + 1
				#print "i: ",i,"term: ",term.text
				ICD10_root.add_exclusion_terms_1(term.text)


		elif (child.tag == 'excludes2'):
			#print 'There are exclude 2 term(s) for:', xml_root.find('name')
			# add exclusion 2 terms to ICD10 node
			excl_terms = child.findall('note')
			#print excl_term
			i = 0
			for term in excl_terms:
				i = i + 1
				#print "i: ",i,"term: ",term.text
				ICD10_root.add_exclusion_terms_2(term.text)

		elif (child.tag == 'desc'):
			#print 'This is a description child' 
			# add description to ICD10 node ?? -- adding to root node
			desc = xml_root.find('desc').text
			#print "desc: ",desc 
			#desc = child.get('desc')
			#print desc 
			ICD10_root.add_description(desc)
		elif (child.tag == 'name'):	
			# checks to see if there is a 'name' tag, and if there is adds the text value of this 
			# 'name' child to the ICD10_root's code via .add_code(new_code)
			#print 'This is a name child' 
			code = xml_root.find('name').text
			ICD10_root.add_code(code)
			#print "Code: ", code 
			# add exclusion 2 terms to ICD10 node 
		elif (child.tag == 'diag'):
			# checks to see if the child's tag is 'diag' (indicates a child node)
			# creates a new ICD10() node, adds the current node as the parent of the new node
			new_node = ICD10()
			new_node.add_parent(ICD10_root)
			#print "calling another add_children_ICD10() (tag = diag)"
			# calls add_children_ICD10(xml_child, new_ICD10_child) to add the attributes code, description,
			# etc. to the new child node. 
			new_node = add_children_ICD10(child, new_node)
			#print "*********************************************************"
			#print "child description: ", new_node.get_description()
			#print "child code: ", new_node.get_code()
			#print "child inclusion terms: ", new_node.get_inclusion_terms()
			#print "child exclusion_terms_1: ", new_node.get_exclusion_terms_1()
			#print "child exclusion_terms_2: ", new_node.get_exclusion_terms_2()
			#print "**********************************************************"
		else :
			#print child.tag
			print "Taking no other actions. -- tag = ",child.tag
			#code = child.find('name').text
			#desc = child.find('desc').text
			#new_node.add_code(code)
			#new_node.add_description(desc)
			#new_node.add_parent(ICD10_root)
			#print "calling another add_children_ICD10()"
			#add_children_ICD10(child, new_node)
			#get name/description, get code (if there is one), get list of potential other references (<see> and <seeAlso>) check for children & get children
			# What format do we want this data in? 
			# nested loop for children/children of children 
			# code = term.find('code').text
			# name = term.get('title') #or description 
		#x = raw_input("end of child")
	#print "\t\t description: ",ICD10_root.get_description()
	#print "\t\t code: ",ICD10_root.get_code()	
	ICD10_list.append(ICD10_root)
	return ICD10_root

# ** Watch for sevenChrNote, SevenChrDef... 




class Ontology(): #MPTTModel): 
	# the generalized ontology class. Will be speciflized into READCODE and ICD-10
	code = "no code yet"
	description = "no description yet"

	#parent = ''
	def add_code(self, new_code):	
		self.code = new_code
		#print "adding a new code//////////////////////////////////////"
	def add_description(self, new_desc):
		self.description = new_desc	
		#print "adding a new description///////////////////////////////"
	def search(self, search_term):
		# see children classes for specific funtion
		print "searching for: ",search_term
	def add_parent(self, new_parent):
		# ...
		self.parent = new_parent

	def get_parent(self):
		return self.parent 
	def get_code(self):
		#print "returning code: ",self.code
		return self.code
	def get_description(self):
		#print "returning description: ", self.description
		return self.description 




class ICD10 (Ontology):
	#code = ''
	#description = ''
	#parent = ''
	inclusion_terms = ""
	exclusion_terms_1 = "" 
	exclusion_terms_2 = "" 
	def add_code(self, new_code):	
		self.code = new_code
		#print "adding a new code////////////////////////////////////// = ",self.code

	def add_description(self, new_desc):
		self.description = new_desc	
		#print "adding a new description/////////////////////////////// = ", self.description

	def search(self, search_term):
		#...]
		#print search_term
		if (search_term in self.exclusion_terms_1) or (search_term in self.exclusion_terms_2) :
			return False
		elif ((search_term in self.description) or(search_term in self.code)):
			return True
		elif (search_term in self.inclusion_terms):
			return True
		else :
			return False
		#print search_term
	def add_parent(self, new_parent):
		self.parent = new_parent 
	def add_inclusion_term(self, new_term):
		self.inclusion_terms = self.inclusion_terms + ", "+new_term
		# appends a new inclusion term to the end of the current inclusion terms
	def add_exclusion_terms_1(self, new_term):
		self.exclusion_terms_1 = self.exclusion_terms_1 + ", " + new_term 
		# appends a new exclusion term 1 to the end of the current exclusion terms 1
	def add_exclusion_terms_2(self, new_term):
		self.exclusion_terms_2 = self.exclusion_terms_2 + ", " + new_term 
		# appends a new exclusion term 2 to the end of the current exclusion terms 2
	#def get_description(self):
	#	return description 
	def get_inclusion_terms(self):
		return self.inclusion_terms
	def get_exclusion_terms_1(self):
		return self.exclusion_terms_1
	def get_exclusion_terms_2(self):
		return self.exclusion_terms_2

class READCODE (Ontology):
	#code = ''
	#description = ''
	#parent = ''
	def add_code(self, new_code):	
		self.code = new_code
	def add_description(self, new_desc):
		self.description = new_desc	
	def search(self, search_term):
		#...
		if ((search_term in self.code) or (search_term in self.description)):
			return true
		else :
			return false 

tree = ET. parse('ICD10CM_FY2014_Full_XML_Tabular.xml')
root = tree.getroot()
x = raw_input('hit enter') 
#root = ET.fromstring(ICD10CM_FY2014_Full_XML_Tabular_as_string) # root == ICD10CM.tabular 
ICD10_list = []
for child in root:
	print child.tag 
	if (child.tag == 'introduction'):
		# ?? do we want to save any of this info?
		print 'introduction'
	if (child.tag == 'chapter'):
		# get nodes from chapters
		# want to divide it up by section (should section headers be their own node?)
		print 'chapter'
		chapter_desc = child.get('desc')
		for section in child:
			#x = raw_input('hit enter')
			if (section.tag == 'section'):
				#print "section"
				section_name = section.get('id')
				print "section name:", section_name
				section_desc = section.find('desc').text
				print "section description:", section_desc
				ICD10_root = ICD10()
				ICD10_root = add_children_ICD10(section, ICD10_root)
				ICD10_list.append(ICD10_root)
y = raw_input("Hit enter to continue")
for node in ICD10_list:
	print "there is a child: ",node.get_code()
print "done. "
x = raw_input("enter a search term: ")
while x != "done":
	#x = raw_input("enter a search term: ")
	search_list = []
	for node in ICD10_list:
		if node.search(x) == True :
			search_list.append(node)
			print "a node was added. "

	y = raw_input("Finished searching. Hit enter to continue.")
	print "\n\n The term searched for is: ",x,"\n The results are: "
	for node in search_list:
		print "\tCode: ",node.get_code(),"\t Description: ",node.get_description()
	x = raw_input("enter a search term: ")
print "done"



# want root.tag == 'section id'

