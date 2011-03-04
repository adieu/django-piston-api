from django.utils.datastructures import SortedDict


class RegisterError(Exception):
    pass

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class APIHandler(object):
    """
    An APIHandler object holds registered api resources that could be used in
    Piston.
    """

    def __init__(self, name=None, app_name='api'):
        self._registry = SortedDict() # model_class class -> admin_class instance
        self.root_path = None
        if name is None:
            self.name = 'api'
        else:
            self.name = name
        self.app_name = app_name

    def register(self, urlpattern, resource, name=None):
        if not name:
            if not resource.handler.model:
                raise RegisterError('name should not be None')
            name = resource.handler.model._meta.object_name
        if name in self._registry:
            raise AlreadyRegistered('API %s has already been registered' % name)
        self._registry[name] = {'urlpattern': urlpattern, 'resource': resource}

    def unregister(self, name):
        """
        Unregisters the given name.

        If an api isn't already registered, this will raise NotRegistered.
        """
        if name not in self._registry:
            raise NotRegistered('The resource %s is not registered' % name)
        del self._registry[name]

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        # Admin-site-wide views.
        urlpatterns = patterns('')
        
        for name, item in self._registry.iteritems():
            urlpatterns += patterns('',
                url(item['urlpattern'], item['resource'], name=name)
            )

        return urlpatterns

    def urls(self):
        return self.get_urls(), self.app_name, self.name
    urls = property(urls)


handler = APIHandler()
