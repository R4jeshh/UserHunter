import os
import requests
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.progress import track
from time import sleep

# Console Setup
console = Console()

# Tool Header
def display_header():
    os.system("clear")
    header = """
[bold cyan]
  _   _                 _   _             _            
 | | | |___  ___ _ __  | | | |_   _ _ __ | |_ ___ _ __ 
 | | | / __|/ _ \ '__| | |_| | | | | '_ \| __/ _ \ '__|
 | |_| \__ \  __/ |    |  _  | |_| | | | | ||  __/ |   
  \___/|___/\___|_|    |_| |_|\__,_|_| |_|\__\___|_|   

[bold yellow]Username Availability Checker - 50+ Popular Platforms[/bold yellow]
[bold green]Developed By: [bold red]@ImR4jesh[/bold red]
"""
    console.print(header)

# Popular Platforms List
def get_platforms(username):
    return {
        "Instagram": f"https://www.instagram.com/{username}/",
        "YouTube": f"https://www.youtube.com/{username}",
        "Telegram": f"https://t.me/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Snapchat": f"https://story.snapchat.com/u/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "StackOverflow": f"https://stackoverflow.com/users/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "WordPress": f"https://{username}.wordpress.com",
        "Blogger": f"https://{username}.blogspot.com",
        "Quora": f"https://www.quora.com/profile/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
    }

# Check Username on a Single Platform
def check_platform(username, platform, url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return platform, "[bold red]Taken[/bold red]"
        elif response.status_code == 404:
            return platform, "[bold green]Available[/bold green]"
        else:
            return platform, "[bold yellow]Unknown[/bold yellow]"
    except requests.exceptions.RequestException:
        return platform, "[bold magenta]Error[/bold magenta]"

# Multi-Threaded Search
def search_username(username):
    platforms = get_platforms(username)
    results = []

    console.print(f"[bold cyan]Searching '{username}' on {len(platforms)} platforms...[/bold cyan]\n")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(check_platform, username, platform, url)
            for platform, url in platforms.items()
        ]
        for future in track(futures, description="[bold yellow]Scanning platforms...[/bold yellow]"):
            results.append(future.result())

    # Display Results
    table = Table(title="Username Search Results", style="cyan")
    table.add_column("Platform", justify="left", style="green")
    table.add_column("Status", justify="center", style="magenta")
    for platform, status in results:
        table.add_row(platform, status)
    console.print(table)

# Tool Lock Mechanism
def show_startup_message():
    console.print("[bold green]Redirecting to Telegram Channel...[/bold green]")
    sleep(3)
    os.system("termux-open-url https://t.me/R4jeshh")

# Main Function
def main():
    display_header()
    if not os.path.exists(".channel_opened"):
        show_startup_message()
        with open(".channel_opened", "w") as file:
            file.write("Telegram channel visited.")
    display_header()  # Re-display after returning from the Telegram Channel

    while True:
        username = console.input("[bold yellow]Enter a username to search: [/bold yellow]").strip()
        if not username:
            console.print("[bold red]Please enter a valid username![/bold red]")
            continue

        search_username(username)
        retry = console.input("\n[bold cyan]Do you want to search again? (y/n): [/bold cyan]").strip().lower()
        if retry != 'y':
            break
    console.print("\n[bold green]Thank you for using the tool![/bold green]")

# Entry Point
if __name__ == "__main__":
    os.system("clear")
    main()
