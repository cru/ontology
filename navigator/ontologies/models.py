from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Ontology(MPTTModel): 
	# the generalized ontology class. Will be speciflized into READCODE and ICD-10
	code = "no code yet"
	description = "no description yet"
	parent = TreeForeignKey('self', null=True, blank=True, related_name="children")
	index = models.SlugField()

	class MPTTMeta:
		order_insertion_by = ['index']
		#app_label = "sites"

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