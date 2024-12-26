import environ

import google.generativeai as genai
from django.db.models.signals import post_save
from django.dispatch import receiver

from event.models import Event
from event.models import GenerativeMetadata

env = environ.Env()

genai.configure(api_key=env("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


@receiver(post_save, sender=Event)
def update_genre(sender, instance, created, **kwargs):
    if created:
        query = (
            "return a csv only including type of event, genre and one subgenre for the chicago event titled: "
            + instance.name
            + " at the venue: "
            + instance.venue
        )
        if instance.description:
            query += " with description: " + instance.description
        print(query)
        response = model.generate_content(query)

        print(response.text)
        even_type, genre, subgenre = response.text.split("\n")[2].split(",")

        GenerativeMetadata.objects.update_or_create(
            event=instance,
            type=even_type,
            genre=genre,
            subgenre=subgenre,
        )
