from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the testapp index.")


def about(request):
    return HttpResponse("You're looking at the testapp about page.")


def contact(request):
    return HttpResponse("You're looking at the test app contact page")


def boolean(request, user_boolean):
    if user_boolean in [0, 1]:
        choice = bool(user_boolean)
    else:
        choice = 'invald'
    return HttpResponse("{0}".format(choice))
