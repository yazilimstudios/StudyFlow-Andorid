import flet as ft
import requests
from datetime import datetime

API_URL = "https://script.google.com/macros/s/AKfycbz7yteEHPaUOCqR5_dho1oE4aiLwVUMo8ndBdDTJjNdHjRL9TJeNcdgPFjS81dE-J3I/exec"

def main(page: ft.Page):
    page.title = "StudyFlow - Mobil Çalışma Asistanı"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    current_user = {"name": None}

    def send_api_request(payload):
        try:
            res = requests.post(API_URL, json=payload, timeout=15)
            return res.json()
        except:
            return {"status": "error", "message": "Sunucuya bağlanılamadı!"}

    def show_view(view_name):
        page.clean()
        if view_name == "login":
            page.appbar = None
            page.add(login_view())
        elif view_name == "register":
            page.appbar = None
            page.add(register_view())
        elif view_name == "dashboard":
            page.add(dashboard_view())
        page.update()

    # --- 1. GİRİŞ EKRANI ---
    def login_view():
        username_field = ft.TextField(label="Kullanıcı Adı", width=300, border_radius=10)
        password_field = ft.TextField(label="Şifre", password=True, can_reveal_password=True, width=300, border_radius=10)
        status_text = ft.Text(value="", color=ft.Colors.RED_400)

        def do_login(e):
            if not username_field.value or not password_field.value:
                status_text.value = "Tüm alanları doldurun!"
                page.update()
                return
            
            status_text.value = "Giriş yapılıyor..."
            status_text.color = ft.Colors.YELLOW_400
            page.update()

            res = send_api_request({"action": "login", "username": username_field.value, "password": password_field.value})
            if res.get("status") == "success":
                current_user["name"] = username_field.value
                show_view("dashboard")
            else:
                status_text.value = res.get("message", "Giriş başarısız!")
                status_text.color = ft.Colors.RED_400
                page.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.BOLT_ROUNDED, size=70, color=ft.Colors.BLUE_400),
                    ft.Text("StudyFlow", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text("Mobil Çalışma Asistanı", size=16, color=ft.Colors.GREY_400),
                    ft.Container(height=20),
                    username_field,
                    password_field,
                    status_text,
                    ft.ElevatedButton("Giriş Yap", on_click=do_login, width=300, height=45),
                    ft.TextButton("Hesabın yok mu? Kayıt Ol", on_click=lambda e: show_view("register"))
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    # --- 2. KAYIT OL EKRANI ---
    def register_view():
        username_field = ft.TextField(label="Yeni Kullanıcı Adı", width=300, border_radius=10)
        password_field = ft.TextField(label="Şifre", password=True, can_reveal_password=True, width=300, border_radius=10)
        status_text = ft.Text(value="", color=ft.Colors.RED_400)

        def do_register(e):
            if not username_field.value or not password_field.value:
                status_text.value = "Tüm alanları doldurun!"
                page.update()
                return
            
            status_text.value = "Kayıt oluşturuluyor..."
            status_text.color = ft.Colors.YELLOW_400
            page.update()

            res = send_api_request({"action": "register", "username": username_field.value, "password": password_field.value})
            if res.get("status") == "success":
                status_text.value = "✅ Kayıt başarılı! Giriş yapabilirsiniz."
                status_text.color = ft.Colors.GREEN_400
            else:
                status_text.value = res.get("message", "Kayıt başarısız!")
                status_text.color = ft.Colors.RED_400
            page.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=70, color=ft.Colors.GREEN_400),
                    ft.Text("Kayıt Ol", size=32, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),
                    username_field,
                    password_field,
                    status_text,
                    ft.ElevatedButton("Kayıt Ol", on_click=do_register, width=300, height=45),
                    ft.TextButton("Zaten hesabın var mı? Giriş Yap", on_click=lambda e: show_view("login"))
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    # --- 3. ANA PANEL & SOLDAN AÇILIR MENÜ (DRAWER) ---
    def dashboard_view():
        content_area = ft.Column(scroll="auto", expand=True)

        # İçerik 1: Özet Sayfası
        def load_home_content():
            content_area.controls.clear()
            content_area.controls.append(ft.Text("Veriler Yükleniyor...", color=ft.Colors.YELLOW_400))
            page.update()

            res = send_api_request({"action": "get_records", "username": current_user["name"]})
            records = res.get("records", []) if res.get("status") == "success" else []

            total_q = sum(r.get("questions", 0) for r in records)
            total_dur = sum(r.get("duration", 0) for r in records)
            total_net = round(sum(r.get("net", 0.0) for r in records), 2)

            content_area.controls = [
                ft.Text(f"Hoş Geldin, {current_user['name']}! 🚀", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Text("Toplam Soru"), ft.Text(str(total_q), size=20, weight="bold")]), bgcolor=ft.Colors.BLUE_900, padding=15, border_radius=10, expand=True),
                    ft.Container(content=ft.Column([ft.Text("Çalışma Süresi"), ft.Text(f"{total_dur} dk", size=20, weight="bold")]), bgcolor=ft.Colors.GREEN_900, padding=15, border_radius=10, expand=True),
                ]),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Text("Toplam Kayıt"), ft.Text(str(len(records)), size=20, weight="bold")]), bgcolor=ft.Colors.AMBER_900, padding=15, border_radius=10, expand=True),
                    ft.Container(content=ft.Column([ft.Text("Toplam Net"), ft.Text(str(total_net), size=20, weight="bold")]), bgcolor=ft.Colors.PURPLE_900, padding=15, border_radius=10, expand=True),
                ]),
            ]
            page.update()

        # İçerik 2: Ders Kaydetme Sayfası (Boş Sayısı Dahil)
        def load_add_content():
            lesson_dropdown = ft.Dropdown(
                label="Ders Seç",
                options=[ft.dropdown.Option(x) for x in ["Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler", "İngilizce", "Geometri", "Fizik", "Kimya", "Biyoloji"]],
                border_radius=10
            )
            topic_input = ft.TextField(label="Konu", border_radius=10)
            dur_input = ft.TextField(label="Süre (Dakika)", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
            q_input = ft.TextField(label="Soru Sayısı", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
            c_input = ft.TextField(label="Doğru Sayısı", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
            w_input = ft.TextField(label="Yanlış Sayısı", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
            b_input = ft.TextField(label="Boş Sayısı", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
            add_status = ft.Text(value="")

            def save_record_click(e):
                try:
                    dur = int(dur_input.value or 0)
                    q = int(q_input.value or 0)
                    c = int(c_input.value or 0)
                    w = int(w_input.value or 0)
                    b = int(b_input.value or 0)
                    net = max(0, round(c - (w / 4.0), 2))

                    payload = {
                        "action": "add_record",
                        "username": current_user["name"],
                        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "lesson": lesson_dropdown.value or "Matematik",
                        "topic": topic_input.value or "Belirtilmedi",
                        "duration": dur,
                        "questions": q,
                        "correct": c,
                        "wrong": w,
                        "blank": b,
                        "net": net
                    }
                    res = send_api_request(payload)
                    if res.get("status") == "success":
                        add_status.value = "✅ Başarıyla E-Tabloya Kaydedildi!"
                        add_status.color = ft.Colors.GREEN_400
                    else:
                        add_status.value = "⚠️ Kaydedilemedi!"
                        add_status.color = ft.Colors.RED_400
                    page.update()
                except:
                    add_status.value = "⚠️ Sayısal alanları doğru girin!"
                    add_status.color = ft.Colors.RED_400
                    page.update()

            content_area.controls = [
                ft.Text("Yeni Çalışma Kaydı Ekle", size=20, weight="bold"),
                ft.Divider(),
                lesson_dropdown, topic_input, dur_input, q_input, c_input, w_input, b_input,
                add_status,
                ft.ElevatedButton("E-Tabloya Kaydet", on_click=save_record_click, width=300, height=45)
            ]
            page.update()

        # İçerik 3: Geçmiş Kayıtlar Sayfası
        def load_history_content():
            content_area.controls.clear()
            content_area.controls.append(ft.Text("Geçmiş Kayıtlar Yükleniyor...", color=ft.Colors.YELLOW_400))
            page.update()

            res = send_api_request({"action": "get_records", "username": current_user["name"]})
            records = res.get("records", []) if res.get("status") == "success" else []

            if not records:
                content_area.controls = [
                    ft.Text("Geçmiş Kayıtlar", size=20, weight="bold"),
                    ft.Divider(),
                    ft.Text("Henüz kaydedilmiş bir çalışmanız yok.", color=ft.Colors.GREY_400)
                ]
                page.update()
                return

            list_items = []
            for r in reversed(records): # En son eklenen en üstte gözüksün
                list_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"📚 {r.get('lesson', 'Ders')}", weight="bold", size=16),
                                ft.Text(f"Tarih: {r.get('date', '-')}", color=ft.Colors.GREY_400, size=12)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Konu: {r.get('topic', '-')}", size=14),
                            ft.Row([
                                ft.Text(f"Süre: {r.get('duration', 0)} dk", size=12),
                                ft.Text(f"Soru: {r.get('questions', 0)}", size=12),
                                ft.Text(f"Net: {r.get('net', 0)}", size=12, weight="bold", color=ft.Colors.GREEN_400),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ]),
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=12,
                        border_radius=10,
                        margin=ft.margin.only(bottom=10)
                    )
                )

            content_area.controls = [
                ft.Text("Geçmiş Çalışmalarım", size=20, weight="bold"),
                ft.Divider(),
                *list_items
            ]
            page.update()

        # İçerik 4: Pomodoro Sayacı Sayfası
        def load_pomodoro_content():
            pomo_status = ft.Text("25:00", size=48, weight="bold", color=ft.Colors.BLUE_400)
            
            content_area.controls = [
                ft.Text("Pomodoro Odak Modu", size=20, weight="bold"),
                ft.Divider(),
                ft.Container(content=pomo_status, alignment=ft.alignment.center, padding=30),
                ft.Row([
                    ft.ElevatedButton("Başlat", icon=ft.Icons.PLAY_ARROW),
                    ft.OutlinedButton("Sıfırla", icon=ft.Icons.REFRESH),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]
            page.update()

        drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(icon=ft.Icons.HOME_ROUNDED, label="Özet ve İstatistikler"),
                ft.NavigationDrawerDestination(icon=ft.Icons.ADD_TASK_ROUNDED, label="Ders / Soru Kaydet"),
                ft.NavigationDrawerDestination(icon=ft.Icons.HISTORY_ROUNDED, label="Geçmiş Kayıtlar"),
                ft.NavigationDrawerDestination(icon=ft.Icons.TIMER_ROUNDED, label="Pomodoro Sayaç"),
                ft.Divider(thickness=1),
                ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT_ROUNDED, label="Çıkış Yap"),
            ],
            on_change=lambda e: drawer_changed(e.control.selected_index)
        )

        def drawer_changed(index):
            page.drawer.open = False
            if index == 0:
                load_home_content()
            elif index == 1:
                load_add_content()
            elif index == 2:
                load_history_content()
            elif index == 3:
                load_pomodoro_content()
            elif index == 4:
                show_view("login")
            page.update()

        app_bar = ft.AppBar(
            leading=ft.IconButton(ft.Icons.MENU_ROUNDED, on_click=lambda e: page.open(drawer)),
            leading_width=40,
            title=ft.Text("StudyFlow Asistanı"),
            center_title=True,
            bgcolor=ft.Colors.BLUE_GREY_900,
        )

        page.drawer = drawer
        page.appbar = app_bar
        
        load_home_content()
        
        return ft.Container(content=content_area, padding=20, expand=True)

    show_view("login")

if __name__ == "__main__":
    ft.app(target=main)