from django.shortcuts import redirect


class RedirectToLoginMixin:
    def handle_exception(self, exc):
        return redirect('login')
