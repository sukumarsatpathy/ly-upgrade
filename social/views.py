from django.shortcuts import render


def feedsView(request):
    context = {}
    return render(request, 'fe/social/feeds.html', context)