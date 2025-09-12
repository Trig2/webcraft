from django.shortcuts import render

def chat_widget(request):
    return render(request, 'chat/widget.html')
