import requests 
import csv 
from bs4 import BeautifulSoup


# get response of wikipedia
def get_reponse(url="https://en.wikipedia.org/wiki/2023_AFL_season"):
    response = requests.get(url)
    print(response.status_code)
    return response.text






#read response and extract table data 
def read_response(response):
    """
    1.	Round Number (example: "1")
    2.	Day of the game (example: "Friday")
    3.	Date of the game (example: "19-Sep")
    4.	Time of the game (example: "7:50 pm")
    5.	First team name (example: "Brisbane Lions")
    6.	First team score in points only (example: "57")
    7.	First team win status (either "def. by" or "def.")
    8.	Second team name (example: "Melbourne")
    9.	Second team score in points only (example: "115")
    10.	Game location (example: "The Gabba")
    11.	Stadium Attendees (example: "32172")
    """
    data = []
    # with open("index.html", "r", encoding="utf-8") as html_file:
    soup = BeautifulSoup(response, "html.parser")
    tables = soup.find_all('table', {'cellspacing': '0', 'style': 'width: 100%; background-color: #f1f5fc; border: 2px solid #D0E5F5'})
    for table in tables:
        tbody = table.find("tbody")
        round = table.find_all('tr')[1].find('th', {'style': 'text-align:center;'})
        if "Round" in round.text:
            round_number = str(round.text).split(" ")[1].strip()
            row_count = len(table.find_all('tr'))
            print (row_count)
            for i in range(2, (row_count-1)):
                
                allrow = tbody.find_all('tr')[i].find('td').text
                if "pm)" in allrow or "am)" in allrow:
                    game_date_day = allrow.strip()
                    game_day = game_date_day.split(", ")[0]
                    game_date = game_date_day.split(', ')[-1].split("(")[0]
                    game_time = game_date_day.split(', ')[-1].split("(")[-1].split(")")[0]
                    
                    try:
                        first_team_name =  tbody.find_all('tr')[i].find_all('td')[1].find("a")['title'] 
                    except Exception as e:
                        first_team_name =  "Na" 
                    try:
                        first_team_score = tbody.find_all('tr')[i].find_all('td')[1].text.split("(")[-1].split(")")[0].strip() 
                    except Exception as e:
                        first_team_score = "Na" 
                    try:
                        first_team_win_status = tbody.find_all('tr')[i].find_all('td')[2].text.strip() 
                    except Exception as e:
                        first_team_win_status = "Na" 
                    try:
                        second_team_name = tbody.find_all('tr')[i].find_all('td')[3].find("a")['title'] 
                    except Exception as e:
                        second_team_name = "Na" 
                    try:
                        second_team_score = tbody.find_all('tr')[i].find_all('td')[3].text.split("(")[-1].split(")")[0].strip()

                    except Exception as e:
                        second_team_score = "Na"

                    try:
                        game_location_raw =tbody.find_all('tr')[i].find_all('td')[4].text.strip() 
                    except Exception as e:
                        game_location_raw ="Na"
                    
                    try:
                        crowd_raw = tbody.find_all('tr')[i].find_all('td')[4].text.split("(")[-1].split(")")[0].split(" ")[-1].strip() 
                    except Exception as e:
                        crowd_raw = "Na"

                    game_day = game_day.replace('\xa0', ' ')
                    game_date = game_date.replace('\xa0', ' ')
                    game_time = game_time.replace('\xa0', ' ')
                    game_location = game_location_raw.replace('\n', '').replace('\t', '').replace('\xa0', ' ').split("(crowd:")[0]
                    crowd = crowd_raw.replace('crowd:', '').replace('\xa0', '').strip()
                    details = [
                        round_number, game_day, game_date, game_time, 
                        first_team_name, first_team_score, 
                        first_team_win_status, second_team_name, 
                        second_team_score, game_location, crowd]
                    data.append(details)
    return data 
            




#store data of each url in a csv_file
#take csv file name from the url itself 
def create_csv_file(file_name, data):
    # with open(file_name, "w", encoding="utf-8") as file:
    with open(f"csv/{file_name}", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Round', "Day", "Date", "Time", "First Team Name",
                         "First Team Score", "First Team win Status", "Second Team name", "Second Team Score",
                         "Game Location", "Croud"])
        for row in data:
            cleaned_row = [element.strip() if isinstance(element, str) else element for element in row]
            writer.writerow(cleaned_row)
        print(f"All data is saved in {file_name}.")

    
    
    
def run(txt_file="url.txt"):
    with open(txt_file, "r", encoding="utf-8") as file:
        urls = file.readlines()
        uls = [url.strip() for url in urls]
        for url in uls:
            print(url)
            try:
                csv_name = url.split("/")[-1].replace("\n", "") + ".csv"
                resp = get_reponse(url=url)
                data = read_response(response=resp)
                create_csv_file(file_name=csv_name, data=data)
            except Exception as e:
                print(e)
            



if __name__ == "__main__":
    run(txt_file="url.txt")