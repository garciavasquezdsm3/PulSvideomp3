import flet as ft
import yt_dlp
import threading

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "PulSvideomp3"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 390
    page.window_height = 780
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    selected_platform = "youtube"
    selected_format = "mp4"

    def update_status(message, progress_val=None, color="white"):
        status_text.value = message
        status_text.color = color
        if progress_val is not None:
            progress_bar.value = progress_val
            progress_bar.visible = True
        page.update()

    def run_download(url, format_type):
        try:
            update_status("Obteniendo información...", 0.2, "cyan")

            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
            }

            if format_type == "mp3":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                })

            update_status("Descargando archivo...", 0.6, "amber")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            update_status("¡Descarga completada con éxito!", 1.0, "green")
            download_btn.disabled = False
            page.update()

        except Exception as e:
            update_status(f"Error: {str(e)[:50]}...", 0, "red")
            download_btn.disabled = False
            page.update()

    def start_download_click(e):
        url = url_input.value.strip() if url_input.value else ""
        if not url:
            update_status("Por favor pega una URL válida.", 0, "red")
            return

        download_btn.disabled = True
        progress_bar.visible = True
        page.update()

        threading.Thread(target=run_download, args=(url, selected_format), daemon=True).start()

    def platform_changed(e):
        nonlocal selected_platform
        selected_platform = e.control.data

    def format_changed(e):
        nonlocal selected_format
        selected_format = e.control.value

    # --- COMPONENTES DE LA INTERFAZ ---

    # Encabezado
    header = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Icon("download_for_offline_rounded", size=32, color="indigo400"),
            ft.Text("PulSvideomp3", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text("PRO", size=10, weight=ft.FontWeight.BOLD, color="indigo300"),
                bgcolor="indigo900",
                padding=ft.padding.all(5),
                border_radius=8
            )
        ]
    )

    # Selector de Plataforma
    platform_selector = ft.RadioGroup(
        value="youtube",
        on_change=platform_changed,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Icon("you_tube", color="red", size=30),
                        ft.Text("YouTube", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    data="youtube",
                    padding=10,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Icon("facebook", color="blue", size=30),
                        ft.Text("Facebook", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    data="facebook",
                    padding=10,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Icon("camera_alt", color="pink", size=30),
                        ft.Text("Instagram", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    data="instagram",
                    padding=10,
                ),
            ]
        )
    )

    # Campo de URL
    url_input = ft.TextField(
        hint_text="Pega el enlace del video aquí...",
        border_radius=15,
        border_color="indigo500",
        focused_border_color="purple400",
        prefix_icon="link",
        text_size=14
    )

    # Selector MP4 / MP3
    format_selector = ft.SegmentedButton(
        selected={"mp4"},
        allow_multiple_selection=False,
        on_change=lambda e: format_changed(type('obj', (object,), {'value': list(e.selection)[0]})),
        segments=[
            ft.Segment(value="mp4", label=ft.Text("Video (MP4)"), icon=ft.Icon("video_library")),
            ft.Segment(value="mp3", label=ft.Text("Audio (MP3)"), icon=ft.Icon("music_note")),
        ]
    )

    # Botón de Descarga
    download_btn = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon("file_download"),
            ft.Text("Descargar Contenido", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER),
        style=ft.ButtonStyle(
            bgcolor="indigo600",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=15
        ),
        on_click=start_download_click,
        width=300
    )

    # Estado y progreso
    status_text = ft.Text("", size=12, text_align=ft.TextAlign.CENTER)
    progress_bar = ft.ProgressBar(width=300, value=0, visible=False, color="indigo400")

    # Créditos de Autoría corregidos
    credits_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon("code", size=14, color="grey500"),
                        ft.Text("Desarrollado por", size=11, color="grey500"),
                        ft.Text("OSCAR GARCIA", size=12, weight=ft.FontWeight.BOLD, color="indigo300")
                    ]
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.only(top=15)
    )

    # Montaje de pantalla
    page.add(
        header,
        ft.Divider(height=15, color="transparent"),
        ft.Text("1. Selecciona la plataforma", size=12, color="grey400"),
        platform_selector,
        ft.Divider(height=10, color="transparent"),
        ft.Text("2. Pega el enlace", size=12, color="grey400"),
        url_input,
        ft.Divider(height=10, color="transparent"),
        ft.Text("3. Elige el formato", size=12, color="grey400"),
        format_selector,
        ft.Divider(height=20, color="transparent"),
        download_btn,
        ft.Column([status_text, progress_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        credits_section
    )

if __name__ == "__main__":
    ft.app(target=main)