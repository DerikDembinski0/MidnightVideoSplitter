import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import moviepy.editor as mp

def dividir_video_em_partes_iguais(caminho_video, pasta_destino, partes, log_callback):
    try:
        video = mp.VideoFileClip(caminho_video)
        duracao_total = video.duration
        duracao_parte = duracao_total / partes

        os.makedirs(pasta_destino, exist_ok=True)

        log_callback(f"🔧 Iniciando divisão em {partes} partes (~{duracao_parte:.2f} seg cada)\n")

        for i in range(partes):
            inicio = i * duracao_parte
            fim = (i + 1) * duracao_parte
            subclip = video.subclip(inicio, min(fim, duracao_total))
            nome_arquivo = f"Corte {i+1} de {partes}.mp4"
            saida = os.path.join(pasta_destino, nome_arquivo)
            log_callback(f"🎬 Processando {nome_arquivo}...")
            subclip.write_videofile(saida, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            log_callback(f"✅ {nome_arquivo} salvo!\n")

        log_callback("✅ Todos os arquivos foram salvos em MP4 com sucesso.\n")
    except Exception as e:
        log_callback(f"❌ Erro: {str(e)}\n")

def iniciar_interface():
    def log_terminal(msg):
        log_text.config(state='normal')
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)
        log_text.config(state='disabled')

    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Vídeo", "*.mp4 *.mov *.avi")])
        entrada_video.delete(0, tk.END)
        entrada_video.insert(0, caminho)

    def selecionar_pasta():
        pasta = filedialog.askdirectory()
        entrada_pasta.delete(0, tk.END)
        entrada_pasta.insert(0, pasta)

    def ao_clicar_fatiar():
        caminho_video = entrada_video.get()
        pasta_destino = entrada_pasta.get()
        partes_str = entrada_partes.get()

        if partes_str == placeholder_text:
            partes_str = ""

        if not os.path.isfile(caminho_video):
            messagebox.showerror("Erro", "Arquivo de vídeo inválido.")
            return

        if not os.path.isdir(pasta_destino):
            messagebox.showerror("Erro", "Pasta de destino inválida.")
            return

        try:
            partes = int(partes_str)
            if partes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade de partes deve ser um número inteiro positivo.")
            return

        threading.Thread(
            target=dividir_video_em_partes_iguais,
            args=(caminho_video, pasta_destino, partes, log_terminal),
            daemon=True
        ).start()

    # 🎨 Estilo Midnight
    cor_fundo = "#1A1B26"
    cor_secundaria = "#2E2F3E"
    cor_destaque = "#9D7FFB"
    cor_texto = "#FFFFFF"
    cor_placeholder = "#888888"

    root = tk.Tk()
    root.title("Midnight Video Splitter")
    root.geometry("900x500")
    root.configure(bg=cor_fundo)

    # 🟣 Ícone da janela com suporte para PyInstaller
    try:
        if getattr(sys, 'frozen', False):
            caminho_icone = os.path.join(sys._MEIPASS, "icone.ico")
        else:
            caminho_icone = "icone.ico"
        root.iconbitmap(caminho_icone)
    except Exception as e:
        print(f"Erro ao definir ícone: {e}")

    style_opts = {
        "bg": cor_secundaria,
        "fg": cor_texto,
        "insertbackground": cor_texto,
        "highlightbackground": cor_destaque,
        "relief": "flat"
    }

    # 📦 Lado esquerdo
    frame_esquerdo = tk.Frame(root, width=450, bg=cor_fundo)
    frame_esquerdo.pack(side="left", fill="both", padx=20, pady=20)

    tk.Label(frame_esquerdo, text="LOCAL DO ARQUIVO:", bg=cor_fundo, fg=cor_texto).pack(anchor="w")
    entrada_video = tk.Entry(frame_esquerdo, width=50, **style_opts)
    entrada_video.pack(pady=5)
    tk.Button(frame_esquerdo, text="Selecionar", command=selecionar_arquivo, bg=cor_destaque, fg="black").pack(pady=2)

    tk.Label(frame_esquerdo, text="PASTA DE DESTINO:", bg=cor_fundo, fg=cor_texto).pack(anchor="w", pady=(15, 0))
    entrada_pasta = tk.Entry(frame_esquerdo, width=50, **style_opts)
    entrada_pasta.pack(pady=5)
    tk.Button(frame_esquerdo, text="Selecionar", command=selecionar_pasta, bg=cor_destaque, fg="black").pack(pady=2)

    tk.Label(frame_esquerdo, text="FATIAR EM QUANTAS PARTES IGUAIS:", bg=cor_fundo, fg=cor_texto).pack(anchor="w", pady=(15, 0))

    # ⌨️ Entrada com placeholder
    placeholder_text = "INSIRA AQUI A QUANTIDADE DE PARTES"

    def on_focus_in(event):
        if entrada_partes.get() == placeholder_text:
            entrada_partes.delete(0, tk.END)
            entrada_partes.config(fg=cor_texto)

    def on_focus_out(event):
        if entrada_partes.get() == "":
            entrada_partes.insert(0, placeholder_text)
            entrada_partes.config(fg=cor_placeholder)

    entrada_partes = tk.Entry(
        frame_esquerdo,
        width=50,
        fg=cor_placeholder,
        bg=cor_secundaria,
        insertbackground=cor_texto,
        highlightbackground=cor_destaque,
        relief="flat"
    )
    entrada_partes.insert(0, placeholder_text)
    entrada_partes.bind("<FocusIn>", on_focus_in)
    entrada_partes.bind("<FocusOut>", on_focus_out)
    entrada_partes.pack(pady=5)

    tk.Button(frame_esquerdo, text="FATIAR", width=20, command=ao_clicar_fatiar, bg=cor_destaque, fg="black").pack(pady=20)

    # 📋 Lado direito - Terminal
    frame_direito = tk.Frame(root, width=450, bg=cor_secundaria, bd=1, relief="solid")
    frame_direito.pack(side="right", fill="both", expand=True, padx=10, pady=20)

    tk.Label(frame_direito, text="LOG TERMINAL:", anchor="w", bg=cor_secundaria, fg=cor_texto).pack(anchor="nw", padx=10, pady=5)

    log_text = tk.Text(frame_direito, state='disabled', wrap='word', bg=cor_fundo, fg=cor_texto, insertbackground=cor_texto, relief="flat")
    log_text.pack(fill="both", expand=True, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
