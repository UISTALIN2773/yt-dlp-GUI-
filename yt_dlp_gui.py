"""
Interfaz grafica simple para yt-dlp.
Requiere que yt-dlp este instalado y accesible (en el PATH o en la
misma carpeta que este script).

Como ejecutar:
    python yt_dlp_gui.py
"""

import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def find_yt_dlp():
    """Busca yt-dlp en el PATH, o yt-dlp.exe junto a este script."""
    found = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    if found:
        return found

    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yt-dlp.exe")
    if os.path.isfile(local):
        return local

    return None


class YtDlpGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Descargador de YouTube (yt-dlp)")
        self.geometry("560x360")
        self.resizable(False, False)

        self.yt_dlp_path = find_yt_dlp()
        self.dest_folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.modo = tk.StringVar(value="video")
        self.proceso = None

        self._construir_interfaz()

        if not self.yt_dlp_path:
            messagebox.showwarning(
                "yt-dlp no encontrado",
                "No se encontro yt-dlp en el PATH ni junto a este script.\n\n"
                "Instala yt-dlp o coloca yt-dlp.exe en la misma carpeta que este archivo.",
            )

    def _construir_interfaz(self):
        padding = {"padx": 12, "pady": 6}

        # URL
        tk.Label(self, text="URL del video:", font=("Segoe UI", 10, "bold")).pack(anchor="w", **padding)
        self.entry_url = tk.Entry(self, width=70, font=("Segoe UI", 10))
        self.entry_url.pack(padx=12, fill="x")

        # Modo: video o audio
        frame_modo = tk.Frame(self)
        frame_modo.pack(anchor="w", **padding)
        tk.Label(frame_modo, text="Descargar como:", font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Radiobutton(frame_modo, text="Video (MP4)", variable=self.modo, value="video").pack(side="left", padx=8)
        tk.Radiobutton(frame_modo, text="Solo audio (MP3)", variable=self.modo, value="audio").pack(side="left", padx=8)

        # Carpeta destino
        frame_carpeta = tk.Frame(self)
        frame_carpeta.pack(anchor="w", fill="x", **padding)
        tk.Label(frame_carpeta, text="Carpeta destino:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        subframe = tk.Frame(frame_carpeta)
        subframe.pack(fill="x", pady=4)
        self.entry_carpeta = tk.Entry(subframe, textvariable=self.dest_folder, font=("Segoe UI", 10))
        self.entry_carpeta.pack(side="left", fill="x", expand=True)
        tk.Button(subframe, text="Elegir...", command=self._elegir_carpeta).pack(side="left", padx=6)

        # Boton descargar
        self.btn_descargar = tk.Button(
            self,
            text="Descargar",
            font=("Segoe UI", 11, "bold"),
            bg="#1f6feb",
            fg="white",
            command=self._iniciar_descarga,
        )
        self.btn_descargar.pack(pady=10)

        # Barra de progreso (indeterminada, yt-dlp no da % facil de parsear en GUI simple)
        self.progressbar = ttk.Progressbar(self, mode="indeterminate", length=520)
        self.progressbar.pack(pady=4)

        # Log de salida
        tk.Label(self, text="Estado:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12)
        self.text_log = tk.Text(self, height=8, font=("Consolas", 9))
        self.text_log.pack(padx=12, pady=4, fill="both", expand=True)
        self.text_log.configure(state="disabled")

    def _elegir_carpeta(self):
        carpeta = filedialog.askdirectory(initialdir=self.dest_folder.get() or os.path.expanduser("~"))
        if carpeta:
            self.dest_folder.set(carpeta)

    def _log(self, mensaje):
        self.text_log.configure(state="normal")
        self.text_log.insert("end", mensaje + "\n")
        self.text_log.see("end")
        self.text_log.configure(state="disabled")

    def _iniciar_descarga(self):
        url = self.entry_url.get().strip()
        carpeta = self.dest_folder.get().strip()

        if not url:
            messagebox.showerror("Falta URL", "Pega la URL del video antes de descargar.")
            return

        if not self.yt_dlp_path:
            messagebox.showerror("yt-dlp no encontrado", "No se encontro yt-dlp instalado.")
            return

        if not os.path.isdir(carpeta):
            try:
                os.makedirs(carpeta, exist_ok=True)
            except OSError as e:
                messagebox.showerror("Carpeta invalida", f"No se pudo crear la carpeta:\n{e}")
                return

        self.btn_descargar.configure(state="disabled", text="Descargando...")
        self.progressbar.start(12)
        self._log(f"Iniciando descarga ({self.modo.get()}) en: {carpeta}")

        hilo = threading.Thread(target=self._ejecutar_descarga, args=(url, carpeta, self.modo.get()), daemon=True)
        hilo.start()

    def _ejecutar_descarga(self, url, carpeta, modo):
        output_template = os.path.join(carpeta, "%(title)s.%(ext)s")

        comando = [self.yt_dlp_path, "--no-playlist", "-o", output_template]

        if modo == "audio":
            comando += ["-x", "--audio-format", "mp3"]
        else:
            comando += ["-t", "mp4"]

        comando.append(url)

        try:
            proceso = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )

            for linea in proceso.stdout:
                self.after(0, self._log, linea.rstrip())

            codigo = proceso.wait()

            if codigo == 0:
                self.after(0, self._log, "\n✅ Descarga completada con exito.")
                self.after(0, lambda: messagebox.showinfo("Listo", "La descarga termino correctamente."))
            else:
                self.after(0, self._log, f"\n❌ yt-dlp termino con codigo de error {codigo}.")
                self.after(0, lambda: messagebox.showerror("Error", "Hubo un problema durante la descarga. Revisa el log."))

        except Exception as e:
            self.after(0, self._log, f"\n❌ Error inesperado: {e}")
            self.after(0, lambda: messagebox.showerror("Error", str(e)))

        finally:
            self.after(0, self._finalizar_descarga)

    def _finalizar_descarga(self):
        self.progressbar.stop()
        self.btn_descargar.configure(state="normal", text="Descargar")


if __name__ == "__main__":
    app = YtDlpGUI()
    app.mainloop()
