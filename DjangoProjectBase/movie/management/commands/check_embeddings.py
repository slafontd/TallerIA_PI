import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Check stored embeddings"

    def handle(self, *args, **kwargs):
        for movie in Movie.objects.all():
            if movie.emb:
                embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
                print(movie.title, embedding_vector[:5])
            else:
                print(movie.title, "No embedding")