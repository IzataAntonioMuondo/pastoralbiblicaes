import datetime
import re
import json
import threading
import logging
import requests
from bs4 import BeautifulSoup
import flet as ft
import datetime
import os
#Para imprimir em pdf devermos importar as seguintes bibliotecas:
#################################################################################
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line                                             #
from reportlab.lib.pagesizes import letter                                      #
from reportlab.lib import colors as cores                                                #
from reportlab.lib.styles import getSampleStyleSheet                            #
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table, TableStyle #
                                , Spacer, Image as imagemPDF)                                       #
#################################################################################
import sqlite3
from random import randint
from fletCalendar import *
from myckeck import MyCheckbox
conn = sqlite3.connect('db/membro.db', check_same_thread = False)
conecta_cursta = sqlite3.connect('db/cursista.db', check_same_thread = False)
conecta_actividade = sqlite3.connect('db/actividade.db', check_same_thread = False)
conecta_cargo = sqlite3.connect('db/cargo.db', check_same_thread = False)

tb = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de nascimento')), 
        ft.DataColumn(ft.Text('Genero')),   
        ft.DataColumn(ft.Text('Morada')), 
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('E-mail')),
    ], 
    rows=[]

)

tb_membro = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Contacto')),
    ],
    rows=[]
)

tb_membro_dataNasc = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de nascimento')), 
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('E-mail')),
        ft.DataColumn(ft.Text('Idade')),
    ],
    rows=[]
)

tb_membro_directivos = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Cargo')), 
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('E-mail')), 
    ],
    rows=[]
)

tb_membro_sacramentos = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Sacramentos')), 
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('E-mail')), 
    ],
    rows=[]
)

tb_membro_quotas = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome do Membro')),
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('Mêses Pagos')),
        ],
    rows=[]
)

tb_cursita = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Paróquia')),
        ft.DataColumn(ft.Text('Centro')),
        ft.DataColumn(ft.Text('Curso')),
        ft.DataColumn(ft.Text('Data de início')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Nota final')),
    ],
    rows=[]
)

tb_actividade = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de início')),
        ft.DataColumn(ft.Text('Hora de início')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Hora de término')),
        ft.DataColumn(ft.Text('Local')),
        ft.DataColumn(ft.Text('Status')),
    ],
    rows=[]
)

tb_actividade_em_andamento = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de início')),
        ft.DataColumn(ft.Text('Hora de início')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Hora de término')),
        ft.DataColumn(ft.Text('Local')),
        ft.DataColumn(ft.Text('Status')),
    ],
    rows=[]
)

tb_actividade_concluida = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de início')),
        ft.DataColumn(ft.Text('Hora de início')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Hora de término')),
        ft.DataColumn(ft.Text('Local')),
        ft.DataColumn(ft.Text('Status')),
    ],
    rows=[]
)

tb_membro_promessa = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('Data da promessa')),
    ],
    rows=[]
)

tb_membro_leitura = ft.DataTable( 
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Data')), 
        ft.DataColumn(ft.Text('Tempo Litúrgico')), 
        ft.DataColumn(ft.Text('Primeria Leitura')), 
        ft.DataColumn(ft.Text('Salmo')), 
        ft.DataColumn(ft.Text('Segunda Leitura')), 
        ft.DataColumn(ft.Text('Evangelho')), 
    ],
    rows=[], 
)
def capitalize_first_letter(e):
        e.control.value = e.control.value.title()
        e.control.update()

id_edit_membro = ft.Text()
nome_edit_membro = ft.TextField(label='Nome completo', on_change=capitalize_first_letter,prefix_icon=ft.icons.PERSON, width=790)

cal_date_birth = SetCalendar(update_callback=None, start_year=2015)
date_birth = DateSetUp(cal_grid=cal_date_birth)

calendar_container = Container()

open_calendar_button = OpenCalendarButton(date_birth, calendar_container, date_birth.get_selected_date())
data_nasc_edit_membro = cal_date_birth.output_date_label(1)
genero_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Masculino', label='Masculino'),
        ft.Radio(value='Feminino', label='Feminino')
    ])
]))
morada_edit_membro = ft.TextField(
    label='Morada', 
    hint_text='Exemplo: Sagrada Esperança, Prenda, Luanda', 
    prefix_icon=ft.icons.HOUSE, 
    helper_text='Segue a ordem: Rua, Bairro, Município', 
    width=790, 
    on_change=capitalize_first_letter
)

def on_input_change(e):
    if e.control.value.isnumeric():
        e.control.value = ''.join(filter(str.isnumeric, e.control.value))
        if len(e.control.value) > 9:
            e.control.value = e.control.value[:9]  # Trunca para apenas nove dígitos
            e.control.update()
    else:
        e.control.value = ''
        e.control.update()

contacto_edit_membro = TextField(
    label="Contacto",
    on_change=on_input_change,
    width=250,
    prefix_icon=icons.PHONE,
    hint_text='Exemplo: 929078877',
)
def on_email_change(e):
    email = e.control.value
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(padrao, email):
        e.control.error = None
        e.control.value = e.control.value.lower()
        e.control.color=colors.BLACK
        e.control.update()
    else:
        #e.control.error = "Formato de e-mail inválido"
        e.control.color=colors.RED
        e.control.update()

email_edit_membro = ft.TextField(label='E-mail',hint_text='Exemplo: pastoralbiblica@gmail.com', on_change=on_email_change, prefix_icon=ft.icons.EMAIL, width=350)
moradia_edit_membro = ft.Dropdown(options=[
        ft.dropdown.Option("Com os pais"),
        ft.dropdown.Option("Com o tio"),
        ft.dropdown.Option("Com o tia"),
        ft.dropdown.Option("Com avó"),
        ft.dropdown.Option("Com os irmãos"),
        ft.dropdown.Option("Com irmão"),
        ft.dropdown.Option("Com irmã"),
        ft.dropdown.Option("No lar"),
        ft.dropdown.Option("Sozinho"),
        ft.dropdown.Option("Outra situação"),
    ], width=170, label='Com quem vive?', prefix_icon=icons.FAMILY_RESTROOM
)

def on_frequenta_escola_change(e):
    if e.control.value == 'Sim':
        estuda_sabado_edit_membro.disabled = False
        curso_acad_edit_membro.disabled = False
        estuda_sabado_edit_membro.update()
        curso_acad_edit_membro.update()
    else:
        estuda_sabado_edit_membro.disabled = True
        curso_acad_edit_membro.disabled = True
        estuda_sabado_edit_membro.update()
        curso_acad_edit_membro.update()

frequenta_escola_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), on_change=on_frequenta_escola_change)
frequenta_escola_edit_membro.value = 'Não'
estuda_sabado_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]),  disabled=True)
curso_acad_edit_membro = ft.TextField(label='Curso', width=400, disabled = True, prefix_icon=ft.icons.BOOK)

def on_trabalhador_change(e):
    if e.control.value == 'Sim':
        local_trabalho_edit_membro.disabled = False
        funcao_edit_membro.disabled = False
        trabalha_fim_sem_edit_membro.disabled = False
        local_trabalho_edit_membro.update()
        funcao_edit_membro.update()
        trabalha_fim_sem_edit_membro.update()
    else:
        local_trabalho_edit_membro.disabled = True
        funcao_edit_membro.disabled = True
        trabalha_fim_sem_edit_membro.disabled = True
        local_trabalho_edit_membro.update()
        funcao_edit_membro.update()
        trabalha_fim_sem_edit_membro.update()

trabalhador_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), on_change=on_trabalhador_change)
trabalhador_edit_membro.value = 'Não'
local_trabalho_edit_membro = ft.TextField(label='Onde trabalha?', width=400, disabled = True)
funcao_edit_membro = ft.TextField(label='Em que área ou função trabalha?', width=400, disabled = True)
trabalha_fim_sem_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), disabled = True)

def on_catequese_change(e):
    if catecumeno_edit_membro.value=='Sim':
        n_f_catequese_edit_membro.disabled = True
        n_f_catequese_edit_membro.update()
    else:
        n_f_catequese_edit_membro.disabled = False
        n_f_catequese_edit_membro.update()
    

catecumeno_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não'),
        ft.Radio(value='Já não frequento', label='Já não frequenta')
    ])
]), on_change=on_catequese_change)
catecumeno_edit_membro.value = 'Sim'


n_f_catequese_edit_membro = ft.TextField(label='Nunca frequentou ou se já não frequenta, porquê?', width=400, disabled=True)
opcoes = [       
        ft.dropdown.Option('1 mês'),
        ft.dropdown.Option('2 mêses'),
        ft.dropdown.Option('3 mêses'),
        ft.dropdown.Option('4 mêses'),
        ft.dropdown.Option('5 mêses'),
        ft.dropdown.Option('6 mêses'),
        ft.dropdown.Option('7 mêses'),
        ft.dropdown.Option('8 mêses'),
        ft.dropdown.Option('9 mêses'),
        ft.dropdown.Option('10 mêses'),
        ft.dropdown.Option('11 mêses'),
        ft.dropdown.Option('1 ano'),
        ft.dropdown.Option('2 anos'),
        ft.dropdown.Option('3 anos'),
        ft.dropdown.Option('4 anos'),
        ft.dropdown.Option('5 anos'),
        ft.dropdown.Option('6 anos'),
        ft.dropdown.Option('7 anos'),
        ft.dropdown.Option('8 anos'),
        ft.dropdown.Option('9 anos'),
        ft.dropdown.Option('10 anos'),
        ft.dropdown.Option('11 anos'),
        ft.dropdown.Option('12 anos'),
        ft.dropdown.Option('13 anos'),
        ft.dropdown.Option('14 anos'),
        ft.dropdown.Option('15 anos'),
        ft.dropdown.Option('16 anos'),
        ft.dropdown.Option('17 anos'),
        ft.dropdown.Option('18 anos'),
        ft.dropdown.Option('19 anos'),
        ft.dropdown.Option('20 anos'),
        ft.dropdown.Option('21 anos'),
        ft.dropdown.Option('22 anos'),
        ft.dropdown.Option('23 anos'),
        ft.dropdown.Option('24 anos'),
        ft.dropdown.Option('25 anos')

        ]
def on_change_tempo(e):
    data = e.control.value 
    if (data == '1 mês' or '2 mêses' or '3 mêses' 
        or '4 mêses' or '5 mêses' or '6 mêses' or '7 mêses'
        or '8 mêses'or '9 mêses' or '10 mêses' or '11 mêses'): 
        ano_entrada_edit_membro.value = '2023'
        ano_entrada_edit_membro.update()
    if data == '1 ano':
        ano_entrada_edit_membro.value = '2022'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '2 anos':
        ano_entrada_edit_membro.value = '2021'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '3 anos':
        ano_entrada_edit_membro.value = '2020'
        ano_entrada_edit_membro.update()
        e.control.update()    
    if data == '4 anos':
        ano_entrada_edit_membro.value = '2019'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '5 anos':
        ano_entrada_edit_membro.value = '2018'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '6 anos':
        ano_entrada_edit_membro.value = '2017'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '7 anos':
        ano_entrada_edit_membro.value = '2016'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '8 anos':
        ano_entrada_edit_membro.value = '2015'
        ano_entrada_edit_membro.update()
        e.control.update()    
    if data == '9 anos':
        ano_entrada_edit_membro.value = '2014'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '10 anos':
        ano_entrada_edit_membro.value = '2013'
        ano_entrada_edit_membro.update()
        e.control.update() 
    if data == '11 anos':
        ano_entrada_edit_membro.value = '2012'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '12 anos':
        ano_entrada_edit_membro.value = '2011'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '13 anos':
        ano_entrada_edit_membro.value = '2010'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '14 anos':
        ano_entrada_edit_membro.value = '2009'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '15 anos':
        ano_entrada_edit_membro.value = '2008'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '16 anos':
        ano_entrada_edit_membro.value = '2007'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '17 anos':
        ano_entrada_edit_membro.value = '2006'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '18 anos':
        ano_entrada_edit_membro.value = '2005'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '19 anos':
        ano_entrada_edit_membro.value = '2004'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '20 anos':
        ano_entrada_edit_membro.value = '2003'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '21 anos':
        ano_entrada_edit_membro.value = '2002'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '22 anos':
        ano_entrada_edit_membro.value = '2001'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '23 anos':
        ano_entrada_edit_membro.value = '2000'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '24 anos':
        ano_entrada_edit_membro.value = '1999'
        ano_entrada_edit_membro.update()
        e.control.update()
    if data == '25 anos':
        ano_entrada_edit_membro.value = '1998'
        ano_entrada_edit_membro.update()
        e.control.update()

tempo_grupo_edit_membro = ft.Dropdown(
    options=opcoes,
    label="Tempo no Grupo",
    width=315,
    on_change=on_change_tempo
)
tempo_grupo_edit_membro.value = '1 mês'

ft.TextField(label='Tempo no grupo', width=315)

def on_change_ano(e):
    data = e.control.value 
    if data == '2022':
        tempo_grupo_edit_membro.value = '1 ano'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2021':
        tempo_grupo_edit_membro.value = '2 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2020':
        tempo_grupo_edit_membro.value = '3 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()    
    if data == '2019':
        tempo_grupo_edit_membro.value = '4 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2018':
        tempo_grupo_edit_membro.value = '5 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2017':
        tempo_grupo_edit_membro.value = '6 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2016':
        tempo_grupo_edit_membro.value = '7 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2015':
        tempo_grupo_edit_membro.value = '8 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()    
    if data == '2014':
        tempo_grupo_edit_membro.value = '9 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2013':
        tempo_grupo_edit_membro.value = '10 anos'
        tempo_grupo_edit_membro.update()
        e.control.update() 
    if data == '2012':
        tempo_grupo_edit_membro.value = '11 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2011':
        tempo_grupo_edit_membro.value = '12 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2010':
        tempo_grupo_edit_membro.value = '13 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2009':
        tempo_grupo_edit_membro.value = '14 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2008':
        tempo_grupo_edit_membro.value = '15 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2007':
        tempo_grupo_edit_membro.value = '16 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2006':
        tempo_grupo_edit_membro.value = '17 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2005':
        tempo_grupo_edit_membro.value = '18 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2004':
        tempo_grupo_edit_membro.value = '19 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2003':
        tempo_grupo_edit_membro.value = '20 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2002':
        tempo_grupo_edit_membro.value = '21 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2001':
        tempo_grupo_edit_membro.value = '22 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '2000':
        tempo_grupo_edit_membro.value = '23 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '1999':
        tempo_grupo_edit_membro.value = '24 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '1998':
        tempo_grupo_edit_membro.value = '25 anos'
        tempo_grupo_edit_membro.update()
        e.control.update()
    if data == '1998':
        tempo_grupo_edit_membro.value = '1 mês'
        tempo_grupo_edit_membro.update()
        e.control.update()

opcoes_anos_entrada = [ft.dropdown.Option(str(ano)) for ano in range(2023, 1997, -1)]
ano_entrada_edit_membro = ft.Dropdown(options=opcoes_anos_entrada, label='Ano de entrada', width=315, on_change=on_change_ano)
    

tem_cargo_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), )
tem_cargo_edit_membro.value = 'Não'

cargos_edit_membro = ft.Text()
def on_checkbox_click(e):
    # Atualiza a lista de cargos selecionados
        selected_cargos.clear()
        for checkbox in checkboxes:
            if checkbox.label=='Coordenador':
                checkbox.value = True
                selected_cargos.append('Coordenador')
            elif checkbox.label=='Vice-Coordenador':
                selected_cargos.append('Vice-Coordenador')
            elif checkbox.label=='Secretário':
                selected_cargos.append('Vice-secretário')
        cargos_edit_membro.value = f'{selected_cargos}'

def on_buscar_click(e):
    # Limpa a tabela antes de adicionar novos membros
    tb_membro_dataNasc.rows.clear()

    # Chama a função para buscar membros pelos cargos selecionados
    chamar_db_por_cargos(selected_cargos)

# Lista de cargos disponíveis
cargos_disponiveis = [
    "Coordenador", "Vice-Coordenador", "Secretário","Vice-secretário", "Tesoureiro",
    "Vice-tesoureiro","Responsável pela infância Bíblica","Responsável pela comunicação social", 
    "Responsável pelo Desporto", "Responsável pela caridade e convívio","Responsável pelos Cursos Bíblicos", 
    "Responsável pelos materiais","Conselheiro", 'Outros cargos'
]

# Lista para manter os cargos selecionados
selected_cargos = []

# Cria as checkboxes e adiciona ao layout
checkboxes = []
for cargo in cargos_disponiveis:
    checkbox = ft.Checkbox(label=cargo)
    #value = ckeckbox.
    checkboxes.append(checkbox)


column = ft.Column(controls=checkboxes)

cargos_membro = ft.Container(column, on_click=on_checkbox_click)

sacra_baptismo_edit_membro = ft.Checkbox(label="Baptismo", width=150, disabled = True)
sacra_crisma_edit_membro = ft.Checkbox(label="Crisma", width=150, disabled = True)
sacra_penitencia_edit_membro = ft.Checkbox(label="Penitência", disabled = True)
sacra_casamento_edit_membro = ft.Checkbox(label="Casamento", disabled = True)

def on_sacramento_change(e):
    if e.control.value == 'Sim':
        sacra_baptismo_edit_membro.disabled = False
        sacra_crisma_edit_membro.disabled = False
        sacra_penitencia_edit_membro.disabled = False
        sacra_casamento_edit_membro.disabled = False
        sacra_baptismo_edit_membro.update()
        sacra_crisma_edit_membro.update()
        sacra_penitencia_edit_membro.update()
        sacra_casamento_edit_membro.update()
    else:
        sacra_baptismo_edit_membro.disabled = True
        sacra_crisma_edit_membro.disabled = True
        sacra_penitencia_edit_membro.disabled = True
        sacra_casamento_edit_membro.disabled = True
        sacra_baptismo_edit_membro.update()
        sacra_crisma_edit_membro.update()
        sacra_penitencia_edit_membro.update()
        sacra_casamento_edit_membro.update()
        
tem_sacramento_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), on_change=on_sacramento_change)
tem_sacramento_edit_membro.value = 'Não'


cal_date_promise = SetCalendar(update_callback=None, start_year=2022)
date_promise = DateSetUp(cal_grid=cal_date_promise)

calendar_container_promise = Container()

open_calendar_button_promise = OpenCalendarButton(date_promise, calendar_container_promise, date_promise.get_selected_date())

data_promessa_edit_membro = cal_date_promise.output_date_label(2) 
column_promise = Column(
    alignment=MainAxisAlignment.CENTER,
    controls=[
        open_calendar_button_promise,
        calendar_container_promise,
    ], disabled=True
)


def on_promessa_change(e):
    
    if e.control.value == 'Não':
        e.control.value = 'Não'
        column_promise.disabled = True
        column_promise.update()
    else:
        column_promise.disabled = False
        column_promise.update()

tem_promessa_edit_membro = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Sim', label='Sim'),
        ft.Radio(value='Não', label='Não')
    ])
]), on_change=on_promessa_change)
tem_promessa_edit_membro.value = 'Não'
column = Column(
        alignment=MainAxisAlignment.CENTER,
        controls=[
            open_calendar_button,
            calendar_container,
        ]
    )
#opcoes_anos_promessa = [ft.dropdown.Option(str(ano)) for ano in range(2023, 1997, -1)]  # Adapte o intervalo de anos conforme necessário




id_edit_cursista = ft.Text()
nome_edit_cursista = ft.TextField(label='Nome do cursista')
paroquia_edit_cursista = ft.TextField(label='Paróquia', read_only=True, value="São Pedro Apóstolo")
centro_edit_cursista = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Arcanjo Gabriel', label='Arcanjo Gabriel'), ft.Radio(value='Espírito Santo', label='Espírito Santo'),
        ft.Radio(value='Santa Terezinha do Menino Jesus', label='Santa Terezinha do Menino Jesus'), ft.Radio(value='São Pedro Apóstolo', label='São Pedro Apóstolo')
    ])
]))
curso_edit_cursista = ft.Dropdown(options=[
        ft.dropdown.Option("Conceitos Gerais da Bíblia"),
        ft.dropdown.Option("São Pedro"),
        ft.dropdown.Option("São Lucas"),
        ft.dropdown.Option("Carta aos Coríntios"),
        ft.dropdown.Option("Carta de Pedro"),
    ],
)
hoje = datetime.date.today()
datas = [hoje - datetime.timedelta(days=i) for i in range(1000)]

# Formatar as datas como strings
opcoes_datas = [ft.dropdown.Option(text=data.strftime("%d/%m/%Y")) for data in datas]

# Criar o dropdown
dataI_edit_cursista = ft.Dropdown(options=opcoes_datas)
dataT_edit_cursista = ft.Dropdown(options=opcoes_datas)
local_edit_cursista = ft.RadioGroup(content=ft.Column([
    ft.Row([
        ft.Radio(value='Arcanjo Gabriel', label='Arcanjo Gabriel'), ft.Radio(value='Espírito Santo', label='Espírito Santo'),
        ft.Radio(value='Santa Terezinha do Menino Jesus', label='Santa Terezinha do Menino Jesus'), ft.Radio(value='São Pedro Apóstolo', label='São Pedro Apóstolo')
    ])
]))
# Criar opções para o dropdown de notas
opcoes_notas = [ft.dropdown.Option(str(nota)) for nota in range(21)]
# Criar o dropdown
nota_edit_cursista = ft.Dropdown(options=opcoes_notas)

id_edit_actividade = ft.Text()
nome_edit_actividade = ft.TextField(label='Nome da atividade')
hoje = datetime.date.today()
datas = [hoje + datetime.timedelta(days=i) for i in range(365)]
opcoes_datas = [ft.dropdown.Option(text=data.strftime("%d/%m/%Y")) for data in datas]
data_edit_actividade = ft.Dropdown(options=opcoes_datas)
horas_com_minutos = []
for hora in range(24):
    for minuto in range(0, 60, 15):  # Adicionando minutos a cada 15 minutos
        hora_formatada = f"{hora:02d}:{minuto:02d}"
        horas_com_minutos.append(hora_formatada)
opcoes_horas_com_minutos = [ft.dropdown.Option(hora) for hora in horas_com_minutos]
hora_edit_actividade = ft.Dropdown(options=opcoes_horas_com_minutos)
data_ter_edit_actividade = ft.Dropdown(options=opcoes_datas)
hora_ter_edit_actividade = ft.Dropdown(options=opcoes_horas_com_minutos)
local_edit_actividade = ft.TextField(label='Local de realização da actividade')
status_actividade = ''

id_edit_cargo = ft.Text()
nome_edit_cargo = ft.TextField(label='Nome do cargo')


def esconder_dlg(evento):
    dlg.visible = False
    minha_tabela.visible = True
    dlg.update()
    minha_tabela.update()

def esconder_dlg_cursista(evento):
    dlg_cursista.visible = False
    minha_tabela_cursista.visible = True
    minha_tabela_cursista.update()
    dlg_cursista.update()

def esconder_dlg_actividade(evento):
    minha_tabela_actividade.visible = True
    dlg_actividade.visible = False
    tb_actividade.update()
    dlg_actividade.update()

def save_and_update(evento):
    try:
        meu_id = id_edit_membro.value
        cargos_json = json.dumps(selected_cargos)
        c = conn.cursor()
        c.execute("""
            UPDATE membros SET 
            nome=?, data_nasc=?, genero=?, morada=?, 
            contacto=?, email=?, moradia=?, frequenta_escola=?, estuda_sabado=?, curso_acad=?, 
            e_trabalhador=?, local_trabalho=?, funcao_trabalho=?, trabalha_fim_semana=?, catecumeno=?, 
            n_f_catequese=?, tempo_grupo=?, ano_entrada=?, tem_cargo=?, cargos=?, 
            sacra_baptismo=?, sacra_crisma=?, sacra_penitencia=?, sacra_casamento=?, tem_sacramento=?, 
            tem_promessa=?, data_promessa=? WHERE id=?                    
        """, (
            nome_edit_membro.value, data_nasc_edit_membro.value, genero_edit_membro.value,  
            morada_edit_membro.value,  
            contacto_edit_membro.value, email_edit_membro.value, moradia_edit_membro.value,  
            frequenta_escola_edit_membro.value, estuda_sabado_edit_membro.value, curso_acad_edit_membro.value, 
            trabalhador_edit_membro.value, local_trabalho_edit_membro.value, 
            funcao_edit_membro.value, trabalha_fim_sem_edit_membro.value, 
            catecumeno_edit_membro.value, n_f_catequese_edit_membro.value, 
            tempo_grupo_edit_membro.value, ano_entrada_edit_membro.value, 
            tem_cargo_edit_membro.value, cargos_json, sacra_baptismo_edit_membro.value, 
            sacra_crisma_edit_membro.value, sacra_penitencia_edit_membro.value, 
            sacra_casamento_edit_membro.value, tem_sacramento_edit_membro.value, 
            tem_promessa_edit_membro.value, data_promessa_edit_membro.value, meu_id
        ))
        conn.commit()
        print('Registro editado com sucesso!')
        tb.rows.clear()
        tb_membro_dataNasc.clear()
        chamar_db()
        chamar_db_dataNasc()
        dlg.visible = False
        dlg.update()
        tb.update()
        tb_membro_dataNasc.update()
        print(f"ID do membro: {meu_id}")
        print(f"Valores dos campos de edição:")
        print(f"Nome: {nome_edit_membro.value}")
        print(f"Dia de Nascimento: {data_nasc_edit_membro.value}")
        
    except Exception as e:
        print(e)

def save_and_update_cursista(evento):
    try:
        meu_id = id_edit_cursista.value
        c=conecta_cursta.cursor()
        c.execute('UPDATE cursistas SET nome=?, paroquia=?, centro=?, curso=?, data_ini=?, data_ter=?, local=?, nota=? WHERE id=?', (nome_edit_cursista.value,  paroquia_edit_cursista.value, centro_edit_cursista.value, curso_edit_cursista.value, dataI_edit_cursista.value, dataT_edit_cursista.value, local_edit_cursista.value, nota_edit_cursista.value, meu_id))
        conecta_cursta.commit()
        print('Registro editado com sucesso!')
        tb_cursita.rows.clear()
        chamar_db_cursista()
        dlg_cursista.visible = False
        dlg_cursista.update()
        tb_cursita.update()

    except Exception as e:
        print(e,': Não foi possível editar os dados!')

def save_and_update_actividade(evento):
    try:
        meu_id = id_edit_actividade.value
        c=conecta_actividade.cursor()
        c.execute('UPDATE actividades SET nome=?, data_ini=?, hora_ini=?, data_ter=?, hora_ter=?, local=? WHERE id=?', (nome_edit_actividade.value,  data_edit_actividade.value, hora_edit_actividade.value,data_ter_edit_actividade.value, hora_ter_edit_actividade.value, local_edit_actividade.value, meu_id))
        conecta_actividade.commit()
        print('Registro editado com sucesso!')
        tb_actividade.rows.clear()
        tb_actividade_em_andamento.rows.clear()
        tb_actividade_concluida.rows.clear()
        chamar_db_actividade()
        chamar_db_actividade_concluida()
        chamar_db_actividade_em_andamento()
        dlg_actividade.visible = False
        dlg_actividade.update()
        tb_actividade.update()
        tb_actividade_em_andamento.update()
        tb_actividade_concluida.update()

    except Exception as e:
        print(e,': Não foi possível editar os dados!')


dlg =  ft.Column([
    ft.Container(
        bgcolor=ft.colors.GREEN_200,
        padding = 10,
        content = ft.Column([
          ft.Row([
                ft.Text('Editar dados', size=15, weight='bold'),
                ft.IconButton(icon='close', on_click=esconder_dlg),
                ], alignment='spaceBetween'),
                    ft.Row([
                        ft.Text('       '),nome_edit_membro, 
                    ]),
                    ft.Row([
                        ft.Text('       ', weight='bold', size= 16), data_nasc_edit_membro, column, 
                        ft.Text('Gênero:', size=16, weight='bold'), genero_edit_membro, 
                    ]),
                    ft.Row([
                        ft.Text('         Morada: ', size=16, weight='bold'), morada_edit_membro,
                    ]),
                    ft.Row([
                        ft.Text('       '),contacto_edit_membro, email_edit_membro, moradia_edit_membro, 
                        ], 
                    ),
                    ft.Row([
                        ft.Row([
                            ft.Text('  '),ft.Row(
                                [ft.Container(
                                    
                                    image_fit= ft.ImageFit.FIT_HEIGHT,
                                    content=ft.Column([
                                    ft.Text(),
                                    ft.Row([ft.Text('Dados relacionados aos compromissos', size=20, weight='bold', text_align='SpaceBetween')], alignment='center'),
                                    ft.Row([ft.Text('     É estudante?', size=16, weight='bold'), frequenta_escola_edit_membro]),
                                    ft.Row([ft.Text('     Estuda até aos sábados?', size=16, weight='bold'), estuda_sabado_edit_membro]),
                                    ft.Row([ft.Text('   '),curso_acad_edit_membro, ]), 
                                    ft.Row([ft.Text('     Trabalha?', weight='bold', size=16),trabalhador_edit_membro ]),
                                    ft.Row([ft.Text('   '),local_trabalho_edit_membro]),
                                    ft.Row([ft.Text('   '),funcao_edit_membro]),
                                    ft.Row([ft.Text('     Trabalha até aos fins de semanas?', size=16, weight='bold'), trabalha_fim_sem_edit_membro,]),
                                    ft.Row([ft.Text('     Frequenta a catequese?', size=16, weight='bold') ]),
                                    ft.Row([ft.Text('   '),catecumeno_edit_membro, ]),
                                    ft.Row([ft.Text('   '),n_f_catequese_edit_membro, ]),
                                    ft.Text(height=600),
                                    ], width=450 )),
                                ], alignment='SpaceBetween'),
                        ]),
                        ft.Row([
                            ft.Text('  '),ft.Row(
                                [ft.Container(
                                    bgcolor=ft.colors.GREEN_200,
                                    content=ft.Column([
                                    ft.Text(),
                                    ft.Row([ft.Text('Dados relacionados a Pastoral', size=20, weight='bold', text_align='SpaceBetween')], width=350, alignment='center'),
                                    ft.Row([tempo_grupo_edit_membro,], width=350, alignment='center'),
                                    ft.Row([ano_entrada_edit_membro,], width=350, alignment='center'),
                                    ft.Row([ft.Text('     Tem cargo no grupo?', size=16, weight='bold'), tem_cargo_edit_membro], width=350),
                                    ft.Row([ft.Text('     Quais?', size=16, weight='bold')], width=350),
                                    ft.Row([ft.Text(' '), cargos_membro], width=350),
                                    ft.Row([ft.Text('     Tem sacramento?', size=16, weight='bold'), tem_sacramento_edit_membro], width=350),
                                    ft.Row([ft.Text('     Quais?', size=16, weight='bold'),], width=350),
                                    ft.Row([ft.Text(' '),sacra_baptismo_edit_membro, sacra_penitencia_edit_membro], width=350), 
                                    ft.Row([ft.Text(' '),sacra_crisma_edit_membro, sacra_casamento_edit_membro], width=350),
                                    ft.Row([ft.Text('     É promessado(a)?', size=16, weight='bold'), tem_promessa_edit_membro], width=350),
                                    ft.Row([ft.Text('     Quando fez a promessa?', size=16, weight='bold') ], width=350),
                                    ft.Row([ft.Text(' '), data_promessa_edit_membro, column_promise], width=500),
                                    ft.Text(height=10),
                                    ], width=500 )),
                                ], alignment='SpaceBetween'),
                        ]),
                    ]),ft.ElevatedButton('Actualizar', on_click=save_and_update)
                ]))
    ], scroll=True, expand=1)



dlg_cursista = ft.Column([
    ft.Container(
    bgcolor=ft.colors.BLUE_200,
    padding = 10,
    content = ft.Column([
        ft.Row([
            ft.Text('Editar dados', size=15, weight='bold'),
            ft.IconButton(icon='close', on_click=esconder_dlg_cursista),
            ], alignment='spaceBetween'),
            nome_edit_cursista,
            paroquia_edit_cursista,
            ft.Text('Selecione o centro', size=15),
            centro_edit_cursista,
            ft.Text('Selecione o curso', size=15),
            curso_edit_cursista,
            ft.Text('Data de início', size=15),
            dataI_edit_cursista,
            ft.Text('Data de término', size=15),
            dataT_edit_cursista,
            ft.Text('Local onde foi realizado o curso', size=15),
            local_edit_cursista,
            ft.Text('Nota final', size=15),
            nota_edit_cursista,
            ft.ElevatedButton('Actualizar', on_click=save_and_update_cursista)
        ])
    )
    ], scroll=True, expand=1)

dlg_actividade = ft.Column([
    ft.Container(
    bgcolor=ft.colors.BLUE_200,
    padding = 10,
    content = ft.Column([
        ft.Row([
            ft.Text('Editar dados', size=15, weight='bold'),
            ft.IconButton(icon='close', on_click=esconder_dlg_actividade),
            ], alignment='spaceBetween'),
            nome_edit_actividade,
            ft.Row([
                ft.Text('Data de início:', size=15),
                data_edit_actividade,
                ft.Text('Hora de início:', size=15),
                hora_edit_actividade,
            ]),
            ft.Row([
                ft.Text('Data de término:', size=15),
                data_ter_edit_actividade,
                ft.Text('Hora de término:', size=15),
                hora_ter_edit_actividade,
            ]),
            local_edit_actividade,
            ft.ElevatedButton('Actualizar', on_click=save_and_update_actividade)
        ])
    )
    ], scroll=True, expand=1)


def showdelet(evento):
    #try:
        meu_id = int(evento.control.data)
        c = conn.cursor()
        conn.execute('DELETE FROM membros WHERE id=?', (meu_id,))
        conn.execute('DELETE FROM associacao_membro_cargo WHERE membro_id=?', (meu_id,))
        conn.execute('DELETE FROM associacao_membro_sacramento WHERE membro_id=?', (meu_id,))
        conn.commit()
        tb_membro_dataNasc.rows.clear()
        tb_membro_directivos.rows.clear()
        tb_membro_sacramentos.rows.clear()
        tb_membro.rows.clear()
        tb_imprime.rows.clear()
        tab_imagem.controls.clear()
        chamar_db()
        chamar_db_membro()
        chamar_db_dataNasc()
        chamar_db_por_cargos()
        chamar_db_associacao_membro_cargo()
        chamar_db_por_sacramentos()
        chamar_db_por_quotas()
        chamar_db_promessa()
        chamar_print_img_membro()
        chamar_print_membro()
        minha_tabela.update()
        minha_tab_print_membro.update()
        minha_tab_imagem.update()
        minha_tabela_dataNasc.update()
        minha_tabela_direccao.update()
        minha_tabela_sacramento.update()
        print('Dados eliminados com sucesso!')
        #tb.update()
        #tb_membro_dataNasc.update()
        #tb_membro_directivos.update()
        #tb_membro_sacramentos.update()
    #except Exception as e:
        #print(e,': Não foi possível eliminar os dados!')

def showdelet_cursista(evento):
    try:
        # Esta função será chamada quando o usuário confirmar a exclusão
        meu_id = int(evento.control.data)
        c = conecta_cursta.cursor()
        conecta_cursta.execute('DELETE FROM cursistas WHERE id=?', (meu_id,))
        conecta_cursta.commit()
        print('Dados eliminados com sucesso!')
        tb_cursita.rows.clear()
        tb_imprime_cursista.rows.clear()
        #tabela_cursos.controls.clear()
        #minha_tab_print_cursista.controls.clear()
        chamar_db_cursista()
        #minha_tabela_cursista.content.clean()
        chamar_print_cursistas(curso_to_pdf.value)
        chamar_print_cursista()
        tabela_cursos.update()
        minha_tab_cursos.update()
        minha_tabela_cursista.update()
        minha_tab_print_cursista.update()

    except Exception as e:
        print(e,': Não foi possível eliminar os dados!')
page_dialog = ft.AlertDialog()

"""def confirma_delete_cursista(evento):
    
    try:
        meu_id = int(evento.control.data)
        
        mdialog = ft.AlertDialog(
            title='Confirmação de Exclusão',
            content=ft.Column(
                ft.Row([
                    ft.Text(f'Tem certeza de que deseja excluir o cursista {nome_edit_cursista.value}?'),
                ])
         ,
            ),
            actions = [
                ft.ElevatedButton('Imprimir recibo', bgcolor=ft.colors.BLUE, color= ft.colors.RED, 
                    on_click=lambda e:showdelet_cursista(meu_id)
                )
            ]
        )
        print('Confirma')
        page_dialog = mdialog
    except Exception as e:
        print(e, ': Não foi possível iniciar a confirmação de exclusão!')"""

def showdelet_actividade(evento):
    try:
        meu_id = int(evento.control.data)
        c = conn.cursor()
        conecta_actividade.execute('DELETE FROM actividades WHERE id=?', (meu_id,))
        conecta_actividade.commit()
        print('Dados eliminados com sucesso!')
        tb_actividade.rows.clear()
        tb_actividade_em_andamento.rows.clear()
        tb_actividade_concluida.rows.clear()
        tb_imprime_actividade.rows.clear()
        tab_imagem_ac.controls.clear()
        chamar_db_actividade()
        chamar_db_actividade_em_andamento()
        chamar_db_actividade_concluida()
        chamar_print_actividades()
        chamar_print_actividade()
        minha_tabela_actividade.update()
        minha_tabela_actividade_concluida.update()
        minha_tabela_actividade_em_andamento.update()
        minha_tab_print_actividade.update()
        minha_tab_imagem_ac.update()
    except Exception as e:
        print(e,': Não foi possível eliminar os dados!')


def showedit(evento):
    try: 
        data_edit = evento.control.data
        id_edit_membro.value = data_edit['id']
        nome_edit_membro.value = data_edit['nome']
        data_nasc_edit_membro.value = data_edit['data_nasc']
        contacto_edit_membro.value = data_edit['contacto']
        genero_edit_membro.value = data_edit['genero']
        morada_edit_membro.value = data_edit['morada']
        moradia_edit_membro.value = data_edit['moradia']
        email_edit_membro.value = data_edit['email']
        frequenta_escola_edit_membro.value = data_edit['frequenta_escola']
        estuda_sabado_edit_membro.value = data_edit['estuda_sabado']
        curso_acad_edit_membro.value = data_edit['curso_acad']
        trabalhador_edit_membro.value = data_edit['e_trabalhador']
        local_trabalho_edit_membro.value = data_edit['local_trabalho']
        funcao_edit_membro.value = data_edit['funcao_trabalho']
        trabalha_fim_sem_edit_membro.value = data_edit['trabalha_fim_semana']
        catecumeno_edit_membro.value = data_edit['catecumeno']
        n_f_catequese_edit_membro.value = data_edit['n_f_catequese']
        tempo_grupo_edit_membro.value = data_edit['tempo_grupo']
        ano_entrada_edit_membro.value = data_edit['ano_entrada']
        tem_cargo_edit_membro.value = data_edit['tem_cargo']
        tem_sacramento_edit_membro.value = data_edit['tem_sacramento']
        tem_promessa_edit_membro.value = data_edit['tem_promessa']
        data_promessa_edit_membro.value = data_edit['data_promessa']
        minha_tabela.visible = False 
        dlg.visible = True
        minha_tabela.update()
        dlg.update()
    except Exception as e:
        print(e)

def showedit_cursista(evento):
    try: 
        data_edit = evento.control.data
        id_edit_cursista.value = data_edit['id']
        nome_edit_cursista.value = data_edit['nome']
        paroquia_edit_cursista.value = data_edit['paroquia']
        centro_edit_cursista.value = data_edit['centro']
        curso_edit_cursista.value = data_edit['curso']
        dataI_edit_cursista.value = data_edit['data_ini']
        dataT_edit_cursista.value = data_edit['data_ter']
        local_edit_cursista.value = data_edit['local']
        nota_edit_cursista.value = data_edit['nota']
        minha_tabela_cursista.visible = False
        dlg_cursista.visible = True
        minha_tabela_cursista.update()
        dlg_cursista.update()
    except Exception as e:
        print(e)
   
def showedit_actividade(evento):
    try: 
        data_edit = evento.control.data
        id_edit_actividade.value = data_edit['id']
        nome_edit_actividade.value = data_edit['nome']
        data_edit_actividade.value = data_edit['data_ini']
        hora_edit_actividade.value = data_edit['hora_ini']
        data_ter_edit_actividade.value = data_edit['data_ter']
        hora_ter_edit_actividade.value = data_edit['hora_ter']
        local_edit_actividade.value = data_edit['local']
        minha_tabela_actividade.visible = False
        dlg_actividade.visible = True
        dlg_actividade.update()
    except Exception as e:
        print(e)


minha_tabela = ft.Column([]) 

def chamar_db():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM membros ORDER BY nome")
        users = c.fetchall()
        print(users)
        minha_tabela.controls.clear()
        # Limpa as linhas da tabela antes de adicionar novos dados
        tb.rows.clear()

        if not users == '':
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                tb.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon='create', icon_color=ft.colors.GREEN, tooltip='Editar',
                                              data=x,
                                              on_click=showedit
                                              ),

                                ft.IconButton(icon='delete', icon_color=ft.colors.RED, tooltip='Eliminar',
                                              data=x['id'],
                                              on_click=showdelet
                                              ),
                            ])),
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['data_nasc'])),
                            ft.DataCell(ft.Text(x['genero'])),
                            ft.DataCell(ft.Text(x['morada'])),
                            ft.DataCell(ft.Text(x['contacto'])),
                            ft.DataCell(ft.Text(x['email'])),
                        ],
                    ),
                )
        if users==[]:
            minha_tabela.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), width = 1000, height = 700,  border = ft.border.all(2, ft.colors.RED), alignment = ft.alignment.center)]
            minha_tabela.alignment = ft.alignment.center
            minha_tabela.width = 1000
            minha_tabela.height = 700
        else:
            minha_tabela.controls = [ft.Row([tb])]
            minha_tabela.alignment = ft.alignment.top_left
            minha_tabela.scroll = 'auto'
            #minha_tabela.border = ft.border.all(2, ft.colors.RED)
    except Exception as e:
        print(e)
chamar_db()
dlg.visible = False
dlg_cursista.visible = False

minha_tabela_membro = ft.Container(ft.Column([ 
    ft.Row([ft.VerticalDivider(width=1),ft.Text('Lista de Membros da Pastoral', weight='bold')], alignment=ft.MainAxisAlignment.CENTER),
    ft.Row([ft.VerticalDivider(width=1)], scroll='auto')
])) 


def chamar_db_membro():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM membros ORDER BY nome")
        users = c.fetchall()
        print(users)

        # Limpa as linhas da tabela antes de adicionar novos dados
        tb_membro.rows.clear()

        if not users == '':
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                tb_membro.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['contacto'])),
                        ],
                    ),
                )

        if users==[]:
            minha_tabela_membro.content = ft.Text('Não há dados na tabela!', weight='bold', size=40)
            minha_tabela_membro.alignment = ft.alignment.center
            minha_tabela_membro.width = 600
            minha_tabela_membro.height = 700
            minha_tabela_membro.border = ft.border.all(2, ft.colors.RED)
        else:
            minha_tabela_membro.content = ft.Row([tb_membro])
            minha_tabela_membro.width = 600
            minha_tabela_membro.height = 700
            minha_tabela_membro.alignment = ft.alignment.top_left
            #minha_tabela_membro.border = ft.border.all(2, ft.colors.RED)
    except Exception as e:
        print(e)
chamar_db_membro()

minha_tabela_cursista = ft.Column([]) 

def chamar_db_cursista():
    try:
        c=conecta_cursta.cursor()
        c.execute("SELECT * FROM cursistas ORDER BY nome")
        cursistas = c.fetchall()
        print(cursistas)
        if not cursistas == '':
            keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota']
            result = [dict(zip(keys, values)) for values in cursistas]
            for x in result:
                tb_cursita.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon='create', icon_color=ft.colors.GREEN, tooltip='Editar',
                                    data=x,
                                    on_click=showedit_cursista              
                                ),

                                ft.IconButton(icon='delete', icon_color=ft.colors.RED, tooltip='Eliminar',
                                    data=x['id'],
                                    on_click=showdelet_cursista              
                                ),
                            ])),
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['paroquia'])),
                            ft.DataCell(ft.Text(x['centro'])),
                            ft.DataCell(ft.Text(x['curso'])), 
                            ft.DataCell(ft.Text(x['data_ini'])),
                            ft.DataCell(ft.Text(x['data_ter'])),
                            ft.DataCell(ft.Text(x['local'])),
                            ft.DataCell(ft.Text(x['nota'])),   
                        ],
                    ),
                )
        if cursistas==[]:
            minha_tabela_cursista.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), width = 1000, height = 700,  border = ft.border.all(2, ft.colors.RED), alignment = ft.alignment.center)]
            minha_tabela_cursista.alignment = ft.alignment.center
            minha_tabela_cursista.width = 1000
            minha_tabela_cursista.height = 700
            #minha_tabela_cursista.border = ft.border.all(2, ft.colors.RED)
        else:
            minha_tabela_cursista.controls = [ft.Row([tb_cursita])]
            minha_tabela_cursista.alignment = ft.alignment.top_left
            minha_tabela_cursista.scroll = 'auto'
            #minha_tabela_cursista.border = ft.border.all(2, ft.colors.RED)
    except Exception as e:
        print(e)
        
chamar_db_cursista()
def converter_data_hora_para_segundos(data_str, hora_str):
    try:
        data = datetime.datetime.strptime(data_str, '%d/%m/%Y')
        hora = datetime.datetime.strptime(hora_str, '%H:%M')
        
        # Convertendo a data e hora para um único objeto datetime
        data_hora = datetime.datetime.combine(data.date(), hora.time())
        
        # Convertendo para segundos desde a época (timestamp)
        segundos = (data_hora - datetime.datetime(1970, 1, 1)).total_seconds()

        return int(segundos)
    except Exception as e:
        print(e)

def duracao_tempo_atual_em_segundos(duracao):
    hora = datetime.datetime.strptime(duracao, '%H:%M')
    segundos = (hora - datetime.datetime(1970, 1, 1)).total_seconds()
    return int(segundos)

def obter_tempo_atual_em_segundos():
    agora = datetime.datetime.now()
    segundos = (agora - datetime.datetime(1970, 1, 1)).total_seconds()
    return int(segundos)

minha_tabela_actividade = ft.Column([], scroll=True)
def chamar_db_actividade():
    try:
        c=conecta_actividade.cursor()
        c.execute('SELECT * FROM actividades')
        actividades = c.fetchall()
        print(actividades)
        tb_actividade.rows.clear()
        if not actividades == []:
            keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
            resultados = [dict(zip(keys, values)) for values in actividades]
            for actividade in resultados:
                tb_actividade.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon='create', icon_color=ft.colors.GREEN, tooltip='Editar',
                                    data=actividade,
                                    on_click=showedit_actividade              
                                ),

                                ft.IconButton(icon='delete', icon_color=ft.colors.RED, tooltip='Eliminar',
                                    data=actividade['id'],
                                    on_click=showdelet_actividade              
                                ),
                            ])),
                            ft.DataCell(ft.Text(actividade['nome'])),
                            ft.DataCell(ft.Text(actividade['data_ini'])),
                            ft.DataCell(ft.Text(actividade['hora_ini'])),
                            ft.DataCell(ft.Text(actividade['data_ter'])), 
                            ft.DataCell(ft.Text(actividade['hora_ter'])), 
                            ft.DataCell(ft.Text(actividade['local'])),
                            ft.DataCell(ft.Text(actividade['status'])),   
                        ],
                    ),
                )
        if actividades==[]:
            minha_tabela_actividade.controls.clear()
            minha_tabela_actividade.controls.append(ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border=ft.border.all(2, ft.colors.RED), width=1100, height=700, alignment=ft.alignment.center))
            minha_tabela_actividade.width = 1000
            minha_tabela_actividade.height = 700
            minha_tabela_actividade.alignment = ft.alignment.center
        else:
            minha_tabela_actividade.controls.clear()
            minha_tabela_actividade.controls.append(ft.Row([tb_actividade]))
            minha_tabela_actividade.alignment = ft.alignment.top_left
            minha_tabela_actividade.scroll = 'auto'
            #minha_tabela_actividade.border = ft.border.all(2, ft.colors.RED)
    except Exception as e:
        print(e)
    
chamar_db_actividade()
dlg_actividade.visible = False

minha_tabela_actividade_em_andamento = ft.Column([])

def chamar_db_actividade_em_andamento():
    try:
        c=conecta_actividade.cursor()
        c.execute('SELECT * FROM actividades WHERE status="Em andamento"')
        actividades = c.fetchall()
        minha_tabela_actividade_em_andamento.controls.clear()
        tb_actividade_em_andamento.rows.clear()
        print(actividades)
        if not actividades == '':
            keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
            resultados = [dict(zip(keys, values)) for values in actividades]
            for actividade in resultados:
                tb_actividade_em_andamento.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(actividade['nome'])),
                            ft.DataCell(ft.Text(actividade['data_ini'])),
                            ft.DataCell(ft.Text(actividade['hora_ini'])),
                            ft.DataCell(ft.Text(actividade['data_ter'])), 
                            ft.DataCell(ft.Text(actividade['hora_ter'])), 
                            ft.DataCell(ft.Text(actividade['local'])),
                            ft.DataCell(ft.Text(actividade['status'])),   
                        ],
                    ),
                )
        if actividades==[]:
            minha_tabela_actividade_em_andamento.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40),width=1000, height=700, alignment=ft.alignment.center, border = ft.border.all(2, ft.colors.RED))]
        else:
            minha_tabela_actividade_em_andamento.controls=[ft.Row([tb_actividade_em_andamento])]
            minha_tabela_actividade_em_andamento.alignment = ft.alignment.top_left
    except Exception as e:
        print(e)
chamar_db_actividade_em_andamento()



audio1 = ft.Audio(src="/home/izata/Downloads/Parabéns Pra Você - Atchim e Espirro.mpga" , autoplay=False)


minha_tabela_actividade_concluida = ft.Column([]) 
def chamar_db_actividade_concluida():
    try:
        c=conecta_actividade.cursor()
        c.execute('SELECT * FROM actividades WHERE status="Concluída"')
        actividades = c.fetchall()
        print(actividades)
        minha_tabela_actividade_concluida.controls.clear()
        tb_actividade_concluida.rows.clear()
        if not actividades == []:
            keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
            resultados = [dict(zip(keys, values)) for values in actividades]
            for actividade in resultados:
                tb_actividade_concluida.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(actividade['nome'])),
                            ft.DataCell(ft.Text(actividade['data_ini'])),
                            ft.DataCell(ft.Text(actividade['hora_ini'])),
                            ft.DataCell(ft.Text(actividade['data_ter'])), 
                            ft.DataCell(ft.Text(actividade['hora_ter'])), 
                            ft.DataCell(ft.Text(actividade['local'])),
                            ft.DataCell(ft.Text(actividade['status'])),   
                        ],
                    ),
                )
        if actividades==[]:
            minha_tabela_actividade_concluida.controls = [ft.Container(ft.Text('Não há dados na tabela!', weight='bold', size=40), width=1000, height=700, alignment=ft.alignment.center, border = ft.border.all(2, ft.colors.RED))]
        else:
            minha_tabela_actividade_concluida.controls.append(ft.Row([tb_actividade_concluida]))
            minha_tabela_actividade_concluida.alignment = ft.alignment.top_left    
            minha_tabela_actividade_concluida.update()

    except Exception as e:
        print(e)
chamar_db_actividade_concluida()

#import datetime

aniversariante = ft.Column([], visible=False)
minha_tabela_dataNasc = ft.Column([])
def chamar_db_dataNasc():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM membros')
        membros = c.fetchall()
        
        if membros:
            today = datetime.date.today()
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa', 'imagem']
            resultados = [dict(zip(keys, values)) for values in membros]
            
            # Separar aniversariantes passados e futuros
            aniversariantes_futuros = []
            aniversariantes_passados = []

            for membro in resultados:
                data_nascimento = datetime.datetime.strptime(membro['data_nasc'], '%d/%m/%Y').date()
                idade = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))

                if (today.month, today.day) <= (data_nascimento.month, data_nascimento.day):
                    aniversariantes_futuros.append((membro, idade))
                else:
                    aniversariantes_passados.append((membro, idade))
            
            # Ordenar por data de aniversário
            aniversariantes_futuros.sort(key=lambda x: (x[0]['data_nasc'].split('/')[1], x[0]['data_nasc'].split('/')[0]))
            aniversariantes_passados.sort(key=lambda x: (x[0]['data_nasc'].split('/')[1], x[0]['data_nasc'].split('/')[0]))
            
            # Adicionar aniversariantes futuros
            for membro, idade in aniversariantes_futuros:
                tb_membro_dataNasc.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(membro['nome'])),
                            ft.DataCell(ft.Text(membro['data_nasc'])),
                            ft.DataCell(ft.Text(membro['contacto'])),
                            ft.DataCell(ft.Text(membro['email'])),
                            ft.DataCell(ft.Text(str(idade))),  # Adicionando idade
                        ],
                    ),
                )
                data_nascimento = datetime.datetime.strptime(membro['data_nasc'], '%d/%m/%Y').date()
                if today.month == data_nascimento.month and today.day == data_nascimento.day:
                    audio1.autoplay=True
                    aniversariante.controls=[ft.Text(height=50)]
                    aniversariante.controls=[ft.Text('Aniversariantes do dia', size=20, weight='bold')]
                    aniversariante.width=1000
                    aniversariante.alignment='center'
                    
                    aniversariante.controls.append(ft.Row([ft.Image(src=membro['imagem'], width=100, height=100),ft.Text(f"Hoje o aniversário de {membro['nome']}."),ft.Text('Vamos desejá-lo parabéns!') if membro['genero']=='Masculino' else ft.Text('Vamos desejá-la parabéns!')]))
            
            # Adicionar aniversariantes passados
            for membro, idade in aniversariantes_passados:
                tb_membro_dataNasc.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(membro['nome'])),
                            ft.DataCell(ft.Text(membro['data_nasc'])),
                            ft.DataCell(ft.Text(membro['contacto'])),
                            ft.DataCell(ft.Text(membro['email'])),
                            ft.DataCell(ft.Text(str(idade))),  # Adicionando idade
                        ],
                    ),
                )
        if membros == []:
            minha_tabela_dataNasc.controls.clear()
            minha_tabela_dataNasc.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tabela_dataNasc.alignment = ft.alignment.center
            minha_tabela_dataNasc.width = 995
            minha_tabela_dataNasc.height = 700
        else:
            minha_tabela_dataNasc.controls.clear()
            minha_tabela_dataNasc.controls = [ft.Row([tb_membro_dataNasc])]
            minha_tabela_dataNasc.alignment = ft.alignment.top_left
            minha_tabela_dataNasc.scroll = 'auto'
    except Exception as e:
        print(e)

chamar_db_dataNasc()


minha_tabela_direccao = ft.Column([])
def chamar_db_por_cargos():
    try:
        c = conn.cursor()
        c.execute("""SELECT associacao_membro_cargo.id, membros.nome as nome_membro, cargos.nome as nome_cargo, membros.contacto, membros.email
                    FROM associacao_membro_cargo
                    JOIN membros ON associacao_membro_cargo.membro_id = membros.id
                    JOIN cargos ON associacao_membro_cargo.cargo_id = cargos.id
                    ORDER BY cargos.id
                    """)

        membros = c.fetchall()

        if membros:
            keys = ['id', 'nome_membro', 'nome_cargo', 'contacto', 'email']
            resultados = [dict(zip(keys, values)) for values in membros]
            for membro in resultados:
                tb_membro_directivos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(membro['nome_membro'])),
                            ft.DataCell(ft.Text(membro['nome_cargo'])),
                            ft.DataCell(ft.Text(membro['contacto'])),
                            ft.DataCell(ft.Text(membro['email'])),
                        ],
                    ),
                )
        if membros == []:
            minha_tabela_direccao.controls.clear()
            minha_tabela_direccao.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tabela_direccao.alignment = ft.alignment.center
            minha_tabela_direccao.width = 995
            minha_tabela_direccao.height = 700
        else:
            minha_tabela_direccao.controls.clear()
            minha_tabela_direccao.controls = [ft.Row([tb_membro_directivos])]
            minha_tabela_direccao.alignment = ft.alignment.top_left
            minha_tabela_direccao.scroll = 'auto'
    except Exception as e:
        print(e)

chamar_db_por_cargos()

minha_tabela_sacramento = ft.Column([])
def chamar_db_por_sacramentos():
    try:
        c = conn.cursor()

        c.execute("""SELECT associacao_membro_sacramento.id, membros.nome as nome_membro, 
                    REPLACE(GROUP_CONCAT(sacramentos.nome), ',', ', ') as nome_sacramento, membros.contacto, membros.email
                    FROM associacao_membro_sacramento
                    INNER JOIN membros ON associacao_membro_sacramento.membro_id = membros.id
                    INNER JOIN sacramentos ON associacao_membro_sacramento.sacramento_id = sacramentos.id
                    GROUP BY membros.nome
                    ORDER BY membros.nome""")

        membros = c.fetchall()

        if membros:
            keys = ['id', 'nome_membro', 'nome_sacramento', 'contacto', 'email']
            resultados = [dict(zip(keys, values)) for values in membros]
            for membro in resultados:
                tb_membro_sacramentos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(membro['nome_membro'])),
                            ft.DataCell(ft.Text(membro['nome_sacramento'])),
                            ft.DataCell(ft.Text(membro['contacto'])),
                            ft.DataCell(ft.Text(membro['email'])),
                        ],
                    ),
                )
        if membros == []:
            minha_tabela_sacramento.controls.clear()
            minha_tabela_sacramento.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tabela_sacramento.alignment = ft.alignment.center
            minha_tabela_sacramento.width = 995
            minha_tabela_sacramento.height = 700
        else:
            minha_tabela_sacramento.controls.clear()
            minha_tabela_sacramento.controls = [ft.Row([tb_membro_sacramentos])]
            minha_tabela_sacramento.alignment = ft.alignment.top_left
            minha_tabela_sacramento.scroll = 'auto'
    except Exception as e:
        print(e)

chamar_db_por_sacramentos()


minha_tabela_quotas = ft.Column([])
def chamar_db_por_quotas():
    try:
        c = conn.cursor()

        c.execute("""SELECT associacao_membro_quota.id, membros.nome as nome_membro, membros.contacto as contacto,
                    REPLACE(GROUP_CONCAT(quotas.mes), ',', ', ') as mes_quota 
                    FROM associacao_membro_quota
                    INNER JOIN membros ON associacao_membro_quota.membro_id = membros.id
                    INNER JOIN quotas ON associacao_membro_quota.quota_id = quotas.id
                    GROUP BY membros.nome
                    ORDER BY membros.nome""")

        membros = c.fetchall()
        print(membros)
        if membros:
            keys = ['id','nome_membro', 'contacto','mes_quota']
            resultados = [dict(zip(keys, values)) for values in membros]
            for membro in resultados:
                tb_membro_quotas.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(membro['nome_membro'])),
                            ft.DataCell(ft.Text(membro['contacto'])),
                            ft.DataCell(ft.Text(membro['mes_quota'])),
                        ],
                    ),
                )
        if membros == []:
            minha_tabela_quotas.controls.clear()
            minha_tabela_quotas.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tabela_quotas.alignment = ft.alignment.center
            minha_tabela_quotas.width = 995
            minha_tabela_quotas.height = 700
        else:
            minha_tabela_quotas.controls.clear()
            minha_tabela_quotas.controls = [ft.Row([tb_membro_quotas])]
            minha_tabela_quotas.alignment = ft.alignment.top_left
            minha_tabela_quotas.scroll = 'auto'
    except Exception as e:
        print(e)

chamar_db_por_quotas()

minha_tabela_promessa = ft.Column([])
def chamar_db_promessa():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM membros WHERE tem_promessa='Sim' ORDER BY data_promessa")
        users = c.fetchall()
        print(users)

        # Limpa as linhas da tabela antes de adicionar novos dados
        tb_membro_promessa.rows.clear()

        if not users == '':
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                tb_membro_promessa.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['contacto'])),
                            ft.DataCell(ft.Text(x['data_promessa'])),
                        ],
                    ),
                )
                print(x['data_promessa'])
        if users == []:
            minha_tabela_promessa.controls.clear()
            minha_tabela_promessa.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tabela_promessa.alignment = ft.alignment.center
            minha_tabela_promessa.width = 995
            minha_tabela_promessa.height = 700
        else:
            minha_tabela_promessa.controls.clear()
            minha_tabela_promessa.controls = [ft.Row([tb_membro_promessa])]
            minha_tabela_promessa.alignment = ft.alignment.top_left
            minha_tabela_promessa.scroll = 'auto'
    except Exception as e:
        print(e)
chamar_db_promessa()

def remover_espacos_extras(texto):
    linhas = texto.split('\n')
    linhas_sem_espacos_extras = [linha.strip() for linha in linhas if linha.strip()]
    texto_sem_espacos_extras = '\n'.join(linhas_sem_espacos_extras)
    return texto_sem_espacos_extras

def extrair_informacao_desejada(texto):
    try:
        padrao = r'\d+\s?–\s[A-ZÇÃÕÁÉÍÓÚ0-9\s.,:-]+'
        padrao_semana = r'\d{1,2}[ªº]\sSEMANA\sDO\sTEMPO\sCOMUM'
        padrao_leitura = r'Primeira Leitura: [A-Za-z]+\s\d{1,2},\d{1,2}-\d{1,2},\d{1,2}\.\d{1,2}'
        padrao_salmo = r'Salmo Responsorial: [A-Za-z]+\s\d{1,2}'
        padrao_seg_leitura = r'Segunda Leitura: [A-Za-z]+\s\d{1,2}'
        padrao_evangelho = r'Evangelho: [A-Za-z]+\s\d{1,2},\d{1,2}-\d{1,2}'

        informacoes_extraidas = []
        padroes = [padrao, padrao_semana, padrao_leitura, padrao_salmo, padrao_seg_leitura, padrao_evangelho]

        for padrao_atual in padroes:
            informacoes = re.findall(padrao_atual, texto)
            informacoes_extraidas.extend(informacoes)
            
        texto_final = '\n'.join(informacoes_extraidas)

        linhas = texto_final.split('\n')
        novas_linhas = [linhas[i] for i in range(len(linhas)) if i not in [1, 2, 3, 4, 8, 10]]
        texto_final = '\n'.join(novas_linhas)
        c = conn.cursor()
        data = datetime.datetime.today()
        data_f = datetime.datetime.strftime(data, '%Y-%m-%d')
        print(data_f)
        tempo_liturgico = ft.Text()
        pri_leitura = ft.Text()
        salmo = ft.Text()
        seg_leitura = ft.Text()
        evangelho = ft.Text()
        agenda = texto_final
        
        for padrao in padroes:
            informacoes = re.findall(padrao, agenda)
            if len(informacoes) > 0:
                informacao = informacoes[0]
                if informacao.startswith('Primeira Leitura'):
                    pri_leitura.value = informacao
                    print(pri_leitura)
                elif informacao.startswith('Segunda Leitura'):
                    seg_leitura.value = informacao
                    print(seg_leitura)
                elif informacao.startswith('Salmo Responsorial'):
                    salmo.value = informacao
                    print(salmo)
                elif informacao.startswith('Evangelho'):
                    evangelho.value = informacao
                    print(evangelho)
                elif informacao.startswith(('SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA', 'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SÁBADO', 'DOMINGO')):
                    pass #semana = informacao
                    #print(semana)
                else:
                    tempo_liturgico.value = informacao
                    print(tempo_liturgico)
        c = conn.cursor()
        print(salmo.value)
        c.execute("""INSERT OR IGNORE INTO leituras (data, tempo_liturgico, pri_leitura, salmo, seg_leitura, evangelho) 
                VALUES (?,?,?,?,?,?)""", (data_f, tempo_liturgico.value, pri_leitura.value, salmo.value, seg_leitura.value, evangelho.value),)
        print('Passou aqui!')
        conn.commit()
        return texto_final
    except Exception as e:
        print(e)

def buscar_texto():
        #url = "https://www.paulus.com.br/portal/liturgia-diaria/"

        try:
            #response = requests.get(url)
            #soup = BeautifulSoup(response.content, "html.parser")
            texto = 'soup.get_text()'
            conteudo = ft.Text(texto)
            texto_import = ft.Text(remover_espacos_extras(conteudo.value))
            print(ft.Text(extrair_informacao_desejada(texto_import.value)).value)
            return   ft.Text(extrair_informacao_desejada(texto_import.value))

        except Exception as e:
            return print(f"Erro ao buscar texto: {e}")
buscar_texto()


def chamar_db_quota():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM quotas ')
        quotas = c.fetchall()
        print(f'=============={quotas}============')
        return quotas
    except Exception as e:
        print(e)

chamar_db_quota()

def chamar_db_leitura():
    try:
        c = conn.cursor()
        data = datetime.datetime.today()
        data_f = datetime.datetime.strftime(data, '%Y-%m-%d')
        
        c.execute("SELECT * FROM leituras WHERE data=?", (data_f,))
        users = c.fetchall()
        print(f'????????{users}')

        # Limpa as linhas da tabela antes de adicionar novos dados
        tb_membro_leitura.rows.clear()

        if not users == '':
            keys = ['data', 'tempo_liturgico', 'pri_leitura', 'salmo', 'seg_leitura', 'evangelho']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                tb_membro_leitura.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x['data'])), 
                            ft.DataCell(ft.Text(x['tempo_liturgico'])), 
                            ft.DataCell(ft.Text(x['pri_leitura'])), 
                            ft.DataCell(ft.Text(x['salmo'])), 
                            ft.DataCell(ft.Text(x['seg_leitura'])), 
                            ft.DataCell(ft.Text(x['evangelho'])), 
                        ], 
                    ),
                )
    except Exception as e:
        print(e)


chamar_db_leitura()

def chamar_db_cargo():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM cargos ')
        cargos = c.fetchall()
        print(f'=============={cargos}============')
        return cargos
    except Exception as e:
        print(e)

chamar_db_cargo()

def chamar_db_associacao_membro_cargo():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM associacao_membro_cargo ')
        associacao_membro_cargos = c.fetchall()
        print(f'---{associacao_membro_cargos}---')
        return associacao_membro_cargos
    except Exception as e:
        print(e)
chamar_db_associacao_membro_cargo()

def chamar_db_sacramento():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM sacramentos ')
        sacramentos = c.fetchall()
        print(f'=============={sacramentos}============')
        #interateble = []
        #interateble
        return sacramentos
    except Exception as e:
        print(e)

chamar_db_sacramento()

tb_imprime = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Data de nascimento')), 
        ft.DataColumn(ft.Text('Genero')),   
        ft.DataColumn(ft.Text('Morada')), 
        ft.DataColumn(ft.Text('Contacto')),
        ft.DataColumn(ft.Text('E-mail')),
    ],
    rows=[]

)

now = datetime.datetime.now()
formated_data = now.strftime('%d-%m-%Y')
    
def save_nota_membro(e:FilePickerResultEvent):
    
    c = conn.cursor()
    meu_id = id_m_print.value
    if meu_id is None:
        print("ID não foi obtido corretamente.")
        return
    c.execute("SELECT * FROM membros WHERE id=?", (meu_id,))
    users = c.fetchall()
    print(users)
    if not users == '':
        keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            nome_m_print.value = x['nome']
            datanasc_m_print.value = x['data_nasc']
            genero_m_print.value = x['genero']
            morada_m_print.value = x['morada']
            contacto_m_print.value = x['contacto']
            email_m_print.value = x['email']
            frequenta_escola_m_print.value = x['frequenta_escola']
            estuda_sabado_m_print.value = x['estuda_sabado']
            curso_acad_m_print.value = x['curso_acad']
            trabalhador_m_print.value = x['e_trabalhador']
            local_trabalho_m_print.value = x['local_trabalho']
            funcao_m_print.value = x['funcao_trabalho']
            trabalha_fim_sem_m_print.value = x['trabalha_fim_semana']
            catecumeno_m_print.value = x['catecumeno']
            n_f_catequese_m_print.value = x['n_f_catequese']
            tempo_grupo_m_print.value = x['tempo_grupo']
            ano_entrada_m_print.value = x['ano_entrada']
            tem_cargo_m_print.value = x['tem_cargo']
            tem_sacramento_m_print.value = x['tem_sacramento']
            tem_promessa_m_print.value = x['tem_promessa']
            data_promessa_m_print.value = x['data_promessa']
    print('Passou aqui!')
    #your_file_save_location = e.path
    
    nome_membro_formatado = nome_m_print.value.replace(' ', '_').lower()
    #your_file_save_location = nome_membro_formatado
    e.file_name = nome_membro_formatado + ".pdf"
    file_path = f'{nome_membro_formatado}.pdf'
    doc = SimpleDocTemplate(file_path, pagesizes=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Times-Roman'
    styles['Normal'].fontSize = 12
    styles['Normal'].leading = 18
    styles['Title'].fontName = 'Times-Bold'
    styles['Title'].fontSize = 14
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Paragraph('Ficha de Membro', styles['Title']))
    elements.append(Paragraph(f'Nome: {nome_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Data de nascimento: {datanasc_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Gênero: {genero_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Morada: {morada_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Contacto: {contacto_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Estuda? {frequenta_escola_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Estuda aos sábados? {estuda_sabado_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Curso: {curso_acad_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Trabalha? {trabalhador_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Função: {funcao_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Trabalha até aos fins de semana? {trabalha_fim_sem_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Frequenta a catequese? {catecumeno_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Motivo de não frequentar a catequese: {n_f_catequese_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Está a {tempo_grupo_m_print.value} no grupo', styles['Normal']))
    elements.append(Paragraph(f'Entrou em  {ano_entrada_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Exerce algum cargo no grupo?: {tem_cargo_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Tem algum sacramento? {tem_sacramento_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'É promessado? {tem_promessa_m_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Data da promessa: {data_promessa_m_print.value}', styles['Normal']))
    #list_order = []
    #list_order.append(['Nome do curso', 'Data de início', 'Data de término', 'Local onde foi realizado', 'Nata final'])
    #for curso in all_curso.controls:
    #    list_order.append([
    #        curso.content.controls[0].value,
    #        curso.content.controls[1].value,
    #        curso.content.controls[2].value,
    #        curso.content.controls[3].value,
    #        curso.content.controls[4].value,
    #    ])

    #table = Table(list_order)
    #table.setStyle(TableStyle([
    ##    ('BACKGROUND', (0,0), (-1,0), colors.grey),
        #   ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        #   ('ALIGN', (0,0), (-1,0), 'CENTER'),
        #   ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        #   ('FONTSIZE', (0,0), (-1,0), 14),
        #   ('BUTTONPADDING', (0,0), (-1,0), 12),

        # ('BACKGROUND', (0,0), (-1,-1), colors.beige),
        #('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        #('ALIGN', (0,0), (-1,-1), 'CENTER'),
        #('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        #('FONTSIZE', (0,0), (-1,-1), 14),
        #('BUTTONPADDING', (0,0), (-1,-1), 8),
    # ]))

    #elements.append(table)
    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    #elements.append(Paragraph())
    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    doc.build(elements)

file_save=ft.FilePicker(on_result=save_nota_membro)


def on_click_handle(e):
    meu_id = e.control.data['id']  # Assumindo que o ID está no campo 'id' do dicionário
    id_m_print.value = meu_id
    nome_m_print.value = e.control.data['nome']  # Adicione esta linha para configurar o nome corretamente
    file_save.file_name = nome_m_print.value
    file_save.save_file()

id_m_print = ft.Text()
nome_m_print = ft.Text()
datanasc_m_print = ft.Text()
genero_m_print = ft.Text()
morada_m_print = ft.Text()
contacto_m_print = ft.Text()
email_m_print = ft.Text()
frequenta_escola_m_print = ft.Text()
estuda_sabado_m_print = ft.Text()
curso_acad_m_print = ft.Text()
trabalhador_m_print = ft.Text()
local_trabalho_m_print = ft.Text()
funcao_m_print = ft.Text()
trabalha_fim_sem_m_print = ft.Text()
catecumeno_m_print = ft.Text()
n_f_catequese_m_print = ft.Text()
tempo_grupo_m_print = ft.Text()   
ano_entrada_m_print = ft.Text()
tem_cargo_m_print = ft.Text()
tem_sacramento_m_print = ft.Text()
tem_promessa_m_print = ft.Text()
data_promessa_m_print = ft.Text()


def chamar_print_membro():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM membros ORDER BY nome")
        users = c.fetchall()
        print(users)

        tb_imprime.rows.clear()
        if not users == '':
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                #id.value = ['id']
                
                tb_imprime.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon=ft.icons.PICTURE_AS_PDF_ROUNDED, icon_color=ft.colors.GREEN, tooltip='Editar',
                                                data=x, 
                                                on_click=on_click_handle
                                                ),

                                ])),
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['data_nasc'])),
                            ft.DataCell(ft.Text(x['genero'])),
                            ft.DataCell(ft.Text(x['morada'])),
                            ft.DataCell(ft.Text(x['contacto'])),
                            ft.DataCell(ft.Text(x['email'])),
                        ],
                    ),
                )
        
        if users == []:
            minha_tab_print_membro.controls.clear()
            minha_tab_print_membro.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tab_print_membro.alignment = ft.alignment.center
            minha_tab_print_membro.width = 995
            minha_tab_print_membro.height = 700
        else:
            minha_tab_print_membro.controls.clear()
            minha_tab_print_membro.controls = [ft.Row([tb_imprime])]
            minha_tab_print_membro.alignment = ft.alignment.top_left
            minha_tab_print_membro.scroll = 'auto'
        
    except Exception as e:
        print(e)
minha_tab_print_membro = ft.Column([], scroll = 'auto')
chamar_print_membro()

def save_nota_membros(e:FilePickerResultEvent):
    
    c = conn.cursor()
    c.execute("SELECT * FROM membros ORDER BY nome")
    users = c.fetchall()
    print(users)
    print('Passou aqui!')
    #your_file_save_location = e.path
    
    #your_file_save_location = nome_membro_formatado
    e.file_name = 'lista_de_membros' + ".pdf"
    file_path = 'lista_de_membros.pdf'
    doc = SimpleDocTemplate(file_path, pagesizes=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Times-Roman'
    styles['Normal'].fontSize = 12
    styles['Normal'].leading = 18
    styles['Title'].fontName = 'Times-Bold'
    styles['Title'].fontSize = 14
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Paragraph('Lista de Membros', styles['Title']))
    
    keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa']
    result = [dict(zip(keys, values)) for values in users]
    list_order = []
    list_order.append(['Nº','Nome', 'Data de nacimento', 'Contacto', 'E-mail'])
    count = 0
    for x in result:
        count +=1
        list_order.append([
            count,
            x['nome'],
            x['data_nasc'],
            x['contacto'],
            x['email']
        ])
    table = Table(list_order)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cores.beige),
        ('TEXTCOLOR', (0,0), (-1,0), cores.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
        
        ('ALIGN', (1,0), (0,-1), 'CENTER'),
        ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
        ('FONTSIZE', (1,0), (0,-1), 12),
        ('BUTTONPADDING', (1,0), (0,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.25, cores.black),
        ('BOX', (0,0), (-1,-1), 0.25, cores.black)
    ]))

    elements.append(table)
    doc.build(elements)

files_save=ft.FilePicker(on_result=save_nota_membros)

def on_click_handles(e):
    files_save.save_file()


tab_imagem = ft.Column([], scroll=True)
def chamar_print_img_membro():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM membros ORDER BY nome")
        users = c.fetchall()
        print(users)

        tab_imagem.controls.append(ft.Row([ft.Text('Lista de Membros', weight='bold', size=20)], width=1000, alignment=ft.MainAxisAlignment.CENTER))
        if not users == []:
            keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'tem_sacramento', 'tem_promessa', 'data_promessa', 'imagem']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                #id.value = ['id']
                if x['imagem']==None:
                    tab_imagem.controls.append(ft.Row([ft.Text('        '), ft.Text('Não há imagem disponível', width=200, height=200), ft.Text(x['nome'])]))    
                else:
                    tab_imagem.controls.append(ft.Container(content=ft.Row([ft.Text('        '), ft.Image(src=x['imagem'], border_radius=ft.border_radius.all(10), width=100, height=100), ft.Text(x['nome'])], )))
            tab_imagem.controls.append(ft.Container(content=ft.Row([ft.FloatingActionButton(text='Guardar em pdf', icon=ft.icons.SAVE, on_click=on_click_handles)], width=1000, alignment=ft.MainAxisAlignment.CENTER)))
        else:
            tab_imagem.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), alignment=ft.alignment.center, width=1000, height=700, border = ft.border.all(2, ft.colors.RED))]
    except Exception as e:
        print(e)
chamar_print_img_membro()

minha_tab_imagem = ft.Container(content=tab_imagem, border=ft.border.all(2, ft.colors.RED), width=950, height=700)
    
####################################################################################################################

##################################################### PDF LISTA DE CURSISTAS ###########################################################

tb_imagem = ft.DataTable(
    border=ft.border.all(2, "red"),
    rows=[]

)

curso_to_pdf = ft.Dropdown(options=[
        ft.dropdown.Option("Todos cursos"),
        ft.dropdown.Option("Conceitos Gerais da Bíblia"),
        ft.dropdown.Option("São Pedro"),
        ft.dropdown.Option("São Lucas"),
        ft.dropdown.Option("Carta aos Coríntios"),
        ft.dropdown.Option("Carta de Pedro"),
    ], 
)
def save_nota_cursistas(e:FilePickerResultEvent):
    c = conecta_cursta.cursor()
    if curso_to_pdf.value=='Todos cursos':
        c.execute(f"SELECT * FROM cursistas ORDER BY nome")
        users = c.fetchall()
        print(users)
        print('Passou aqui!')
        #your_file_save_location = e.path
        
        #your_file_save_location = nome_cursista_formatado
        #e.file_name = 'lista_de_cursistas' + ".pdf"
        print(f'OOOOODODODOD{curso_to_pdf.value}')
        file_path = f'lista_de_cursistas_de_{curso_to_pdf.value}.pdf'
        doc = SimpleDocTemplate(file_path, pagesizes=letter)
        elements = []
        styles = getSampleStyleSheet()
        styles['Normal'].fontName = 'Times-Roman'
        styles['Normal'].fontSize = 12
        styles['Normal'].leading = 18
        styles['Title'].fontName = 'Times-Bold'
        styles['Title'].fontSize = 14
        src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
        imagem = imagemPDF(src, width=50, height=50)
        elements.append(imagem)
        elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
        elements.append(Paragraph('Lista de cursistas', styles['Title']))
        elements.append(Paragraph(f'{curso_to_pdf.value}', styles['Title']))
        
        keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota']
        result = [dict(zip(keys, values)) for values in users]
        list_order = []
        list_order.append(['Nº','Nome', 'Paróquia', 'Centro', 'Local', 'Nota'])
        count = 0
        for x in result:
            count +=1
            list_order.append([
                count,
                x['nome'],
                x['paroquia'],
                x['centro'],
                x['local'],
                x['nota']
            ])
        table = Table(list_order)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), cores.beige),
            ('TEXTCOLOR', (0,0), (-1,0), cores.black),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BUTTONPADDING', (0,0), (-1,0), 12),
            
            ('ALIGN', (1,0), (0,-1), 'CENTER'),
            ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
            ('FONTSIZE', (1,0), (0,-1), 12),
            ('BUTTONPADDING', (1,0), (0,-1), 8),
            ('INNERGRID', (0,0), (-1,-1), 0.25, cores.black),
            ('BOX', (0,0), (-1,-1), 0.25, cores.black)
        ]))

        elements.append(table)
        doc.build(elements)

    else:    
        c.execute(f"SELECT * FROM cursistas WHERE curso='{curso_to_pdf.value}' ORDER BY nome")
        users = c.fetchall()
        print(users)
        print('Passou aqui!')
        #your_file_save_location = e.path
        
        #your_file_save_location = nome_cursista_formatado
        #e.file_name = 'lista_de_cursistas' + ".pdf"
        print(f'OOOOODODODOD{curso_to_pdf.value}')
        file_path = f'lista_de_cursistas_{curso_to_pdf.value}.pdf'
        doc = SimpleDocTemplate(file_path, pagesizes=letter)
        elements = []
        styles = getSampleStyleSheet()
        styles['Normal'].fontName = 'Times-Roman'
        styles['Normal'].fontSize = 12
        styles['Normal'].leading = 18
        styles['Title'].fontName = 'Times-Bold'
        styles['Title'].fontSize = 14
        src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
        imagem = imagemPDF(src, width=50, height=50)
        elements.append(imagem)
        elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
        elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
        elements.append(Paragraph('Lista de cursistas', styles['Title']))
        elements.append(Paragraph(F'Curso de {curso_to_pdf.value}', styles['Title']))
        
        keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota']
        result = [dict(zip(keys, values)) for values in users]
        list_order = []
        list_order.append(['Nº','Nome', 'Paróquia', 'Centro', 'Local', 'Nota'])
        count = 0
        for x in result:
            count +=1
            list_order.append([
                count,
                x['nome'],
                x['paroquia'],
                x['centro'],
                x['local'],
                x['nota']
            ])
        table = Table(list_order)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), cores.beige),
            ('TEXTCOLOR', (0,0), (-1,0), cores.black),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BUTTONPADDING', (0,0), (-1,0), 12),
            
            ('ALIGN', (1,0), (0,-1), 'CENTER'),
            ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
            ('FONTSIZE', (1,0), (0,-1), 12),
            ('BUTTONPADDING', (1,0), (0,-1), 8),
            ('INNERGRID', (0,0), (-1,-1), 0.25, cores.black),
            ('BOX', (0,0), (-1,-1), 0.25, cores.black)
        ]))

        elements.append(table)
        doc.build(elements)

files_saves=ft.FilePicker(on_result=save_nota_cursistas)


def on_clicks_handles(e):
    files_saves.save_file()


tabela_cursos = ft.Column([], scroll=True, visible=False)
def chamar_print_cursistas(curso_to_pdf):
    try:
        #curso_to_pdf = curso_to_pdf.value
        c = conecta_cursta.cursor()
        if curso_to_pdf == 'Todos cursos':
            c.execute(f"SELECT * FROM cursistas ORDER BY nome")
        else:    
            c.execute("SELECT * FROM cursistas WHERE curso=?", (curso_to_pdf,))
        users = c.fetchall()
        print(users)
        tabela_cursos.controls.clear()
        tabela_cursos.controls.append(ft.Row([ft.Text('Lista de cursistas', weight='bold', size=20)], width=1000, alignment=ft.MainAxisAlignment.CENTER))
        if not users == []:
            keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota', 'imagem']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                #id.value = ['id']
                if x['imagem']==None:
                    tabela_cursos.controls.append(ft.Row([ft.Text('        '), ft.Text('Não há imagem disponível', width=200, height=200), ft.Text(x['nome'])]))    
                else:
                    tabela_cursos.controls.append(ft.Container(content=ft.Row([ft.Text('        '),  ft.Image(src=x['imagem'], border_radius=ft.border_radius.all(10), width=100, height=100), ft.Text(x['nome'])], )))
            tabela_cursos.controls.append(ft.Container(content=ft.Row([ft.FloatingActionButton(text='Guardar em pdf', icon=ft.icons.SAVE, on_click=on_clicks_handles)], width=1000, alignment=ft.MainAxisAlignment.CENTER)))
        else:
            tabela_cursos.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), alignment=ft.alignment.center, width=990, height=630)]
    except Exception as e:
        print(e)
chamar_print_cursistas(curso_to_pdf.value)
minha_tab_cursos = ft.Container(content=ft.Column([curso_to_pdf, tabela_cursos]), border=ft.border.all(2, ft.colors.RED), width=950, height=700)


#########################################################################################################
   
def save_nota_actividades(e:FilePickerResultEvent):
    
    c = conecta_actividade.cursor()
    c.execute("SELECT * FROM actividades ORDER BY data_ini")
    users = c.fetchall()
    print(users)
    print('Passou aqui!')
    #your_file_save_location = e.path
    
    #your_file_save_location = nome_actividade_formatado
    e.file_name = 'lista_de_actividades' + ".pdf"
    file_path = 'lista_de_actividades.pdf'
    doc = SimpleDocTemplate(file_path, pagesizes=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Times-Roman'
    styles['Normal'].fontSize = 12
    styles['Normal'].leading = 18
    styles['Title'].fontName = 'Times-Bold'
    styles['Title'].fontSize = 14
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Paragraph('Programa de actividades', styles['Title']))
    
    keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
    result = [dict(zip(keys, values)) for values in users]
    list_order = []
    list_order.append(['Nº','Nome', 'Data de realização', 'Local'])
    count = 0
    for x in result:
        count +=1
        list_order.append([
            count,
            x['nome'],
            x['data_ini'],
            x['local'],
        ])
        #list_order.append([Spacer(1, 12)])
        
    table = Table(list_order)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cores.beige),
        ('TEXTCOLOR', (0,0), (-1,0), cores.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
        
        ('ALIGN', (1,0), (0,-1), 'CENTER'),
        ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
        ('FONTSIZE', (1,0), (0,-1), 12),
        ('BUTTONPADDING', (1,0), (0,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.25, cores.black),
        ('BOX', (0,0), (-1,-1), 0.25, cores.black)
    ]))

    elements.append(table)
    doc.build(elements)

files_save_ac=ft.FilePicker(on_result=save_nota_actividades)

def on_click_handles_ac(e):
    files_save_ac.save_file()


tab_imagem_ac = ft.Column([], scroll=True)
def chamar_print_actividades():
    try:
        c = conecta_actividade.cursor()
        c.execute("SELECT * FROM actividades ORDER BY data_ini")
        users = c.fetchall()
        print(f'4343443434343{users}')
        tab_imagem_ac.controls.append(ft.Row([ft.Text('Lista de actividades', weight='bold', size=20)], width=1000, alignment=ft.MainAxisAlignment.CENTER))

        if not users == []:
            keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status', 'imagem']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                #id.value = ['id']
                if x['imagem']==None:
                    tab_imagem_ac.controls.append(ft.Row([ft.Text('        '), ft.Text('Não há imagem disponível', width=200, height=200), ft.Text(x['nome'])]))    
                else:
                    tab_imagem_ac.controls.append(ft.Container(content=ft.Row([ft.Text('        '), ft.Image(src=x['imagem'], border_radius=ft.border_radius.all(10), width=100, height=100), ft.Text(x['nome']), ft.Text(x['data_ini'])], )))
            tab_imagem_ac.controls.append(ft.Container(content=ft.Row([ft.FloatingActionButton(text='Guardar em pdf', icon=ft.icons.SAVE, on_click=on_click_handles_ac)], width=1000, alignment=ft.MainAxisAlignment.CENTER)))
        else:
            tab_imagem_ac.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), alignment=ft.alignment.center, width=1000, height=700, border = ft.border.all(2, ft.colors.RED))]
    except Exception as e:
        print(e)
chamar_print_actividades()

minha_tab_imagem_ac = ft.Container(content=tab_imagem_ac, border=ft.border.all(2, ft.colors.RED), width=950, height=700)
    
####################################################################################################################

tb_imprime_cursista = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Paróquia')),
        ft.DataColumn(ft.Text('Centro')),
        ft.DataColumn(ft.Text('Curso')),
        ft.DataColumn(ft.Text('Data de início')),
        ft.DataColumn(ft.Text('Data de término')),
        ft.DataColumn(ft.Text('Local de Realização')),
        ft.DataColumn(ft.Text('Nota final')),
    ],
    rows=[]

)

########################################################## PDF Cursista ##############################    
def save_nota_cursista(e:FilePickerResultEvent):
    c = conecta_cursta.cursor()
    meu_id = id_c_print.value
    if meu_id is None:
        print("ID não foi obtido corretamente.")
        return
    c.execute("SELECT * FROM cursistas WHERE id=?", (meu_id,))
    users = c.fetchall()
    print(users)
    
    tb_imprime_cursista.rows.clear()

    # Limpa as linhas da tabela antes de adicionar novos dados
    if not users == '':
        keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota']
        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            nome_c_print.value = x['nome']
            paroquia_c_print.value = x['paroquia']
            centro_c_print.value = x['centro']
            curso_c_print.value = x['curso']
            data_ini_c_print.value = x['data_ini']
            data_ter_c_print.value = x['data_ter']
            local_c_print.value = x['local']
            nota_c_print.value = x['nota']
    print('Passou aqui!')

    espaco = ft.Text()
    espaco.value = '\U00002702'+'-'*100
    
    your_file_save_location = e.path
    
    nome_cursista_formatado = nome_c_print.value.replace(' ', '_').lower()
    your_file_save_location = nome_cursista_formatado
    #e.file_name = your_file_save_location + ".pdf"
    #file_path = f'{your_file_save_location}.pdf'
    doc = SimpleDocTemplate(f'{your_file_save_location}.pdf', pagesizes=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Times-Roman'
    styles['Normal'].fontSize = 12
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Paragraph('Ficha de cursista', styles['Title']))
    elements.append(Paragraph(f'Nome do cursista: {nome_c_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Paróquia: {paroquia_c_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Centro: {centro_c_print.value}', styles['Normal']))
    elements.append(Spacer(1, 12))
    list_order = []
    list_order.append(['Nome do curso', 'Data de início', 'Data de término', 'Local de realização', 'Nota'])
    list_order.append([
        curso_c_print.value,
        data_ini_c_print.value,
        data_ter_c_print.value,
        local_c_print.value,
        nota_c_print.value,
    ])

    table = Table(list_order)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cores.beige),
        ('TEXTCOLOR', (0,0), (-1,0), cores.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
            
        ('ALIGN', (1,0), (0,-1), 'CENTER'),
        ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
        ('FONTSIZE', (1,0), (0,-1), 12),
        ('BUTTONPADDING', (1,0), (0,-1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    
    assinatura = Table([[
        Paragraph(f'<para alignment="CENTER">O(A) cursista</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">O(A) Secretário(a)</para>', styles['Normal']),
    ]])

    assinatura.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))

    elements.append(assinatura)

    linha = Table([[
        Paragraph(f'<para alignment="CENTER">__________________________</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">__________________________</para>', styles['Normal']),
    ]])

    linha.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))
    elements.append(linha)

    nome_sec = ft.Text()
    d = conn.cursor()
    d.execute("""SELECT associacao_membro_cargo.id, membros.nome as nome_membro, cargos.nome as nome_cargo, membros.contacto, membros.email
                FROM associacao_membro_cargo
                JOIN membros ON associacao_membro_cargo.membro_id = membros.id
                JOIN cargos ON associacao_membro_cargo.cargo_id = cargos.id
                WHERE cargos.id=3
                """)
    membros = d.fetchall()
    if not membros == []:
        keys = ['id', 'nome_membro', 'nome_cargo', 'contacto', 'email']
        resultados = [dict(zip(keys, values)) for values in membros]
        for membro in resultados:
            nome_sec.value = membro['nome_membro']

    nomes = Table([[
        Paragraph(f'<para alignment="CENTER">{nome_c_print.value}</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">{nome_sec.value}</para>', styles['Normal']),
    ]])

    nomes.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))
    elements.append(nomes)
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))


    elements.append(Paragraph(f'{espaco.value}', styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Paragraph('Ficha de cursista', styles['Title']))
    elements.append(Paragraph(f'Nome do cursista: {nome_c_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Paróquia: {paroquia_c_print.value}', styles['Normal']))
    elements.append(Paragraph(f'Centro: {centro_c_print.value}', styles['Normal']))
    elements.append(Spacer(1, 12))
    list_order = []
    list_order.append(['Nome do curso', 'Data de início', 'Data de término', 'Local de realização', 'Nota'])
    list_order.append([
        curso_c_print.value,
        data_ini_c_print.value,
        data_ter_c_print.value,
        local_c_print.value,
        nota_c_print.value,
    ])

    table = Table(list_order)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cores.beige),
        ('TEXTCOLOR', (0,0), (-1,0), cores.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
            
        ('ALIGN', (1,0), (0,-1), 'CENTER'),
        ('FONTNAME', (1,0), (0,-1), 'Times-Roman'),
        ('FONTSIZE', (1,0), (0,-1), 12),
        ('BUTTONPADDING', (1,0), (0,-1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    
    assinatura = Table([[
        Paragraph(f'<para alignment="CENTER">O(A) cursista</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">O(A) Secretário(a)</para>', styles['Normal']),
    ]])

    assinatura.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))

    elements.append(assinatura)

    linha = Table([[
        Paragraph(f'<para alignment="CENTER">__________________________</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">__________________________</para>', styles['Normal']),
    ]])

    linha.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))
    elements.append(linha)

    nome_sec = ft.Text()
    d = conn.cursor()
    d.execute("""SELECT associacao_membro_cargo.id, membros.nome as nome_membro, cargos.nome as nome_cargo, membros.contacto, membros.email
                FROM associacao_membro_cargo
                JOIN membros ON associacao_membro_cargo.membro_id = membros.id
                JOIN cargos ON associacao_membro_cargo.cargo_id = cargos.id
                WHERE cargos.id=3
                """)
    membros = d.fetchall()
    if not membros == []:
        keys = ['id', 'nome_membro', 'nome_cargo', 'contacto', 'email']
        resultados = [dict(zip(keys, values)) for values in membros]
        for membro in resultados:
            nome_sec.value = membro['nome_membro']

    nomes = Table([[
        Paragraph(f'<para alignment="CENTER">{nome_c_print.value}</para>', styles['Normal']),
        Paragraph(f'<para alignment="CENTER">{nome_sec.value}</para>', styles['Normal']),
    ]])

    nomes.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BUTTONPADDING', (0,0), (-1,0), 12),
    ]))
    elements.append(nomes)

    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    #elements.append(Paragraph())
    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    doc.build(elements)

file_save_cursista=ft.FilePicker(on_result=save_nota_cursista)

def on_cursista_handle(e):
    meu_id = e.control.data['id']  # Assumindo que o ID está no campo 'id' do dicionário
    id_c_print.value = meu_id
    nome_c_print.value = e.control.data['nome']  # Adicione esta linha para configurar o nome corretamente
    file_save_cursista.file_name = nome_c_print.value
    file_save_cursista.save_file()

id_c_print = ft.Text()
nome_c_print = ft.Text()
paroquia_c_print = ft.Text()
centro_c_print = ft.Text()
curso_c_print = ft.Text()
data_ini_c_print = ft.Text()
data_ter_c_print = ft.Text()
local_c_print = ft.Text()
nota_c_print = ft.Text()

minha_tab_print_cursista = ft.Column([])
def chamar_print_cursista():
    try:
        c = conecta_cursta.cursor()
        c.execute("SELECT * FROM cursistas ORDER BY nome")
        users = c.fetchall()
        print(users)

        tb_imprime_cursista.rows.clear()

        if not users == '':
            keys = ['id', 'nome', 'paroquia', 'centro', 'curso', 'data_ini', 'data_ter', 'local','nota']
            result = [dict(zip(keys, values)) for values in users]
            for x in result:
                tb_imprime_cursista.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon=ft.icons.PICTURE_AS_PDF_ROUNDED, icon_color=ft.colors.GREEN, tooltip='Editar',
                                                data=x, 
                                                on_click=on_cursista_handle
                                                ),

                                ])),
                            ft.DataCell(ft.Text(x['nome'])),
                            ft.DataCell(ft.Text(x['paroquia'])),
                            ft.DataCell(ft.Text(x['centro'])),
                            ft.DataCell(ft.Text(x['curso'])), 
                            ft.DataCell(ft.Text(x['data_ini'])),
                            ft.DataCell(ft.Text(x['data_ter'])),
                            ft.DataCell(ft.Text(x['local'])),
                            ft.DataCell(ft.Text(x['nota'])),   
                        ],
                    ),
                )
        if users == []:
            minha_tab_print_cursista.controls.clear()
            minha_tab_print_cursista.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tab_print_cursista.alignment = ft.alignment.center
            minha_tab_print_cursista.width = 995
            minha_tab_print_cursista.height = 700
        else:
            minha_tab_print_cursista.controls.clear()
            minha_tab_print_cursista.controls = [ft.Row([tb_imprime_cursista])]
            minha_tab_print_cursista.alignment = ft.alignment.top_left
            minha_tab_print_cursista.scroll = 'auto'
    except Exception as e:
        print(e)
chamar_print_cursista()

##################################################################################################################

################################################### PDF ACTIVIDADE ################################################

tb_imprime_actividade = ft.DataTable(
    border=ft.border.all(2, "red"),
    columns=[
        ft.DataColumn(ft.Text('Acção')),
        ft.DataColumn(ft.Text('Nome')),
        ft.DataColumn(ft.Text('Local')),
    ],
    rows=[]
)

def save_nota_actividade(e:FilePickerResultEvent):
    c = conecta_actividade.cursor()
    meu_id = id_ac_print.value
    if meu_id is None:
        print("ID não foi obtido corretamente.")
        return
    c.execute("SELECT * FROM actividades WHERE id=?", (meu_id,))
    users = c.fetchall()
    print(users)
    
    tb_imprime_actividade.rows.clear()

    # Limpa as linhas da tabela antes de adicionar novos dados
    if not users == '':
        keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            nome_ac_print.value = x['nome']
            data_ini_ac_print.value = x['data_ini']
            hora_ini_ac_print.value = x['hora_ini']
            data_ter_ac_print.value = x['data_ter']
            hora_ter_ac_print.value = x['hora_ter']
            local_ac_print.value = x['local']
    print('Passou aqui!')

    espaco = ft.Text()
    espaco.value = '\U00002702'+'-'*100
    
    your_file_save_location = e.path
    
    nome_actividade_formatado = nome_ac_print.value.replace(' ', '_').lower()
    your_file_save_location = nome_actividade_formatado
    #e.file_name = your_file_save_location + ".pdf"
    #file_path = f'{your_file_save_location}.pdf'
    doc = SimpleDocTemplate(f'{your_file_save_location}.pdf', pagesizes=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Times-Roman'
    styles['Normal'].fontSize = 12
    src ='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Monitor Biblico Lenço Vermelho/Pastoral Biblica _LOGO.jpg'
    imagem = imagemPDF(src, width=50, height=50)
    elements.append(imagem)
    elements.append(Paragraph(f'<para alignment="CENTER">Arquidiocese de Luanda</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Paróquia de São Pedro Apóstolo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Centro do Espírito Santo</para>', styles['Normal']))
    elements.append(Paragraph(f'<para alignment="CENTER">Pastoral Bíblica</para>', styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f'<para alignment="CENTER">{nome_ac_print.value}</para>', styles['Heading3']))
    elements.append(Spacer(1, 12))
    if data_ter_ac_print.value!=None and hora_ter_ac_print.value!=None:
        elements.append(Paragraph(f'Data de início: {data_ini_ac_print.value}', styles['Normal']))
        elements.append(Paragraph(f'Hora de início: {hora_ini_ac_print.value}', styles['Normal']))
        elements.append(Paragraph(f'Data de término: {data_ter_ac_print.value}', styles['Normal']))
        elements.append(Paragraph(f'Hora de término: {hora_ter_ac_print.value}', styles['Normal']))
    else:
        elements.append(Paragraph(f'Data de realização: {data_ini_ac_print.value}', styles['Normal']))
    
    elements.append(Paragraph(f'Local de realização: {local_ac_print.value}', styles['Normal']))
        
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))

    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    #elements.append(Paragraph())
    #grand_total = sum([float(row[2]) for row in list_order[1:]])
    doc.build(elements)

file_save_actividade=ft.FilePicker(on_result=save_nota_actividade)

def on_actividade_handle(e):
    meu_id = e.control.data['id']  # Assumindo que o ID está no campo 'id' do dicionário
    id_ac_print.value = meu_id
    nome_ac_print.value = e.control.data['nome']  # Adicione esta linha para configurar o nome corretamente
    file_save_actividade.file_name = nome_ac_print.value
    file_save_actividade.save_file()

id_ac_print = ft.Text()
nome_ac_print = ft.Text()
data_ini_ac_print = ft.Text()
hora_ini_ac_print = ft.Text()
data_ter_ac_print = ft.Text()
hora_ter_ac_print = ft.Text()
local_ac_print = ft.Text()

minha_tab_print_actividade = ft.Column([])
def chamar_print_actividade():
    try:
        c = conecta_actividade.cursor()
        c.execute("SELECT * FROM actividades ORDER BY nome")
        users = c.fetchall()
        print(users)

        tb_imprime_actividade.rows.clear()

        if not users == '':
            keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
            result = [dict(zip(keys, values)) for values in users]
            for actividade in result:
                tb_imprime_actividade.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Row([
                                ft.IconButton(icon=ft.icons.PICTURE_AS_PDF_ROUNDED, icon_color=ft.colors.GREEN, tooltip='Editar',
                                                data=actividade, 
                                                on_click=on_actividade_handle
                                                ),

                                ])),
                            ft.DataCell(ft.Text(actividade['nome'])),
                            #ft.DataCell(ft.Text(actividade['data_ini'])),
                            #ft.DataCell(ft.Text(actividade['hora_ini'])),
                            #ft.DataCell(ft.Text(actividade['data_ter'])), 
                            #ft.DataCell(ft.Text(actividade['hora_ter'])), 
                            ft.DataCell(ft.Text(actividade['local'])),
                        ],
                    ),
                )
        if users == []:
            minha_tab_print_actividade.controls.clear()
            minha_tab_print_actividade.controls = [ft.Container(content=ft.Text('Não há dados na tabela!', weight='bold', size=40), border = ft.border.all(2, ft.colors.RED), width = 1000, height = 700, alignment = ft.alignment.center)]
            minha_tab_print_actividade.alignment = ft.alignment.center
            minha_tab_print_actividade.width = 995
            minha_tab_print_actividade.height = 700
        else:
            minha_tab_print_actividade.controls.clear()
            minha_tab_print_actividade.controls = [ft.Row([tb_imprime_actividade])]
            minha_tab_print_actividade.alignment = ft.alignment.top_left
            minha_tab_print_actividade.scroll = 'auto'
    except Exception as e:
        print(e)
chamar_print_actividade()


####################################################################################################################

#minha_tabela_cursista.visible = False 

minha_tabela_dataNasc.visible = False

minha_tabela_direccao.visible = True

minha_tabela_quotas.visible = False

minha_tabela_sacramento.visible = False

minha_tabela_promessa.visible = False

#buscar_texto()
minha_tabela_leitura = ft.Column([
    ft.Row([tb_membro_leitura], alignment=ft.MainAxisAlignment.CENTER
           )
])
minha_tabela_leitura.visible = False
