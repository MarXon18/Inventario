import flet as ft
import httpx # Usamos httpx que es compatible con la web

# --- CONFIGURACIÓN DE LA NUBE ---
URL_NUBE = "https://kfnlhjxecolizlqhuglj.supabase.co"
KEY_NUBE = "sb_publishable_qMAe7GjzjPlX1rr0-XvN-w_3eOgEekM"



HEADERS = {
    "apikey": KEY_NUBE,
    "Authorization": f"Bearer {KEY_NUBE}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def main(page: ft.Page):
    page.title = "Control de Stock SysAcad"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Elementos de la interfaz
    nombre_in = ft.TextField(label="Producto", expand=True)
    variedad_in = ft.TextField(label="Variedad (Talle/Color)", expand=True)
    cantidad_in = ft.TextField(label="Cant.", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    lista_stock = ft.Column(spacing=10)

    def cargar_datos():
        lista_stock.controls.clear()
        try:
            # Petición GET a la API de Supabase
            with httpx.Client() as client:
                res = client.get(f"{URL_NUBE}/rest/v1/stock?select=*", headers=HEADERS)
                if res.status_code == 200:
                    for fila in res.json():
                        lista_stock.controls.append(
                            ft.Container(
                                content=ft.ListTile(
                                    title=ft.Text(f"{fila['nombre']} - {fila['variedad']}"),
                                    subtitle=ft.Text(f"Existencias: {fila['cantidad']}"),
                                    trailing=ft.Row([
                                        ft.IconButton(ft.icons.ADD_CIRCLE, icon_color="green", 
                                                     on_click=lambda e, i=fila['id'], c=fila['cantidad']: actualizar(i, c + 1)),
                                        ft.IconButton(ft.icons.REMOVE_CIRCLE, icon_color="red", 
                                                     on_click=lambda e, i=fila['id'], c=fila['cantidad']: actualizar(i, c - 1)),
                                    ], tight=True)
                                ),
                                border=ft.border.all(1, ft.colors.BLACK12),
                                border_radius=10
                            )
                        )
        except Exception as ex:
            print(f"Error al cargar: {ex}")
        page.update()

    def agregar_click(e):
        if nombre_in.value and cantidad_in.value:
            nuevo_item = {
                "nombre": nombre_in.value,
                "variedad": variedad_in.value,
                "cantidad": int(cantidad_in.value)
            }
            with httpx.Client() as client:
                client.post(f"{URL_NUBE}/rest/v1/stock", headers=HEADERS, json=nuevo_item)
            nombre_in.value = ""; variedad_in.value = ""; cantidad_in.value = ""
            cargar_datos()

    def actualizar(id_prod, nuevo_valor):
        # Aseguramos que el stock no sea menor a 0
        valor_final = max(0, nuevo_valor)
        with httpx.Client() as client:
            client.patch(f"{URL_NUBE}/rest/v1/stock?id=eq.{id_prod}", 
                         headers=HEADERS, json={"cantidad": valor_final})
        cargar_datos()

    # Construcción de la pantalla
    page.add(
        ft.Text("Gestión de Inventario", size=32, weight="bold", color="blue700"),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([nombre_in, variedad_in]),
                    ft.Row([cantidad_in, ft.ElevatedButton("Añadir al Stock", 
                           icon=ft.icons.SAVE, on_click=agregar_click, expand=True)]),
                ]), padding=20
            )
        ),
        ft.Divider(),
        ft.Text("Productos en Almacén", size=20, weight="w500"),
        lista_stock
    )
    cargar_datos()

ft.app(target=main)
