from django.core.mail import EmailMultiAlternatives


class PasswordReset:
    def send_email(self, email, title, content):
        email = EmailMultiAlternatives(
            title,
            content,
            'noreply@pyxilink.com',
            [email],
        )
        email.attach_alternative(content, "text/html")
        email.send()
