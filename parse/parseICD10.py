#from django.db import models
#from mptt.models import MPTTModel, TreeForeignKey
import xml.etree.ElementTree as ET 


def add_children_ICD10(xml_root, ICD10_root):
	for child in xml_root:
		print child.tag 
		if (child.tag == 'inclusionTerm'):
			print 'There are inclusions term(s) for:', xml_root.find('name')
			# add these inclusion terms to ICD10 node
		elif (child.tag == 'excludes1'):
			print 'There are exclude 1 term(s) for:', xml_root.find('name')
			# add exclusion 1 terms to ICD10 node
		elif (child.tag == 'excludes2'):
			print 'There are exclude 2 term(s) for:', xml_root.find('name')
			# add exclusion 2 terms to ICD10 node 
		else :
			new_node = ICD10()
			code = child.find('name').text
			desc = child.find('desc').text
			new_node.add_code(code)
			new_node.add_description(desc)
			new_node.add_parent(ICD10_root)
			add_children_ICD10(child, new_node)
			#get name/description, get code (if there is one), get list of potential other references (<see> and <seeAlso>) check for children & get children
			# What format do we want this data in? 
			# nested loop for children/children of children 
			# code = term.find('code').text
			# name = term.get('title') #or description 


class Ontology(): #MPTTModel): 
	# the generalized ontology class. Will be speciflized into READCODE and ICD-10
	code = ''
	description = ''
	parent = ''
	def add_code(self, new_code):	
		code = new_code
	def add_description(self, new_desc):
		description = new_desc	
	def search(self, search_term):
		# see children classes for specific funtion
		print search_term
	def add_parent(self, new_parent):
		# ...
		parent = new_parent

	def get_parent(self):
		return parent 



class ICD10 (Ontology):
	code = ''
	description = ''
	parent = ''
	inclusion_terms = ''
	exclusion_terms = '' 
	def add_code(self, new_code):	
		code = new_code
	def add_description(self, new_desc):
		description = new_desc	
	def search(self, search_term):
		#...]
		print search_term
		if (search_term in exclusion_terms):
			return false
		elif ((search_term in description) or(search_term in code)):
			return true
		elif (search_term in inclusion_terms):
			return true
		else :
			return false
		print search_term
	def add_parent(self, new_parent):
		parent = new_parent 

class READCODE (Ontology):
	code = ''
	description = ''
	parent = ''
	def add_code(self, new_code):	
		code = new_code
	def add_description(self, new_desc):
		description = new_desc	
	def search(self, search_term):
		#...
		if ((search_term in code) or (search_term in description)):
			return true
		else :
			return false 

tree = ET. parse('ICD10CM_FY2014_Full_XML_Tabular.xml')
root = tree.getroot()

#root = ET.fromstring(ICD10CM_FY2014_Full_XML_Tabular_as_string) # root == ICD10CM.tabular 
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
			if (section.tag == 'section'):
				section_name = section.get('id')
				section_desc = section.find('desc').text
				ICD10_root = ICD10()
				add_children_ICD10(section, ICD10_root)
# want root.tag == 'section id'

