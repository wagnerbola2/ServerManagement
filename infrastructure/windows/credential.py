import win32security
import win32con

class credential():
    @staticmethod
    def GenerateCredential(user, password, server_domain):
        return win32security.LogonUser(
            user,
            server_domain,
            password,
            win32con.LOGON32_LOGON_NEW_CREDENTIALS,
            win32con.LOGON32_PROVIDER_DEFAULT
        )