import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from local folder"

    def handle(self, *args, **kwargs):
        # 📁 Carpeta donde están las imágenes
        image_folder = "media/movie/images/"

        if not os.path.exists(image_folder):
            self.stderr.write(f"Folder not found: {image_folder}")
            return

        updated_count = 0

        # 🔄 Recorre todas las películas
        for movie in Movie.objects.all():
            # 🧠 Nombre esperado del archivo (ej: Titanic.jpg)
            filename = f"m_{movie.title}.png"
            image_path = os.path.join(image_folder, filename)

            # ✅ Verifica si existe la imagen
            if os.path.exists(image_path):
                # ⚠️ Ajusta según el campo de tu modelo
                movie.image = f"movie/images/{filename}"
                movie.save()

                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} images"))