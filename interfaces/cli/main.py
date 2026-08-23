from config.settings import settings
from config.servers_settings import config_servers
from infrastructure.windows.windows_repository import windowsRepository
from interfaces.cli.views import view
from domain.emun import Options
import win32service

def main():
    servers = config_servers.list()
    server_selected = view.SelectServers(servers)

    if not server_selected:
        return

    repository = windowsRepository(
       host=server_selected.host,
       user=settings.server_user,
       server_domain=settings.server_domain,
       password=settings.server_password
    )

    totvs_services = repository.getServices(settings.services_filter)
    view.ShowServices(totvs_services)

    option = None
    while option != Options.EXIT:
        option = view.SelectOptions()
        match option:
            case Options.START_SERVICE:
                service = view.SelectService(totvs_services, win32service.SERVICE_STOPPED)
                if service:
                    repository.startStopService(service, Options.START_SERVICE)
                totvs_services = repository.getServices(settings.services_filter)
                view.ShowServices(totvs_services)
            case Options.STOP_SERVICE:
                service = view.SelectService(totvs_services, win32service.SERVICE_RUNNING)
                if service:
                    repository.startStopService(service, Options.STOP_SERVICE)                   
                totvs_services = repository.getServices(settings.services_filter)
                view.ShowServices(totvs_services)
            case Options.RESTART_SERVICE:
                service = view.SelectService(totvs_services, None)
                if service:
                    repository.startStopService(service, Options.STOP_SERVICE)
                    print("\n")
                    repository.startStopService(service, Options.START_SERVICE)
                totvs_services = repository.getServices(settings.services_filter)
                view.ShowServices(totvs_services)
            case Options.START_ALL_SERVICES:
                print("Iniciar Todos serviço")
            case Options.STOP_ALL_SERVICES:
                print("Para Todos serviço")
            case Options.RESTART_ALL_SERVICES:
                print("Reinicia Todos serviço")
            case Options.CHANGE_SERVER:
                server_selected = view.SelectServers(servers)
                if not server_selected:
                    continue
                repository.host = server_selected.host
                totvs_services = repository.getServices(settings.services_filter)
                view.ShowServices(totvs_services)
            case Options.EXIT:
                pass

if __name__ == "__main__":
    main()
    view.waitEnd()
    view.Clean(False)