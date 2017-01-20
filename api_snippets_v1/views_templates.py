from django.conf import settings
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['version'] = settings.VERSION
        context['is_debug'] = settings.DEBUG
        context['is_prod'] = (settings.BUILD == 'prod')
        context['is_staging'] = (settings.BUILD == 'staging')
        context['is_dev'] = (settings.BUILD == 'dev')
        return context
