import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

class NasaAPI:
    def __init__(self, query): 
        self.url = "https://images-api.nasa.gov/search"
        self.query = query
        self.params = {'q': self.query}

    def fetch_data(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Nie udało się pobrać pliku: {response.status_code}')

    def get_images(self):
        data = self.fetch_data()
        return data.get("collection", {}).get("items", [])


class NasaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NASA Wyszukiwarka")
        self.root.configure(bg="black")

        self.left_frame = tk.Frame(root, bg="black")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root, bg="black")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.query_entry = tk.Entry(self.left_frame, bg="black", fg="green", insertbackground="green")
        self.query_entry.pack(padx=10, pady=10)
        self.query_entry.bind("<Return>", lambda event: self.search_images())

        self.search_button = tk.Button(self.left_frame, text="Szukaj", command=self.search_images, bg="black", fg="green")
        self.search_button.pack(pady=5)

        self.image_listbox = tk.Listbox(self.left_frame, bg="black", fg="green")
        self.image_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.image_listbox.bind("<<ListboxSelect>>", self.show_image)

        self.image_label = tk.Label(self.right_frame, bg="black")
        self.image_label.pack(padx=10, pady=10)

        self.image_urls = []

    def search_images(self):
        query = self.query_entry.get()
        if not query:
            return

        self.image_listbox.delete(0, tk.END)
        self.image_urls.clear()

        try:
            api = NasaAPI(query)
            items = api.get_images()
            for item in items:
                title = item.get("data", [{}])[0].get("title", "Brak tytułu")
                link = item.get("links", [{}])[0].get("href", "")
                self.image_listbox.insert(tk.END, title)
                self.image_urls.append(link)
        except Exception as e:
            self.image_listbox.insert(tk.END, f"Błąd: {e}")

    def show_image(self, event):
        selection = event.widget.curselection()
        if not selection:
            return

        index = selection[0]
        url = self.image_urls[index]

        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_data = response.content
                image = Image.open(io.BytesIO(img_data))
                image = image.resize((500, 500))
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
        except Exception as e:
            self.image_listbox.insert(tk.END, f"Błąd obrazu: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NasaApp(root)
    root.mainloop()