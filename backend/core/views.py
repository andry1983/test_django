from django.shortcuts import render


def handler403(request, exception):
    context = {
        'exception': str(exception),
    }
    return render(request, '403.jinja2', context=context, status=403)


def handler404(request, exception):
    context = {
        'exception': str(exception),
    }
    return render(request, '404.jinja2', context=context, status=404)


def handler500(request):
    return render(request, '500.jinja2', status=500)
