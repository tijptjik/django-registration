from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationFormInstitutional

from mycroft.base.models import Institution

class InstitutionalBackend(object):
    def register(self, request, **kwargs):
        print request.POST
        print
        print request.POST['institution']
        print
        print kwargs
        institution = request.POST['institution']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password1']
        
        try:
            User.objects.get(email__iexact=email)
            return User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)

            new_user = User.objects.create_user(username, email, password)
            print new_user
            new_user.is_active = True
            print new_user
            new_user.first_name = first_name
            print new_user
            new_user.last_name = last_name
            print new_user
            new_user.save()
            print 'GOT THERE'

            signals.user_registered.send(sender=self.__class__,
                                         user=new_user,
                                         request=request)

            try:
                Institution.objects.get(name__iexact=institution)
                raise NotImplementedError
            except Institution.DoesNotExist:
                Institution.objects.create_insitution(institution, new_user)
            return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.
        
        """
        return RegistrationFormInstitutional
