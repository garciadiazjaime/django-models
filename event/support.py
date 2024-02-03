def get_location_rank(metadata):
    rank = 0
    if not metadata:
        return rank

    for key in metadata.keys():
        if metadata[key]:
            rank += 100

    return rank


def get_rank(event):
    rank = 0
    metadata = event.location.metadata
    if metadata:
        if (
            metadata.twitter
            or metadata.facebook
            or metadata.youtube
            or metadata.instagram
            or metadata.tiktok
        ):
            rank += 100

        if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
            rank += 1000

    for artist in event.artists.all():
        metadata = artist.metadata
        if metadata:
            if (
                metadata.twitter
                or metadata.facebook
                or metadata.youtube
                or metadata.instagram
                or metadata.tiktok
            ):
                rank += 100

            if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
                rank += 1000

    return rank
