import random
import secrets
import hashlib
import uuid
import os
import pathlib
import json
import datetime
import time
import re
import ipaddress
import socket
import base64


def pause():
    input("\nPress Enter to continue...")


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")


def header(title):
    clear()
    print("=" * 50)
    print(f" {title}")
    print("=" * 50)


def ask_again(prompt):
    while True:
        answer = input(f"\n{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def run_repeated(action, prompt):
    while True:
        action()
        if not ask_again(prompt):
            return



def random_number():
    header("Random Number")
    try:
        minimum = int(input("Minimum: "))
        maximum = int(input("Maximum: "))
        if minimum > maximum:
            minimum, maximum = maximum, minimum
    except ValueError:
        print("Please enter valid integers.")
        pause()
        return

    def roll():
        print(f"\nRandom number: {random.randint(minimum, maximum)}")

    run_repeated(roll, "Reroll using the same range?")


def dice_roller():
    header("Dice Roller")
    text = input("Dice (example: 2d6): ").lower().replace(" ", "")
    match = re.fullmatch(r"(\d*)d(\d+)", text)

    if not match:
        print("Invalid format. Example: 2d6")
        pause()
        return

    amount = int(match.group(1) or 1)
    sides = int(match.group(2))

    if amount <= 0 or sides <= 0:
        print("Dice count and sides must be positive.")
        pause()
        return

    def roll():
        rolls = [random.randint(1, sides) for _ in range(amount)]
        print("\nRolls:", rolls)
        print("Total:", sum(rolls))

    run_repeated(roll, "Roll the same dice again?")


def coin_flip():
    header("Coin Flip")

    def flip():
        print("\nResult:", random.choice(["Heads", "Tails"]))

    run_repeated(flip, "Flip again?")


def random_choice():
    header("Random Choice")
    text = input("Enter choices separated by commas:\n> ")
    choices = [item.strip() for item in text.split(",") if item.strip()]

    if not choices:
        print("No choices provided.")
        pause()
        return

    def choose():
        print("\nSelected:", random.choice(choices))

    run_repeated(choose, "Choose again from the same list?")


def password_generator():
    header("Password Generator")
    try:
        length = int(input("Password length: "))
        if length <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive whole number.")
        pause()
        return

    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()-_=+"
    )

    def generate():
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        print("\nPassword:")
        print(password)

    run_repeated(generate, "Generate another password with the same length?")


def uuid_generator():
    header("UUID Generator")

    def generate():
        print("\n", uuid.uuid4())

    run_repeated(generate, "Generate another UUID?")


def percentage_calculator():
    header("Percentage Calculator")
    try:
        value = float(input("Value: "))
        percentage = float(input("Percentage: "))
    except ValueError:
        print("Invalid number.")
        pause()
        return

    def calculate():
        result = value * percentage / 100
        print(f"\n{percentage}% of {value} = {result}")

    calculate()


def prime_checker():
    header("Prime Checker")
    try:
        number = int(input("Number: "))
    except ValueError:
        print("Invalid integer.")
        pause()
        return

    def check():
        if number < 2:
            print("Not prime.")
            return
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                print("Not prime.")
                return
        print("Prime!")

    check()



def text_counter():
    header("Text Counter")
    text = input("Enter text:\n> ")

    def count():
        print("\nWords:", len(text.split()))
        print("Characters:", len(text))
        print("Lines:", len(text.splitlines()) or 1)

    count()


def case_converter():
    header("Case Converter")
    text = input("Text:\n> ")
    print("\n1. UPPERCASE")
    print("2. lowercase")
    print("3. Title Case")
    print("4. Swap Case")

    choice = input("\nChoice: ").strip()
    converters = {
        "1": str.upper,
        "2": str.lower,
        "3": str.title,
        "4": str.swapcase,
    }

    if choice not in converters:
        print("Invalid choice.")
        pause()
        return

    def convert():
        print("\n" + converters[choice](text))

    convert()


def base64_tool():
    header("Base64 Encoder / Decoder")
    print("1. Encode")
    print("2. Decode")
    choice = input("\nChoice: ").strip()
    text = input("Text: ")

    if choice not in ("1", "2"):
        print("Invalid choice.")
        pause()
        return

    def convert():
        try:
            if choice == "1":
                result = base64.b64encode(text.encode("utf-8")).decode("ascii")
                print("\nEncoded:", result)
            else:
                result = base64.b64decode(text, validate=True).decode("utf-8")
                print("\nDecoded:", result)
        except (ValueError, UnicodeDecodeError):
            print("Could not decode input. Check that it is valid Base64 UTF-8 text.")

    convert()


def json_formatter():
    header("JSON Formatter")
    text = input("Paste JSON:\n")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        print("Invalid JSON:")
        print(error)
        pause()
        return

    def format_json():
        print("\nFormatted JSON:\n")
        print(json.dumps(data, indent=4, ensure_ascii=False))

    format_json()



def file_hash():
    header("SHA-256 File Hash")
    path = input("File path: ").strip().strip('"')

    if not os.path.isfile(path):
        print("File does not exist.")
        pause()
        return

    def hash_file():
        sha256 = hashlib.sha256()
        try:
            with open(path, "rb") as file:
                for chunk in iter(lambda: file.read(8192), b""):
                    sha256.update(chunk)
            print("\nSHA-256:")
            print(sha256.hexdigest())
        except OSError as error:
            print("Error:", error)

    hash_file()


def format_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def folder_stats():
    header("Folder Statistics")
    path = input("Folder path: ").strip().strip('"')

    if not os.path.isdir(path):
        print("Folder does not exist.")
        pause()
        return

    def show_stats():
        total_files = 0
        total_size = 0
        extensions = {}

        for root, _, files in os.walk(path):
            for filename in files:
                full_path = os.path.join(root, filename)
                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    continue

                total_files += 1
                total_size += size
                extension = pathlib.Path(filename).suffix.lower() or "[no extension]"
                extensions[extension] = extensions.get(extension, 0) + 1

        print("\nFiles:", total_files)
        print("Total size:", format_bytes(total_size))
        print("\nExtensions:")
        for extension, count in sorted(extensions.items()):
            print(f"  {extension}: {count}")

    show_stats()


def file_organizer():
    header("File Organizer")
    folder = input("Folder to organize: ").strip().strip('"')

    if not os.path.isdir(folder):
        print("Folder does not exist.")
        pause()
        return

    def organize():
        moved = 0
        try:
            entries = list(os.scandir(folder))
        except OSError as error:
            print("Could not read folder:", error)
            return

        for entry in entries:
            if not entry.is_file(follow_symlinks=False):
                continue

            filename = entry.name
            extension = pathlib.Path(filename).suffix.lower().lstrip(".")
            destination_name = extension if extension else "no_extension"
            destination = os.path.join(folder, destination_name)

            if os.path.abspath(entry.path) == os.path.abspath(destination):
                continue

            try:
                os.makedirs(destination, exist_ok=True)
                target = os.path.join(destination, filename)

                if os.path.exists(target):
                    stem = pathlib.Path(filename).stem
                    suffix = pathlib.Path(filename).suffix
                    counter = 1
                    while os.path.exists(target):
                        target = os.path.join(
                            destination, f"{stem}_{counter}{suffix}"
                        )
                        counter += 1

                os.replace(entry.path, target)
                moved += 1
            except OSError as error:
                print(f"Could not move {filename}: {error}")

        print(f"\nOrganized {moved} files.")

    organize()



def ip_checker():
    header("IP Address Checker")
    address = input("IP address: ").strip()

    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        print("Invalid IP address.")
        pause()
        return

    def check():
        print("\nValid IP!")
        print("Version:", ip.version)
        print("Private:", ip.is_private)
        print("Loopback:", ip.is_loopback)
        print("Multicast:", ip.is_multicast)

    check()


def dns_lookup():
    header("DNS Lookup")
    hostname = input("Hostname: ").strip()

    def lookup():
        try:
            results = socket.getaddrinfo(hostname, None)
            addresses = sorted({result[4][0] for result in results})
            print("\nAddresses:")
            for address in addresses:
                print(" ", address)
        except socket.gaierror:
            print("Could not resolve hostname.")

    lookup()



def countdown():
    header("Countdown Timer")
    try:
        duration = int(input("Seconds: "))
        if duration < 0:
            raise ValueError
    except ValueError:
        print("Enter a non-negative whole number of seconds.")
        pause()
        return

    def start_timer():
        remaining = duration
        while remaining > 0:
            minutes, seconds = divmod(remaining, 60)
            print(
                f"\rTime remaining: {minutes:02d}:{seconds:02d}",
                end="",
                flush=True,
            )
            time.sleep(1)
            remaining -= 1
        print("\rTime remaining: 00:00")
        print("\nDone!")

    run_repeated(start_timer, "Start the same countdown again?")


def current_time():
    header("Current Date & Time")

    def show_time():
        now = datetime.datetime.now()
        print("\nDate:", now.strftime("%Y-%m-%d"))
        print("Time:", now.strftime("%H:%M:%S"))

    run_repeated(show_time, "Show the current date and time again?")



TOOLS = {
    "1": ("Random Number", random_number, "RANDOM"),
    "2": ("Dice Roller", dice_roller, "RANDOM"),
    "3": ("Coin Flip", coin_flip, "RANDOM"),
    "4": ("Random Choice", random_choice, "RANDOM"),
    "5": ("Password Generator", password_generator, "RANDOM"),
    "6": ("UUID Generator", uuid_generator, "RANDOM"),
    "7": ("Percentage Calculator", percentage_calculator, "MATH"),
    "8": ("Prime Checker", prime_checker, "MATH"),
    "9": ("Text Counter", text_counter, "TEXT"),
    "10": ("Case Converter", case_converter, "TEXT"),
    "11": ("Base64 Tool", base64_tool, "TEXT"),
    "12": ("JSON Formatter", json_formatter, "TEXT"),
    "13": ("SHA-256 File Hash", file_hash, "FILES"),
    "14": ("Folder Statistics", folder_stats, "FILES"),
    "15": ("File Organizer", file_organizer, "FILES"),
    "16": ("IP Checker", ip_checker, "NETWORK"),
    "17": ("DNS Lookup", dns_lookup, "NETWORK"),
    "18": ("Countdown Timer", countdown, "TIME"),
    "19": ("Current Date & Time", current_time, "TIME"),
}


def main():
    categories = ["RANDOM", "MATH", "TEXT", "FILES", "NETWORK", "TIME"]

    while True:
        clear()
        print("╭────────────────────────────────────╮")
        print("          PYTOOLS by monkysnatchr       ")
        print("                  v1.0.0               ")
        print("╰────────────────────────────────────╯\n")

        for category in categories:
            print(f"  {category}")
            print("  " + "-" * 30)
            for number, (name, _, tool_category) in TOOLS.items():
                if tool_category == category:
                    print(f"  {number}. {name}")
            print()

        print("  0. Exit\n")
        choice = input("  Select a tool: ").strip()

        if choice == "0":
            clear()
            print("Goodbye!")
            return

        selected = TOOLS.get(choice)
        if selected is None:
            print("\nInvalid choice.")
            time.sleep(1)
            continue

        _, function, _ = selected
        try:
            function()
            
            if choice in {"7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"}:
                while ask_again("Run this tool again with new inputs?"):
                    function()

        except (KeyboardInterrupt, EOFError):
            print("\n\nReturning to the main menu...")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
