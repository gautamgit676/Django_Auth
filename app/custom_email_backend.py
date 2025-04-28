# app/custom_email_backend.py

from django.core.mail.backends.smtp import EmailBackend
import ssl
import certifi

class CustomEmailBackend(EmailBackend):
    def _get_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        return ssl_context

    def open(self):
        """
        Ensure we have a connection to the email server.
        """
        if self.connection:
            return False

        # Set up the connection
        self.connection = self.connection_class(
            host=self.host,
            port=self.port,
            timeout=self.timeout,
       
        )

        # Secure the connection with TLS if required
        if self.use_tls:
            self.connection.starttls(context=self._get_ssl_context())

        # Log in to the SMTP server if username and password are set
        if self.username and self.password:
            self.connection.login(self.username, self.password)

        return True
