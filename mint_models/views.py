from django.http import HttpResponse


def challenge(request, code):
    return HttpResponse(f"{code}.KY_NNECSQw1GMrXHsW-uij1aTpIesmtDVTbaktJBZss")
