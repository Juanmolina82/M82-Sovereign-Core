from time import sleep
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

console = Console()


def make_portfolio_table():
    table = Table(title="Caribe – Venezuela Portfolio")
    table.add_column("Ticker", style="cyan", no_wrap=True)
    table.add_column("Sector", style="magenta")
    table.add_column("Weight %", justify="right", style="green")
    table.add_column("View", style="yellow")

    positions = [
        ("PDVSA", "Energy", "25.0", "Overweight"),
        ("VENZ 2027", "Sov. Debt", "20.0", "Core"),
        ("USD.CASH", "Cash", "15.0", "Dry powder"),
        ("COPP", "Metals", "10.0", "Tactical"),
        ("CARIBE_EQ", "Equity", "30.0", "Growth"),
    ]

    for t, s, w, v in positions:
        table.add_row(t, s, w, v)

    return table


def make_ticker():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"[bold yellow]{now}[/bold yellow]")
    lines.append("[green]Oil spreads tighten vs WTI.[/green]")
    lines.append("[cyan]FX: VEF remains structurally weak.[/cyan]")
    lines.append("[magenta]Flows: local banks add duration.[/magenta]")
    return "
".join(lines)


def make_audit_block():
    lines = []
    lines.append("[bold]QUANT AUDIT[/bold]")
    lines.append("[green]VaR within limits.[/green]")
    lines.append("[green]Liquidity OK.[/green]")
    lines.append("[yellow]Concentration: Energy 55%.[/yellow]")
    lines.append("[red]Stress +300bps shock = -7.2%.[/red]")
    return "
".join(lines)


def make_layout():
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right", size=40),
    )

    layout["left"].update(
        Panel(make_portfolio_table(), border_style="cyan")
    )

    layout["right"].split(
        Layout(name="ticker"),
        Layout(name="audit"),
    )

    layout["ticker"].update(
        Panel(make_ticker(), title="LIVE TICKER", border_style="yellow")
    )

    layout["audit"].update(
        Panel(make_audit_block(), title="RISK ENGINE", border_style="red")
    )

    layout["header"].update(
        Panel(
            "[bold cyan]MOLINA AI PLATFORM[/bold cyan] | Termux TUI demo",
            border_style="blue",
        )
    )

    layout["footer"].update(
        Panel(
            "[bold]Ctrl+C[/bold] to quit | demo refresh...",
            border_style="green",
        )
    )

    return layout


def main():
    with Live(
        make_layout(),
        console=console,
        screen=True,
        refresh_per_second=2,
    ):
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
