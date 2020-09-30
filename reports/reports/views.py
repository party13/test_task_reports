from django.shortcuts import redirect


def redirect_index(request):
    return redirect('index_page', permanent=True)