import flet as ft
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LA NUBE ---
URL_NUBE = "https://kfnlhjxecolizlqhuglj.supabase.co"
KEY_NUBE = "sb_publishable_qMAe7GjzjPlX1rr0-XvN-w_3eOgEekM"
supabase: Client = create_client(URL_NUBE, KEY_NUBE)

def main(page: ft.Page):
    page.title = "Stock en la Nube"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    
    nombre_in = ft.TextField(label="Producto", expand=True)
    variedad_in = ft.TextField(label="Variedad", expand=True)
    cantidad_in = ft.TextField(label="Cant.", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    lista_stock = ft.ListView(expand=True, spacing=10)

    def cargar_datos():
        lista_stock.controls.clear()
        # Traemos los datos de la nube
        respuesta = supabase.table("stock").select("*").execute()
        for fila in respuesta.data:
            lista_stock.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{fila['nombre']} ({fila['variedad']})"),
                    subtitle=ft.Text(f"Cantidad: {fila['cantidad']}"),
                    trailing=ft.Row([
                        ft.IconButton(ft.icons.ADD, on_click=lambda e, i=fila['id'], c=fila['cantidad']: actualizar(i, c + 1)),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e, i=fila['id'], c=fila['cantidad']: actualizar(i, c - 1)),
                    ], tight=True)
                )
            )
        page.update()

    def agregar_click(e):
        if nombre_in.value:
            supabase.table("stock").insert({
                "nombre": nombre_in.value,
                "variedad": variedad_in.value,
                "cantidad": int(cantidad_in.value or 0)
            }).execute()
            nombre_in.value = ""; variedad_in.value = ""; cantidad_in.value = ""
            cargar_datos()

    def actualizar(id_prod, nuevo_valor):
        supabase.table("stock").update({"cantidad": nuevo_valor}).eq("id", id_prod).execute()
        cargar_datos()

    page.add(
        ft.Text("Inventario en la Nube", size=25, weight="bold"),
        ft.Row([nombre_in, variedad_in]),
        ft.Row([cantidad_in, ft.ElevatedButton("Guardar", icon=ft.icons.CLOUD_UPLOAD, on_click=agregar_click)]),
        ft.Divider(),
        lista_stock
    )
    cargar_datos()

ft.app(target=main)
