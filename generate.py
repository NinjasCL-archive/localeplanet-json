#!/usr/bin/python
# 
# python 2.7
# generate.py
# output json for locale files from localeplanet.com
# December 2015 
# https://github.com/NinjasCL/localeplanet-json
# Camilo Castro <camilo@ninjas.cl>
# MIT LICENCE

import json
import os
import urllib2


print "Cleaning Up"

print "Removing locales dir ", os.system("rm -rf ./locales")
print "Removing locales json dir ", os.system("rm -rf ./locales_json")
print "Removing locales node dir ", os.system("rm -rf ./locales_node")

print "Creating locales dir ", os.system("mkdir ./locales")
print "Creating locales json dir ", os.system("mkdir ./locales_json")
print "Creating locales node dir ", os.system("mkdir ./locales_node")

print "Downloading locales from localeplanet ", os.system("python ./lpmirror.py")
print "Moving files to locales dir ", os.system("mv ./icu_* ./locales")

print "Begin Creating JSON Files"

locales = []

f = urllib2.urlopen("http://www.localeplanet.com/api/codelist.json")
str_list = f.read()
f.close()

locales = json.loads(str_list)

for locale in locales:
	
	print "Working With", locale

	name = 'icu_{locale}'.format(locale=locale)

	script = '{name}.js'.format(name=name)
	json = '{name}.json'.format(name=name)
	

	f = open("./locales/" + script, "r")
	js = f.read()
	f.close()


	print "Replacing the Code for Compatibility with NodeJS"

	js = js.replace("(function() {","")
	js = js.replace("window.icu = window.icu || new Object();","")
	js = js.replace("var icu = window.icu;","var icu = {};")
	js = js.replace("var df =", "// var df =")
	js = js.replace("icu.getDateFormat = ", "// icu.getDateFormat = ")
	js = js.replace("icu.getLocaleName","icu.getLocaleUnderscore = function(){ " \
		"return icu.getLocale().replace('-','_') }; icu.getLocaleName")

	functionOutput = """
	var locale = {};
	locale.country = icu.getCountry();
	locale.countryName = icu.getCountryName();

	locale.dateFormatSymbols = icu.getDateFormatSymbols();

	locale.decimalFormatSymbols = icu.getDecimalFormatSymbols();


	locale.languageCode = icu.getLanguage();
	locale.languageName = icu.getLanguageName();
	locale.locale = icu.getLocale();
	locale.localeUnderscore = icu.getLocaleUnderscore();
	locale.localeName = icu.getLocaleName();

	console.log(JSON.stringify(locale));
	"""

	js = js.replace("})();", functionOutput)

	nodeJSFile = "./locales_node/{js}".format(js=script)

	f = open(nodeJSFile, "w")
	f.write(js)
	f.close()

	print "Executing NodeJS for Getting JSON"
	command = "node {nodejs} > ./locales_json/{json}".format(nodejs=nodeJSFile, json=json)
	print command, os.system(command)

print "Jobs Done"