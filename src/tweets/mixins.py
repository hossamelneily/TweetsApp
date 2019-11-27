from django.utils.http import is_safe_url
class NextUrlMixin(object):
    def get_next_url(self):
        next_ = self.request.GET.get("next")
        next_post = self.request.POST.get("next")
        redirected_path = next_ or next_post or None
        print(redirected_path)
        if is_safe_url(redirected_path, self.request.get_host()):
            return redirected_path     # we changed the return to be the path only