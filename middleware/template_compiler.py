import os
import sys
from pathlib import Path
import pypugjs
import jinja2
import datetime

class TemplateCompiler():
  def __init__(self):
    self.templateDir = str(Path.cwd()) + '/templates/' 
    self.templateLoader = jinja2.FileSystemLoader(searchpath=self.templateDir)
    self.templateEnv = jinja2.Environment(loader=self.templateLoader,extensions=['pypugjs.ext.jinja.PyPugJSExtension'])		
    self.ROOT_TEMPLATE = "mail_temp.pug"

  def compile(self,templateName,templateOptions):
    templateName = templateName+".pug"
    self.template = self.templateEnv.get_template(templateName)
    templateNameOutput = self.template.render(**templateOptions)
    now = datetime.datetime.now()	
    template = self.templateEnv.get_template(self.ROOT_TEMPLATE)
    outputText = template.render(contentstring=templateNameOutput,currentyear=now.year)
    return outputText