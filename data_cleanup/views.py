from django.views.generic import TemplateView


class DataCleaUpView(TemplateView):
    template_name = "data_cleanup/filter.html"