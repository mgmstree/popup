import tkinter as tk
import keyboard
import threading
import time
import ctypes
import win32clipboard
import os
import subprocess
import pyautogui
import pyperclip

class PopupTeclas:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.withdraw()
        
        self.cores = {
            'fundo': '#2c2c2c',
            'texto': '#ffffff',
            'borda_clara': '#404040',
            'borda_escura': '#1a1a1a',
            'tecla_especial': '#00ff9d'
        }
        
        self.teclas_especiais = {
            'space': 'ESPAÇO',
            'enter': 'ENTER',
            'backspace': '⌫',
            'shift': 'SHIFT',
            'ctrl': 'CTRL',
            'alt': 'ALT',
            'tab': 'TAB',
            'caps lock': 'CAPS',
            'esc': 'ESC'
        }
        
        self.popup = None
        self.shift_pressionado = False
        self.executando = True
        self.historico = []
        self.indice_historico = 0
        
        keyboard.add_hotkey('esc', self.destruir_popup_seguro)
        keyboard.add_hotkey('ctrl+c', self.verificar_selecao_thread)
        
        self.janela.after(100, self.atualizar_interface)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

    def _iniciar_arrasto(self, event):
        if self.popup:
            self.popup._offsetx = event.x
            self.popup._offsety = event.y

    def _durante_arrasto(self, event):
        if self.popup:
            x = self.popup.winfo_pointerx() - self.popup._offsetx
            y = self.popup.winfo_pointery() - self.popup._offsety
            self.popup.geometry(f"+{x}+{y}")

    def get_capslock_state(self):
        return ctypes.windll.user32.GetKeyState(0x14) & 0x0001 != 0

    def criar_borda_3d(self, master):
        tk.Frame(master, height=2, bg=self.cores['borda_clara']).place(relx=0, rely=0, relwidth=1)
        tk.Frame(master, width=2, bg=self.cores['borda_clara']).place(relx=0, rely=0, relheight=1)
        tk.Frame(master, height=2, bg=self.cores['borda_escura']).place(relx=0, rely=1, relwidth=1, anchor='sw')
        tk.Frame(master, width=2, bg=self.cores['borda_escura']).place(relx=1, rely=0, relheight=1, anchor='ne')

    def destruir_popup_seguro(self):
        if self.popup:
            try:
                self.popup.destroy()
            except tk.TclError:
                pass
            finally:
                self.popup = None

    def mostrar_popup(self, texto):
        self.destruir_popup_seguro()
        
        try:
            self.popup = tk.Toplevel(self.janela)
            self.popup.attributes('-topmost', True)
            self.popup.overrideredirect(True)
            self.popup.configure(bg=self.cores['fundo'])
            
            container = tk.Frame(self.popup, bg=self.cores['fundo'])
            container.pack(expand=True, fill='both', padx=2, pady=2)
            self.criar_borda_3d(container)
            
            self.label_texto = tk.Label(
                container,
                text=texto,
                font=('Segoe UI', 11),
                fg=self.cores['texto'],
                bg=self.cores['fundo'],
                padx=10,
                pady=10,
                wraplength=400
            )
            self.label_texto.pack(expand=True, fill='both')
            
            frame_controles = tk.Frame(container, bg=self.cores['fundo'])
            frame_controles.pack(pady=5, fill='x')
            
            frame_navegacao = tk.Frame(frame_controles, bg=self.cores['fundo'])
            frame_navegacao.pack(side=tk.LEFT, padx=10)
            
            self.btn_esquerda = tk.Button(
                frame_navegacao,
                text="←",
                command=lambda: self.navegar_historico(1),
                bg=self.cores['borda_clara'],
                fg=self.cores['texto'],
                state='normal' if len(self.historico) > 1 else 'disabled'
            )
            self.btn_esquerda.pack(side=tk.LEFT)
            
            self.btn_direita = tk.Button(
                frame_navegacao,
                text="→",
                command=lambda: self.navegar_historico(-1),
                bg=self.cores['borda_clara'],
                fg=self.cores['texto'],
                state='disabled'
            )
            self.btn_direita.pack(side=tk.LEFT)
            
            frame_botoes = tk.Frame(frame_controles, bg=self.cores['fundo'])
            frame_botoes.pack(side=tk.RIGHT)
            
            tk.Button(
                frame_botoes,
                text="Salvar",
                command=self.salvar_texto,
                bg=self.cores['borda_clara'],
                fg=self.cores['texto']
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                frame_botoes,
                text="Enviar",
                command=self.enviar_texto,
                bg=self.cores['borda_clara'],
                fg=self.cores['texto']
            ).pack(side=tk.LEFT, padx=5)
            
            for widget in [container, self.label_texto]:
                widget.bind("<ButtonPress-1>", self._iniciar_arrasto)
                widget.bind("<B1-Motion>", self._durante_arrasto)
            
            self.popup.after(100, self.centralizar_popup)
            
        except Exception as e:
            print(f"Erro controlado: {e}")

    def centralizar_popup(self):
        if self.popup:
            self.popup.update_idletasks()
            largura = self.popup.winfo_width()
            altura = self.popup.winfo_height()
            x = (self.popup.winfo_screenwidth() - largura) // 2
            y = (self.popup.winfo_screenheight() - altura) // 2
            self.popup.geometry(f"+{x}+{y}")

    def salvar_texto(self):
        try:
            texto = self.historico[self.indice_historico]
            documentos = os.path.join(os.path.expanduser('~'), 'Documents')
            caminho = os.path.join(documentos, 'texto_copiado.txt')
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            subprocess.Popen(['notepad.exe', caminho])
        except Exception as e:
            print(f"Erro ao salvar: {e}")
        finally:
            self.destruir_popup_seguro()

    def enviar_texto(self):
        try:
            texto = self.historico[self.indice_historico]
            self.destruir_popup_seguro()
            
            # Salva o clipboard atual
            clipboard_original = pyperclip.paste()
            
            # Copia o texto para o clipboard
            pyperclip.copy(texto)
            
            # Cola o texto usando atalho
            pyautogui.hotkey('ctrl', 'v')
            
            # Restaura o clipboard original após pequeno delay
            time.sleep(0.5)
            pyperclip.copy(clipboard_original)
            
        except Exception as e:
            print(f"Erro ao enviar: {e}")

    def verificar_selecao_thread(self):
        threading.Thread(target=self.verificar_selecao, daemon=True).start()

    def verificar_selecao(self):
        try:
            time.sleep(0.1)
            win32clipboard.OpenClipboard()
            
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                texto = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                texto_processado = self.filtrar_texto(texto)
                
                if texto_processado:
                    self.historico.insert(0, texto_processado)
                    self.historico = self.historico[:4]
                    self.indice_historico = 0
                    self.janela.after(0, self.mostrar_popup, texto_processado)
            
            win32clipboard.CloseClipboard()
            
        except Exception as e:
            print(f"Erro no clipboard: {e}")

    def filtrar_texto(self, texto):
        linhas = []
        for linha in texto.splitlines():
            linha_limpa = linha.strip()
            if (
                linha_limpa 
                and not linha_limpa.startswith(('http://', 'https://', 'www.'))
                and not any(p in linha_limpa.lower() for p in ['fonte:', 'source:', 'referência:', 'reference:'])
            ):
                linhas.append(linha_limpa)
        return '\n'.join(linhas) if linhas else None

    def navegar_historico(self, direcao):
        novo_indice = self.indice_historico + direcao
        if 0 <= novo_indice < len(self.historico):
            self.indice_historico = novo_indice
            self.label_texto.config(text=self.historico[self.indice_historico])
            
            # Atualizar estados dos botões
            self.btn_esquerda.config(state='normal' if self.indice_historico < len(self.historico)-1 else 'disabled')
            self.btn_direita.config(state='normal' if self.indice_historico > 0 else 'disabled')

    def atualizar_interface(self):
        try:
            if self.executando:
                self.janela.after(100, self.atualizar_interface)
        except Exception as e:
            print(f"Erro na atualização: {e}")

    def fechar_aplicativo(self):
        self.executando = False
        self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = PopupTeclas()
    app.iniciar()