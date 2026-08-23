from config.settings import settings
from config.servers_settings import config_servers
from infrastructure.windows.windows_repository import windowsRepository
from interfaces.cli.views import view
from domain.emun import Options

def main():
    servers = config_servers.list()
    server_selected = view.SelectServers(servers)

    repository = windowsRepository(
       host=server_selected.host,
       user=settings.server_user,
       server_domain=settings.server_domain,
       password=settings.server_password
    )

    totvs_services = repository.getServices()
    view.ShowServices(totvs_services)
    option = view.SelectOptions()

    match option:
        case Options.START_SERVICE:
            print("Inicia serviço")
        case Options.STOP_SERVICE:
            print("Para serviço")
        case Options.RESTART_SERVICE:
            print("Reiniciar serviço")
        case Options.START_ALL_SERVICES:
            print("Iniciar Todos serviço")
        case Options.STOP_ALL_SERVICES:
            print("Para Todos serviço")
        case Options.RESTART_ALL_SERVICES:
            print("Reinicia Todos serviço")
        case Options.EXIT:
            print("Sair")

    view.waitEnd()
    view.Clean(False)

if __name__ == "__main__":
    main()