##Importing the requests module
import requests

def handler():
    r = requests.get('https://swapi.dev/api/')
    return r.json()

##Tell the program how to look for spaceships for later
##Setting it up so we can later itterate through pages
def getSpaceships(page: int):
    r = requests.get('https://swapi.dev/api/starships/?page=' + str(page))
    if r.status_code == 200:
        return r.json()
    else:
        return None

##Creating a function that creates and populates a list of starships for us
def fetch_all_spaceships():
    all_spaceships = []  ##first make an empty list to store all the spaceships
    page = 1  ##tells it to start with page 1

    while True: ##keep the door open and start collecting starships
        data = getSpaceships(page)
        if data is not None: ##check there's data there
            all_spaceships.extend(data.get('results', []))
            if data.get('next'): ##there was a next function in the api, woo hoo!
                page += 1 ##so keep adding 1 to the url and add that ship to the list until...
            else:
                break  ##no more pages? break
        else:
            break  ##somehow also no data? break

    return all_spaceships

##tell the program how to look for pilots, we'll need this in a bit
def get_pilot_name(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get('name') ##we only care about pilot name, specify this
    return None

##Let's make it easier and map the speed rangers to a numbered selection
speed_ranges = [
    ("1", 850, 1000, "Slow"),
    ("2", 1001, 1200, "Medium"),
    ("3", 1201, 1500, "Fast"),
    ("4", 1501, 8001, "Super Fast")
]

##Alright, got all our info lined up, let's get some input from our user!
print("Welcome to Star Wars Uber!")
print("How fast do you need to travel between planets?")
print("1. Slow (850-1000)")
print("2. Medium (1001-1200)")
print("3. Fast (1201-1500)")
print("4. Super Fast (1501+)")

speed_choice = input("Select the number from our list: ")

##turning the selected speed range into a single thing to refer back to, reduces repetition
selected_range = None
for range in speed_ranges:
    if range[0] == speed_choice:
        selected_range = range
        break

if not selected_range:
    print("Incorrect, please select from the range. Restart program.")
else:
    speed_description = selected_range[3]
    print(f"You selected the {speed_description} speed range. Please wait while we load available spaceships...")

    ##fetch all spaceships
    spaceships = fetch_all_spaceships()

    ##make a list of the spaceships in the selected range
    filtered_spaceships = []
    min_speed, max_speed = selected_range[1], selected_range[2] ##setting the min+max based on the range we set earlier
    for spaceship in spaceships:
        speed = spaceship.get('max_atmosphering_speed')
        if speed.isdigit() and min_speed <= int(speed) <= max_speed: ##check it's a number, then look in the range
            filtered_spaceships.append(spaceship) ##if it's in the range, add to the list

    if not filtered_spaceships:
        print("No spaceships available in your selected speed range. Please try again.")
    else:
        print("List of spaceships in your selected speed range:")
        for idx, spaceship in enumerate(filtered_spaceships, start=1): ##make a numbered list
            print(f"{idx}. {spaceship['name']} (Max Speed: {spaceship['max_atmosphering_speed']})") ##display as this

        spaceship_choice = int(input("Enter the number of the spaceship you want to choose: "))
        selected_spaceship = filtered_spaceships[spaceship_choice - 1]

        ##now we need to show the polits for that ship
        pilots = selected_spaceship.get('pilots', [])
        if not pilots:
            print(f"The selected spaceship ({selected_spaceship['name']}) has no pilots available. Please restart the program.")
        else:
            print(f"Pilots for the spaceship {selected_spaceship['name']}:")
            pilot_names = [get_pilot_name(pilot) for pilot in pilots]
            for i, pilot in enumerate(pilot_names, start=1):
                print(f"{i}. {pilot}")

            pilot_choice = int(input("Enter the number of the pilot you want to choose: "))
            selected_pilot = pilot_names[pilot_choice - 1]

            #calculate the trip cost, let's say 1000th of the total cost of the ship
            cost_in_credits = selected_spaceship.get('cost_in_credits', 'unknown')
            if cost_in_credits != 'unknown' and cost_in_credits != 'n/a':
                trip_cost = int(cost_in_credits) / 1000
                result_text = ("Thank you for choosing Star Wars Uber!\n" ##define a receipt to print as a file
                f"You selected {selected_spaceship['name']} for your ride\n"
                f"You selected {selected_pilot} as your pilot.\n"
                f"Your total will be {trip_cost} credits"
                )
                print(result_text)
            else:
                print(f"You selected {selected_pilot} as your pilot. The cost of the trip could not be determined.")
            with open("trip_result.txt", "w") as file: ##creates a file for the receipt
                file.write(result_text)
                
