import datetime
import spacy
import json
import re
import logging
import transformers
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import threading
import flet as ft
from selenium import webdriver
import flet.version
from datepicker import DatePicker
from selection_type import SelectionType
from datetime import datetime, timedelta
from fletCalendar import *
from dadosgaleria import *
from myckeck import *
import datetime
import os
#Para imprimir em pdf devermos importar as seguintes bibliotecas:
#################################################################################
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line                                             #
from reportlab.lib.pagesizes import letter                                      #
from reportlab.lib import colors                                                #
from reportlab.lib.styles import getSampleStyleSheet                            #
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table, TableStyle #
                                , Spacer, Image)                                       #
#################################################################################
from tabela_usuario import (create_table, create_table_cargo, insert_into_cargos, create_table_associacao_membro_cargo, 
                            create_table_sacramento, insert_into_sacramentos, create_table_associacao_membro_sacramento,
                            create_table_quota, insert_into_quotas, create_table_associacao_membro_quota, create_table_leitura)
from tabela_cursista import create_table_cursista
from tabela_actividade import create_table_actividade
#from tabela_cargo import create_table_cargo
import sqlite3
#from datatable import (minha_tabela, tb, chamar_db, minha_tabela_cursista, tb_cursita, chamar_db_cursista, 
#                       minha_tabela_actividade, tb_actividade, chamar_db_actividade, 
#                       minha_tabela_actividade_em_andamento, chamar_db_actividade_em_andamento, tb_actividade_em_andamento, 
#                       minha_tabela_actividade_concluida, chamar_db_actividade_concluida, tb_actividade_concluida,
#                       minha_tabela_dataNasc, chamar_db_dataNasc, tb_membro_dataNasc, minha_tabela_direccao, chamar_db_por_cargos,
#                       tb_membro_directivos, chamar_db_cargo, chamar_db_associacao_membro_cargo,
#                       chamar_db_sacramento, minha_tabela_sacramento, tb_membro_sacramentos, chamar_db_por_sacramentos, 
#                       minha_tabela_quotas, tb_membro_quotas, chamar_db_por_quotas, chamar_db_quota, chamar_db_promessa, 
#                       tb_membro_promessa, audio1, minha_tabela_promessa, minha_tabela_leitura, minha_tabela_membro, 
#                       chamar_db_membro, tb_membro, aniversariante, dlg, dlg_actividade, dlg_cursista, chamar_print_membro, 
#                       file_save, tb_imprime, minha_tab_print_membro, chamar_print_img_membro, tab_imagem, minha_tab_imagem, files_save,
#                       chamar_print_cursistas, tabela_cursos, curso_to_pdf, files_saves, minha_tab_cursos, chamar_print_actividades, tab_imagem_ac,
#                       minha_tab_imagem_ac, files_save_ac)
from datatable import *
conn = sqlite3.connect('db/membro.db', check_same_thread = False)
conecta_cursista = sqlite3.connect('db/cursista.db', check_same_thread=False)
conecta_actividade = sqlite3.connect('db/actividade.db', check_same_thread=False)
conecta_cargo = sqlite3.connect('db/cargo.db', check_same_thread = False)

thread = threading.Lock() 

def main(page: ft.Page):
    page.title = "Sistema de Gestão da Pastoral Bíblica"  
    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    }
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.BLUE_200,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.RED,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=10,
            radius=10,
            main_axis_margin=1,
            cross_axis_margin=1,
            interactive=True,
        )
    )
    create_table()
    create_table_cursista()
    create_table_actividade()
    create_table_cargo()
    insert_into_cargos()
    create_table_associacao_membro_cargo()
    create_table_sacramento()
    insert_into_sacramentos()
    create_table_associacao_membro_sacramento()
    create_table_quota()
    insert_into_quotas()
    create_table_associacao_membro_quota()
    create_table_leitura()
    #create_table_cargo()
    #mycal = FletCalendar(page)
    page.overlay.append(audio1)
    
    page.overlay.append(file_save)

    page.overlay.append(files_save)

    page.overlay.append(files_saves)  

    page.overlay.append(files_save_ac)

    
    page.overlay.append(file_save_cursista)

    page.overlay.append(file_save_actividade)

    def on_submit_curso(e):
        chamar_print_cursistas(curso_to_pdf.value)
        tabela_cursos.visible = True
        print('Chegou aqui!')
        tabela_cursos.update()
        minha_tab_cursos.update()
        page.update()

    curso_to_pdf.on_change = on_submit_curso
    
    def show_input(event):
        minha_tabela.visible = False
        minha_tabela_actividade.visible = False
        minha_tabela_cursista.visible = False
        inputcon.visible = True
        inputcon.offset = ft.transform.Offset(0, 0)
        inputcon.update()
        page.update()

    def show_input_cursista(event):
        minha_tabela.visible = False
        minha_tabela_actividade.visible = False
        minha_tabela_cursista.visible = False
        inputcon_cursista.visible = True
        inputcon_cursista.offset = ft.Offset(0, 0)
        inputcon_cursista.update()
        page.update()

    def show_input_actividade(event):
        minha_tabela.visible = False
        minha_tabela_actividade.visible = False
        minha_tabela_cursista.visible = False        
        inputcon_actividade.visible = True
        inputcon_actividade.offset = ft.Offset(0, 0)
        inputcon_actividade.update()
        print('Não sei porquê não abre!')
        page.update()

    def esconder_icon(event):
        minha_tabela.visible = True
        minha_tabela_actividade.visible = False
        minha_tabela_cursista.visible = False
        inputcon.visible = False
        minha_tabela.update()
        page.update()

    def esconder_icon_cursista(event):
        minha_tabela.visible = False
        minha_tabela_actividade.visible = False
        minha_tabela_cursista.visible = True
        inputcon_cursista.visible = False
        minha_tabela_cursista.update()
        page.update()

    def esconder_icon_actividade(event):
        minha_tabela.visible = False
        minha_tabela_actividade.visible = True
        minha_tabela_cursista.visible = False
        inputcon_actividade.visible = False
        minha_tabela_actividade.update()
        page.update()

    def salvar_dados(event):
        try:
            with thread:
                c=conn.cursor()

                if (nome.value=='' or data_nasc.value=='' or contacto.value=='' or genero.value=='' 
                    or email.value=='' or morada.value==''):
                            
                    page.snack_bar = ft.SnackBar(
                        ft.Text('Não foi possível salvar os dados. Há, pelo menos falta de uma informação!'),
                        bgcolor=ft.colors.RED    
                    )
                    page.snack_bar.open = True

                else: 
                    data_nasc_value = datetime.datetime.strptime(data_nasc.value, '%d/%m/%Y')
                    sete_anos_atras = datetime.datetime(2017, 1, 1) 

                    if data_nasc_value > sete_anos_atras:
                        print(f'{data_nasc_value} e {sete_anos_atras}')
                        page.snack_bar = ft.SnackBar(
                            ft.Text("Data de nascimento não pode ser superior a 2017"),                            
                            bgcolor=ft.colors.RED    
                        )
                        page.snack_bar.open = True
                        page.update()
                    else:
                        c.execute("""INSERT INTO membros 
                        (nome, data_nasc, genero, morada, contacto, email,
                        moradia, frequenta_escola, estuda_sabado, curso_acad,
                        e_trabalhador, local_trabalho, funcao_trabalho, trabalha_fim_semana,
                        catecumeno, n_f_catequese, tempo_grupo, ano_entrada, tem_cargo,
                        tem_sacramento, tem_promessa, data_promessa, imagem) VALUES
                        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)                     
                            """, (
                        nome.value, data_nasc.value, genero.value, morada.value, contacto.value,
                        email.value, moradia.value, frequenta_escola.value, estuda_sabado.value,
                        curso_acad.value, trabalhador.value, local_trabalho.value, funcao.value,
                        trabalha_fim_sem.value, catecumeno.value, n_f_catequese.value, tempo_grupo.value,
                        ano_entrada.value, tem_cargo.value, tem_sacramento.value, tem_promessa.value,
                        data_promessa.value, imagem.src                  
                        ))    
                        membro = c.lastrowid
                        print(selected_cargos)
                        salvar_dados_membro_cargo(membro, selected_cargos)
                        salvar_dados_membro_sacramento(membro, selected_sacramentos)
                        conn.commit()    
                        nome.value='' 
                        data_nasc.value='' 
                        genero.value='' 
                        morada.value='' 
                        contacto.value=''
                        email.value='' 
                        frequenta_escola.value='Não' 
                        estuda_sabado.value=None
                        curso_acad.value='' 
                        trabalhador.value='Não' 
                        local_trabalho.value='' 
                        funcao.value=''
                        trabalha_fim_sem.value=None 
                        catecumeno.value='Sim'
                        n_f_catequese.value='' 
                        tempo_grupo.value='1 mês'
                        ano_entrada.value='2023' 
                        tem_cargo.value='Não' 
                        tem_sacramento.value='Não' 
                        tem_promessa.value='Não'
                        data_promessa.value='' 
                        imagem.src='/home/izata/Downloads/CARTOON.png'
                        tb_membro_dataNasc.rows.clear()
                        tb_membro_directivos.rows.clear()
                        tb_membro_sacramentos.rows.clear()
                        tb_membro.rows.clear()
                        tb_imprime.rows.clear()
                        tab_imagem.controls.clear()
                        minha_tabela.visible = True
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
                        inputcon.offset = ft.transform.Offset(2, 0)
                        inputcon.visible = False
                        print('Dados salvados com sucesso!')
                        page.snack_bar = ft.SnackBar(
                            ft.Text('Dados salvados com sucesso!'),
                            bgcolor=ft.colors.GREEN    
                        )
                        #page.snack_bar.open = True
                        #inputcon.update()
                        page.update()
        except Exception as e:
            inputcon.visible = False
            print('Não foi possível salvar os dados!')
            page.snack_bar = ft.SnackBar(
                ft.Text('Erro ao salvar os dados!'),
                bgcolor=ft.colors.RED    
            )
            page.snack_bar.open = True
            page.update()

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


    def update_status():
        try:  
            with thread:          
                c = conecta_actividade.cursor()
                c.execute('SELECT * FROM actividades WHERE status="Em andamento"')
                em_andamento = c.fetchall()
                if not em_andamento == []:
                    keys = ['id', 'nome', 'data_ini', 'hora_ini', 'data_ter', 'hora_ter', 'local', 'status']
                    resultados = [dict(zip(keys, values)) for values in em_andamento]
                    for actividade in resultados:
                        data_ter = converter_data_hora_para_segundos(actividade['data_ter'], actividade['hora_ter']) 
                        tempo_atual = obter_tempo_atual_em_segundos()
                        data_activ = data_ter
                        for row in em_andamento:
                            id_atividade = row[0]

                            if data_activ  < tempo_atual:
                                c.execute('UPDATE actividades SET status="Concluída" WHERE id=?', (id_atividade,))
                                conecta_actividade.commit()
                            else:
                                c.execute('UPDATE actividades SET status="Em andamento" WHERE id=?', (id_atividade,))
                                conecta_actividade.commit()
                            tb_actividade.rows.clear()
                            tb_actividade_em_andamento.rows.clear()
                            tb_actividade_concluida.rows.clear()
                            chamar_db_actividade()
                            chamar_db_actividade_em_andamento()
                            chamar_db_actividade_concluida()
                            print('Vamos adicionar control!')
                            #tb_actividade.update()
                            #tb_actividade_em_andamento.update()
                            #tb_actividade_concluida.update()
                            page.update()
        except Exception as e:
            print(e)
    update_status()

    def salvar_dados_cursista(event):
        try:
            c=conecta_cursista.cursor()
            c.execute("INSERT INTO cursistas (nome, paroquia, centro, curso, data_ini, data_ter, local, nota, imagem) VALUES(?,?,?,?,?,?,?,?,?)", (nome_cursista.value, paroquia.value, centro.value, curso.value, data_ini.value, data_ter.value, local.value, nota.value, imagem_cursista.src))
            conecta_cursista.commit()
            inputcon_cursista.visible = False
            print('Dados salvados com sucesso!')
            page.snack_bar = ft.SnackBar(
                ft.Text('Dados salvados com sucesso!'),
                bgcolor=ft.colors.GREEN    
            )
            page.snack_bar.open = True
            tb_cursita.rows.clear()
            #tabela_cursos.controls.clear()
            tb_imprime_cursista.rows.clear()
            #minha_tab_print_cursista.controls.clear()
            chamar_db_cursista()
            #minha_tabela_cursista.content.clean()
            chamar_print_cursistas(curso_to_pdf)
            chamar_print_cursista()
            tabela_cursos.update()
            minha_tab_cursos.update()

            #tb_cursita.update()
            minha_tabela_cursista.update()
            minha_tab_print_cursista.update()
            minha_tabela_cursista.visible = True
            page.update()
        except Exception as e:
            inputcon_cursista.visible = False
            minha_tabela_cursista.visible = True
            print('Não foi possível salvar os dados!')
            page.snack_bar = ft.SnackBar(
                ft.Text(e, ': Erro ao salvar os dados!'),
                bgcolor=ft.colors.RED    
            )
            page.snack_bar.open = True
            page.update()


    def salvar_dados_actividade(evento):
        try:
            with thread:
                c=conecta_actividade.cursor()
                c.execute('INSERT INTO actividades (nome, data_ini, hora_ini, data_ter, hora_ter, local, status, imagem) VALUES(?,?,?,?,?,?,?,?)', (nome_actividade.value, data_actividade.value, hora_actividade.value, data_fim_actividade.value, hora_fim_actividade.value ,local_actividade.value, status_actividade, imagem_actividade.src))
                if nome_actividade.value=='' or data_actividade.value=='' or hora_actividade.value=='' or data_fim_actividade.value=='' or hora_fim_actividade.value=='' or  local_actividade.value=='' or status_actividade=='':
                    inputcon_cursista.visible = False
                    page.snack_bar = ft.SnackBar(
                        ft.Text('Não foi possível salvar os dados. Há, pelo menos falta de uma informação!'),
                        bgcolor=ft.colors.RED    
                    )
                    page.snack_bar.open = True
                    page.update()
                else:
                    conecta_actividade.commit()
                    
                    inputcon_actividade.visible = False
                    page.snack_bar = ft.SnackBar(
                        ft.Text('Uma actividade foi programada!'),
                        bgcolor=ft.colors.GREEN
                    )
                    page.snack_bar.open = True
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
                    #tb_actividade.update()
                    #tb_actividade_concluida.update()
                    #tb_actividade_em_andamento.update()
                    minha_tabela_actividade.visible = True

                    page.update()

        except Exception as e:
            inputcon_cursista.visible = False
            print(e, 'Não foi possível salvar os dados!')
            page.snack_bar = ft.SnackBar(
                ft.Text('Erro ao salvar os dados!'),
                bgcolor=ft.colors.RED    
            )
            page.snack_bar.open = True
            page.update()


    def capitalize_first_letter(e):
        print(f'Valor original: {e.control.value}')
        e.control.value = e.control.value.title()
        print(f'Novo valor: {e.control.value.split()}')
        if 'Da' in e.control.value.strip():
            print(e.control.value.strip())
            e.control.value = e.control.value.replace(' Da ', ' da ')
        if 'Do' in e.control.value.strip():
            print(e.control.value.strip())
            e.control.value = e.control.value.replace(' Do ', ' do ')
        if 'Das' in e.control.value.strip():
            print(e.control.value.strip())
            e.control.value = e.control.value.replace(' Das ', ' das ')
        if 'Dos' in e.control.value.strip():
            print(e.control.value.strip())
            e.control.value = e.control.value.replace(' Dos ', ' dos ')
        if 'De' in e.control.value.strip():
            print(e.control.value.strip())
            e.control.value = e.control.value.replace(' De ', ' de ')
             
            
        e.control.update()



    nome = ft.TextField(label='Nome completo', on_change=capitalize_first_letter,prefix_icon=ft.icons.PERSON, width=790)
    
    cal_date_birth = SetCalendar(update_callback=None, start_year=2015)
    date_birth = DateSetUp(cal_grid=cal_date_birth)

    calendar_container = Container()
    
    open_calendar_button = OpenCalendarButton(date_birth, calendar_container, date_birth.get_selected_date())
    data_nasc = ft.TextField(label="Data de nascimento", dense=True, hint_text="dd/mm/yyyy", width=260)

    def callback(e):
        if SelectionType.SINGLE.value==0:
            data_nasc.value = e[0].strftime("%d/%m/%Y") if len(e) > 0 else None
            print(data_nasc.value)
            data_nasc.update()
        """elif SelectionType.MULTIPLE.value and len(e) > 0:
            self.from_to_text.value = f"{[d.isoformat() for d in e]}"
            self.from_to_text.visible = True
        elif SelectionType.RANGE.value and len(e) > 0:
            self.from_to_text.value = f"From: {e[0]} To: {e[1]}"
            self.from_to_text.visible = True"""
    
    datepicker1 = DatePicker(
            selected_date=[data_nasc.value] if data_nasc.value else None,
            selection_type=int(SelectionType.SINGLE.value),
            locale="pt_PT",
            on_change=callback
            )
    
    def confirm_dlg(e):
        dlg_modal1.open = False
        dlg_modal1.update()
        page.update()
    
    def cancel_dlg(e):
        dlg_modal1.open = False
        dlg_modal1.update()
        page.update()
    
    dlg_modal1 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Calendário"),
            actions=[
                ft.TextButton("Sair", on_click=cancel_dlg),
                #ft.TextButton("Confirmar", on_click=confirm_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content=datepicker1,
            content_padding=0
        )
    def open_dlg_modal1(e):
        dlg_modal1.open = True
        page.update()

    cal_icon1 = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH, 
            on_click=open_dlg_modal1, 
            
            width=40,
            right=0,
            style=ft.ButtonStyle(
                padding=ft.Padding(4,0,0,0),
                shape={
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                    },
            ))

    stack = ft.Stack([data_nasc, cal_icon1])


    genero = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Masculino', label='Masculino'),
            ft.Radio(value='Feminino', label='Feminino')
        ])
    ]))
    morada = ft.TextField(
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

    contacto = TextField(
        label="Contacto",
        on_change=on_input_change,
        width=250,
        prefix_icon=icons.PHONE, color=ft.colors.BLUE,
        hint_text='Exemplo: 929078877',
    )
    def on_email_change(e):
        email = e.control.value
        padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(padrao, email):
            e.control.error = None
            e.control.value = e.control.value.lower()
            e.control.color=ft.colors.BLACK
            e.control.update()
        else:
            e.control.error = "Formato de e-mail inválido"
            e.control.color=ft.colors.RED
            e.control.update()

    email = ft.TextField(label='E-mail',hint_text='Exemplo: pastoralbiblica@gmail.com', on_change=on_email_change, prefix_icon=ft.icons.EMAIL, width=350)
    moradia = ft.Dropdown(options=[
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
        ], width=170, 
         label='Com quem vive?', prefix_icon=icons.FAMILY_RESTROOM
    )

    def on_frequenta_escola_change(e):
        if e.control.value == 'Sim':
            estuda_sabado.disabled = False
            curso_acad.disabled = False
            estuda_sabado.update()
            curso_acad.update()
        else:
            estuda_sabado.disabled = True
            curso_acad.disabled = True
            estuda_sabado.update()
            curso_acad.update()

    frequenta_escola = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), on_change=on_frequenta_escola_change)
    frequenta_escola.value = 'Não'
    estuda_sabado = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]),  disabled=True)
    curso_acad = ft.TextField(label='Curso', width=400, disabled = True, prefix_icon=ft.icons.BOOK, )
    
    def on_trabalhador_change(e):
        if e.control.value == 'Sim':
            local_trabalho.disabled = False
            funcao.disabled = False
            trabalha_fim_sem.disabled = False
            local_trabalho.update()
            funcao.update()
            trabalha_fim_sem.update()
        else:
            local_trabalho.disabled = True
            funcao.disabled = True
            trabalha_fim_sem.disabled = True
            local_trabalho.update()
            funcao.update()
            trabalha_fim_sem.update()

    trabalhador = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), on_change=on_trabalhador_change)
    trabalhador.value = 'Não'
    local_trabalho = ft.TextField(label='Onde trabalha?', width=400, disabled = True)
    funcao = ft.TextField(label='Em que área ou função trabalha?', width=400, disabled = True)
    trabalha_fim_sem = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), disabled = True)

    def on_catequese_change(e):
        if catecumeno.value=='Sim':
            n_f_catequese.disabled = True
            n_f_catequese.update()
        else:
            n_f_catequese.disabled = False
            n_f_catequese.update()
        
    
    catecumeno = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não'),
            ft.Radio(value='Já não frequento', label='Já não frequenta')
        ])
    ]), on_change=on_catequese_change)
    catecumeno.value = 'Sim'


    n_f_catequese = ft.TextField(label='Nunca frequentou ou se já não frequenta, porquê?', width=400, disabled=True)
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
            ano_entrada.value = '2023'
            ano_entrada.update()
            #data.update()
        if data == '1 ano':
            ano_entrada.value = '2022'
            ano_entrada.update()
            e.control.update()
        if data == '2 anos':
            ano_entrada.value = '2021'
            ano_entrada.update()
            e.control.update()
        if data == '3 anos':
            ano_entrada.value = '2020'
            ano_entrada.update()
            e.control.update()    
        if data == '4 anos':
            ano_entrada.value = '2019'
            ano_entrada.update()
            e.control.update()
        if data == '5 anos':
            ano_entrada.value = '2018'
            ano_entrada.update()
            e.control.update()
        if data == '6 anos':
            ano_entrada.value = '2017'
            ano_entrada.update()
            e.control.update()
        if data == '7 anos':
            ano_entrada.value = '2016'
            ano_entrada.update()
            e.control.update()
        if data == '8 anos':
            ano_entrada.value = '2015'
            ano_entrada.update()
            e.control.update()    
        if data == '9 anos':
            ano_entrada.value = '2014'
            ano_entrada.update()
            e.control.update()
        if data == '10 anos':
            ano_entrada.value = '2013'
            ano_entrada.update()
            e.control.update() 
        if data == '11 anos':
            ano_entrada.value = '2012'
            ano_entrada.update()
            e.control.update()
        if data == '12 anos':
            ano_entrada.value = '2011'
            ano_entrada.update()
            e.control.update()
        if data == '13 anos':
            ano_entrada.value = '2010'
            ano_entrada.update()
            e.control.update()
        if data == '14 anos':
            ano_entrada.value = '2009'
            ano_entrada.update()
            e.control.update()
        if data == '15 anos':
            ano_entrada.value = '2008'
            ano_entrada.update()
            e.control.update()
        if data == '16 anos':
            ano_entrada.value = '2007'
            ano_entrada.update()
            e.control.update()
        if data == '17 anos':
            ano_entrada.value = '2006'
            ano_entrada.update()
            e.control.update()
        if data == '18 anos':
            ano_entrada.value = '2005'
            ano_entrada.update()
            e.control.update()
        if data == '19 anos':
            ano_entrada.value = '2004'
            ano_entrada.update()
            e.control.update()
        if data == '20 anos':
            ano_entrada.value = '2003'
            ano_entrada.update()
            e.control.update()
        if data == '21 anos':
            ano_entrada.value = '2002'
            ano_entrada.update()
            e.control.update()
        if data == '22 anos':
            ano_entrada.value = '2001'
            ano_entrada.update()
            e.control.update()
        if data == '23 anos':
            ano_entrada.value = '2000'
            ano_entrada.update()
            e.control.update()
        if data == '24 anos':
            ano_entrada.value = '1999'
            ano_entrada.update()
            e.control.update()
        if data == '25 anos':
            ano_entrada.value = '1998'
            ano_entrada.update()
            e.control.update()

    tempo_grupo = ft.Dropdown(
        options=opcoes,
        label="Tempo no Grupo",
        width=315,
        
        on_change=on_change_tempo
    )
    tempo_grupo.value = '1 mês'

    ft.TextField(label='Tempo no grupo', width=315)

    def on_change_ano(e):
        data = e.control.value 
        if data == '2022':
            tempo_grupo.value = '1 ano'
            tempo_grupo.update()
            e.control.update()
        if data == '2021':
            tempo_grupo.value = '2 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2020':
            tempo_grupo.value = '3 anos'
            tempo_grupo.update()
            e.control.update()    
        if data == '2019':
            tempo_grupo.value = '4 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2018':
            tempo_grupo.value = '5 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2017':
            tempo_grupo.value = '6 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2016':
            tempo_grupo.value = '7 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2015':
            tempo_grupo.value = '8 anos'
            tempo_grupo.update()
            e.control.update()    
        if data == '2014':
            tempo_grupo.value = '9 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2013':
            tempo_grupo.value = '10 anos'
            tempo_grupo.update()
            e.control.update() 
        if data == '2012':
            tempo_grupo.value = '11 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2011':
            tempo_grupo.value = '12 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2010':
            tempo_grupo.value = '13 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2009':
            tempo_grupo.value = '14 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2008':
            tempo_grupo.value = '15 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2007':
            tempo_grupo.value = '16 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2006':
            tempo_grupo.value = '17 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2005':
            tempo_grupo.value = '18 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2004':
            tempo_grupo.value = '19 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2003':
            tempo_grupo.value = '20 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2002':
            tempo_grupo.value = '21 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2001':
            tempo_grupo.value = '22 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '2000':
            tempo_grupo.value = '23 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '1999':
            tempo_grupo.value = '24 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '1998':
            tempo_grupo.value = '25 anos'
            tempo_grupo.update()
            e.control.update()
        if data == '1998':
            tempo_grupo.value = '1 mês'
            tempo_grupo.update()
            e.control.update()

    opcoes_anos_entrada = [ft.dropdown.Option(str(ano)) for ano in range(2023, 1997, -1)]
    ano_entrada = ft.Dropdown(options=opcoes_anos_entrada, label='Ano de entrada', width=315, on_change=on_change_ano)
    ano_entrada.value = '2023'
    def on_cargo_change(e):
        if e.control.value == 'Sim':
            cargo_outro.disabled = False
            cargo_outro.update()
        else:
            cargo_outro.disabled = True
            cargo_outro.update()  
              
    tem_cargo = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), on_change=on_cargo_change)
    tem_cargo.value = 'Não'
    
#====================================================================== CHECKBOX PARA CARGOS =================================================================================================
    selected_cargos = []

    # Lista de cargos disponíveis
    cargos_disponiveis = chamar_db_cargo()

    # Lista para manter os cargos selecionados
    checkboxes = []
    # Cria as checkboxes e adiciona ao layout
    def on_change_box(e):
        try:
            selected_cargos.clear()
            for checkbox in checkboxes:
                if checkbox.value == e.control.value:
                    e.control.checked = True
                    checkbox.set_checked(checkbox.is_checked())
                    if checkbox.is_checked()==True:
                        if checkbox.label=='Coordenador(a)':
                            selected_cargos.append(1)
                        if checkbox.label=='Vice-Coordenador(a)':
                            selected_cargos.append(2)
                        if checkbox.label=='Secretário(a)':
                            selected_cargos.append(3)
                        if checkbox.label=='Vice-secretário(a)':
                            selected_cargos.append(4)
                        if checkbox.label=='Tesoreiro(a)':
                            selected_cargos.append(5)
                        if checkbox.label=='Vice-Tesoreiro(a)':
                            selected_cargos.append(6)
                        if checkbox.label=='Responsável pela infância Bíblica':
                            selected_cargos.append(7)
                        if checkbox.label=='Responsável pela comunicação social':
                            selected_cargos.append(8)
                        if checkbox.label=='Responsável pelo Desporto':
                            selected_cargos.append(9)
                        if checkbox.label=='Responsável pela caridade e convívio':
                            selected_cargos.append(10)
                        if checkbox.label=='Responsável pelos Cursos Bíblicos':
                            selected_cargos.append(11)
                        if checkbox.label=='Responsável pelos materiais':
                            selected_cargos.append(12)
                        if checkbox.label=='Conselheiro':
                            selected_cargos.append(13)
                        if checkbox.label=='Outros cargos':
                            selected_cargos.append(14)
                    e.control.update()
            print(selected_cargos)
        except Exception as e:
            print(e)
    def create_checkbox():
        if not cargos_disponiveis=='':
            keys = ['id', 'nome', 'membro_id']  
            resultados =  [dict(zip(keys, values)) for values in cargos_disponiveis] 
            for cargo in resultados:
                checkbox = MyCheckbox(label=cargo['nome'], value=cargo['id'])
                checkbox.on_change = on_change_box
                checkboxes.append(checkbox)
                print(checkbox.value)
        return checkboxes
    create_checkbox()

    def salvar_dados_membro_cargo(membro, cargos):
        c=conn.cursor()

        for cargo in cargos:
            print(f'O membro {membro} possui o cargo {cargo}')
            c.execute('INSERT INTO associacao_membro_cargo (membro_id, cargo_id) VALUES (?,?)', (membro, cargo))
            conn.commit()
        
        
    column = ft.Column(controls=checkboxes)
    cargo_outro = ft.Container(column, disabled=True)
    
    
#====================================================================== CHECKBOX PARA SACRAMENTOS =================================================================================================

    selected_sacramentos = []
    
    sacramentos_disponiveis = chamar_db_sacramento()

    # Lista para manter os cargos selecionados
    sacra_checkboxes = []
    # Cria as checkboxes e adiciona ao layout
    def on_change_box_sacra(e):
        try:
            selected_sacramentos.clear()
            for checkbox in sacra_checkboxes:
                if checkbox.value == e.control.value:
                    e.control.checked = True
                    checkbox.set_checked(checkbox.is_checked())
                    if checkbox.is_checked()==True:
                        if checkbox.label=='Baptismo':
                            selected_sacramentos.append(1)
                        if checkbox.label=='1ª Comunhão':
                            selected_sacramentos.append(2)
                        if checkbox.label=='Crisma':
                            selected_sacramentos.append(3)
                        if checkbox.label=='Penitência':
                            selected_sacramentos.append(4)
                        if checkbox.label=='Matrimónio':
                            selected_sacramentos.append(5)                        
                    e.control.update()
            print(selected_sacramentos)
        except Exception as e:
            print(e)
    def create_checkbox_sacramento():
        if not sacramentos_disponiveis=='':
            keys = ['id', 'nome']  
            resultados =  [dict(zip(keys, values)) for values in sacramentos_disponiveis] 
            for sacramento in resultados:
                checkbox = MyCheckbox(label=sacramento['nome'], value=sacramento['id'])
                checkbox.on_change = on_change_box_sacra
                sacra_checkboxes.append(checkbox)
                print(checkbox.value)
        return checkboxes

    create_checkbox_sacramento()

    def salvar_dados_membro_sacramento(membro, sacramentos):
        c=conn.cursor()

        for sacramento in sacramentos:
            print(f'O membro {membro} possui o sacramento {sacramento}')
            c.execute('INSERT INTO associacao_membro_sacramento (membro_id, sacramento_id) VALUES (?,?)', (membro, sacramento))
            conn.commit()
        
    column_sacra = ft.Column(controls=sacra_checkboxes)
    lista_sacramento = ft.Container(column_sacra, disabled=True)
        
    def on_sacramento_change(e):
        if e.control.value == 'Sim':
            lista_sacramento.disabled = False
            lista_sacramento.update()
        else:
            lista_sacramento.disabled = True
            lista_sacramento.update()
            
    tem_sacramento = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), on_change=on_sacramento_change)
    tem_sacramento.value = 'Não'

    imagem = ft.Image(src='/home/izata/Downloads/CARTOON.png',width=200, height=200, visible=False)
    
    def insere_image(e: ft.FilePickerResultEvent):
        source = e.path
        #if os.path.exists(source):
        if source == None:
            imagem.src = '/home/izata/Downloads/CARTOON.png'
            imagem.visible = False
            imagem.update()
        else:
            imagem.src = source
            imagem.visible = True
            imagem.update()
            
    
    image_picker = ft.FilePicker(on_result=insere_image)
    page.overlay.append(image_picker)

    def on_image_handle(e):
        page.update()
        image_picker.save_file()


    control_imagem = ft.Stack([
        imagem,
        ft.IconButton(
            icon=ft.icons.PHOTO, 
            icon_size=ft.colors.BLUE, 
            on_click=on_image_handle
        )
    ])
    #control_imagem = ft.Stack([
    #    imagem_column, icon, 
    #], width=350, height=350)


#====================================================================== CHECKBOX PARA QUOTAS =================================================================================================
    selected_quotas = []

    quota_checkboxes = []
    
    def on_change_box_quota(e):
        try:
            selected_quotas.clear()
            for checkbox in quota_checkboxes:
                if checkbox.value == e.control.value:
                    e.control.checked = True
                    checkbox.set_checked(checkbox.is_checked())
                    if checkbox.is_checked()==True:
                        if checkbox.label=='Janeiro':
                            selected_quotas.append(1)
                        if checkbox.label=='Fevereiro':
                            selected_quotas.append(2)
                        if checkbox.label=='Março':
                            selected_quotas.append(3)
                        if checkbox.label=='Abril':
                            selected_quotas.append(4)
                        if checkbox.label=='Maio':
                            selected_quotas.append(5)
                        if checkbox.label=='Junho':
                            selected_quotas.append(6)
                        if checkbox.label=='Julho':
                            selected_quotas.append(7)
                        if checkbox.label=='Agosto':
                            selected_quotas.append(8)
                        if checkbox.label=='Setembro':
                            selected_quotas.append(9)
                        if checkbox.label=='Outubro':
                            selected_quotas.append(10)
                        if checkbox.label=='Novembro':
                            selected_quotas.append(11)
                        if checkbox.label=='Dezembro':
                            selected_quotas.append(12)                        
                    e.control.update()
            print(selected_quotas)
        except Exception as e:
            print(e)
    id_membro = ft.Text()

    def create_checkbox_quota(id_m):
        c = conn.cursor()
        c.execute('SELECT * FROM quotas')
        d = conn.cursor()
        d.execute('SELECT * FROM associacao_membro_quota WHERE membro_id=?', (id_m,))
        membro_quotas = d.fetchall()
        qt = []
        qt.clear()
        quota_checkboxes.clear()
        print(f'======{membro_quotas}======')
        quotas_disponiveis = c.fetchall()
        for q in membro_quotas:
            q[2]
            print(f'------{q[2]}------')
            qt.append(q[2])
        
        id_df = [membro_quota[1] for membro_quota in membro_quotas]  
        # Lista de checkboxes
        id_m = int(id_membro.value)
        print('Tudo bem?',id_m)
        #if id_m in id_df:   
        if quotas_disponiveis:
            print('Está em quotas associadas?')
            keys = ['id', 'valor', 'mes']
            resultados = [dict(zip(keys, values)) for values in quotas_disponiveis]            
            for quota in resultados:
                if   quota['id'] not in qt:
                    print('Está em quotas associadas?')
                    checkbox = MyCheckbox(label=quota['mes'], value=quota['id'])
                    checkbox.on_change = on_change_box_quota
                    quota_checkboxes.append(checkbox)
                    print(checkbox.value)
        return quota_checkboxes


    nome_membro = ft.TextField(label='Digite o nome do membro que pagou a quota', prefix_icon=ft.icons.MONEY_SHARP, width=400)
    lista_membro = []
    
    def retornar_membro(nome_membro_text):
        try:
            c = conn.cursor()

            c.execute("""SELECT * FROM membros
                        WHERE nome=?""", (nome_membro_text,))
            membros = c.fetchall()
            print(membros)
            if not membros == []:
                if membros:
                    keys = ['id', 'nome', 'data_nasc', 'genero', 'morada', 'contacto','email', 'moradia','frequenta_escola', 'estuda_sabado', 'curso_acad', 'e_trabalhador', 'local_trabalho', 'funcao_trabalho', 'trabalha_fim_semana', 'catecumeno', 'n_f_catequese', 'tempo_grupo', 'ano_entrada', 'tem_cargo', 'cargos', 'sacra_baptismo', 'sacra_crisma', 'sacra_penitencia', 'sacra_casamento', 'tem_sacramento', 'tem_promessa', 'data_promessa']
                    resultados = [dict(zip(keys, values)) for values in membros]
                    for membro in resultados:
                        lista_membro.append(membro)
                        print(membro)
                        id_membro.value = membro['id']
                        return membro['nome']
            if membros == []:
                return 'Não existe membro com este nome'
        except Exception as e:
            print(e)

    

    retornar_texto = ft.Text(visible=False)
    retornar_null = ft.Text(visible=False)
    column_quota = ft.Column(controls=quota_checkboxes )
    
    lista_quota = ft.Container(column_quota, visible=False)

    def salvar_dados_membro_quota(e):
        c=conn.cursor()
        print(id_membro.value)
        membro = int(id_membro.value)

        for quota in selected_quotas:
            print(f'O membro {membro} possui o quota {quota}')
            c.execute('INSERT INTO associacao_membro_quota (membro_id, quota_id) VALUES (?,?)', (membro, quota))
            conn.commit()
        nome_membro.visible = True
        nome_membro.update()
        retornar_texto.visible = False
        retornar_texto.update()
        column_quota.visible = False
        column_quota.update()
        lista_quota.visible = False
        lista_quota.update()
        btn_salvar_cancelar.visible = False
        btn_salvar_cancelar.update()
        tb_membro_quotas.rows.clear()
        chamar_db_por_quotas()
        tb_membro_quotas.update()
        page.update()

    def on_click_cancelar(e):
        nome_membro.visible = True
        nome_membro.update()
        retornar_texto.visible = False
        retornar_texto.update()
        column_quota.visible = False
        column_quota.update()
        lista_quota.visible = False
        lista_quota.update()
        btn_salvar_cancelar.visible = False
        btn_salvar_cancelar.update()


    salvar = ft.FilledButton('Salvar', on_click=salvar_dados_membro_quota)
    cancelar = ft.FilledButton('Cancelar', on_click=on_click_cancelar)
    btn_salvar_cancelar = ft.Row([salvar, cancelar,], visible=False)
    
    def on_click_container(e):
        membro_encontrado = retornar_membro(nome_membro.value)
        if membro_encontrado != 'Não existe membro com este nome':
            retornar_texto.value = membro_encontrado
            retornar_texto.visible = True
            create_checkbox_quota(int(id_membro.value))
            retornar_texto.update()
            column_quota.visible = True
            column_quota.update()
            lista_quota.visible = True
            lista_quota.update()
            btn_salvar_cancelar.visible = True
            btn_salvar_cancelar.update()
        if membro_encontrado == 'Não existe membro com este nome':
            retornar_texto.value = membro_encontrado
            retornar_texto.visible = True
            retornar_texto.update()
            column_quota.visible = False
            column_quota.update()
            lista_quota.visible = False
            lista_quota.update()
            btn_salvar_cancelar.visible = False
            btn_salvar_cancelar.update()

    nome_membro.on_change = on_click_container

    cal_date_promise = SetCalendar(update_callback=None, start_year=2022)
    date_promise = DateSetUp(cal_grid=cal_date_promise)

    calendar_container_promise = Container()

    open_calendar_button_promise = OpenCalendarButton(date_promise, calendar_container_promise, date_promise.get_selected_date())

    data_promessa = ft.TextField(label="Data da promessa", dense=True, hint_text="yyyy-mm-dd", width=260)

    def callback2(e):
        if SelectionType.SINGLE.value==0:
            data_promessa.value = e[0].strftime("%d/%m/%Y") if len(e) > 0 else None
            print(data_promessa.value)
            data_promessa.update()
        """elif SelectionType.MULTIPLE.value and len(e) > 0:
            self.from_to_text.value = f"{[d.isoformat() for d in e]}"
            self.from_to_text.visible = True
        elif SelectionType.RANGE.value and len(e) > 0:
            self.from_to_text.value = f"From: {e[0]} To: {e[1]}"
            self.from_to_text.visible = True"""
    
    datepicker2 = DatePicker(
            selected_date=[data_promessa.value] if data_promessa.value else None,
            selection_type=int(SelectionType.SINGLE.value),
            locale="pt_PT",
            on_change=callback2
            )
    def confirm_dlg2(e):
        dlg_modal2.open = False
        dlg_modal2.update()
        page.update()
    
    def cancel_dlg2(e):
        dlg_modal2.open = False
        dlg_modal2.update()
        page.update()
    
    dlg_modal2 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Calendário"),
            actions=[
                ft.TextButton("Sair", on_click=cancel_dlg2),
                #ft.TextButton("Confirmar", on_click=confirm_dlg2),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content=datepicker2,
            content_padding=0
        )
    def open_dlg_modal2(e):
        dlg_modal2.open = True
        page.update()

    cal_icon2 = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH, 
            on_click=open_dlg_modal2, 
            
            width=40,
            right=0,
            style=ft.ButtonStyle(
                padding=ft.Padding(4,0,0,0),
                shape={
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                    },
            ))

    stack2 = ft.Stack([data_promessa, cal_icon2], disabled=True)
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
            stack2.disabled = True
            stack2.update()
        else:
            stack2.disabled = False
            stack2.update()

    tem_promessa = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Sim', label='Sim'),
            ft.Radio(value='Não', label='Não')
        ])
    ]), on_change=on_promessa_change)
    tem_promessa.value = 'Não'

    #opcoes_anos_promessa = [ft.dropdown.Option(str(ano)) for ano in range(2023, 1997, -1)]  # Adapte o intervalo de anos conforme necessário
    




    nome_cursista = ft.TextField(label='Nome do cursista')
    paroquia = ft.TextField(label='Paróquia', read_only=True, value="São Pedro Apóstolo")
    centro = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Arcanjo Gabriel', label='Arcanjo Gabriel'), ft.Radio(value='Espírito Santo', label='Espírito Santo'),
            ft.Radio(value='Santa Terezinha do Menino Jesus', label='Santa Terezinha do Menino Jesus'), ft.Radio(value='São Pedro Apóstolo', label='São Pedro Apóstolo')
        ])
    ]))
    curso = ft.Dropdown(options=[
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
    #todas_datas = mycal.output
    opcoes_datas = [ft.dropdown.Option(text=data.strftime("%d/%m/%Y")) for data in datas]
    # Criar o dropdown
    data_ini = ft.Dropdown(options=opcoes_datas)
    data_ter = ft.Dropdown(options=opcoes_datas)
    local = ft.RadioGroup(content=ft.Column([
        ft.Row([
            ft.Radio(value='Arcanjo Gabriel', label='Arcanjo Gabriel'), ft.Radio(value='Espírito Santo', label='Espírito Santo'),
            ft.Radio(value='Santa Terezinha do Menino Jesus', label='Santa Terezinha do Menino Jesus'), ft.Radio(value='São Pedro Apóstolo', label='São Pedro Apóstolo')
        ])
    ]))
    # Criar opções para o dropdown de notas
    opcoes_notas = [ft.dropdown.Option(str(nota)) for nota in range(21)]
    # Criar o dropdown
    nota = ft.Dropdown(options=opcoes_notas)
    imagem_cursista = ft.Image(src='/home/izata/Downloads/CARTOON.png', width=200, height=200, visible=False)
    
    def insere_image_cursista(e: ft.FilePickerResultEvent):
        source = e.path
        #if os.path.exists(source):
        if source == None:
            imagem_cursista.src='/home/izata/Downloads/CARTOON.png'
            imagem_cursista.visible = True
            imagem_cursista.update()
        else:
            imagem_cursista.src = source
            imagem_cursista.visible = True
            imagem_cursista.update()
            
    
    image_cursista_picker = ft.FilePicker(on_result=insere_image_cursista)
    page.overlay.append(image_cursista_picker)

    def on_image_cursista_handle(e):
        page.update()
        image_cursista_picker.save_file()


    control_cursista_imagem = ft.Column([
        imagem_cursista,
        ft.IconButton(
            icon=ft.icons.PHOTO, 
            icon_size=ft.colors.BLUE, 
            on_click=on_image_cursista_handle
        )
    ])



    nome_actividade = ft.TextField(label='Nome da atividade', dense=True, width=370, on_change=capitalize_first_letter)
    hoje = datetime.date.today()
    datas = [hoje + datetime.timedelta(days=i) for i in range(365)]
    opcoes_datas = [ft.dropdown.Option(text=data.strftime("%Y-%m-%d")) for data in datas]
    
    data_actividade = ft.TextField(label="Data de início", dense=True, hint_text="yyyy-mm-dd", width=260)
    data_fim_actividade = ft.TextField(label="Data de término", dense=True, hint_text="yyyy-mm-dd", width=260, visible=False)
    from_to_text = ft.Text(visible=False)

    datepicker3 = None

    def on_change_selection(e):
        data_actividade.value = ''
        hora_actividade.value = ''
        data_actividade.update()
        hora_actividade.update()
        data_fim_actividade.visible = False
        hora_fim_actividade.visible = False
        data_fim_actividade.value = ''
        hora_fim_actividade.value = ''
        data_fim_actividade.update()
        hora_fim_actividade.update()
    
    cg = ft.RadioGroup(content=ft.Column(
        [
            #ft.Text("Tipos de selecções"),
            ft.Radio(value=SelectionType.SINGLE.value, label='Selecção para uma data'),
            ft.Radio(value=SelectionType.RANGE.value, label='Selecção para uma sequência data'),
            ft.Radio(value=SelectionType.MULTIPLE.value, label='Selecção para várias data', disabled=True)
        ]), on_change=on_change_selection,value=SelectionType.RANGE.value 
    )
    

    def callback3(e):
        print(f'Callback3 chamada. Comprimento de e: {len(e)}, e: {e}')
        print(cg.value)
        if int(cg.value) == SelectionType.SINGLE.value:
            data_actividade.value = e[0].strftime('%d/%m/%Y') if len(e) > 0 else None
            print(data_actividade.value)
            data_fim_actividade.visible = False
            data_fim_actividade.value = e[0].strftime('%d/%m/%Y') if len(e) > 0 else None
            hora_fim_actividade.visible = True
            data_fim_actividade.update()
            hora_fim_actividade.update()
        if int(cg.value) == SelectionType.MULTIPLE.value and len(e) > 0:
            print(cg.value)
            from_to_text.value = f"{[d.isoformat() for d in e]}"
            print(f"{[d.isoformat() for d in e]}")
            from_to_text.visible = True
            
        if int(cg.value) == SelectionType.RANGE.value and len(e)  >= 2:
            print(cg.value)
            #print(f"From: {e[0]} To: {e[1]}")
            #from_to_text.value = f"From: {e[0]} To: {e[1]}"
            data_actividade.value = e[0].strftime('%d/%m/%Y')
            data_fim_actividade.value = e[1].strftime('%d/%m/%Y')
            data_fim_actividade.visible = True
            hora_fim_actividade.visible = True
            from_to_text.visible = True
            
    
    print(f'FFFFFFFF{cg.value}')
    
    def cancel_dlg3(e):
        dlg_modal3.open = False
        page.update()
    def confirm_dlg3(e):
        dlg_modal3.open = False
        dlg_modal3.update()
        page.update()
    
    dlg_modal3 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Calendário"),
            actions=[
                ft.TextButton("Sair", on_click=cancel_dlg3),
                ft.TextButton("Confirmar", on_click=confirm_dlg3),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content=datepicker3,
            content_padding=0
        )
    def open_dlg_modal3(e):
        datepicker3 = DatePicker(
            hour_minute=False,
            selected_date=[data_actividade.value] if data_actividade.value else None,
            selection_type=int(cg.value),
            locale="pt_PT",
            on_change=callback3
            )
        dlg_modal3.content = datepicker3
        dlg_modal3.open = True
        page.update()

    cal_icon3 = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH, 
            on_click=open_dlg_modal3, 
            
            width=40,
            right=0,
            style=ft.ButtonStyle(
                padding=ft.Padding(4,0,0,0),
                shape={
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                    },
            ))

    stack3 = ft.Stack([data_actividade, cal_icon3])
        
    horas_com_minutos = []
    for hora in range(24):
        for minuto in range(0, 60, 15):  # Adicionando minutos a cada 15 minutos
            hora_formatada = f"{hora:02d}:{minuto:02d}"
            horas_com_minutos.append(hora_formatada)
    opcoes_horas_com_minutos = [ft.dropdown.Option(hora) for hora in horas_com_minutos]
    hora_actividade = ft.Dropdown(options=opcoes_horas_com_minutos, dense=True, width=100)
    
    hora_fim_actividade = ft.Dropdown(options=opcoes_horas_com_minutos, dense=True, width=100, visible=False)
    local_actividade = ft.TextField(label='Local de realização', dense=True, width=370)
    status_actividade = 'Em andamento'

    imagem_actividade = ft.Image(top='top', src='/home/izata/Downloads/CARTOON.png', width=350, height=350, visible=False)
    
    def insere_image_actividade(e: ft.FilePickerResultEvent):
        source = e.path
        #if os.path.exists(source):
        print(e.path)

        if source == None:
            imagem_actividade.src='/home/izata/Downloads/CARTOON.png'
            imagem_actividade.visible = False
            imagem_actividade.update()
        else:
            imagem_actividade.src = source
            imagem_actividade.visible = True
            imagem_actividade.update()
            
    
    image_actividade_picker = ft.FilePicker(on_result=insere_image_actividade)
    page.overlay.append(image_actividade_picker)

    def on_image_actividade_handle(e):
        page.update()
        image_actividade_picker.save_file()
    imagem_column = ft.Container(border=ft.Border.top, content=imagem_actividade)

    icon = ft.IconButton(
            icon=ft.icons.PHOTO, 
            icon_color=ft.colors.BLUE_800, 
            tooltip='Clique aqui para inserir a fotografia do local!',
            on_click=on_image_actividade_handle
        )

    control_actividade_imagem = ft.Stack([
        imagem_column, icon, 
    ], width=350, height=350)

    # Crie uma coluna para empilhar o botão "Abrir Calendário" e o container do calendário
    column = Column(
        alignment=MainAxisAlignment.CENTER,
        controls=[
            open_calendar_button,
            calendar_container,
        ]
    )
    nome_cargo = ft.TextField(label='Nome do cargo')


    inputcon = ft.Column(
        offset = ft.transform.Offset(2,0),
        animate_offset=ft.animation.Animation(600, curve='easeIn'),
        #elevation = 30,
        controls=[ft.Container(
            image_fit= ft.ImageFit.FIT_HEIGHT,
            bgcolor=ft.colors.GREEN_100,
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Row([ft.Text('     Novo registro de Membro', size=30, weight='bold', color=ft.colors.GREEN, text_align='SpaceBetween')], alignment=ft.alignment.center, width=1000),]),
                    ft.IconButton(icon=ft.icons.CLOSE, icon_size=25,
                        on_click=esconder_icon),
                        ], alignment='spaceBetween'),
                    ft.Row([
                        ft.Text('       Dados pessoais', size=20, weight='bold') 
                    ]),
                    ft.Row([
                        ft.Text('       '),nome, 
                    ]),
                    ft.Row([
                       ft.Text('       '), stack, dlg_modal1,#column, 
                       ft.Text('        Gênero:', size=16, weight='bold'), genero,
                         
                    ]),
                    ft.Row([
                       ft.Text('       '), morada,
                    ]),
                    ft.Row([
                        ft.Text('       '),contacto, email, moradia, 
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
                                    ft.Row([ft.Text('     É estudante?', size=16, weight='bold'), frequenta_escola]),
                                    ft.Row([ft.Text('     Estuda até aos sábados?', size=16, weight='bold'), estuda_sabado]),
                                    ft.Row([ft.Text('   '),curso_acad, ]), 
                                    ft.Row([ft.Text('     Trabalha?', weight='bold', size=16),trabalhador ]),
                                    ft.Row([ft.Text('   '),local_trabalho]),
                                    ft.Row([ft.Text('   '),funcao]),
                                    ft.Row([ft.Text('     Trabalha até aos fins de semanas?', size=16, weight='bold'), trabalha_fim_sem,]),
                                    ft.Row([ft.Text('     Frequenta a catequese?', size=16, weight='bold') ]),
                                    ft.Row([ft.Text('   '),catecumeno, ]),
                                    ft.Row([ft.Text('   '),n_f_catequese, ]),
                                    ft.Row([ft.Text('   '),control_imagem, ]),
                                    ft.Text(height=500),
                                    ], width=450 )),
                                ], alignment='SpaceBetween'),
                        ]),
                        ft.Row([
                            ft.Text('  '),ft.Row(
                                [ft.Container(
                                    content=ft.Column([
                                    ft.Text(),
                                    ft.Row([ft.Text('Dados relacionados a Pastoral', size=20, weight='bold', text_align='SpaceBetween')], width=350 , alignment='center'),
                                    ft.Row([tempo_grupo,], width=350 , alignment='center'),
                                    ft.Row([ano_entrada,], width=350 , alignment='center'),
                                    ft.Row([ft.Text('     Tem cargo no grupo?', size=16, weight='bold'), tem_cargo], width=350 ),
                                    ft.Row([ft.Text('     Quais?', size=16, weight='bold')], width=350 ),
                                    ft.Row([ft.Text(' '),cargo_outro], width=350 ),
                                    ft.Row([ft.Text('     Tem sacramento?', size=16, weight='bold'), tem_sacramento], width=350 ),
                                    ft.Row([ft.Text('     Quais?', size=16, weight='bold'),], width=350 ),
                                    ft.Row([ft.Text(' '), lista_sacramento], width=350 ),
                                    ft.Row([ft.Text('     É promessado(a)?', size=16, weight='bold'), tem_promessa], width=350 ),
                                    ft.Row([ft.Text('     Quando fez a promessa?', size=16, weight='bold')]),
                                    ft.Row([ft.Text(' '), stack2, dlg_modal2]),
                                    ft.Text(),
                                    #imagem, 
                                    
                                    ], width=500 )),
                                ], alignment='SpaceBetween'),
                        ]),
                    ]),                 
                    ft.FilledButton('Salvar dados', on_click=salvar_dados),ft.Text(height=25),                
            ], 
        ), 
    )], scroll=True)

    inputcon_cursista = ft.Column([
        #offset = ft.transform.Offset(2,0),
        #animate_offset=ft.animation.Animation(600, curve='easeIn'),
        #elevation = 30,
        ft.Container(
            bgcolor=ft.colors.BLUE_100,
            content=ft.Column([
                ft.Row([
                    ft.Text('Novo registro', size=20, weight='bold'),
                    ft.IconButton(icon=ft.icons.CLOSE, icon_size=25,
                        on_click=esconder_icon_cursista),
                        ], alignment='spaceBetween'),
                    nome_cursista, paroquia,
                    ft.Text('Selecione o centro', size=15, weight='bold'), 
                    centro, 
                    ft.Text('Selecione o curso', size=15, weight = 'bold'),
                    curso, ft.Text('Data de início', size=15, weight = 'bold'),
                    data_ini, ft.Text('Data de término', size=15, weight = 'bold'),
                    data_ter, 
                    ft.Text('Local onde foi realizado o curso', size=15, weight='bold'),
                    local, 
                    ft.Text('Nota final', size=15, weight='bold'),
                    nota, control_cursista_imagem,
                    ft.FilledButton('Salvar dados', on_click=salvar_dados_cursista),ft.Text(height=25),                
            ], )
        )
    ], scroll=True, width=1000)


    inputcon_actividade = ft.Column([       #offset = ft.transform.Offset(2,0),
        #animate_offset=ft.animation.Animation(600, curve='easeIn'),
        #elevation = 30,
        ft.Container(
            bgcolor=ft.colors.RED_100,
            content=ft.Column([
            ft.Row([
            ft.Text('        Nova registro de actividade', size=20, weight='bold'),
            ft.IconButton(icon=ft.icons.CLOSE, icon_size=25,
                on_click=esconder_icon_actividade)],  alignment='spaceBetween'),    
            ft.Row([
            ft.Row([
                ft.Column([
                    ft.Row([
                    ft.Text('       '), nome_actividade,
                    ]),
                    ft.Row([
                    ft.Text('       '), cg, 
                    ]),
                    ft.Row([
                        ft.Text('       '), stack3,
                        hora_actividade,
                    ]),
                    ft.Row([
                        ft.Text('       '), data_fim_actividade,
                        hora_fim_actividade,
                    ]),
                    ft.Row([
                    ft.Text('       '), local_actividade
                    ]),          
                ]),
            ]),
            
            ft.Row([
                control_actividade_imagem
                ]),
            ]),
            ft.Text(height=300),
            ft.Row([ft.FilledButton('Salvar dados', on_click=salvar_dados_actividade)]), ft.Text(height=25),  
        ],alignment='spaceBetween'),
        )
    ], scroll=True, width=1000)

    inputcon_quota = ft.Container(
            content=ft.Column([
            ft.Row([lista_quota]),  
            ft.FilledButton('Salvar dados', on_click=salvar_dados_membro_quota)   
        ], )
    )
    
    adicionar = ft.TextField(label='Adicone um cargo', width=250, prefix_icon=ft.icons.WORKSPACE_PREMIUM)
    #input_add = ft.Column([ft.Row([adicionar, ft.IconButton(icon=ft.icons.ONE_K, on_click=salvar_dados_cargo)])], visible=False)
    """def abrir_input(e):
        #if e.control == 1:
            input_add.visible = True
            input_add.expand = True
            #minha_tabela_cargo.visible = False
            page.update()"""
       # else:
           # input_add.visible = False
            #page.update()
    

    """inputcon_cargo = ft.Card(
        offset = ft.transform.Offset(2,0),
        animate_offset=ft.animation.Animation(600, curve='easeIn'),
        elevation = 30,
        content = ft.Container(
            bgcolor=ft.colors.RED_100,
            content=ft.Column([
                ft.Row([
                    ft.Text('Nova registro de cargo', size=20, weight='bold'),
                    ft.IconButton(icon=ft.icons.CLOSE, icon_size=25,
                        on_click=esconder_icon_cargo),
                        ], alignment='spaceBetween'),
                    nome_cargo, 
                    ft.FilledButton('Salvar dados', on_click=salvar_dados_cargo)   
            ], )
        )
    )"""
    
    t =   ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            )
    

    img = ft.Image(
        src=f"/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Logotipos  da Pastoral e Grupos Biblicos/Pastoral Biblica_LOGO_PNG.png",
        width=500,
        height=500,
        fit=ft.ImageFit.CONTAIN,
    )

    def control_group_selected(e):
        control_group_name = e.control.selected_index
        page.go(f"/{control_group_name}")

    
    container = ft.Container(
        bgcolor=ft.colors.BLUE_200,
        padding = 10,
    )

    barra = ft.VerticalDivider(width=1, visible=False)


    def actualizar_estado():
        barra.visible = False
        inputcon.visible = False
        inputcon_actividade.visible = False
        inputcon_cursista.visible = False
        minha_tabela_cursista.visible = False
        minha_tabela.visible = True
        minha_tabela_actividade.visible = False
        nome_membro.visible = False
        minha_tabela_membro.visible = False
        minha_tabela_actividade_concluida.visible = False
        minha_tabela_actividade_em_andamento.visible = False
        minha_tab_print_cursista.visible = False
        minha_tab_print_membro.visible = True
        minha_tab_print_actividade.visible = False
        aniversariante.visible = False
        minha_tab_imagem.visible = False
        minha_tab_cursos.visible = False
        minha_tab_imagem_ac.visible = False
        page.update()
    actualizar_estado()

   
    
    def on_change_index_reg(e):
        if e.control.selected_index == 0:
            barra.visible = False
            inputcon.visible = False
            inputcon_actividade.visible = False
            inputcon_cursista.visible = False
            minha_tabela_cursista.visible = False
            minha_tabela.visible = True
            minha_tabela_actividade.visible = False
            nome_membro.visible = False
            minha_tabela_membro.visible = False
            dlg_cursista.visible = False
            dlg_actividade.visible = False
            page.update()
            print("O índice selecionado é 0.")
        if e.control.selected_index == 1:
            print("O índice selecionado é 1.")
            barra.visible = False
            inputcon.visible = False
            inputcon_actividade.visible = False
            inputcon_cursista.visible = False
            minha_tabela.visible = False
            minha_tabela_cursista.visible = True
            minha_tabela_actividade.visible = False
            nome_membro.visible = False
            minha_tabela_membro.visible = False
            dlg.visible = False
            dlg_actividade.visible = False
            page.update()
        if e.control.selected_index == 2:
            print("O índice selecionado é 2.")
            barra.visible = False
            inputcon.visible = False
            inputcon_actividade.visible = False
            inputcon_cursista.visible = False
            minha_tabela.visible = False
            minha_tabela_cursista.visible = False
            minha_tabela_actividade.visible = True
            nome_membro.visible = False
            minha_tabela_membro.visible = False
            dlg.visible = False
            dlg_cursista.visible = False
            page.update()
        if e.control.selected_index == 3:
            print("O índice selecionado é 3.")
            barra.visible = True
            inputcon.visible = False
            inputcon_actividade.visible = False
            inputcon_cursista.visible = False
            minha_tabela.visible = False
            minha_tabela_cursista.visible = False
            minha_tabela_actividade.visible = False
            nome_membro.visible =True
            minha_tabela_membro.visible = True
            dlg.visible = False
            dlg_actividade.visible = False
            dlg_cursista.visible = False
            page.update()
    

    def on_change_index(e):
        if e.control.selected_index == 0:
            #name = ft.Text('direcção')
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_direccao.visible = True
            minha_tabela_sacramento.visible = False
            minha_tabela_quotas.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_leitura.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False            
            page.update()
            print("O índice selecionado é 0.")
        if e.control.selected_index == 1:
            print("O índice selecionado é 1.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = True
            minha_tabela_dataNasc.visible = True
            minha_tabela_sacramento.visible = False
            minha_tabela_quotas.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_leitura.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 2:
            print("O índice selecionado é 2.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_sacramento.visible = True
            minha_tabela_quotas.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_leitura.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 3:
            print("O índice selecionado é 3.")
            minha_tabela_direccao.visible = False
            minha_tabela_dataNasc.visible = False
            aniversariante.visible = False
            minha_tabela_sacramento.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_leitura.visible = False
            minha_tabela_quotas.visible = True
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 4:
            print("O índice selecionado é 4.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_sacramento.visible = False
            minha_tabela_promessa.visible = True
            minha_tabela_quotas.visible = False
            minha_tabela_leitura.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 5:
            print("O índice selecionado é 5.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_sacramento.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_quotas.visible = False
            minha_tabela_leitura.visible = True
            img_column.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 6:
            print("O índice selecionado é 6.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_sacramento.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_quotas.visible = False
            minha_tabela_leitura.visible = False
            img_column.visible = False
            minha_tabela_actividade_em_andamento.visible = True
            minha_tabela_actividade_concluida.visible = False
            page.update()
        if e.control.selected_index == 7:
            print("O índice selecionado é 7.")
            minha_tabela_direccao.visible = False
            aniversariante.visible = False
            minha_tabela_dataNasc.visible = False
            minha_tabela_sacramento.visible = False
            minha_tabela_promessa.visible = False
            minha_tabela_quotas.visible = False
            minha_tabela_leitura.visible = False
            img_column.visible = False
            minha_tabela_actividade_em_andamento.visible = False
            minha_tabela_actividade_concluida.visible = True
            page.update()

    def on_change_index_print(e):
        if e.control.selected_index == 0:
            #name = ft.Text('direcção')
            minha_tab_print_cursista.visible = False
            minha_tab_print_membro.visible = True
            minha_tab_print_actividade.visible = False
            minha_tab_imagem.visible = False
            minha_tab_cursos.visible = False
            minha_tab_imagem_ac.visible = False
            page.update()
            print("O índice selecionado é 0.")
        if e.control.selected_index == 1:
            minha_tab_print_cursista.visible = True
            minha_tab_print_membro.visible = False
            minha_tab_print_actividade.visible = False
            minha_tab_cursos.visible = False
            minha_tab_imagem_ac.visible = False
            minha_tab_imagem.visible = False
            page.update()
            print("O índice selecionado é 1.")
        if e.control.selected_index == 2:
            minha_tab_print_cursista.visible = False
            minha_tab_print_membro.visible = False
            minha_tab_print_actividade.visible = True
            minha_tab_imagem.visible = False
            minha_tab_imagem_ac.visible = False
            minha_tab_cursos.visible = False
            page.update()
            print("O índice selecionado é 2.")
        if e.control.selected_index == 3:
            minha_tab_print_cursista.visible = False
            minha_tab_print_membro.visible = False
            minha_tab_print_actividade.visible = False
            minha_tab_imagem.visible = True
            minha_tab_cursos.visible = False
            minha_tab_imagem_ac.visible = False
            page.update()
            print("O índice selecionado é 3.")
        if e.control.selected_index == 4:
            minha_tab_print_cursista.visible = False
            minha_tab_print_membro.visible = False
            minha_tab_print_actividade.visible = False
            minha_tab_imagem.visible = False
            minha_tab_cursos.visible = True
            minha_tab_imagem_ac.visible = False
            page.update()
            print("O índice selecionado é 4.")
        if e.control.selected_index == 5:
            minha_tab_print_cursista.visible = False
            minha_tab_print_membro.visible = False
            minha_tab_print_actividade.visible = False
            minha_tab_imagem.visible = False
            minha_tab_cursos.visible = False
            minha_tab_imagem_ac.visible = True
            page.update()
            print("O índice selecionado é 5.")
        
    img_column = ft.Column([
    ft.Row([img], scroll='auto')
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)  

    #dlg.
    
    #page.add(dados)
    pagina = ft.Container(
        content=ft.Column(
            controls=[ft.Tabs(
                selected_index = 0,
                divider_color = ft.colors.BLUE,
                indicator_color = ft.colors.RED,
                indicator_tab_size=True,
                label_color=ft.colors.GREEN,
                unselected_label_color=ft.colors.BLUE_200,
                 overlay_color={
                    ft.MaterialState.FOCUSED: ft.colors.with_opacity(
                        0.2, ft.colors.GREEN
                    ),
                    ft.MaterialState.DEFAULT: ft.colors.with_opacity(
                        0.2, ft.colors.PINK
                    ),
                },
                
                tabs = [
                    ft.Tab('Criar Registros', 
                        ft.Container(
                            content = ft.Column(
                                controls = [ft.Divider(height=0, color=ft.colors.BLUE_200),
                                    ft.Row([
                                        ft.NavigationRail(
                                            selected_index=0,
                                            label_type=ft.NavigationRailLabelType.ALL,
                                            extended=True,
                                            #expand=True,
                                            #min_width=200,
                                            min_extended_width=200,
                                            #leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
                                            #height=300,
                                            group_alignment=-0.9,
                                            destinations=[
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.PERSON, selected_icon=ft.icons.PERSON, label="Registrar Membros",
                                                    selected_icon_content=ft.IconButton(ft.icons.PERSON, on_click=show_input, tooltip='Clique aqui para registrar um membro!'),      
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.SCHOOL),
                                                    selected_icon_content=ft.IconButton(ft.icons.SCHOOL, on_click=show_input_cursista, tooltip='Clique aqui para registrar um cursista!'),
                                                    label="Registrar Cursistas", 
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.WORKSPACES,
                                                    selected_icon_content=ft.IconButton(ft.icons.WORKSPACES, on_click=show_input_actividade, tooltip='Clique aqui para registrar uma actividade!'),
                                                    label_content=ft.Text("Registrar actividades"),
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.WALLET,
                                                    selected_icon_content=ft.IconButton(ft.icons.MONETIZATION_ON, on_click=on_click_container),
                                                    label_content=ft.Text("Regitrar Quotas"),
                                                ),
                                            ],
                                            on_change=on_change_index_reg, width=250, bgcolor=ft.colors.GREY_200,
                                        ),
                                         ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
                                            ft.Row([
                                                    minha_tabela, inputcon, minha_tabela_cursista, inputcon_cursista, minha_tabela_actividade, inputcon_actividade,  
                                                    ft.Row([nome_membro, retornar_texto, retornar_null, lista_quota, btn_salvar_cancelar,]),
                                                    barra, minha_tabela_membro, dlg, dlg_cursista, dlg_actividade,
                                                    ft.VerticalDivider(width=1), 
                                                ], vertical_alignment=ft.CrossAxisAlignment.START, scroll=True, expand=1, 
                                            ),
                                       ft.VerticalDivider(width=1, color=ft.colors.BLUE_200) ],
                                    spacing=0,
                                    width=1300,
                                    height=700,

                                ),
                                    ft.VerticalDivider(width=1), ft.Divider(height=0, color=ft.colors.BLUE_200),]
                            ), 
                    ), icon=ft.icons.CREATE_SHARP),
                    #ft.Tab('Registrar membros', ft.Container(
                    #content = ft.Column(
                     #   controls = [
                      #  ft.ElevatedButton(
                       #     'Registrar', 
                        #    on_click=show_input),
                            #minha_tabela,
                            #inputcon, 
                        #], 
                   # ),
                #),icon=ft.icons.PERSON),
                    #ft.Tab('Registrar cursistas', ft.Container(
                 
                    #content = ft.Column(
                        #controls = [
                        #ft.ElevatedButton(
                            #'Registrar', 
                            #on_click=show_input_cursista),
                            #minha_tabela_cursista,
                            #inputcon_cursista,
                        #]
                    #)
                #),icon=ft.icons.SCHOOL),
                    
                    #ft.Tab('Registrar actividades',ft.Container(
                    #content = ft.Column(
                        #controls = [
                        #ft.Row([
                            #ft.Container(
                            #content=ft.Column([ft.ElevatedButton(
                            #'Registrar actividade',                              
                            #on_click=show_input_actividade), 
                        #])),
                        #ft.Container(
                            #content=ft.Column([
                                #ft.IconButton(icon=ft.icons.UPDATE, 
                                    #tooltip='Actualizar a página', on_click=update_status)], alignment='end'))], alignment='SpaceBetween',
                                #),
                            #ft.Tabs(
                                #selected_index=0,
                                #divider_color = ft.colors.BLUE,
                                #indicator_color = ft.colors.RED,
                                #indicator_tab_size=True,
                                #label_color=ft.colors.GREEN,
                                #unselected_label_color=ft.colors.BLUE_200,
                                #overlay_color={
                                    #ft.MaterialState.FOCUSED: ft.colors.with_opacity(
                                        #0.2, ft.colors.GREEN
                                    #),
                                    #ft.MaterialState.DEFAULT: ft.colors.with_opacity(
                                        #0.2, ft.colors.PINK
                                    #),
                                #},
                            #tabs=[
                                #ft.Tab("Todas",
                                    #ft.Container(
                                        #content = ft.Column(
                                            #controls = [
                                                #minha_tabela_actividade,
                                                #inputcon_actividade
                                            #]
                                        #)
                                    #) 
                                #), ft.Tab("Em andamento", 
                                    #ft.Container(
                                        #content = ft.Column(
                                            #controls = [
                                                #minha_tabela_actividade_em_andamento,
                                                #]
                                        #)
                                 #) ), ft.Tab("Concluída",
                                        #ft.Container(
                                        #content = ft.Column(
                                            #controls = [
                                                #minha_tabela_actividade_concluida,
                                                #]
                                        #)
                                 #))], 
                        #), 
                        #],
                    #) ),
                    #icon=ft.icons.WORKSPACES)
                    ft.Tab('Listas de dados',
                        ft.Container( 
                            content = ft.Column(
                                controls = [ft.Divider(height=0.1, color=ft.colors.BLUE_200),
                                    ft.Row([
                                        ft.NavigationRail(
                                            selected_index=0,
                                            #label_type=ft.NavigationRailLabelType.ALL,
                                            extended=True,
                                            #expand=True,
                                            #min_width=200,
                                            #min_extended_width=200,
                                            #leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
                                            group_alignment=-0.9,
                                            destinations=[
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.WORKSPACE_PREMIUM, selected_icon=ft.icons.WORKSPACE_PREMIUM_SHARP, label="Membros directivos"
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.CAKE),
                                                    selected_icon_content=ft.Icon(ft.icons.CAKE_ROUNDED),
                                                    label="Aniversariantes", 
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.STAR_PURPLE500,
                                                    selected_icon_content=ft.Icon(ft.icons.STAR_BORDER_PURPLE500_SHARP),
                                                    label_content=ft.Text("Com sacramentos"),
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.MONETIZATION_ON,
                                                    selected_icon_content=ft.Icon(ft.icons.MONETIZATION_ON),
                                                    label_content=ft.Text("Quotas pagas"),
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.CELEBRATION_SHARP,
                                                    selected_icon_content=ft.Icon(ft.icons.CELEBRATION_SHARP),
                                                    label_content=ft.Text("Promessados"),
                                                ),

                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.BOOK_ONLINE,
                                                    selected_icon_content=ft.Icon(ft.icons.BOOK_ONLINE),
                                                    label_content=ft.Text("Leituras"),
                                                ),

                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.WORK_HISTORY,
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    label_content=ft.Text("Actividades em andamento"),
                                                ),

                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.WORK_OFF,
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_OFF),
                                                    label_content=ft.Text("Actividades concluídas"),
                                                ),
                                            ],
                                            on_change=on_change_index, width=250, bgcolor=ft.colors.GREY_200, #height=400
                                        ),
                                         ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
                                         #ft.Container(
                                            ft.Row(
                                                controls = [
                                                    ft.Column([
                                                        minha_tabela_direccao, aniversariante, minha_tabela_dataNasc, minha_tabela_sacramento, minha_tabela_quotas,
                                                        minha_tabela_promessa,  minha_tabela_leitura,
                                                        minha_tabela_actividade_em_andamento, minha_tabela_actividade_concluida
                                                        ])
                                                ], vertical_alignment=ft.CrossAxisAlignment.START, scroll=True, expand=1,
                                            ), 
                                        ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),  #img_column,
                                    ],
                                    spacing=0,
                                    width=1300,
                                    height=700
                                ),
                                ft.Divider(height=0, color=ft.colors.BLUE_200),]
                            ), 
                        )
                        ,icon=ft.icons.VIEW_LIST),
                    ft.Tab('Ficheiros',
                        ft.Container( 
                            content = ft.Column(
                                controls = [ft.Divider(height=0.1, color=ft.colors.BLUE_200),
                                    ft.Row([
                                        ft.NavigationRail(
                                            selected_index=0,
                                            #label_type=ft.NavigationRailLabelType.ALL,
                                            extended=True,
                                            #expand=True,
                                            #min_width=200,
                                            #min_extended_width=200,
                                            #leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
                                            group_alignment=-0.9,
                                            destinations=[
                                                ft.NavigationRailDestination(
                                                    icon=ft.icons.PRINT, 
                                                    selected_icon=ft.icons.PRINT, 
                                                    label="Gurdar um membro em pdf"
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.CAKE_ROUNDED),
                                                    selected_icon_content=ft.Icon(ft.icons.CAKE_ROUNDED),
                                                    label="Guardar um cursista em pdf", 
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    label="Guardar uma actividade em pdf", 
                                                ),

                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    label="Guardar lista de membros em pdf", 
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    label="Guardar lista de cursistas em pdf", 
                                                ),
                                                ft.NavigationRailDestination(
                                                    icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                                                    label="Guardar programa de actividades em pdf", 
                                                ),
                                                
                                            ],
                                            on_change=on_change_index_print, width=300, bgcolor=ft.colors.GREY_200, #height=400
                                        ),
                                         ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
                                         ft.Row([
                                            ft.Column(
                                                [
                                                    minha_tab_print_membro, minha_tab_print_cursista, minha_tab_print_actividade
                                                    , minha_tab_imagem, minha_tab_cursos, minha_tab_imagem_ac
                                                ], #vertical_alignment=ft.MainAxisAlignment.START, 

                                            ), 
                                    ], scroll=True, expand=1,),ft.VerticalDivider(width=1, color=ft.colors.BLUE_200), 
                                    ],
                                    spacing=0,
                                    width=1300,
                                    height=700,
                                ),
                                ft.Divider(height=0, color=ft.colors.BLUE_200),]
                            ), 
                        )
                        ,icon=ft.icons.FILE_DOWNLOAD),
                    #ft.Tab('Registrar pagamentos de quotas', ft.Container(
                 
                    #content = ft.Column(
                        #controls = [
                            #ft.Row([], width=100),
                            #ft.Row([nome_membro]),
                            #retornar_texto, retornar_null, lista_quota, btn_salvar_cancelar
                        #]
                    #), 
                #),icon=ft.icons.ATTACH_MONEY_SHARP),
                        
                ]
            ),
        ]),image_src='/home/izata/izata/Izata Muondo/Documents/CPY_SAVES/bluetooth/Lenço Vermelho  Animador  Biblico/Pastoral Biblica _LOGO.jpg', 
        image_fit=ft.ImageFit.CONTAIN,
         
          
    )
    
    page.add(pagina, dlg_modal3)

    hora = ft.Text()
    def actualiza_hora():
        while True:
            import time 
            # Atualiza o estado do programa aqui
            estado = time.strftime("%H:%M:%S")
            hora.value=f"{estado}"
            print(hora.value)
            update_status()
            tb_membro_dataNasc.rows.clear()
            aniversariante.controls.clear()
            chamar_db_dataNasc()
            time.sleep(1)
            #page.update()
                       
            
    thread_atualizacao = threading.Thread(target=actualiza_hora)
    thread_atualizacao.daemon = True
    thread_atualizacao.start()
    
    
            
    #page.add(column)
if __name__ == "__main__":

    ft.app(target=main, 
        view=ft.AppView.WEB_BROWSER
        )