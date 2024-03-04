import streamlit as st
import streamlit.components.v1 as components
import pathlib
import re
import subprocess
from time import time

import base64

from datetime import datetime

import numpy as np
import pandas as pd

from files.constants import FOR_LANGUAGE, TASKS_NUMBER, TASKS_NUMBER_USER_1, TASKS_NUMBER_USER_2, USERNAME_DICT, STYLE_SVG
from files.db_server import create_connection, create_connection_sql, make_request
from files.for_stats import get_statistic_image, get_statistic_image_math
from files.google_files import link_to_var, list_files
from files.widget_variants import create_variants_tab_test


import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

st.set_page_config(layout='wide')

import os


def add_info_who_did(subject, variant, num):
    lst_names = []

    for name in USERNAME_DICT.keys():
        request_one = f'''
                            SELECT 
                                *
                            FROM
                                Main
                            WHERE
                                StudentID = {USERNAME_DICT[name]}
                                AND Subject = '{subject}'
                                AND Variant = {variant}
                                AND Num = {num}
                        '''

        temp = make_request(request_one, 'tasks_done')
        if  temp != []:
            lst_names.append(name)

    if lst_names != []:
        st.info(lst_names)
    else:
        st.success('Nobody!')
    
    

def get_task_number(task, find_task_num):
    """
    Determines the task number based on the given task and find_task_num.

    Args:
        task (str): The task name.
        find_task_num (int): The task number to find.

    Returns:
        str: The corresponding task number.
    """

    if task == 'Тригонометрия':
        if 101 <= find_task_num <= 257 or find_task_num > 532:
            return '13'
        else:
            return '12'
    elif task == 'Стереометрия':
        if 101 <= find_task_num <= 257 or find_task_num > 532:
            return '14'
        else:
            return '13'
    elif task == 'Неравенство':
        if 101 <= find_task_num <= 257 or find_task_num > 532:
            return '15'
        else:
            return '14'
    elif task == 'Параметр':
        if 101 <= find_task_num <= 257 or find_task_num > 532:
            return '18'
        else:
            return '17'
    elif task == 'Последняя':
        if 101 <= find_task_num <= 257 or find_task_num > 532:
            return '19'
        else:
            return '18'
    elif task == 'Планиметрия':
        if 101 <= find_task_num <= 532:
            return '16'
        elif find_task_num > 532:
            return '17'
    elif task == 'Экономика':
        if 101 <= find_task_num <= 257:
            return '17'
        elif 258 <= find_task_num <= 532:
            return '15'
        elif find_task_num > 532:
            return '16'



table_names = {
  'Тригонометрия': 'math_tasks_trig',
  'Стереометрия': 'math_tasks_stereo',
  'Неравенство': 'math_tasks_ineq',
  'Планиметрия': 'math_tasks_plan',
  'Экономика': 'math_tasks_econ',
  'Параметр': 'math_tasks_param',
  'Последняя': 'math_tasks_last'
}

S3_BUCKET_NAMES = {
  'Тригонометрия': 'trigonometriya',
  'Стереометрия': 'math_tasks_stereo',
  'Неравенство': 'math_tasks_ineq',
  'Планиметрия': 'math_tasks_plan',
  'Экономика': 'math_tasks_econ',
  'Параметр': 'math_tasks_param',
  'Последняя': 'math_tasks_last'
}

for_language = FOR_LANGUAGE

def change_color(color):
    return '#FFFFFF' if color == '#000000' else '#000000'

def change_color_name(color):
    return 'black' if color == '#000000' else 'white'

def change_color_right(color):
    if color == '#FFFFFF':
        return 15, 17, 22
    else:
        return 255, 255, 255

def add_log(ans, task, num, username):
    """
    Adds a log entry to the log database.

    Args:
        ans (str): The answer provided.
        task (str): The task name.
        num (int): The task number.
        username (str): The username associated with the log entry.

    Returns:
        None
    """

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S")
    text = {'task': task, 'num': num, 'answer': ans, 'date': formatted_datetime, 'username': username}
    client_log = create_connection("log_db") 
    db_log = client_log['log_db']
    db_log.logs.insert_one(text)


def one_student(username):
    """
    Contains the main function for the application.

    This function handles the user interface and logic for different menu choices, such as Informatics, Mathematics, Homework, and Statistics.

    Args:
        None

    Returns:
        None
    """

    menu = ['Homework', 'Informatics', 'Statistics']
    if username == 'user_1':
        TASK_NUMBERS = TASKS_NUMBER_USER_1
        menu = ['Homework', 'Informatics', 'Mathematics', 'Variants', 'Statistics']
        menu_for_stats = [' ', 'Completing Tasks', 'Completing Tasks MATH']
    elif username == 'user_2':
        TASK_NUMBERS = TASKS_NUMBER_USER_2
        menu = ['Homework', 'Informatics', 'Variants', 'Statistics']
        menu_for_stats = [' ', 'Completing Tasks']
    else:
        TASK_NUMBERS = TASKS_NUMBER
        menu = ['Homework', 'Informatics', 'Mathematics', 'Variants', 'Statistics']

    choice = st.sidebar.radio('Menu', menu, key='main_menu_choice')


    if choice == 'Informatics':
        tasks = [''] + list(TASK_NUMBERS.keys())
        task = st.selectbox('Choose Task: ', tasks, key='inf_task_selectobox')

        try:
            if username != 'demo':
                nums = [''] + list(range(1, TASK_NUMBERS[task]))
            else:
                nums = [''] + list(range(1, 4))
        except:
            nums = ['']

        num = st.selectbox('Choose Num: ', nums, key='inf_num_selectobox')
        
        
        if task != '' and num != '':

            if task in [20, 21]:
                task = 19

            request_one = f'SELECT task FROM t_{task} WHERE num = {num}'
            task_text_sql = make_request(request_one, 'inf_tasks')[0][0]
            
            if 'font_color' not in st.session_state:
                st.session_state['font_color'] = '#000000'
                

            if 'curr_task' not in st.session_state:
                st.session_state['curr_task'] = task
            elif st.session_state['curr_task'] != task and st.session_state['font_color'] == '#FFFFFF':
               task_text_sql = task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 
            elif st.session_state['curr_task'] != task and st.session_state['font_color'] == '#000000':
               task_text_sql = task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 

            if 'curr_num' not in st.session_state:
                st.session_state['curr_num'] = num

            elif st.session_state['curr_num'] != num and st.session_state['font_color'] == '#FFFFFF':
               task_text_sql = task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 

            elif st.session_state['curr_num'] != num and st.session_state['font_color'] == '#000000':
               task_text_sql = task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 
                

            col1, col2 = st.columns([4, 1])
            with col1:  
                st.info(f"You chose Number {num} of Task {task}")


            st.write("") 
            with col2:
                change_font_button = st.button(label='Press me')

            if change_font_button:
                # Toggle the font color
                old_color = st.session_state['font_color']
                st.session_state['font_color'] = change_color(st.session_state['font_color'])
                task_text_sql = task_text_sql.replace(f'color: {old_color}', f"color: {st.session_state['font_color']}")

            if username == 'admin':
                who_done_button = st.button(label='Show Who Done')
                if who_done_button:
                    add_info_who_did('Inf', task, num)


            red, green, blue = change_color_right(st.session_state['font_color'])

            components.html(f"<style>:root {{background-color: rgb({red}, {green}, {blue});}}</style>"  + task_text_sql, scrolling=True, height=700)

            prob_answer = st.text_input('Your answer: ', value='', key='prob_answer_text_input').strip()

            request_one = f'SELECT task FROM t_{task} WHERE num = {num}'
            answer = make_request(request_one, 'inf_answers')[0][0]

            submit_button_ans = st.button(label='Check', key='check_button')
            
            if submit_button_ans and answer == prob_answer:
                st.success("True!")
                if username not in ['admin', 'demo']:
                    add_log(prob_answer, task, num, username)
            elif submit_button_ans and answer != prob_answer:
                st.error('Try again')
                if prob_answer != '' and username != 'admin':
                    add_log(prob_answer, task, num, username)
            else:
                print(st.session_state.prob_answer_text_input)
                st.info('Enter the answer')

    #########################################################################


    if choice == 'Mathematics':

        if username == 'user_1':
            tasks = ['', 'Тригонометрия', 'Стереометрия', 'Неравенство', 'Экономика']
        elif username == 'user_2':
            tasks = ['', 'Тригонометрия', 'Неравенство', 'Экономика']
        else:
            tasks = ['', 'Тригонометрия', 'Стереометрия', 'Неравенство', 'Экономика', 'Планиметрия', 'Параметр', 'Последняя']
        task = st.selectbox('Choose Task: ', tasks, key='math_task_selectobox')

        if username != 'demo':
            nums = [''] + list(range(1, 242))
        else:
            nums = [''] + list(range(1, 4))

        num = st.selectbox('Choose Num: ', nums, key='math_num_selectobox')
        
        
        if task != '' and num != '':

            request_one = f'SELECT task FROM {table_names[task]} WHERE task_id = {num}'
            task_text_sql = for_language + make_request(request_one, 'maths')[0][0]

            student_task_text_sql = make_request(request_one, 'maths')[0][0]
            index = student_task_text_sql.index('Задание ')
            student_task_text_sql = for_language +  student_task_text_sql[index:]
            color = 'black'
            
            if 'font_color' not in st.session_state:
                st.session_state['font_color'] = '#000000'
                color = 'black'
                

            if 'curr_task' not in st.session_state:
                st.session_state['curr_task'] = task
                color = 'black'
            elif st.session_state['curr_task'] != task and st.session_state['font_color'] == '#FFFFFF':
               task_text_sql = task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 
               student_task_text_sql = student_task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 
               color = 'white'
            elif st.session_state['curr_task'] != task and st.session_state['font_color'] == '#000000':
               task_text_sql = task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 
               student_task_text_sql = student_task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 
               color = 'black'

            if 'curr_num' not in st.session_state:
                st.session_state['curr_num'] = num

            elif st.session_state['curr_num'] != num and st.session_state['font_color'] == '#FFFFFF':
               task_text_sql = task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 
               student_task_text_sql = student_task_text_sql.replace(f'color: #000000', f"color: {st.session_state['font_color']}") 
               color = 'white'

            elif st.session_state['curr_num'] != num and st.session_state['font_color'] == '#000000':
               task_text_sql =  task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 
               student_task_text_sql =  student_task_text_sql.replace(f'color: #FFFFFF', f"color: {st.session_state['font_color']}") 
               color = 'black'
                

            col1, col2 = st.columns([4, 1])
            with col1:  
                st.info(f"You chose Number {num} of Task {task}")


            st.write("") 
            with col2:
                change_font_button = st.button(label='Change the Font')

            if change_font_button:
                old_color = st.session_state['font_color']
                st.session_state['font_color'] = change_color(st.session_state['font_color'])
                task_text_sql = task_text_sql.replace(f'color: {old_color}', f"color: {st.session_state['font_color']}")
                student_task_text_sql = student_task_text_sql.replace(f'color: {old_color}', f"color: {st.session_state['font_color']}")
                color = change_color_name(st.session_state['font_color'])



            if username == 'admin':
                find_task_num = re.findall('Вариант: \d+', task_text_sql)[0]
                st.write(find_task_num)
                find_task_num = int(re.findall('\d+', find_task_num)[0])
                st.write('Number of task: ', get_task_number(task, find_task_num))

                who_done_button = st.button(label='Show Who Done')
                if who_done_button:
                    add_info_who_did("Math", find_task_num, int(get_task_number(task, find_task_num)))

                mask = 'https:\/\/replace_pattern.svg'
                all_links = re.findall(mask, task_text_sql)
                for idx, link_mask in enumerate(all_links):
                    task_text_sql = task_text_sql.replace(link_mask, f'https://kosokolovsky-bucket-svgs.s3.eu-central-1.amazonaws.com/{S3_BUCKET_NAMES[task]}/z{num}im{idx + 1}{color}.svg', 1)

                red, green, blue = change_color_right(st.session_state['font_color'])
                components.html(STYLE_SVG + f"<style>:root {{background-color: rgb({red}, {green}, {blue});}}</style>" + task_text_sql, scrolling=True, height=400)
                

            
            
            else:
                mask = 'https:\/\/ege.sdamgia.ru/formula/svg/\w+/\w+.svg'
                all_links = re.findall(mask, student_task_text_sql)
                for idx, link_mask in enumerate(all_links):
                    student_task_text_sql = student_task_text_sql.replace(link_mask, f'https://kosokolovsky-bucket-svgs.s3.eu-central-1.amazonaws.com/{S3_BUCKET_NAMES[task]}/z{num}im{idx + 1}{color}.svg', 1)

                red, green, blue = change_color_right(st.session_state['font_color'])
                components.html(STYLE_SVG + f"<style>:root {{background-color: rgb({red}, {green}, {blue});}}</style>" + student_task_text_sql, scrolling=True, height=400)


    #########################################################################

    elif choice == 'Homework':
        if username == 'admin':
            student_homework_menu = st.selectbox('Choose the student: ', ['admin'] + list(USERNAME_DICT.keys()))
            username_chosen = student_homework_menu


        else:
            username_chosen = username
        
        try:
            shared_link = link_to_var(list_files(username_chosen, 'Homework')[0][:-4])

            embeddable_link = shared_link.replace("/view?usp=sharing", "/preview")

            st.markdown("""
                <style>
                # .pdf-container {
                    # text-align: center;
                    # margin-bottom: 5em;
                # }
                .pdf-container {
                    text-align: center;
                    margin-bottom: 5em;
                    # width: 100%; /* Container takes full width of the parent */
                    height: 100vh; /* Adjust the height as needed */
                    overflow: auto; /* Adds scrollbars if needed */
                    }
                .pdf-container iframe {
                width: 80%; /* iframe takes full width of its parent */
                height: 80%; /* iframe takes full height of its parent */
                border: none; /* Optional: removes the border */
                }
                </style>
                """, unsafe_allow_html=True)

            pdf_display = f'''
            <div class="pdf-container">
                <iframe src="{embeddable_link}" type="application/pdf"></iframe>
            </div>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error('File Not Found')


        
    

    elif choice == 'Statistics':
        if username != 'admin': 
            with st.container():
                stats_checkbox = st.selectbox('Choose the one you are interested in:', menu_for_stats, key='stats_selectbox')
                if stats_checkbox == 'Completing Tasks' and username != 'admin':
                    if 'svg_html' not in st.session_state or st.session_state.user != username:
                        if username == 'demo':
                            svg_data, time_test = get_statistic_image(student_id=USERNAME_DICT['user_1'])
                        else:
                            svg_data, time_test = get_statistic_image(student_id=USERNAME_DICT[username])
                        svg_base64 = base64.b64encode(svg_data).decode('utf-8')
                        svg_html = f'''
                                        <div style="justify-content: center; align-items: center;">
                                        <img src="data:image/svg+xml;base64,{svg_base64}" alt="SVG" style="height: automatic;width: 100%;">
                                        </div>
                                    '''
                        st.session_state['svg_html'] = svg_html
                        st.session_state['user'] = username
                        st.write(svg_html, unsafe_allow_html=True)
                    else:
                        st.write(st.session_state['svg_html'], unsafe_allow_html=True)

                if stats_checkbox == 'Completing Tasks MATH' and username != 'admin':
                    if 'svg_html_math' not in st.session_state or st.session_state.user != username:
                        if username == 'demo':
                            svg_data_math, time_test = get_statistic_image_math(student_id=USERNAME_DICT['user_1'])
                        else:
                            svg_data_math, time_test = get_statistic_image_math(student_id=USERNAME_DICT[username])
                        svg_base64_math = base64.b64encode(svg_data_math).decode('utf-8')
                        svg_html_math = f'''
                                        <div style="justify-content: center; align-items: center;">
                                        <img src="data:image/svg+xml;base64,{svg_base64_math}" alt="SVG" style="height: automatic;width: 100%;">
                                        </div>
                                    '''
                        st.session_state['svg_html_math'] = svg_html_math
                        st.session_state['user'] = username
                        st.write(svg_html_math, unsafe_allow_html=True)
                    else:
                        st.write(st.session_state['svg_html_math'], unsafe_allow_html=True)

    elif choice == 'Variants':
        try:
            if 'Informatics' in menu:
                create_variants_tab_test(username, 'I_')
        except:
            pass
        try:
            if 'Mathematics' in menu:
                create_variants_tab_test(username, 'M_')
        except:
            pass





def main():
    """
    The main function for the application.

    This function handles the authentication process and displays the appropriate content based on the authentication status.

    Args:
        None

    Returns:
        None
    """


    if 'config' not in st.session_state:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path) as file:
            st.session_state.config = yaml.load(file, Loader=SafeLoader)


    authenticator = stauth.Authenticate(
        st.session_state.config['credentials'],
        st.session_state.config['cookie']['name'],
        st.session_state.config['cookie']['key'],
        st.session_state.config['cookie']['expiry_days'],
        st.session_state.config['preauthorized']
    )

    name, authentication_status, username = authenticator.login()


    if authentication_status:
        st.write(f'Welcome, *{name}*')
        one_student(username)
        authenticator.logout('Logout', 'main', key='unique_key')

    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')


if __name__ == '__main__':
    
    main()

