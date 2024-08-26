from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
import telebot
from config import API_TOKEN_BOT
from news.models import Publication, Category, PublicationComment, SocialNetwork, Address, ContactUs

bot = telebot.TeleBot(API_TOKEN_BOT)
LOID = 7065054223


class HomeView(TemplateView):
    model = Publication
    template_name = 'index.html'

    def get_context_data(self):
        publications = Publication.objects.filter(is_active=True)
        input_query = self.request.GET.get("query", "")
        category_pk = self.request.GET.get("category_pk", "")
        if category_pk:
            publications = publications.filter(category_id=category_pk)

        if input_query:
            publications = publications.filter(
                Q(title__icontains=input_query) |
                Q(description__icontains=input_query) |
                Q(short_description__icontains=input_query)
            )
        paginator = Paginator(publications, 2)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "input_query": input_query,
            "page_obj": page_obj,
            "paginator": paginator,
        }
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = {
            'social': SocialNetwork.objects.first(),
            'address': Address.objects.first()
        }
        return context

    def post(self, request):
        input_name = request.POST["name"]
        input_email = request.POST["email"]
        input_subject = request.POST["subject"]
        input_message = request.POST["message"]
        ContactUs.objects.create(name=input_name, email=input_email, subject=input_subject, message=input_message)
        bot.send_message(LOID, F"Новое сообщение от пользователя:\n Имя: {input_name},\n email: {input_email}, \n\n {input_subject}, \n\n {input_message}")
        context = {
            'social': SocialNetwork.objects.first(),
            'address': Address.objects.first()
        }
        return render(request, 'contact.html', context)


class PublicationDetailView(TemplateView):
    template_name = 'publication-detail.html'

    def get_context_data(self, **kwargs):
        publication_pk = kwargs['pk']

        context = {
            'publication': Publication.objects.get(id=publication_pk),
            'categories': Category.objects.all()
        }
        return context

    def post(self, request, **kwargs):
        publication_pk = kwargs['pk']
        input_name = request.POST["name"]
        input_text = request.POST["message"]
        publication = Publication.objects.get(id=publication_pk)
        context = {
            'publication': Publication.objects.get(id=publication_pk),
            'categories': Category.objects.all()
        }
        PublicationComment.objects.create(name=input_name, text=input_text, publication=publication)
        bot.send_message(LOID, F"К вашему публикацию {publication.title} написали комментарий\n имя: {input_name}\n Комментарий: {input_text}")

        return render(request, "publication-detail.html", context=context)
