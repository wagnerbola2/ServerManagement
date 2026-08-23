import os
import subprocess
import inquirer
import win32service
from tabulate import tabulate
from domain.emun import Options
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

class view():

    @staticmethod
    def PutHeader():
        console = Console()

        # Cabeçalho com alinhamento perfeito automático
        header_text = "[bold green]SERVER MANAGEMENT[/bold green]\n[dim text]Painel de Controle do Sistema[/dim text]\n\n[cyan]Status:[/cyan] [bold blink green]ONLINE[/bold blink green]  |  [cyan]Host:[/cyan] 127.0.0.1  |  [cyan]Porta:[/cyan] 8080"

        # O Painel (Panel) cria a moldura perfeita ao redor do texto
        console.print(
            Panel(
                Align.center(header_text),
                border_style="bright_blue",
                title="[bold white]SYS-ADMIN[/bold white]",
                subtitle="[dim]v1.0.0[/dim]"
            )
        )

    @staticmethod
    def Clean(header=True):
        comando = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run(comando, shell=True)
        if header:
            view.PutHeader()

    @staticmethod
    def SelectServers(servers):
        view.Clean()
        formatted_choices = [
            (f"{server.name}", server) 
            for server in servers
        ]
        questions = [
            inquirer.List(
                'server',
                message="Selecione o servidor que seja usar",
                choices=formatted_choices,
            ),
        ]
        return inquirer.prompt(questions)["server"]

    @staticmethod
    def ShowServices(services):
        view.Clean()
        headres = ["Nome", "Descrição", "Status"]
        map_status = {
            win32service.SERVICE_STOPPED: "Parado",
            win32service.SERVICE_RUNNING: "Executando",
        }
        parsed_services = [
            [
                service["ServiceName"], 
                service["DisplayName"], 
                map_status.get(service["CurrentState"], service["CurrentState"])
            ]
            for service in services
        ]
        sorted_services  = sorted(parsed_services, key=lambda x: x[1])
        print(tabulate(sorted_services, headers=headres, tablefmt="grid"))

    @staticmethod
    def SelectOptions():
        options = [
            ("Iniciar Serviço", Options.START_SERVICE),
            ("Parar Serviço", Options.STOP_SERVICE),
            ("Reiniciar Serviço", Options.RESTART_SERVICE),
            ("Iniciar Todos os Serviços", Options.START_ALL_SERVICES),
            ("Parar Todos os Serviços", Options.STOP_ALL_SERVICES),
            ("Reiniciar Todos os Serviços", Options.RESTART_ALL_SERVICES),
            ("Sair", Options.EXIT),
        ]
        questions = [
            inquirer.List(
                'option',
                message="Selecione uma Opção",
                choices=options,
            ),
        ]
        return inquirer.prompt(questions)["option"]

    @staticmethod
    def waitEnd():
        input("Pressione ENTER para continuar")
