import os
import numpy as np
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie

# cargar API key
load_dotenv('../openAI.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recommend_view(request):
    best_movie = None
    similarity = None

    if request.method == "POST":
        prompt = request.POST.get("prompt")

        # embedding del prompt
        response = client.embeddings.create(
            input=[prompt],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

        max_similarity = -1

        for movie in Movie.objects.all():
            if movie.emb:
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)

                # ⚠️ evitar error de dimensiones
                if len(prompt_emb) != len(movie_emb):
                    continue

                sim = cosine_similarity(prompt_emb, movie_emb)

                if sim > max_similarity:
                    max_similarity = sim
                    best_movie = movie

        similarity = max_similarity

    return render(request, "recommend.html", {
        "movie": best_movie,
        "similarity": similarity
    })