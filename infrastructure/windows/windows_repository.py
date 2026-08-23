import win32security
import win32service
from infrastructure.windows.credential import credential

class windowsRepository():
    def __init__(self, host, user, server_domain, password):
        self.host = host
        self.windows_credential = credential.GenerateCredential(user=user, server_domain= server_domain,password=password)

    def getServices(self):
        win32security.ImpersonateLoggedOnUser(self.windows_credential)
        scm_handle = None
        try:
            # 3. Conecta ao SCM do servidor REMOTO passando o nome/IP dele
            scm_handle = win32service.OpenSCManager(
                self.host,
                None,
                win32service.SC_MANAGER_ENUMERATE_SERVICE
            )
        
            # 4. Enumera os serviços no servidor alvo
            tipo_servico = win32service.SERVICE_WIN32
            estado_servico = win32service.SERVICE_STATE_ALL
            services = win32service.EnumServicesStatusEx(
                scm_handle, 
                tipo_servico, 
                estado_servico, 
                None
            )
            like_filter = "totvs"
            return tuple(
                service for service in services
                if like_filter in service["ServiceName"].lower()
            )

        finally:
            if scm_handle:
                win32service.CloseServiceHandle(scm_handle)

            win32security.RevertToSelf()
            # Fecha o token de segurança para evitar vazamento de memória
            self.windows_credential.Close()
        