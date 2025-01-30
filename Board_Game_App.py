# Importing Libraries
import pandas as pd
import streamlit as st
import ast
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Turning the data to a pandas dataframe
df = pd.read_csv('Board Game Data.csv')

# Getting Category/Mechanic as Lists
df['Game_Categories'] = df['Game_Categories'].apply(ast.literal_eval)
df['Game_Mechanics'] = df['Game_Mechanics'].apply(ast.literal_eval)

# Setting index to be equal to BGG Rank
df = df.set_index('BGG_Rank')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Initialise session state
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = df.copy()
if 'history' not in st.session_state:
    st.session_state['history'] = []
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# How many games to be output
x = 8
# Recommend the top games
def recommend():
    if st.session_state.filtered_df.empty:
        st.warning("Sorry, no available board games! Refresh to try again.")
        st.markdown("Common reasonings for this will be an unconvential group size for game types or lower game times with heavy games")
    else:
        st.markdown('### Top Recommended Board Games:')
        st.markdown('##### *Want to try a new selection? Simply refresh the page!*')
        st.markdown('---')
        top_games = st.session_state.filtered_df[['Name', 'Release_Year', 'Description']].head(x)
        for id, row in top_games.iterrows():
            st.markdown(f'**BGG Rank: {id}** \n\n ##### {row['Name']} ({row['Release_Year']}) \n\n {row['Description']} \n\n ---')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Introducing the Recommendation system
st.title("Welcome to the Board Game Recommendation App! 🎲")  
st.subheader("Find the perfect board game based on your preferences!")  

st.markdown("##### How It Works:")
st.markdown("- Enter details about the type of board game you're looking for.")
st.markdown("- Receive a list of the **highest rated games**, from board game geek (BGG), tailored to your wants and needs.")
st.markdown("- If somehow no matching games are found, you simply **refresh the page** and try again. (Recommendations and Advice Provided)")

st.markdown("---")
st.markdown("Ready to find your next favorite board game?") 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# My personal favourite games and recommendations
st.sidebar.markdown("# :rainbow[Oats' Favourite Games]")
st.sidebar.markdown('---')

dune_imp = df.loc[df['Name'] == "Dune: Imperium"]
st.sidebar.markdown(f"### {dune_imp.iloc[0]['Name']} ({dune_imp.iloc[0]['Release_Year']})")
st.sidebar.markdown(f"{dune_imp.iloc[0]['Description']}")
st.sidebar.markdown(f"{dune_imp.iloc[0]['Minimum_Players']}-{dune_imp.iloc[0]['Maximum_Players']} Players")
st.sidebar.markdown(":rainbow[Oat Note:] My favourite worker placement game! Blocking your friends has never felt better! Brilliant expansions too!")
st.sidebar.markdown('---')

botc = df.loc[df['Name'] == "Blood on the Clocktower"]
st.sidebar.markdown(f"### {botc.iloc[0]['Name']} ({botc.iloc[0]['Release_Year']})")
st.sidebar.markdown(f"{botc.iloc[0]['Description']}")
st.sidebar.markdown(f"{botc.iloc[0]['Minimum_Players']}-{botc.iloc[0]['Maximum_Players']} Players")
st.sidebar.markdown(":rainbow[Oat Note:] The best game for large groups! If you enjoy lying, this game is for you!")
st.sidebar.markdown('---')

ticket = df.loc[df['Name'] == "Ticket to Ride"]
st.sidebar.markdown(f"### {ticket.iloc[0]['Name']} ({ticket.iloc[0]['Release_Year']})")
st.sidebar.markdown(f"{ticket.iloc[0]['Description']}")
st.sidebar.markdown(f"{ticket.iloc[0]['Minimum_Players']}-{ticket.iloc[0]['Maximum_Players']} Players")
st.sidebar.markdown(":rainbow[Oat Note:] My favourite beginner friendly game! A must have board game! Ideal for people starting their new hobby!")
st.sidebar.markdown('---')

b_rage = df.loc[df['Name'] == "Blood Rage"]
st.sidebar.markdown(f"### {b_rage.iloc[0]['Name']} ({b_rage.iloc[0]['Release_Year']})")
st.sidebar.markdown(f"{b_rage.iloc[0]['Description']}")
st.sidebar.markdown(f"{b_rage.iloc[0]['Minimum_Players']}-{b_rage.iloc[0]['Maximum_Players']} Players")
st.sidebar.markdown(":rainbow[Oat Note:] Fighting other players as viking clans with the power of the Norse Gods? Absolutely!")
st.sidebar.markdown('---')

b_birmingham = df.loc[df['Name'] == "Brass: Birmingham"]
st.sidebar.markdown(f"### {b_birmingham.iloc[0]['Name']} ({b_birmingham.iloc[0]['Release_Year']})")
st.sidebar.markdown(f"{b_birmingham.iloc[0]['Description']}")
st.sidebar.markdown(f"{b_birmingham.iloc[0]['Minimum_Players']}-{b_birmingham.iloc[0]['Maximum_Players']} Players")
st.sidebar.markdown(":rainbow[Oat Note:] The number 1 game on board game geek for a reason! Peak board game experience!")
st.sidebar.markdown('---')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Player Count
def game_players():
    """Asks questions to identify player counts"""
    
    st.markdown('#### Do you know how many players you want to play with?')
    game_player_resp = st.radio('Players: ', ('Yes', 'No'), index=None)
    if game_player_resp is not None:
        if game_player_resp == 'Yes':
            st.markdown('#### How many players (including yourself) will you have?')
            player_count = st.number_input('Player Number', min_value=1, max_value=100, value=None)
                
            if player_count is not None:
                st.session_state.filtered_df = st.session_state.filtered_df[(st.session_state.filtered_df['Minimum_Players'] <= player_count) & (st.session_state.filtered_df['Maximum_Players'] >= player_count)]
                if len(st.session_state.filtered_df) <= x:
                    recommend()
                else:
                    game_time()
        
        elif game_player_resp == 'No':
            st.markdown("#### What's the maximum number of players (including yourself) you would want to play with?")
            max_player_count = st.number_input('Player Number', min_value=1, max_value=100, value=None)
                
            if max_player_count is not None:
                st.session_state.filtered_df = st.session_state.filtered_df[(st.session_state.filtered_df['Minimum_Players'] <= max_player_count)]
                if len(st.session_state.filtered_df) <= x:
                    recommend()
                else:
                    game_time()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Length
def game_time():
    """Asks questions to identify how long they would like a game to take"""
    
    st.markdown('#### How long would you like one playthrough to take on average?')
    play_time = st.number_input('Game Time (minutes):', min_value=x, max_value=1200, value=None)

    if play_time is not None:
        st.markdown('#### Is there a maximum time you wish for the game to not go over?')
        max_time_question = st.radio('Select:', ("Yes", "No"), index=None)

        if max_time_question is not None:
            if max_time_question == "Yes":
                max_time = st.number_input('Max Time', min_value=play_time, max_value=1200, value=None)
                
                if max_time is not None:
                    st.session_state.filtered_df = st.session_state.filtered_df[(st.session_state.filtered_df['Minimum_Time'] <= play_time) & (st.session_state.filtered_df['Maximum_Time'] <= max_time) & (st.session_state.filtered_df['Maximum_Time'] >= play_time)]
                    if len(st.session_state.filtered_df) <= x:
                        recommend()
                    else:
                        age_rating()
                        
            elif max_time_question == "No":
                st.session_state.filtered_df = st.session_state.filtered_df[(st.session_state.filtered_df['Minimum_Time'] <= play_time) & (st.session_state.filtered_df['Maximum_Time'] >= play_time)]
                if len(st.session_state.filtered_df) <= x:
                    recommend()
                else:
                    age_rating()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Age Rating
def age_rating():
    """Asks whether they have any age requirements for games, if so, what are they"""
    
    st.markdown('#### Would you like to remove games based on their recommended age rating? \n\n *Certain games may have themes unsuitable for younger players*')
    game_age = st.radio('Remove certain games:', ('Yes', 'No'), index = None)

    if game_age is not None:
        if game_age == 'Yes':
            st.markdown('#### How old is the youngest player?')
            min_age_rating = st.slider('Age', min_value = x, max_value = 18)
            
            st.markdown('*Would you like to keep to this as a strict age rating?*')
            age_leniance = st.radio('Age strictness:', ('Yes. Only show me games at this rating or below', 'No. You can include games slightly above'), index = None)
    
            if age_leniance is not None:
                if age_leniance == 'Yes. Only show me games at this rating or below':
                    st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Age_Rating'] <= min_age_rating]
    
                elif age_leniance == 'No. You can include games slightly above':
                    st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Age_Rating'] <= (min_age_rating + 2)]
                    
                if len(st.session_state.filtered_df) <= x:
                    recommend()
                else:
                    complexity()
                    
        elif game_age == 'No':
            complexity()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Complexity
def complexity():
    """Asks how complex of a game they would like to play"""
    
    st.markdown("#### How heavy (complex) of a game would you like to play \n\n *Complexity: Time to learn, time spent thinking on turns, technical skills, randomness, etc*")
    game_complexity = st.radio('Select Complexity:', (
        "Light - Easy party/card games and fun beginner friendly board games able to be learned quickly!",
        "Medium - Usually an hour or more long board games with fun mechanics. The sweet spot of casual/competitive!",
        "Heavy - Can take entire days or multiple sessions, often requiring some preparation. Providing some of the most unique board game experiences!"), index = None)

    if game_complexity is not None:
        if game_complexity == "Light - Easy party/card games and fun beginner friendly board games able to be learned quickly!":
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Complexity_Category'] == 'Light']
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                category_refine()

        elif game_complexity == "Medium - Usually an hour or more long board games with fun mechanics. The sweet spot of casual/competitive!":
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Complexity_Category'] == 'Medium']
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                category_refine()

        elif game_complexity == "Heavy - Can take entire days or multiple sessions, often requiring some preparation. Providing some of the most unique board game experiences!":
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Complexity_Category'] == 'Heavy']
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                category_refine()                     
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Categories
def category_refine():
    """Prompts the user to select one of the broad categories"""
    
    categories_all = {
    "Conflict, Civilisation and Infrastructure Games": [
        "city-building", "territory-building", "wargame", "civilization",
        "negotiation", "economic", "political", "industry-manufacturing", 
        "renaissance", "modern-warfare", "pike-and-shot", "post-napoleonic", 
        "world-war-ii", "world-war-i", "american-revolutionary-war", "american-civil-war", 
        "american-indian-wars", "vietnam-war", "napoleonic", "transportation", 
        "trains", "aviation-flight", "age-of-reason"
    ],
    "Thematic/Setting-Based Games": [
        "fantasy", "science-fiction", "mythology", "horror", "space-exploration",
        "medieval", "ancient", "american-west", "prehistoric", "religious",
        "arabian", "nautical", "pirates", "environmental",
        "adventure", "exploration", "animals", "zombies", "travel"
    ],
    "Party Games": [
        "party-game", "card-game", "humor", "bluffing", "childrens-game",
        "word-game", "trivia", "spies-secret-agents", "mafia", "deduction", "music"
    ],
    "Competitive Games": [
        "fighting", "action-dexterity", "racing", "sports", "real-time", "abstract-strategy"
    ],
    "Puzzle and Trivia Games": [
        "puzzle", "math", "educational", "memory", "murder-mystery", "deduction", "number", "trivia",
    ]}
    # Excluded categories: dice, miniatures, collectible-components, game-system, expansion-for-base-game, print-and-play, electronic, novel-based, movies-tv-radio-theme, video-game-theme, mature-adult, comic-book-strip, maze
    st.markdown("#### Select a game category that most interests you")
    category_choice = st.selectbox("Game Categories:", options = categories_all, index = None)
    
    if category_choice is not None:
        if category_choice == "Conflict, Civilisation and Infrastructure Games":
            conf_civ_filter = set(categories_all["Conflict, Civilisation and Infrastructure Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in conf_civ_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                conf_civ_games()

        elif category_choice == "Thematic/Setting-Based Games":
            thematic_filter = set(categories_all["Thematic/Setting-Based Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                thematic_games()
            
        elif category_choice == "Party Games":
            party_filter = set(categories_all["Party Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in party_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                party_games()
            
        elif category_choice == "Competitive Games":
            competitive_filter = set(categories_all["Competitive Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in competitive_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                competitive_games()
            
        elif category_choice == "Puzzle and Trivia Games":
            puzzle_filter = set(categories_all["Puzzle and Trivia Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in puzzle_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                puzzle_games()


def conf_civ_games():
    """Prompts the user to select a subcategory of this category"""
    
    conf_civ_cats = {
    "Land Building Games": [
        "city-building", "territory-building", "civilization"
    ],
    "Transportation and Travel Games": [
        "transportation", "trains", "aviation-flight"
    ],
    "War Games": [
        "wargame", "modern-warfare", "pike-and-shot", "world-war-ii", "world-war-i", 
        "american-revolutionary-war", "american-civil-war", "american-indian-wars",
        "vietnam-war", "napoleonic", "renaissance", "age-of-reason"
    ],
    "Political/Economic Games": [
        "economic", "political", "industry-manufacturing", "post-napoleonic"
    ]} 
    st.markdown("Conflict and Civilisation Games are all about creating settlements and territories, with potentially political, or war-like themes. \n\n #### Select a game sub-category that most interests you")
    conf_civ_games_resp = st.selectbox("Select a Category:", options = conf_civ_cats, index = None)

    if conf_civ_games_resp is not None:
        if conf_civ_games_resp == "Land Building Games":
            conf_civ_extra_filter = set(conf_civ_cats["Land Building Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in conf_civ_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif conf_civ_games_resp == "Transportation and Travel Games":
            conf_civ_extra_filter = set(conf_civ_cats["Transportation and Travel Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in conf_civ_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif conf_civ_games_resp == "War Games":
            conf_civ_extra_filter = set(conf_civ_cats["War Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in conf_civ_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()

        elif conf_civ_games_resp == "Political/Economic Games":
            conf_civ_extra_filter = set(conf_civ_cats["Political/Economic Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in conf_civ_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                                  
def thematic_games():
    """Prompts the user to select a subcategory of this category"""
    
    thematic_cats = {
    "Fantasy Games": [
        "fantasy", "mythology", "horror", "pirates", "zombies"
    ],
    "Science Fiction Games": [
        "science-fiction", "space-exploration",
    ],
    "Historical Games": [
        "medieval", "ancient", "american-west", "prehistoric", "religious",
        "arabian"
    ],
    "Adventure and Exploration Games": [
        "adventure", "exploration", "nautical", "travel"
    ],
    "Nature Games": [
        "environmental", "animals"
    ]}
    st.markdown("Thematic/Setting-Based Games are all about emersing in a unique world or genre often with fantasy themes/sci-fi themes. \n\n #### Select a game sub-category that most interests you")
    thematic_games_resp = st.selectbox("Select a Category:", options = thematic_cats, index = None)

    if thematic_games_resp is not None:
        if thematic_games_resp == "Fantasy Games":
            thematic_extra_filter = set(thematic_cats["Fantasy Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()

        elif thematic_games_resp == "Science Fiction Games":
            thematic_extra_filter = set(thematic_cats["Science Fiction Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif thematic_games_resp == "Historical Games":
            thematic_extra_filter = set(thematic_cats["Historical Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif thematic_games_resp == "Adventure and Exploration Games":
            thematic_extra_filter = set(thematic_cats["Adventure and Exploration Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif thematic_games_resp == "Nature Games":
            thematic_extra_filter = set(thematic_cats["Nature Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in thematic_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                

def party_games():
    """Prompts the user to select a subcategory of this category"""
    
    party_cats = {
    "Social Deduction Games": [
        "bluffing", "spies-secret-agents", "mafia", "deduction"
    ],
    "Quick and Easy Games": [
        "party-games", "card-game", "humor", "childrens-game", "word-game", "music"
    ]}
    st.markdown("Party Games are all about easy fun, providing entertainment to a gathering of any size. \n\n #### Select a game sub-category that most interests you")
    party_games_resp = st.selectbox("Select a Category:", options = party_cats, index = None)

    if party_games_resp is not None:
        if party_games_resp == "Social Deduction Games":
            party_extra_filter = set(party_cats["Land Building Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in party_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif party_games_resp == "Quick and Easy Games":
            party_extra_filter = set(party_cats["Quick and Easy Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in party_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
def competitive_games():
    """Prompts the user to select a subcategory of this category"""
    
    competitive_cats = {
    "Sports/Racing Games": [
        "racing", "sports"
    ],
    "Strategy Games": [
        "action-dexterity", "real-time", "abstract-strategy"
    ],
    "Combat Games": [
        "fighting"
    ]}
    st.markdown("Competitive Games are all about doing whatever it takes to beat your opponents. \n\n #### Select a game sub-category that most interests you")
    competitive_games_resp = st.selectbox("Select a Category:", options = competitive_cats, index = None)

    if competitive_games_resp is not None:
        if competitive_games_resp == "Sports/Racing Games":
            competitive_extra_filter = set(competitive_cats["Sports/Racing Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in competitive_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif competitive_games_resp == "Strategy Games":
            competitive_extra_filter = set(competitive_cats["Strategy Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in competitive_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif competitive_games_resp == "Combat Games":
            competitive_extra_filter = set(competitive_cats["Combat Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in competitive_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()


def puzzle_games():
    """Prompts the user to select a subcategory of this category"""
    
    puzzle_cats = {
    "Mystery Solving Games": [
        "puzzle", "murder-mystery", "deduction",
    ],
    "Trivia Games": [
        "trivia", "educational",
    ],
    "Mathematical Games": [
        "math", "number", "memory"
    ]}
    st.markdown("Puzzle Games are all about solving problems, making deductions, and engaging in challenges. \n\n #### Select a game sub-category that most interests you")
    puzzle_games_resp = st.selectbox("Select a Category:", options = puzzle_cats, index = None)    

    if puzzle_games_resp is not None:
        if puzzle_games_resp == "Mystery Solving Games":
            puzzle_extra_filter = set(puzzle_cats["Mystery Solving Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in puzzle_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif puzzle_games_resp == "Trivia Games":
            puzzle_extra_filter = set(puzzle_cats["Trivia Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in puzzle_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
                
        elif puzzle_games_resp == "Mathematical Games":
            puzzle_extra_filter = set(puzzle_cats["Mathematical Games"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Categories'].apply(lambda cat_list: any(cat in puzzle_extra_filter for cat in cat_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                mechanic_refine()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game Mechanics
def mechanic_refine():
    """Prompts the user to select one of the main board game mechanics"""
    mechanics_all = {
    "Dice Rolling": [
        'dice-rolling', 'die-icon-resolution', 'worker-placement-with-dice-workers', 'roll-spin-and-move', 'different-dice-movement',
    ],
    "Tile Placement and Map Creation": [
        'network-and-route-building', 'hexagon-grid', 'grid-coverage', 'tile-placement', 'grid-movement',
        'modular-board', 'pattern-building', 'map-addition', 'square-grid', 'map-reduction', 'pieces-as-map', 
        'track-movement', 'relative-movement', 'zone-of-control', 'map-deformation'
    ],
    "Card Drafting and Hand Management": [
        'hand-management', 'open-drafting', 'deck-construction', 'deck-bag-and-pool-building',
        'closed-drafting', 'move-through-deck', 'multi-use-cards'
    ],
    "Worker Placement": [
        'king-of-the-hill', 'worker-placement', 'area-majority-influence', 
        'worker-placement-different-worker-types', 'worker-placement-with-dice-workers',
    ],
    "Storytelling, Roleplaying and Campaigns": [
        'legacy-game', 'scenario-mission-campaign-game', 'campaign-battle-card-driven', 'critical-hits-and-failures', 
        'line-of-sight', 'narrative-choice-paragraph', 'role-playing', 'storytelling', 'once-per-game-abilities', 'events'
    ],
    "Auction and Bidding": [
        'market', 'trading', 'delayed-purchase', 'auction-bidding', 'auction-dutch', 'turn-order-auction',
        'auction-turn-order-until-pass', 'constrained-bidding', 'selection-order-bid', 'auction-fixed-placement',
        'auction-multiple-lot', 'betting-and-bluffing', 'auction-once-around', 'closed-economy-auction',
       'auction-sealed-bid', 'predictive-bid', 'auction-english', 'bids-as-wagers', 'auction-dutch-priority'
    ],
    "Resource Management and Economy": [
        'income', 'loans', 'turn-order-stat-based', 'end-game-bonuses', 'increase-value-of-unchosen-resources',
        'victory-points-as-a-resource', 'automatic-resource-growth', 'investment', 'stock-holding', 'resource-to-move', 'commodity-speculation'
    ],
    "Co-operative Play and Teamwork": [
        'cooperative-game', 'communication-limits', 'voting', 'team-based-game', 'alliances', 'semi-cooperative-game', 'negotiation', 'force-commitment'
    ],
    "Versus Players": [
        'traitor-game', 'kill-steal', 'deduction', 'bribery', 'single-loser-game', 'take-that', 'push-your-luck', 'hidden-roles'
    ]}
    
    st.markdown("#### Select a game mechanic you would want featured in your game")
    mechanic_choice = st.selectbox("Game Mechanics:", options = mechanics_all, index = None)
    
    if mechanic_choice is not None:
        if mechanic_choice == "Dice Rolling":
            dice_filter = set(mechanics_all["Dice Rolling"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()
                
        elif mechanic_choice == "Tile Placement and Map Creation":
            dice_filter = set(mechanics_all["Tile Placement and Map Creation"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Card Drafting and Hand Management":
            dice_filter = set(mechanics_all["Card Drafting and Hand Management"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Worker Placement":
            dice_filter = set(mechanics_all["Worker Placement"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Storytelling, Roleplaying and Campaigns":
            dice_filter = set(mechanics_all["Storytelling, Roleplaying and Campaigns"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Auction and Bidding":
            dice_filter = set(mechanics_all["Auction and Bidding"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Resource Management and Economy":
            dice_filter = set(mechanics_all["Resource Management and Economy"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Co-operative Play and Teamwork":
            dice_filter = set(mechanics_all["Co-operative Play and Teamwork"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Tile Placement and Map Creation":
            dice_filter = set(mechanics_all["Tile Placement and Map Creation"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()

        elif mechanic_choice == "Versus Players":
            dice_filter = set(mechanics_all["Versus Players"])
            st.session_state.filtered_df = st.session_state.filtered_df[st.session_state.filtered_df['Game_Mechanics'].apply(lambda mech_list: any(mech in dice_filter for mech in mech_list))]
            if len(st.session_state.filtered_df) <= x:
                recommend()
            else:
                recommend()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Begin the app button, once triggered, remains active.
if "button_active" not in st.session_state:
    st.session_state.button_active = False

def toggle_button():
    st.session_state.button_active = not st.session_state.button_active

if st.session_state.button_active:
    st.button("BEGUN!", on_click=toggle_button, key="active_button", disabled=True)
    game_players()
else:
    st.button("LET'S BEGIN!", on_click=toggle_button, key="inactive_button")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Recommend now button.
st.markdown('---')
st.markdown("If at any point you wish to take your current selection, hit the **RECOMMEND NOW** button!")
recommend_now = st.button("RECOMMEND NOW")
if recommend_now:
    recommend()



