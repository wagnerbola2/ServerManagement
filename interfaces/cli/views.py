import os
import subprocess
import inquirer
import win32service
from tabulate import tabulate
from domain.emun import Options
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import colorama
from colorama import Fore, Style

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
        console.print("\n")

    @staticmethod
    def Clean(header=True):
        comando = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run(comando, shell=True)
        if header:
            view.PutHeader()
        colorama.init() 

    @staticmethod
    def SelectServers(servers):
        view.Clean()
        formatted_choices = [
            (f"{server.name}", server) 
            for server in servers
        ]
        formatted_choices.append(
            ("Sair", {})
        )
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
        highlight_data = []
        for linha in sorted_services:
            if linha[2] == "Parado":
                highlight_data.append(view.highlight_line(linha, Fore.RED))
            else:
                highlight_data.append(linha)
        print(tabulate(highlight_data, headers=headres, tablefmt="grid"))
        print("\n")

    @staticmethod
    def highlight_line(linha: list, cor: str) -> list:
        """Aplica cor ANSI em cada célula da linha, mantendo o reset no final"""
        return [f"{cor}{str(celula)}{Style.RESET_ALL}" for celula in linha]

    @staticmethod
    def SelectOptions():
        options = [
            ("Iniciar Serviço", Options.START_SERVICE),
            ("Parar Serviço", Options.STOP_SERVICE),
            ("Reiniciar Serviço", Options.RESTART_SERVICE),
            # ("Iniciar Todos os Serviços", Options.START_ALL_SERVICES),
            # ("Parar Todos os Serviços", Options.STOP_ALL_SERVICES),
            # ("Reiniciar Todos os Serviços", Options.RESTART_ALL_SERVICES),
            ("Trocar de Servidor", Options.CHANGE_SERVER),
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
    def SelectService(services, win32serviceState = None):
        view.Clean()
        formatted_choices = []
        sorted_services  = sorted(services, key=lambda x: x["DisplayName"])
        for index, service in enumerate(sorted_services):
            if (not win32serviceState or service["CurrentState"] == win32serviceState) and "license" not in service["ServiceName"]:
                formatted_choices.append(
                    (f"{service["DisplayName"]}", service)
                )
        formatted_choices.append(
                    ("Cancelar", {})
        )
        questions = [
            inquirer.List(
                'server',
                message="Selecione o servidor que seja usar",
                choices=formatted_choices,
            ),
        ]
        return inquirer.prompt(questions)["server"]

    @staticmethod
    def waitEnd():
        print("\n")
        input("Pressione ENTER para finalizar...")
