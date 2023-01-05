import bs4
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

FILE_NAME = "gasoleo"


def read_soup():
    # Open the html file from the current directory
    with open(FILE_NAME + ".html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup


def parse_title(soup):
    title = (
        soup.find(
            "span",
            class_="o4KVKZmeHsoRZ2Ltl078",
        )
        .find("h1")
        .text
    )
    return title


def parse_description(soup):
    try:
        description = soup.find(
            "div",
            class_="xgmjVLxjqfcXK5BV_XyN",
        ).text
    except AttributeError:
        description = ""
    return description


def parse_user(soup):
    user = (
        soup.find(
            "span",
            class_="Type__TypeElement-sc-goli3j-0 jdSGNV",
        )
        .find("a")
        .text
    )
    return user


def extract_songs_divs(soup):
    # First, find the div that groups the songs' divs
    songs_div_group = soup.find_all("div", class_="JUa6JJNj7R_Y3i4P8YUX")[1]
    # Then find all the songs' divs inside that div
    songs_divs = songs_div_group.find_all(
        "div", class_="h4HgbO_Uu1JYg5UGANeQ wTUruPetkKdWAR1dd6w4"
    )
    return songs_divs


def parse_song_info(song: bs4.element.Tag) -> dict:
    info = {}

    info["title"] = song.find(
        "div",
        class_="Type__TypeElement-sc-goli3j-0 kHHFyx t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line",
    ).text
    info["album"] = song.find("a", class_="standalone-ellipsis-one-line").text
    # For the artist, it's a link inside a span, so we need to find the link first
    info["artist"] = (
        song.find(
            "span",
            class_="Type__TypeElement-sc-goli3j-0 dvSMET rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line",
        )
        .find("a")
        .text
    )
    info["date"] = parse_date(
        song.find("span", class_="Type__TypeElement-sc-goli3j-0 dvSMET").text
    )

    return info


def parse_date(date_string):
    if "ago" in date_string:
        target_date = parse_relative_date(date_string)
    else:
        target_date = datetime.strptime(date_string, "%b %d, %Y")
    return target_date.strftime("%Y-%m-%d")


def parse_relative_date(date_string):
    # Parse the number of days from the string
    num_days = int(date_string.split()[0])
    # Calculate the target date by subtracting the number of days from the current date
    target_date = datetime.now() - timedelta(days=num_days)
    return target_date


def write_to_file(soup, songs_divs, verbose=True):
    # Open a new .txt file to write the results
    with open(FILE_NAME + ".txt", "w") as fp:
        # Write the title and description
        fp.write(
            parse_title(soup)
            + "\n\n"
            + parse_description(soup)
            + "\n\n"
            + parse_user(soup)
            + "\n\n"
        )
        for song in songs_divs:
            info = parse_song_info(song)
            record = f'[{info["date"]}] {info["title"]} - {info["artist"]}\n'
            if verbose:
                print(record, end="")
            fp.write(record)


def main():
    soup = read_soup()
    songs_divs = extract_songs_divs(soup)
    write_to_file(soup, songs_divs)


if __name__ == "__main__":
    main()
