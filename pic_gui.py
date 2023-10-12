import PySimpleGUI as sg
import subprocess
import sys
import os
path_files = os.getcwd().replace('\\', '/') + '/assets/gui_files/'
path_media = os.getcwd().replace('\\', '/') + '/assets/media/'
path_script = os.getcwd().replace('\\', '/') + '/assets/script_files/'

red = '#ff331f'
white = '#ffffff'
black = '#1e2326'

layout = [[sg.Image('{}Shutterstock-logo.png'.format(path_media))],
          [sg.HorizontalSeparator(color=red)],
          [sg.Text('enter folder path', text_color=black, background_color=white, font=('', 12, 'bold'))],
          [sg.Input('', key='folder_path', readonly=True),
           sg.FolderBrowse(font=('', 9, 'bold'), button_color=(white, black), key='fb')],
          [sg.Text('enter word to download pics ', text_color=black, background_color=white, font=('', 12, 'bold'))],
          [sg.Input('', key='to_search')],
          [sg.HorizontalSeparator(color=red, pad=(0, 20))],
          [sg.Button('Download', key='download', font=('', 9, 'bold'), button_color=(white, black), pad=(10, 20)),
           sg.Button('Stop', key='stop', font=('', 9, 'bold'), button_color=(black, red), disabled=True),
           sg.Button('Pause', key='pause', font=('', 9, 'bold'), button_color=(black, red), disabled=True, pad=(10, 20)),
           sg.Button('Resume', key='resume', font=('', 9, 'bold'), button_color=(white, black), visible=False, pad=(10, 20))
           ],
          [sg.ProgressBar(max_value=100, bar_color=(red, black), orientation='h', size=(25, 20), key='prog' )],
          [sg.Text('0/1000', key='percent', background_color=white, text_color=black, font=('', 10, 'bold'))]
          ]

window = sg.Window('Pics Downloader', layout=layout, element_justification='c', background_color=white, size=(450, 530))
up = 0
down = 0
while True:

    event, values = window.read(1)
    file_prog = open('{}prog.txt'.format(path_files), 'r')
    prog = file_prog.read()
    file_prog.close()
    if prog == '':
        prog = str(up) + 'by' + str(down)
    pro = prog.split('by')
    up = int(pro[0])
    down = int(pro[1])
    window['prog'].UpdateBar(int((up/down)*100))
    window['percent'].update(str(up) + '/' + str(down))
    if event == sg.WINDOW_CLOSED:
        file = open('{}data.txt'.format(path_files), 'w')
        file.write('')
        file.close()
        file = open('{}prog.txt'.format(path_files), 'w')
        file.write('0by1000')
        file.close()
        break
    elif event == 'download':
        folder_path = values['folder_path']
        word = values['to_search']
        if not folder_path or not word:
            sg.Popup('Please Fill All Fields', background_color=red, text_color=black, button_color=(red, black))
            continue
        file = open('{}data.txt'.format(path_files), 'w')
        file.write(folder_path + '\n' + word)
        file.close()
        window['download'].update(disabled=True)
        window['stop'].update(disabled=False)
        window['pause'].update(disabled=False)
        # file = open('{}prog.txt'.format(path_files), 'w')
        # file.write('0by1000')
        # file.close()
        subprocess.Popen([sys.executable, "{}shutterstock.py".format(path_script)])
    elif event == 'stop':
        file = open('{}data.txt'.format(path_files), 'w')
        file.write('stop')
        file.close()
        window['pause'].update(disabled=True)
        window['stop'].update(disabled=True)
        window['download'].update(disabled=False)
        window['resume'].update(visible=False)
        window['pause'].update(visible=True)
        window['folder_path'].update('')
        window['to_search'].update('')
        window['download'].update(disabled=False)
        window['pause'].update(disabled=True)
    elif event == 'pause':
        file = open('{}data.txt'.format(path_files), 'w')
        file.write('pause')
        file.close()
        window['pause'].update(visible=False)
        window['resume'].update(visible=True)
    elif event == 'resume':
        file = open('{}data.txt'.format(path_files), 'w')
        file.write('resume')
        file.close()
        window['pause'].update(visible=True)
        window['resume'].update(visible=False)
    else:
        file = open('{}data.txt'.format(path_files), 'r')
        data = file.read()
        file.close()
        if data == 'error':
            window['folder_path'].update('')
            window['to_search'].update('')
            window['download'].update(disabled=False)
            window['pause'].update(disabled=True)
            sg.Popup('No Data Found!', background_color=red, text_color=black, button_color=(red, black) )
            file = open('{}data.txt'.format(path_files), 'w')
            file.write('')
            file.close()
        elif data == 'finish':
            window['folder_path'].update('')
            window['to_search'].update('')
            window['download'].update(disabled=False)
            window['pause'].update(disabled=True)
            file = open('{}data.txt'.format(path_files), 'w')
            file.write('')
            file.close()

window.close()
