import time
import win32security
import win32service
import win32serviceutil
from infrastructure.windows.credential import credential
from domain.emun import Options

class windowsRepository():
    def __init__(self, host, user, server_domain, password):
        self.host = host
        self.user = user
        self.server_domain = server_domain
        self.password = password

    def getServices(self, filter=""):
        windows_credential = credential.GenerateCredential(user=self.user, server_domain=self.server_domain,password=self.password)
        win32security.ImpersonateLoggedOnUser(windows_credential)
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
            like_filter = filter
            return tuple(
                service for service in services
                if like_filter in service["ServiceName"].lower()
            )

        finally:
            if scm_handle:
                win32service.CloseServiceHandle(scm_handle)

            win32security.RevertToSelf()
            windows_credential.Close()

    def startStopService(self, service, option: Options):
        windows_credential = credential.GenerateCredential(user=self.user, server_domain=self.server_domain,password=self.password)
        win32security.ImpersonateLoggedOnUser(windows_credential)
        service_status = None
        match option:
            case Options.START_SERVICE:
                service_status = win32service.SERVICE_RUNNING
            case Options.STOP_SERVICE:
                service_status = win32service.SERVICE_STOPPED
        try:
            status = win32serviceutil.QueryServiceStatus(service["ServiceName"], machine=self.host)
            if status[1] != service_status:
                match option:
                    case Options.START_SERVICE:
                        win32serviceutil.StartService(service["ServiceName"], machine=self.host)
                        print("Aguardando a inicialização completa do serviço...", end="")
                    case Options.STOP_SERVICE:
                        win32serviceutil.StopService(service["ServiceName"], machine=self.host)
                        print("Aguardando a finalização completa do serviço...", end="")

                while status[1] != service_status:
                    time.sleep(1)
                    print(".", end="", flush=True)
                    status = win32serviceutil.QueryServiceStatus(service["ServiceName"], machine=self.host)
        except:
            print("An exception occurred") 
        finally:
            win32security.RevertToSelf()
            windows_credential.Close()

