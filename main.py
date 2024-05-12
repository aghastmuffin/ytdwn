import typer
from pytube import YouTube
from tqdm import tqdm
from typing_extensions import Annotated
from typing import Optional
from os import getcwd
import requests
import pkg_resources
import typer
import os


def check_pytube_version():
    installed_version = pkg_resources.get_distribution("pytube").version
    response = requests.get('https://pypi.org/pypi/pytube/json')
    latest_version = response.json()['info']['version']
    if installed_version != latest_version:
        typer.echo(f"A new version of pytube is available. You have {installed_version}, but the latest is {latest_version}. Please update pytube by running: pip install --upgrade pytube")
        raise typer.Exit()
    try:
        os.system("clear")
    except:
        os.system("cls")
app = typer.Typer()
@app.command()
def addcmd(name: Optional[str] = None):
    if name is None:
        name = "ytdwn"
    with open(f"{getcwd()}/{name}.bat", "w+") as f:
        f.write("@echo off\n")
        f.write(f'py "{os.path.realpath(__file__)}" %*')
    typer.echo(f"Adding this command to CLI. Use it via .\{name}!")
    typer.echo(f"Please also add this to PATH to use it globally.")
@app.command()
def download(url: str, output_path: Annotated[Optional[str], typer.Argument()] = None, hq: bool = typer.Option(False, "--hq", help="Download the video in high quality"), audio: bool = typer.Option(False, "--audio", help="Download the video in audio only")):
    if url.startswith("https://www.youtube.com/"):
        yt = YouTube(url, on_progress_callback=on_progress)
        if hq:
            stream = yt.streams.get_highest_resolution()
        else:
            if audio:
                stream = yt.streams.filter(only_audio=True)[0]
            else:
                stream = yt.streams.filter(file_extension='mp4')[0]
#            else:
#                stream = yt.streams.filter(file_extension='mp4', only_video=True)[0]
        file_size = stream.filesize
        if output_path is None:
            output_path = f"{getcwd()}/{yt.title}.mp4"
        typer.echo(f"Downloading {url} to {output_path}")
        global pbar
        with tqdm(total=100, unit='%', desc="Downloading") as pbar:
            stream.download(output_path)
        typer.echo(f"Downloaded {url} to {output_path}. Program exiting")
    else:
        typer.echo("Invalid URL! Please enter a valid YouTube URL.")
        typer.echo("Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
def on_progress(stream, chunk, bytes_remaining):
    current = stream.filesize - bytes_remaining
    percent = (current / stream.filesize) * 100
    pbar.update(percent)
if __name__ == "__main__":
    check_pytube_version()
    app()
    
