from django.conf import settings
from post_office import mail
from post_office.models import Email, EmailTemplate


def introduction_email(to_email, first_name):
    """Send an introduction email to an email address
    This email should only be sent once. We check if we have sent the
    email based upon the subject. If the template changes subject
    we will need to change how we check this.
    """

    # If the template subject changes id we need to alter this check. We use the subject as the
    # check as it doesn't store the `EmailTemplate` used on the created `Email` instance unless
    # it is rendered upon sending.
    template = EmailTemplate.objects.get(name='introduction_email')
    if Email.objects.filter(
        to=to_email,
        subject=template.subject,
    ).exists():
        return

    # As `post_office` automatically queues emails we might want it to generate but not queue. To
    #  do this we can not commit the email instance and change the status to `None` which will
    # create it but do nothing around the queue.
    automatically_send_email = settings.SYDJANGO.get('AUTO_SEND_EMAIL', False)

    email = mail.send(
        [to_email, ],
        'me@stuartdines.com',
        template=template,
        context={
            'name': first_name,
        },
        commit=automatically_send_email,
    )
    if not automatically_send_email:
        email.status = None
        email.save()
    return email
