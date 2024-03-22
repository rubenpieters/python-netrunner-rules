import os

from rules_doc_generator.config import (Config)
from rules_doc_generator.model.text import (RefDict)
from rules_doc_generator.model.section import (Document)

def create_toc_html(id_map: RefDict):
  result = ''
  for id in id_map:
    ref_info = id_map[id]
    if ref_info.toc:
      result += f'<li><a href="#{ref_info.id}">{ref_info.reference} {ref_info.text}</a></li>'
  return result

def standalone_html(document: Document, config: Config, id_map: RefDict, opengraph: bool):
  result = '<?xml encoding="utf-8" ?><!DOCTYPE html><html><head>'
  result += '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible">'
  result += '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />'
  result += '<link rel="stylesheet" href="rules.css">'
  result += f'<title>Netrunner Comprehensive Rules (v{config.version_string()})</title>'
  if opengraph:
    result += '<script src="rules.js" defer></script>'
    result += '<link rel="stylesheet" href="extended.css">'
  result += '</head><body>'
  result += '<div class="RulesGrid">'
  result += f'<ul class="RulesToc">{create_toc_html(id_map)}</ul>'
  result += f'<div class="RulesContent">'
  result += '<div>'
  result += f'<p class="Title">Netrunner Comprehensive Rules</p>'
  result += f'<p class="SubTitle">Null Signal Games</p>'
  result += f'<p>This rules document is to be used as reference material. It is not intended to be read straight through. If you still have questions after consulting this document, please ask us online via <a href="mailto:rules@nullsignal.games">email</a>. This version of the Comprehensive Rules document is effective <b>{config.effective_date_str()}</b>.</p>'
  result += f'<details><summary>Summary of Changes (v{config.version_string()})</summary><ul>'
  for changelog_entry in document.changelog:
    result += f'<li>{changelog_entry.to_html(config, id_map)}</li>'
  result += '</ul></details>'
  result += '</div>'
  result += document.to_html(config, id_map)
  result += '</div>'
  result += '</div>'
  result += '</body></html>'
  return result

def standalone_latex(document: Document, config: Config, id_map: RefDict):
  result = document.to_latex(config, id_map)
  return result

def standalone_json(document: Document, config: Config, id_map: RefDict):
  result = '[\n'
  result += document.to_json(config, id_map)
  result += '\n]'
  return result

def write_to_file(folder: str, filename: str, content: str):
  os.makedirs(folder, exist_ok=True)
  file = open(os.path.join(folder, filename), 'w')
  file.write(content)
  file.close()
