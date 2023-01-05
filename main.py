from bs4 import BeautifulSoup

FILE_NAME = "our spring waiting"
NO_OF_SONGS = 17

# Open the html file from the current directory
with open(FILE_NAME + ".html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Find all the <div> tags that have the given class
songs = soup.find_all("div", class_="h4HgbO_Uu1JYg5UGANeQ wTUruPetkKdWAR1dd6w4")
# and trim them (bc otherwise the recommended songs are also included)
songs = songs[:NO_OF_SONGS]

# Open a new .txt file to write the results
with open(FILE_NAME + ".txt", "w") as fp:
    # Iterate over all the songs
    for song in songs:
        # Get title, artist album and date from the tags
        title = song.find(
            "div",
            class_="Type__TypeElement-sc-goli3j-0 kHHFyx t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line",
        ).text
        album = song.find("a", class_="standalone-ellipsis-one-line").text
        artist = (
            song.find(
                "span",
                class_="Type__TypeElement-sc-goli3j-0 dvSMET rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line",
            )
            .find("a")
            .text
        )
        date = song.find("span", class_="Type__TypeElement-sc-goli3j-0 dvSMET").text
        record = f"[{date}] {title} - {artist}\n"
        print(record)
        fp.write(record)
