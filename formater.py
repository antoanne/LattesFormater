# -*- coding: utf-8 -*-
"""
Created on Apr, 2019

Formatador de currículos Lattes em HTML seguindo template.html

@author: antoanne
"""
import glob, os
import xml.etree.ElementTree as ET
import csv

PATH = '/home/antoanne/FCRB/ExtratorLattes'
CVFolder = "curriculos"
HTMLFolder = "html"

URLPhoto = 'http://servicosweb.cnpq.br/wspessoa/servletrecuperafoto?id='

pessoas = []

class Pessoa():
    root = xml = link = id = nomeCompleto = ''
    instituicao = resumo = ''
    graduacao = mestrado = doutorado = especializacao = {}
    html = ''
    
    def __init__(self, xml):
        self.root = ''
        self.xml = ''
        self.html = ''
        self.link = ''
        self.id = ''
        self.nomeCompleto = ''
        self.instituicao = self.resumo = ''
        self.graduacao = {}
        self.especializacao = {}
        self.mestrado = {}
        self.mestradoProfissionalizante = {}
        self.doutorado = {}
        self.xml = xml
        self.link = self.xml.split('.')[0]
        self.loadFromXML()
        
    def loadFromXML(self):
        self.root = ET.parse(os.path.join(PATH, CVFolder, self.xml)).getroot()
        for data in self.root.findall("./DADOS-GERAIS"):
            self.nomeCompleto = data.attrib['NOME-COMPLETO'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL"):
            self.instituicao = data.attrib['NOME-INSTITUICAO-EMPRESA'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/RESUMO-CV"):
            self.resumo = data.attrib['TEXTO-RESUMO-CV-RH'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/GRADUACAO"):
            self.graduacao['INSTITUICAO'] = data.attrib['NOME-INSTITUICAO'].encode(encoding='UTF-8',errors='strict')
            self.graduacao['CONCLUSAO'] = data.attrib['ANO-DE-CONCLUSAO'].encode(encoding='UTF-8',errors='strict')
            self.graduacao['INICIO'] = data.attrib['ANO-DE-INICIO'].encode(encoding='UTF-8',errors='strict')
            self.graduacao['TITULO'] = data.attrib['TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO'].encode(encoding='UTF-8',errors='strict')
            self.graduacao['CURSO'] = data.attrib['NOME-CURSO'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/ESPECIALIZACAO"):
            self.especializacao['INSTITUICAO'] = data.attrib['NOME-INSTITUICAO'].encode(encoding='UTF-8',errors='strict')
            self.especializacao['CONCLUSAO'] = data.attrib['ANO-DE-CONCLUSAO'].encode(encoding='UTF-8',errors='strict')
            self.especializacao['INICIO'] = data.attrib['ANO-DE-INICIO'].encode(encoding='UTF-8',errors='strict')
            self.especializacao['TITULO'] = data.attrib['TITULO-DA-MONOGRAFIA'].encode(encoding='UTF-8',errors='strict')
            self.especializacao['CURSO'] = data.attrib['NOME-CURSO'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/MESTRADO"):
            self.mestrado['INSTITUICAO'] = data.attrib['NOME-INSTITUICAO'].encode(encoding='UTF-8',errors='strict')
            self.mestrado['CONCLUSAO'] = data.attrib['ANO-DE-CONCLUSAO'].encode(encoding='UTF-8',errors='strict')
            self.mestrado['INICIO'] = data.attrib['ANO-DE-INICIO'].encode(encoding='UTF-8',errors='strict')
            self.mestrado['TITULO'] = data.attrib['TITULO-DA-DISSERTACAO-TESE'].encode(encoding='UTF-8',errors='strict')
            self.mestrado['CURSO'] = data.attrib['NOME-CURSO'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/MESTRADO-PROFISSIONALIZANTE"):
            self.mestradoProfissionalizante['INSTITUICAO'] = data.attrib['NOME-INSTITUICAO'].encode(encoding='UTF-8',errors='strict')
            self.mestradoProfissionalizante['CONCLUSAO'] = data.attrib['ANO-DE-CONCLUSAO'].encode(encoding='UTF-8',errors='strict')
            self.mestradoProfissionalizante['INICIO'] = data.attrib['ANO-DE-INICIO'].encode(encoding='UTF-8',errors='strict')
            self.mestradoProfissionalizante['TITULO'] = data.attrib['TITULO-DA-DISSERTACAO-TESE'].encode(encoding='UTF-8',errors='strict')
            self.mestradoProfissionalizante['CURSO'] = data.attrib['NOME-CURSO'].encode(encoding='UTF-8',errors='strict')
        for data in self.root.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO"):
            self.doutorado['INSTITUICAO'] = data.attrib['NOME-INSTITUICAO'].encode(encoding='UTF-8',errors='strict')
            self.doutorado['CONCLUSAO'] = data.attrib['ANO-DE-CONCLUSAO'].encode(encoding='UTF-8',errors='strict')
            self.doutorado['INICIO'] = data.attrib['ANO-DE-INICIO'].encode(encoding='UTF-8',errors='strict')
            self.doutorado['TITULO'] = data.attrib['TITULO-DA-DISSERTACAO-TESE'].encode(encoding='UTF-8',errors='strict')
            self.doutorado['CURSO'] = data.attrib['NOME-CURSO'].encode(encoding='UTF-8',errors='strict')
            
    def __repr__(self):
        return('LINK=%r, NOME=%r' % (self.link, self.nomeCompleto))

    def asHTML(self, template):
        self.html = template
        if (self.id != None) :
            self.html = self.html.replace('[FOTO]',  (URLPhoto + self.id))
        else:
            self.html = self.html.replace('[FOTO]',  'headshot.jpg')
        self.html = self.html.replace('[NOME]', self.nomeCompleto)
        self.html = self.html.replace('[TITULO]', (self.nomeCompleto + ' - ' + self.instituicao))
        self.html = self.html.replace('[INSTITUICAO]', self.instituicao)
        self.html = self.html.replace('[RESUMO]', self.resumo)
        self.html = self.html.replace('[LINK]', self.link)
        
        if (self.graduacao != {}):
            self.html = self.html.replace('[GRADUACAO-DISPLAY]', 'block')
            self.html = self.html.replace('[GRADUACAO-CURSO]', self.graduacao['CURSO'])
            if (self.graduacao['CONCLUSAO'] != ''):
                self.html = self.html.replace('[GRADUACAO-ANO]', self.graduacao['INICIO'] + ' - ' + self.graduacao['CONCLUSAO'])
            else:
                self.html = self.html.replace('[GRADUACAO-ANO]', self.graduacao['INICIO'])
            self.html = self.html.replace('[GRADUACAO-INSTITUICAO]', self.graduacao['INSTITUICAO'])
            self.html = self.html.replace('[GRADUACAO-TITULO]', self.graduacao['TITULO'])
        else:
            self.html = self.html.replace('[GRADUACAO-DISPLAY]', 'none')

        if (self.especializacao != {}):
            self.html = self.html.replace('[ESPECIALIZACAO-DISPLAY]', 'block')
            self.html = self.html.replace('[ESPECIALIZACAO-CURSO]', self.especializacao['CURSO'])
            if (self.especializacao['CONCLUSAO'] != '') :
                self.html = self.html.replace('[ESPECIALIZACAO-ANO]', self.especializacao['INICIO'] + ' - ' + self.especializacao['CONCLUSAO'])
            else:
                self.html = self.html.replace('[ESPECIALIZACAO-ANO]', self.especializacao['INICIO'])
            self.html = self.html.replace('[ESPECIALIZACAO-INSTITUICAO]', self.especializacao['INSTITUICAO'])
            self.html = self.html.replace('[ESPECIALIZACAO-TITULO]', self.especializacao['TITULO'])
        else:
            self.html = self.html.replace('[ESPECIALIZACAO-DISPLAY]', 'none')
        
        if (self.mestrado != {}):
            self.html = self.html.replace('[MESTRADO-DISPLAY]', 'block')
            self.html = self.html.replace('[MESTRADO-CURSO]', self.mestrado['CURSO'])
            if (self.mestrado['CONCLUSAO'] != '') :
                self.html = self.html.replace('[MESTRADO-ANO]', self.mestrado['INICIO'] + ' - ' + self.mestrado['CONCLUSAO'])
            else:
                self.html = self.html.replace('[MESTRADO-ANO]', self.mestrado['INICIO'])
            self.html = self.html.replace('[MESTRADO-INSTITUICAO]', self.mestrado['INSTITUICAO'])
            self.html = self.html.replace('[MESTRADO-TITULO]', self.mestrado['TITULO'])
        else:
            self.html = self.html.replace('[MESTRADO-DISPLAY]', 'none')
            
        if (self.mestradoProfissionalizante != {}):
            self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-DISPLAY]', 'block')
            self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-CURSO]', self.mestradoProfissionalizante['CURSO'])
            if (self.mestradoProfissionalizante['CONCLUSAO'] != '') :
                self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-ANO]', self.mestradoProfissionalizante['INICIO'] + ' - ' + self.mestradoProfissionalizante['CONCLUSAO'])
            else:
                self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-ANO]', self.mestradoProfissionalizante['INICIO'])
            self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-INSTITUICAO]', self.mestradoProfissionalizante['INSTITUICAO'])
            self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-TITULO]', self.mestradoProfissionalizante['TITULO'])
        else:
            self.html = self.html.replace('[MESTRADO-PROFISSIONALIZANTE-DISPLAY]', 'none')
            
        if (self.doutorado != {}):
            self.html = self.html.replace('[DOUTORADO-DISPLAY]', 'block')
            self.html = self.html.replace('[DOUTORADO-CURSO]', self.doutorado['CURSO'])
            if (self.doutorado['CONCLUSAO'] != '') :
                self.html = self.html.replace('[DOUTORADO-ANO]', self.doutorado['INICIO'] + ' - ' + self.doutorado['CONCLUSAO'])
            else:
                self.html = self.html.replace('[DOUTORADO-ANO]', self.doutorado['INICIO'])
            self.html = self.html.replace('[DOUTORADO-INSTITUICAO]', self.doutorado['INSTITUICAO'])
            self.html = self.html.replace('[DOUTORADO-TITULO]', self.doutorado['TITULO'])
        else:
            self.html = self.html.replace('[DOUTORADO-DISPLAY]', 'none')
        
        return(self.html)
    
class Reader():
    html = ''
    lista = []
    def __init__(self):
        self.XMLList = self.loadXML()
        self.lista = self.loadCSV()
        self.html = self.loadHTMLTemplate()

    def loadXML(self):
        os.chdir(os.path.join(PATH, CVFolder))
        XMLList = glob.glob("*.xml")
        return XMLList
    
    def loadCSV(self):
        os.chdir(os.path.join(PATH))
        csvFile = open('lista.csv', mode='r')
        for row in csv.DictReader(csvFile):
            self.lista.append(row)
        return self.lista
    
    def getIDfromCSV(self, link):
        for item in self.lista:
            if (item['link'] == link):
                return item['id']
        return None
    
    def loadHTMLTemplate(self):
        os.chdir(os.path.join(PATH, HTMLFolder))
        return open('template.html', 'r').read()
    
    def saveHTML(self, id, html):
        os.chdir(os.path.join(PATH, HTMLFolder))
        file = open(id + '.html', 'w')
        file.writelines(html)
        file.close()

def main():
    reader = Reader()
    for cv in reader.XMLList:
        pessoa = Pessoa(cv)
        pessoa.id = reader.getIDfromCSV(pessoa.link)
        pessoas.append(pessoa)
        reader.saveHTML(pessoa.link, pessoa.asHTML(reader.html))
        print(pessoa)

if __name__ == '__main__':
    main()