import time

from colorama import Fore


TEXT = Fore.GREEN
MAG = Fore.MAGENTA
NML = Fore.RESET

ASCII_APP_TITLE_COLOR = \
f"""
{Fore.BLUE}-------------------------------------------------------------{NML}

           {TEXT}__       _ _ _{MAG}   __    __ _                     
          {TEXT}/ _\_ __ | (_) |_{MAG}/ / /\ \ (_)___  ___ _ __  
          {TEXT}\ \| '_ \| | | __{MAG}\ \/  \/ / / __|/ _ \ '__| 
          {TEXT}_\ \ |_) | | | |_{MAG} \  /\  /| \__ \  __/ |    
          {TEXT}\__/ .__/|_|_|\__|{MAG} \/  \/ |_|___/\___|_|    
             {TEXT}|_|{NML}                                      


{Fore.CYAN}~~~~~~~    Hobby Software Development <-> (c) 2024    ~~~~~~~{NML}

                           {MAG}nga-27{NML}

{Fore.BLUE}-------------------------------------------------------------{NML}
"""

def show_title() -> None:
    print(ASCII_APP_TITLE_COLOR)
    time.sleep(2)