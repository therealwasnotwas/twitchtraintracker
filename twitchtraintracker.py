00# ,;' Twitch Raid Train Session Time Tracker - Ross Leak (wasnotwas) v0.1a ';,

# Import required standard libraries into memory - datetime, collections, default dictionary

import re
from datetime import datetime, timedelta
from collections import defaultdict

import os

##
# Text Manipulation (Dont need it but useful for later)
# ANSI escape codes for red and bold
#red_bold = "\033[1;31m"
#reset_text = "\033[0m"

# Your message
#text = "This is a test message with a word in red and bold."

# Replace the word you want to format
#formatted_text = text.replace("word", f"{red_bold}word{reset_text}")

#print(formatted_text)
##



# CORE PROGRAM FUNCTION DEFINITIONS #

# ,;' Define my Regex patterns for "joined" and "left" statements from WeeChat log format ';, 
def build_twitch_patterns_weechat_format(user):
    join = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+-->\s+" + re.escape(user))
    leave = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+<--\s+" + re.escape(user))
    channel = re.compile(r"irc\.twitch\.(#[\w\d_]+)\.weechatlog")
    return join, leave, channel

# Function: Parse the log logic for Weechat format
def function_parse_log_weechat(filename, user):
    join_pattern, leave_pattern, channel_pattern = build_twitch_patterns_weechat_format(user)
    sessions = defaultdict(list)
    pending_joins = defaultdict(list)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            channel_match = channel_pattern.search(line)
            if not channel_match:
                continue
            channel = channel_match.group(1)

            join_match = join_pattern.search(line)
            leave_match = leave_pattern.search(line)

            if join_match:
                timestamp = datetime.strptime(join_match.group(1), "%Y-%m-%d %H:%M:%S")
                pending_joins[channel].append(timestamp)

            elif leave_match:
                timestamp = datetime.strptime(leave_match.group(1), "%Y-%m-%d %H:%M:%S")
                if pending_joins[channel]:
                    join_time = pending_joins[channel].pop(0)
                    sessions[channel].append((join_time, timestamp))

    return sessions

# Function: Need to calculate Total Time "twitchuser" spent in each session from weechat log
def summarise_twitch_sessions(sessions, user):
    total_time = timedelta()
    print(f"\nRaid Train session summary for twitch user: \033[1;31m{user}\033[0m\n")
    print(f"{'Twitch Channel':<20} {'Joined':<20} {'Left':<17} {'Duration'}")
    print("-" * 68)

    for channel, pairs in sessions.items():
        for join, leave in pairs:
            duration = leave - join
            total_time += duration
            print(f"{channel:<20} {join} {leave} {str(duration)}")

    print(f"\nTotal time \033[1;31m{user}\033[0m spent in all streams:", str(total_time))

# ,;' Section: The Main Interface / Initial Prompt for user ';,
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""\

          ******       **                            **+****    ***    **                 
        ****  **#    ***#             ****         *+*** #**%  ***#**#***                 
       ***   ***#  ****#           #   ##         ***#   **#   *** ##***#           #     
      #*#   ****% ****# **** **#****# **#******  #*##    **#  **#**#******* *****#**###   
       ### ****# **#**% **# **#****  **#***# ###        **## **##*# **##**#**#******# ##  
          ***#*#**#**# **# **##*#**#**#***#  #*%        **# **# *###*###*##***##**#*###   
    **# ***#% #####*## *##*###*########*######          *##**  ########### ###########    
    #######    %   ###  %%  #%  ##   #%  %#%            ####    #%  ##%%    %#%  %#       

                                       *#**##########                                     
                                 *******###%%%%%##%#######                                
                             +==+*##%%@%@@@@@@@@@@@@@%@%%%#%##                            
                          *++=*#@%%@%                @@@@@@%%%%%%                         
                        **+*#%%%%                         %@@@%%%%%                       
                       **#%%%%       ###***########%#        %@@%%%%@                     
                     %##%%%%     ++++++++++++**###########     %%%%%%%                    
                   %%%%%%     +=-=++=-**+-==++*#####*%%%%##*%    %%%%@@@                  
                  @%%@%     +=--:-+=:+**=--==+######%%%%%%%%###    @%@@@@                 
                 @%%%%    ++==**++=:+**::-=*#####%%%%%#*##%%%%%##   %%@@@@                
                @@%%%%  **++=+*+:::+*##+=#######%%%%%**####%%%%%###  %%@@@@               
                @@%%@  #*++===-::::+#########%%%%%##%**#%%#%%%%%%%##  %%@@@               
               @@@@%  #**+++====+==*#####%%%%%%%%#*#%##%###%%%%%@@%##  %@@@               
               @@%%%%%#****+====*#####%%%%%%%%%%%%%***#####%%%%@@@@%%%%%%%@@              
             ######%@##**+++*####%%%%%%%%%%%%%%%%%%#######%%%@@@@@@@%%%%######            
           #######%%%##****#%%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@@@@%%%%#######          
          ###*++++%%%#%%##%%%%%%%%%%%%%%%%%%%%%%%###%%%%%@@@@@@@@@@@@%%%#*+**####         
         ###*+==+*#%%@@%%%%%%%%%%%%%%%%%%%%%%%%%%#####%%%@@%@@@@@@@@@%%%#++==+####        
        *###*++++*#@@@%@%%%%%%%%%%%%%%%%%%%%%@%%%####%%%%%%%@@@@@@@@@%%%%*++++**##*       
        +##***+***%@@%%@@@@%%%%%%%%%%%%%%%@@@@%####%%%%%%%%@@@@@@@@@@@@@%**+++**##+       
       *=**+=-=+*#%@@@@@@%%@@%%%%%%%%%@@@@@@@@%##%%%%%%%%%@@@@@@@@@@%@@@%***===+**=       
       +-=-:..:=+*%@@@@@%###**%%@@@@@@@@@@@@@@#%%%%%%%%%%@@@@@@@@@@%@@@%#*+-:..:-=-#      
        =++===+*##@@@@@@@%###***#%@@@@@@@@@@@@%%%%%%%%@@@@@@@@@@@@@%@@@@%%#*===+**=       
        +**##**%%@@@@@@@%%%####**#%@@@@@@@@@@@@@%%%%@@@@@@@@@@@@@%%@@@@@%%%######++       
        **%%%%%%@@@@@%@@@%%%#########%@@@@@@@@@@@@@@@@@@@@@@@@@%%%@@@@@@%@@@@%%%%*        
         #%%@%@@@@%@@@%@@@%%%#########%%@@@@@@@@@@@@@@@@@@@@@%%%@@@%%@@@@@@@%@%%##        
           %%%%@@%%%@@%%%@@%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@%%%%@%%%@@@%%@@@%%%%          
            ###%%%#%%@@%%%@@%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@%%%##%##%@@%%%%%%%%#%           
              ######%%@@%#%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@%%%%#%%###@@%%####%#%             
                  ###%%@ ###%%#%%%%@@@@@@@@@@@@@@@@@@@@%%%##%%###  %%####                 
                           ######%%@@@@@@@@@@@@@@@@@@@@%##%%####                          
                             ####%%@@@@@@@@@@@@@@@@@@@@%%%###                             
                                **#%%%%@@@@@@@@@@@@@%%%####                               
                                    *###%%%%%%%%%%%####                                   
                                                                                          
""")

    print("🎧 Twitch Train Tracker (v0.1a alpha release)")
    print("🎧 \033[1;35mMusic Vibes Version\033[0m")
    print("🎧 © wasnotwas - all rights reserved")
    print("")
    log_file = input("Please enter the full path and filename of the log file: ").strip()
    target_user = input("Please enter the twitch username you wish to track against the log file: ").strip()

    try:
        sessions = function_parse_log_weechat(log_file, target_user)
        summarise_twitch_sessions(sessions, target_user)
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
