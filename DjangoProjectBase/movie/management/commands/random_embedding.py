import numpy as np
import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Show embedding of a random movie"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())

        if not movies:
            print("No movies found")
            return

        movie = random.choice(movies)

        if movie.emb:
            emb = np.frombuffer(movie.emb, dtype=np.float32)
            print(f"🎬 {movie.title}")
            print("Embedding (first 10 values):")
            print(emb[:10])
        else:
            print(f"{movie.title} has no embedding")