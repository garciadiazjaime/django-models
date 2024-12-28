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
    print("post_save", instance, created)
    if created:
        print("==== Event Created ==== " + instance.provider)

        same_meta = GenerativeMetadata.objects.filter(
            event__name=instance.name,
            event__venue=instance.venue,
            event__description=instance.description,
        )
        if same_meta.count():
            print("==== Same Meta Event Found ====")
            GenerativeMetadata.objects.update_or_create(
                event=instance,
                type=same_meta.first().type,
                genre=same_meta.first().genre,
                subgenre=same_meta.first().subgenre,
            )
            return

        query = f'return a csv only including type of event, genre and one subgenre for the chicago event titled: "{instance.name}" at the venue: "{instance.venue}"'
        if instance.description:
            query += f' with description: "{instance.description}"'
        print(query)

        response = None
        try:
            response = model.generate_content(query)

        except Exception as e:
            print(e)

        if not response:
            return

        print(response.text)
        even_type, genre, subgenre = response.text.split("\n")[2].split(",")

        invalid_sub_genres = ["Unspecified", "???"]

        print("==== New Meta Event Created ====")
        GenerativeMetadata.objects.update_or_create(
            event=instance,
            type=even_type,
            genre=genre,
            subgenre=None if subgenre in invalid_sub_genres else subgenre,
        )
