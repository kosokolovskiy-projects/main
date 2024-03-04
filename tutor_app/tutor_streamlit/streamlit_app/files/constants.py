TASKS_NUMBER = {
        2: 102,
        3: 103,
        5: 205,
        6: 206,
        7: 307,
        8: 308,
        9: 129,
        11: 111,
        12: 112,
        13: 113,
        14: 114,
        15: 115,
        16: 116,
        17: 117,
        18: 118,
        19: 119,
        20: 120,
        21: 121,
        22: 222,
        23: 223,
        24: 224,
        25: 525,
        26: 126,
        27: 127
    }
TASKS_NUMBER_USER_1 = {
        2: 102,
        5: 205,
        6: 206,
        7: 307,
        8: 308,
        9: 129,
        12: 112,
        13: 113,
        14: 114,
        15: 115,
        16: 116,
        18: 118,
        19: 119,
        20: 120,
        21: 121,
        23: 223,
        24: 224,
        25: 525,
        27: 127
    }
TASKS_NUMBER_USER_2 = {
        2: 102,
        8: 308,
        9: 129,
        12: 112,
        13: 113,
        15: 115,
        16: 116,
        18: 118,
        21: 121,
        24: 224,
        25: 525,
    }


TASKS_NUMBER_DEMO = TASKS_NUMBER

USERNAME_DICT = {
    'user_1': 1,
    'user_2': 3,
}

TABLE_NAMES = {
  'Тригонометрия': 'math_tasks_trig',
  'Стереометрия': 'math_tasks_stereo',
  'Неравенство': 'math_tasks_ineq',
  'Планиметрия': 'math_tasks_plan',
  'Экономика': 'math_tasks_econ',
  'Параметр': 'math_tasks_param',
  'Последняя': 'math_tasks_last'
}


FOR_LANGUAGE = '''
                <!DOCTYPE html>
                    <head>
                            <meta charset="utf-8">
                            <title>Tasks</title>
                        <style>
                            html *,
                            hr {
                                font-size: 16px;
                                line-height: 2.625;
                                color: #000000;
                                font-family: Nunito, sans-serif;
                                text-align: justify;
                            }

                            hr {
                                display: block;
                                margin-top: 0em;
                                margin-bottom: 1.5em;
                                margin-left: auto;
                                margin-right: auto;
                                border-style: inset;
                                border-width: 1px;
                                width: 100%;
                            }

                            ::selection {
                                background-color: #000;
                                color: #fff;
                            }
                            table {
                                border-collapse: collapse; /* This removes spacing between table cells */
                                width: 100%;
                                border: 2px solid black; /* Border around the table */
                            }

                            th, td {
                                border: 1px solid black; /* Border around header cells and data cells */
                                padding: 8px; /* Add some padding for cell content */
                                text-align: left; /* Align text within cells */
                            }

                            th {
                                background-color: #f2f2f2; /* Background color for header cells */
                            }
                        </style>
                    </head>
    '''

STYLE_SVG = '''
                <style>
                    .white-background {
                        background-color: white; /* Set background color to white */
                        display: inline-block; /* Ensure the div behaves as an inline element */
                        padding: 2px; /* Optional: to create some space around the image */
                    }
                    img.tex {
                        vertical-align: middle; /* Adjust the alignment as needed */
                        background-color: white; /* This will only affect the area of the img element */
                    }
                </style>
    '''