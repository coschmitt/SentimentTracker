from django.shortcuts import redirect


def transfer_view(request):
    return redirect('/tweets/')
