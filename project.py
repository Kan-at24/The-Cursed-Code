import streamlit as st
import random
import base64
import requests
st.set_page_config(page_title="Whispers in the Dark: An AI Horror Experience",page_icon="👻",layout="wide")
for key, default in {
    'user_authenticated': False,
    'username': "",
    'password': "",
    'story': "",
    'story_progress': [],
    'current_step': 0,
    'branch': "",
    'used_twists': [],
    'step':6,
    'story_complete': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
st.title("👻 WHISPERS IN THE DARK")
st.header(" An AI Horror Experience")
st.subheader("Your choices write the fear.")
st.markdown("*Whispers in the Dark is an AI-powered interactive horror experience where every decision you make changes the narrative. The system dynamically generates chilling scenarios, reactions, and outcomes using AI, creating a unique story of fear for every player.*")
if not st.session_state.user_authenticated:
    st.subheader("Register to begin your journey")
    st.markdown("*Your account will keep your choices safe and allow you to unlock your completed story later*")
    username_input = st.text_input("Choose a username")
    password_input = st.text_input("Choose a password", type="password")
    if st.button("Register"):
        if username_input and password_input:
            st.session_state.username = username_input
            st.session_state.password = password_input
            st.session_state.user_authenticated = True
            st.session_state.current_step = 1
            st.success(f"Welcome, {username_input}! Now you can start the story.")
        else:
            st.warning("Please enter both username and password.")
if st.session_state.user_authenticated:
    st.subheader(f"Hello {st.session_state.username}, choose your story beginning:")
    twist_pool = [
        "…and you realize the story itself is staring back at you.",
        "…and every word you just read disappears from your memory instantly.",
        "…and you discover your own name engraved on a tombstone… in the future.",
        "…suddenly, your shadow moves on its own and waves goodbye.",
        "…and the floor beneath you opens into a void shaped like your living room.",
        "…then your hands vanish—but your mind is still awake.",
        "…and a stranger in the distance is holding a book… with your life written in it.",
        "…suddenly, everyone around you starts speaking in a language you invented as a child.",
        "…and you hear your own heartbeat narrating your fears aloud.",
        "…then the sky fractures like broken glass, revealing a different city beneath it.",
        "…and your phone rings—but the caller ID says -You.",
        "…then the furniture in the room rearranges itself into a message: 'Run…'",
        "…and all the clocks stop… except one counting down to a day that hasn’t happened yet.",
        "…then you open a door and step into another version of yourself reading this story.",
        "…and the walls start breathing, inhaling your memories with each pulse.",
        "…and the story’s ending is scribbled on your own hand in ink you never applied.",
        "…then you hear a voice whisper: 'You have been chosen… but not for this life.'",
        "…and the rain outside falls upward, carrying your screams with it.",
        "…then your reflection winks, even though you didn’t move.",
        "…and the floor tiles spell out your deepest secret.",
        "…then the room collapses—but you wake up in the exact same spot, unharmed… yet hours have passed.",
        "…and the mirror shows the ceiling as the floor, and the floor as the sky.",
        "…then your own voice calls your name from somewhere you know you’ve never been.",
        "…and a calendar on the wall counts down to a date you thought didn’t exist.",
        "…then the lights flicker and you see your own shadow leaving the room.",
        "…and you realize every story you have read is about you—but rewritten each time.",
        "…then the page you were reading burns in reverse, as if time itself is undoing you.",
        "…and someone whispers your future… while standing behind you, though the room is empty.",
        "…then the walls pulse like a heartbeat, synchronized with yours.",
        "…and your shoes walk ahead of you, dragging your body behind.",
        "…then a letter appears in your hand, written by you… 20 years in the future.",
        "…and the shadow in the corner waves… even though it has no source.",
        "…then every sound around you repeats one second later, like the world is lagging behind.",
        "…and you see your name on a gravestone… but you’re holding the tombstone in your hands.",
        "…then the staircase spirals endlessly, yet you’re already at the top.",
        "…and the wind whispers your secrets—ones you’ve never told anyone.",
        "…then the story itself laughs, and you hear your own voice joining in.",
        "…and the room’s door leads to a forest that mirrors your childhood memories—but twisted.",
        "…then the ceiling opens like a mouth, inhaling the light around you.",
        "…and someone unseen flips the pages of your life, skipping chapters at will.",
        "…then you blink, and everyone in the room has vanished—except a note that says: ‘Stay.’",
        "…and your reflection holds a knife—but your hands are empty.",
        "…and suddenly, everyone around you vanished—except yourself, and a note saying, ‘Welcome to the experiment.’",
        "…then you realize you’ve been reading your own obituary all along.",
        "…and the world outside your window no longer recognizes your existence.",
        "…only to discover your reflection is laughing… without you moving.",
        "…and you hear a voice from the sky: ‘You forgot you were already dead.’",
        "…then every memory you had of your life flickers like a corrupted video file.",
        "…and the story you were in was someone else’s diary all along—except your name is written at the end.",
        "…suddenly, time freezes, and your body becomes the observer of itself, unable to move or speak.",
        "…and the lights go out—but the darkness itself whispers, ‘We’ve been waiting.’",
        "…and you discover that every choice you ever made was just a simulation someone else was playing.",
        "…then you wake up in a room full of clocks counting backwards—each second erasing something you once loved.",
        "…and the page you were reading tears itself out… revealing a photo of you from decades ago, staring back with a warning: ‘Do not return.’"
    ]
    def non_twist(branch_text, option1_text, option1_narrative,branch_1, option2_text, option2_narrative,branch_2):
        st.subheader(branch_text)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(option1_text):
                st.session_state.story_progress.append(option1_narrative)
                st.session_state.current_step += 1
                st.session_state.branch =branch_1
                st.rerun()
        with col2:
            if st.button(option2_text):
                st.session_state.story_progress.append(option2_narrative)
                st.session_state.current_step += 1
                st.session_state.branch =branch_2
                st.rerun()
    def twist(branch_text, option1_text, option1_narrative, option2_text, option2_narrative):
        st.subheader(branch_text)
        col1, col2 = st.columns(2)
        def pick_twist_and_progress(narrative):
            st.session_state.story_progress.append(narrative)
            available_twists = [t for t in twist_pool if t not in st.session_state.used_twists]
            if available_twists:
                twist = random.choice(available_twists)
                st.session_state.used_twists.append(twist)
                st.session_state.story_progress.append(f"Twist: {twist}")
            st.session_state.story_complete=True
            st.session_state.current_step += 1
            st.session_state.story = "\n".join(st.session_state.story_progress)
            st.rerun()
        with col1:
            if st.button(option1_text):
                pick_twist_and_progress(option1_narrative)
        with col2:
            if st.button(option2_text):
                pick_twist_and_progress(option2_narrative)     
    def twist_hospital(branch_text, option1_text, option1_narrative, option2_text, option2_narrative):
        st.subheader(branch_text)
        col1, col2 = st.columns(2)
        def pick_twist_and_progress(narrative):
            st.session_state.story_progress.append(narrative)
            available_twists = [t for t in twist_pool if t not in st.session_state.used_twists]
            if available_twists:
                twist = random.choice(available_twists)
                st.session_state.used_twists.append(twist)
                st.session_state.story_progress.append(f"Twist: {twist}")
            st.session_state.story_complete=True
            st.session_state.current_step += 1
            st.session_state.story = "\n".join(st.session_state.story_progress)
            st.success("You survived… but the hospital still whispers.")
            st.rerun()
        with col1:
            if st.button(option1_text):
                pick_twist_and_progress(option1_narrative)
        with col2:
            if st.button(option2_text):
                pick_twist_and_progress(option2_narrative)     
    def twist_forest(branch_text, option1_text, option1_narrative, option2_text, option2_narrative):
        st.subheader(branch_text)
        col1, col2 = st.columns(2)
        def pick_twist_and_progress(narrative):
            st.session_state.story_progress.append(narrative)
            available_twists = [t for t in twist_pool if t not in st.session_state.used_twists]
            if available_twists:
                twist = random.choice(available_twists)
                st.session_state.used_twists.append(twist)
                st.session_state.story_progress.append(f"Twist: {twist}")
            st.session_state.story_complete=True
            st.session_state.current_step += 1
            st.session_state.story = "\n".join(st.session_state.story_progress)
            st.success("The forest story concludes with this chilling twist!")
            st.rerun()
        with col1:
            if st.button(option1_text):
                pick_twist_and_progress(option1_narrative)
        with col2:
            if st.button(option2_text):
                pick_twist_and_progress(option2_narrative)
    def twist_carnival(branch_text, option1_text, option1_narrative, option2_text, option2_narrative):
        st.subheader(branch_text)
        col1, col2 = st.columns(2)
        def pick_twist_and_progress(narrative):
            st.session_state.story_progress.append(narrative)
            available_twists = [t for t in twist_pool if t not in st.session_state.used_twists]
            if available_twists:
                twist = random.choice(available_twists)
                st.session_state.used_twists.append(twist)
                st.session_state.story_progress.append(f"Twist: {twist}")
            st.session_state.story_complete=True
            st.session_state.current_step += 1
            st.session_state.story = "\n".join(st.session_state.story_progress)
            st.success("You escaped the carnival… but the laughter still follows you.")
            st.rerun()
        with col1:
            if st.button(option1_text):
                pick_twist_and_progress(option1_narrative)
        with col2:
            if st.button(option2_text):
                pick_twist_and_progress(option2_narrative)
    col1, col2 = st.columns(2)
    with col1:
        length_choice = st.radio("Pick story size (controls depth / complexity):",["Short (Quick scare)", "Big (Epic nightmare)"])
    with col2:
        horror_type = st.selectbox("Choose your nightmare", ["Choose","Ghosts", "Vampires", "Zombies", "Demonic possession"])
    def set_background(image_path):
        with open(image_path,"rb") as f:
            data=f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    if(horror_type=="Choose"):
        set_background("images/front.png")
    elif(horror_type=="Ghosts"):
        set_background("images/Ghost.png")
    elif(horror_type=="Vampires"):
        set_background("images/Vampire.png")
    elif(horror_type=="Zombies"):
        set_background("images/Zombie.png")
    elif(horror_type=="Demonic possession"):
        set_background("images/Demonic.png")
    with st.expander("📖 Story Tracker", expanded=True):
        if st.session_state.story_progress:
            full_story = "\n".join(st.session_state.story_progress)
            st.text_area("Your Story So Far:", value=full_story, height=300, disabled=True)
        else:
            st.caption("No choices made yet. Start your journey...")
    if st.button("🔄 Restart Story"):
        st.session_state.story_progress = []
        st.session_state.current_step = 1
        st.session_state.branch = ""
        st.session_state.used_twists = []
        st.session_state.story_complete=False 
        st.rerun()
    # --- Short Story Beginnings ---
    if length_choice == "Short (Quick scare)" and st.session_state.current_step == 1:
        st.subheader("Choose Your Beginning:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("You step into a dark corridor of the abandoned school, the floorboards creaking under your feet."):
                st.session_state.story_progress.append("You step into a dark corridor of the abandoned school, the floorboards creaking under your feet.")
                st.session_state.current_step += 1
                st.rerun()
        with col2:
            if st.button("A dense fog rolls across the graveyard, and faint whispers seem to come from every shadowed corner."):
                st.session_state.story_progress.append("A dense fog rolls across the graveyard, and faint whispers seem to come from every shadowed corner.")
                st.session_state.current_step += 1
                st.rerun()
        with col3:
            if st.button("The old mansion's front door groans as you push it open, and the smell of damp wood fills your nose."):
                st.session_state.story_progress.append("The old mansion's front door groans as you push it open, and the smell of damp wood fills your nose.")
                st.session_state.current_step += 1
                st.rerun()

    # --- Step 2: Corridor Choice ---
    if st.session_state.current_step == 2 and st.session_state.story_progress:
        st.session_state.step=4
        last_step = st.session_state.story_progress[-1]
        if last_step.startswith("You step into a dark corridor"):
            non_twist("The corridor stretches before you... What do you do?","Open the classroom door with faint scratching inside","You open the classroom door and hear scratching — something is moving inside...", "school_classroom","Walk deeper toward the broken stairwell","You walk deeper into the hallway toward the broken stairwell, the air colder with each step...", "school_stairwell")
    # --- Step 3: School Classroom Branch ---
    if st.session_state.current_step == 3 and st.session_state.branch == "school_classroom":
        non_twist("Something strange happens... What do you do next?","Investigate the sound coming from the shadows","You follow the eerie sound, noticing shadows dancing on the walls...","school_classroom_follow","Hide behind the broken furniture and observe", "You hide behind a broken desk and see a pale figure drifting across the corridor..." ,"school_classroom_hide")
    # --- Step 3: School Stairwell Branch ---
    if st.session_state.current_step == 3 and st.session_state.branch == "school_stairwell":
        non_twist("The stairwell creaks ominously. What do you do next?","Climb the stairs quietly, listening for sounds above","You cautiously climb the broken stairs, each step threatening to give way...","school_stair_climb","Descend the stairs into the dark basement","You step down into the darkness of the basement, the air thick and cold...","school_stair_basement")
    # --- Step 4 Example: Add Twist for School Classroom Follow ---
    if st.session_state.current_step == 4 and st.session_state.branch == "school_classroom_follow":
        twist("The hallway grows darker... What do you do next?","Confront the pale figure drifting across the corridor","You gather your courage and confront the pale figure, its eyes glowing eerily...","Run toward the exit, heart pounding","You sprint down the hallway toward the exit, the shadows seeming to reach for you...")
    # --- Step 4: school_classroom_hide (Final Step with Twist) ---
    if st.session_state.current_step == 4 and st.session_state.branch == "school_classroom_hide":
        twist("You hide behind the broken furniture... What do you do next?","Wait silently and watch the figure move closer","You wait silently, your heart pounding as the pale figure drifts closer.","Sneak out quietly and explore another room","You carefully sneak out from your hiding spot and tiptoe toward another room, trying not to make a sound.")
    # --- Step 4: school_stair_climb ---
    if st.session_state.current_step == 4 and st.session_state.branch == "school_stair_climb":
        twist("You reach the top of the stairs, the corridor ahead shrouded in darkness. What do you do?","Enter the room with the flickering light","You step into the room, the light flickering across broken furniture and cobwebs...","Peek through the doorway silently and observe","You cautiously peek through the doorway, your breath held as shadows move inside...")
    # --- Step 4: school_stair_basement ---
    if st.session_state.current_step == 4 and st.session_state.branch == "school_stair_basement":
        twist("You step into the dark basement. The air is thick and cold. What do you do?","Explore the shadowy corner with strange noises","You cautiously move toward the shadowy corner where you hear faint noises, your flashlight trembling in your hand...","Head toward the old storage room, hoping to find clues","You make your way toward the old storage room, the shelves casting eerie shadows as you try to stay quiet...")
    # --- Step 2: graveyard Choice ---
    if st.session_state.current_step == 2 and st.session_state.story_progress:
        last_step = st.session_state.story_progress[-1]
        if last_step.startswith("A dense fog rolls"):
            non_twist("The fog thickens, and shadows move eerily around you... What do you do?","Follow the faint whispers deeper into the fog","You decide to follow the faint whispers, your footsteps muffled by the thick fog. Shapes loom ahead...", "graveyard_follow","Stay on the path and try to find the exit quickly","You stick to the faintly visible path, heart pounding, trying to find your way out as the whispers seem to grow louder...", "graveyard_escape")
    # --- Step 3: Graveyard Follow Branch ---
    if st.session_state.current_step == 3 and st.session_state.branch == "graveyard_follow":
        non_twist("The whispers grow louder, almost calling your name. Shadows swirl around the tombstones... What do you do next?","Step closer to the source of the whispers","You bravely step closer to the source, the whispers now forming eerie words you almost recognize...","graveyard_whisper_source","Hide behind a tombstone and observe silently","You hide behind a weathered tombstone, watching as shadows twist and flicker unnaturally in the fog...","graveyard_hide")
    # --- Step 3: Graveyard Escape Branch ---
    if st.session_state.current_step == 3 and st.session_state.branch == "graveyard_escape":
        non_twist("The fog swirls around you, and the whispers echo in the distance. You sense movement nearby... What do you do next?","Run quickly along the path, ignoring the whispers","You dash along the barely visible path, ignoring the ghostly whispers, but shadows seem to reach out from the fog...","graveyard_escape_run","Turn back and confront the source of the whispers","Heart pounding, you turn back toward the origin of the whispers, ready to face whatever lurks within the fog...","graveyard_escape_confront")
    # --- Step 4: Graveyard Whisper Source ---
    if st.session_state.current_step == 4 and st.session_state.branch == "graveyard_whisper_source":
        twist("The whispers now sound like your own voice, coming from a shadowy figure ahead... What do you do next?","Reach out to touch the shadowy figure","You cautiously reach out, and the shadowy figure shivers under your hand, revealing a hidden, glowing amulet...","Step back and run deeper into the fog","Fear grips you, and you dash into the thick fog. Shadows twist around you, whispering secrets you can't quite hear...")
    # --- Step 4: Graveyard Hide ---
    if st.session_state.current_step == 4 and st.session_state.branch == "graveyard_hide":
        twist("The shadows swirl more violently, and a cold wind grazes your neck... What do you do next?","Step out and confront the shadows","Summoning courage, you step out from behind the tombstone and face the swirling shadows. A chilling figure emerges, pointing directly at you...","Crawl quietly toward the exit","You crouch low and move silently through the fog, shadows seeming to stretch and whisper around you as you make your escape..." )
    # --- Step 4: Graveyard Escape Run ---
    if st.session_state.current_step == 4 and st.session_state.branch == "graveyard_escape_run":
        twist("The fog swirls around you, and the whispers echo in the distance. You sense movement nearby... What do you do next?","Brace yourself and face the fog head-on","You take a deep breath and step into the living fog. The shadows seem to part before you, as if recognizing your courage...","Fall to your knees and scream","Overwhelmed by fear, you collapse to the ground and scream into the fog. For a moment, the shadows twist violently before vanishing...")
    # --- Step 4: Graveyard Escape Confront ---
    if st.session_state.current_step == 4 and st.session_state.branch == "graveyard_escape_confront":
        twist("A shadowy figure blocks your path, whispering your name. What do you do next?","Stand your ground and confront the figure","Summoning all your courage, you face the shadowy figure. Its form flickers, revealing a familiar face twisted in a ghostly grin...","Turn and sprint past the figure into the fog","Heart pounding, you dash past the shadowy figure into the thick fog. The whispers chase you, echoing your own thoughts...")
    # --- Step 2: Mansion Entrance Choice ---
    if st.session_state.current_step == 2 and st.session_state.story_progress:
        last_step = st.session_state.story_progress[-1]
        if last_step.startswith("The old mansion's front door groans"):
            non_twist("The mansion's interior is dark and musty. Shadows seem to move on their own... What do you do next?","Explore the grand hall quietly","You step into the grand hall, the floorboards creaking under your feet. Portraits on the walls seem to watch you...", "mansion_grandhall","Ascend the creaking staircase","You cautiously climb the grand staircase. Each step groans, and a cold draft brushes past you...", "mansion_staircase")
    # --- Step 3: Mansion Grand Hall ---
    if st.session_state.current_step == 3 and st.session_state.branch == "mansion_grandhall":
        non_twist("The grand hall stretches before you. Shadows flicker along the walls. What do you do next?","Investigate the flickering portraits","You approach the portraits, noticing that the eyes seem to follow your every move. A chill runs down your spine...","mansion_grandhall_investigate","Move quietly toward the side door","You slip toward the side door, trying not to make a sound. The floorboards creak faintly under your feet...","mansion_grandhall_side")
    # --- Step 3: Mansion Staircase ---
    if st.session_state.current_step == 3 and st.session_state.branch == "mansion_staircase":
        non_twist("The staircase leads to a dimly lit corridor. The air is cold and heavy. What do you do next?","Enter the room with the flickering candle","You cautiously enter the room, the flickering candle casting long, twisted shadows across the furniture...","mansion_room_candle","Peek into the dark hallway to the left","You peek into the dark hallway. The walls seem to close in, and a strange whisper brushes past your ear...","mansion_hallway_left")
    # --- Step 4: Mansion Grand Hall Investigate ---
    if st.session_state.current_step == 4 and st.session_state.branch == "mansion_grandhall_investigate":
        twist("The portraits’ eyes seem alive, following your every move. What do you do next?","Touch the closest portrait","You reach out and touch the frame. Suddenly, the eyes blink and the image shifts into a screaming face...","Step back and examine the hall silently","You cautiously step back, trying to take in the hall. The shadows twist unnaturally, almost forming figures that watch you...")
    # --- Step 4: Mansion Grand Hall Side ---
    if st.session_state.current_step == 4 and st.session_state.branch == "mansion_grandhall_side":
        twist("The side door leads to a narrow corridor shrouded in darkness. What do you do next?","Proceed carefully down the corridor","You move forward, each step echoing ominously. The walls seem to whisper secrets you can't understand...","Peek through a small window to see what's ahead","You peer through a cracked window. Outside, shadows move in impossible ways, and a chilling wind brushes your face...")
        # --- Step 4: Mansion Room with Candle ---
    if st.session_state.current_step == 4 and st.session_state.branch == "mansion_room_candle":
        twist("The flickering candle illuminates strange symbols on the walls. What do you do next?","Examine the symbols closely","You move closer, tracing the symbols with your fingers. The shapes seem to shift under your gaze...","Blow out the candle and move into darkness","You extinguish the candle, plunging the room into darkness. Every shadow seems alive and watching...")                                                           
    # --- Step 4: Mansion Hallway Left ---
    if st.session_state.current_step == 4 and st.session_state.branch == "mansion_hallway_left":
        twist("The dark hallway stretches ahead, with strange noises echoing from the walls. What do you do next?","Move cautiously forward, listening for sounds","You step forward, each footfall echoing ominously. Something skims past the walls, barely visible...","Peek into a shadowed room on the right","You glance into the room. The shadows twist unnaturally, forming shapes that resemble hands reaching out...")


    # --- Big Story Beginnings ---
    if length_choice == "Big (Epic nightmare)" and st.session_state.current_step == 1:
        st.subheader("Choose Your MBig Story Beginning:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("You find yourself in a deserted hospital wing, flickering lights revealing peeling wallpaper and empty gurneys."):
                st.session_state.story_progress.append("You find yourself in a deserted hospital wing, flickering lights revealing peeling wallpaper and empty gurneys.")
                st.session_state.current_step += 1
                st.session_state.branch = "hospital_beginning"
                st.rerun()
        with col2:
            if st.button("The forest trail twists unnaturally, and the wind carries voices that mimic your own."):
                st.session_state.story_progress.append("The forest trail twists unnaturally, and the wind carries voices that mimic your own." )
                st.session_state.current_step += 1
                st.session_state.branch = "forest_beginning"
                st.rerun()
        with col3:
            if st.button("Walking into the dimly lit carnival, you notice the rides are rusted, but laughter echoes faintly in the distance."):
                st.session_state.story_progress.append("Walking into the dimly lit carnival, you notice the rides are rusted, but laughter echoes faintly in the distance.")
                st.session_state.current_step += 1
                st.session_state.branch = "carnival_beginning"
                st.rerun()


    # --- Step 2: Hospital Branch ---
    if st.session_state.current_step == 2 and st.session_state.branch == "hospital_beginning":
        non_twist("The hospital wing is eerie and silent. What do you do?","Explore the gurneys for clues","You cautiously explore the gurneys, finding abandoned medical tools and old patient charts.", "hospital_gurneys","Walk down the flickering hallway","You walk carefully down the flickering hallway, the peeling wallpaper revealing strange stains.", "hospital_hallway")
    # --- Step 3: Hospital Gurneys ---
    if st.session_state.current_step == 3 and st.session_state.branch == "hospital_gurneys":
        non_twist("As you inspect the gurneys, a faint movement catches your eye. What do you do?","Investigate the movement in the shadows","You step closer to the shadow and notice a pale figure shifting between the gurneys.", "hospital_gurneys_investigate","Hide behind a gurney and observe","You duck behind a gurney, heart racing, watching the pale figure drift silently across the room.", "hospital_gurneys_hide")
    # --- Step 3: Hospital Hallway ---
    if st.session_state.current_step == 3 and st.session_state.branch == "hospital_hallway":
        non_twist("The hallway stretches into darkness, doors on either side creaking slightly. What will you do?","Enter the nearest patient room","You push open the nearest door. Inside, the room is eerily preserved—an untouched bed, medical charts scattered, and a faint beeping sound echoing from nowhere.", "hospital_room_nearest","Continue walking down the dark hallway","You ignore the side rooms and continue. The flickering lights seem to follow you,and a shadow just ahead slips out of sight.", "hospital_hallway_continue")
    # --- Step 4: Hospital Gurneys Investigate ---
    if st.session_state.current_step == 4 and st.session_state.branch == "hospital_gurneys_investigate":
        non_twist("The gurneys are lined up against the wall, their wheels rusted, sheets torn and stained. You feel uneasy as you move closer...","Lift the stained sheet covering one gurney","With trembling hands, you pull the sheet back. The gurney is empty—except for a set of bloody handprints smeared across the metal surface.","hospital_gurney_sheet","Check beneath the gurneys","You crouch down and peek beneath. The shadows seem to twist unnaturally, and a pair of pale fingers curl out from the darkness—then vanish as if they were never there.","hospital_gurney_beneath")
    # --- Step 4: Hospital Gurneys Hide ---
    if st.session_state.current_step == 4 and st.session_state.branch == "hospital_gurneys_hide":
        non_twist("You squeeze yourself behind one of the gurneys, your breath shallow as the air grows colder...","Stay hidden and listen","You hold your breath as footsteps echo down the hallway. They stop right near your hiding spot. A voice whispers your name, though you never told anyone you were here..." ,"hospital_hid_listen","Peek out from your hiding spot","Slowly, you peek out. The corridor is empty—or so it seems. A shadow, tall and thin, flickers across the wall, ","hospital_hid_peek")
    # --- Step 4: Hospital Room Nearest ---
    if st.session_state.current_step == 4 and st.session_state.branch == "hospital_room_nearest":
        non_twist("You slip quietly into the nearest hospital room, the smell of antiseptic still lingering...","Inspect the medical equipment on the side table","You notice dusty surgical tools scattered across the table. One of them is wet—freshly used. ","hospital_room_equipment","Check the patient bed, something seems to be moving beneath the sheets","The bed creaks as something shifts under the sheets. You slowly approach, unsure if it’s alive—or something far worse.","hospital_room_bed")
    # --- Step 4: Hospital Hallway Continue ---
    if st.session_state.current_step == 4 and st.session_state.branch == "hospital_hallway_continue":
        non_twist("The hallway stretches endlessly, the flickering lights making shadows dance across the peeling walls...","Follow the shadow toward the door","A tall shadow glides across the far wall, vanishing near a door at the end of the hall. Something compels you to follow it, though your instincts scream to turn back.","hospital_shadow_door","Retreat silently and hide","You step back slowly, trying not to make a sound. But the floorboards betray you with a loud creak. The shadows stop moving... and seem to listen.","hospital_hallway_hide")
    
    # --- Step 5: Hospital Gurney Sheet Paths ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_gurney_sheet":
        non_twist("The mannequin’s eyes roll toward you, its porcelain mouth cracking into a smile...","Back away toward the hallway","You stumble back in horror, bumping into the cold wall. When you glance back at the gurney—the mannequin is gone.","hospital_sheet_backaway","Grab a surgical tool to defend yourself","You snatch a rusted scalpel from a tray nearby, clutching it tightly. The mannequin twitches, as if mocking your attempt at defense.","hospital_sheet_defend")
    # --- Step 5: Hospital Gurney Beneath ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_gurney_beneath":
        non_twist("You crouch down, peering beneath the gurney... Something stirs in the darkness.","Pull the figure out from under the gurney","You reach under the gurney and drag out a figure wrapped in decaying bandages. It wheezes, head turning unnaturally toward you.","hospital_beneath_pull","Back away before it notices you","You step back slowly, heart hammering in your chest. The figure crawls out anyway, dragging itself toward you with jagged movements.","hospital_beneath_backaway")
    # --- Step 5: Hospital Hide and Listen ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_hid_listen":
        non_twist("You hold your breath and listen... The sound grows clearer.","Follow the whispers deeper into the wing","The whispers weave into words you almost understand, luring you further down the dim corridor toward a locked operating theater.","hospital_listen_follow","Stay hidden and wait for the source to reveal itself","You press yourself tighter against the shadows. After moments of silence, a figure cloaked in hospital robes glides past—its face hidden beneath gauze.","hospital_listen_wait")
    # --- Step 5: Hospital Hide and Peek ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_hid_peek":
        non_twist("You carefully peek from behind the curtain, the hallway dimly lit and eerily silent...","Step into the hallway to investigate","You tiptoe into the hallway, noticing shadows that twist unnaturally across the walls. The lights flicker with every step.","hospital_peek_step","Retreat further into the room and hide deeper","You squeeze into the far corner, holding your breath. Something brushes past the doorway, almost whispering your name.","hospital_peek_hide")
    # --- Step 5: Hospital Room Equipment ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_room_equipment":
        non_twist("The medical equipment seems to move on its own, rattling and clanging eerily...","Investigate the source of the movement","You step closer to the surgical tools. They shift slightly, forming a path leading to the far corner of the room.","hospital_equipment_investigate","Step back and look for another exit","You glance around nervously, spotting a partially open door at the other end. The tools clang violently as if warning you not to leave.","hospital_equipment_exit")
    # --- Step 5: Hospital Room Bed ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_room_bed":
        non_twist("You approach the patient bed, the sheets twitching slightly as if something is beneath them...","Lift the sheets quickly","You yank the sheets off the bed, revealing a pale figure that blinks at you with hollow eyes.","hospital_bed_lift","Step back and observe silently","You hold your position, watching as the sheets ripple unnaturally, forming shapes that vanish when you blink.","hospital_bed_observe")
    # --- Step 5: Hospital Shadow Door ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_shadow_door":
        non_twist("A dark shadow slips through the partially open door, stretching unnaturally across the floor...","Follow the shadow into the room","You step cautiously into the room, your footsteps silent. The shadow moves ahead, leading you toward a desk covered in strange medical instruments.","hospital_shadow_follow","Close the door quietly and hide nearby","You press yourself against the wall, heart pounding, as the shadow stretches and twists, seeming to search for something—or someone.","hospital_shadow_hide")
    # --- Step 5: Hospital Hallway Hide ---
    if st.session_state.current_step == 5 and st.session_state.branch == "hospital_hallway_hide":
        non_twist("You press yourself against the wall in the hallway, barely breathing, listening to the eerie silence...","Creep forward slowly to see what's ahead","You inch forward, shadows flickering across the walls as if moving with you. Something sharp brushes past your shoulder, sending chills down your spine.","hospital_hallway_creep","Stay hidden and wait for the footsteps to pass","You stay completely still, the footsteps echoing louder until they fade away. A faint whisper seems to brush your ear, but no one is there.","hospital_hallway_wait")
    # --- Step 6: Hospital Sheet Back Away ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_sheet_backaway":
        non_twist("You take a cautious step back, the sheets still twitching under the dim light...","Look under the bed quickly","You peek under the bed, catching a glimpse of something pale and twisted staring back at you.","hospital_sheet_peek","Retreat to the doorway and observe silently","You move back toward the doorway, pressing yourself against the frame. The bed twitches again, but you remain hidden in the shadows.","hospital_sheet_observe")
    # --- Step 6: Hospital Sheet Defend ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_sheet_defend":
        non_twist("You grab a nearby object to defend yourself as the sheets move violently...","Strike under the sheets with the object","You hit the sheets and a figure lunges out, revealing pale eyes that seem to pierce your soul.","hospital_sheet_attack","Step back and brace for whatever emerges","You stumble back, heart racing, as the sheets lift slowly to reveal a twisted shadow with a ghastly grin.","hospital_sheet_brace")
    # --- Step 6: Hospital Beneath Pull ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_beneath_pull":
        non_twist("Something grabs your ankle from beneath the bed, yanking you slightly toward the darkness...","Pull yourself free and run toward the door","You struggle and free yourself, sprinting toward the door as the unseen force retreats into the shadows.","hospital_beneath_escape","Hold on and investigate what’s beneath","You hold your ground, peering beneath the bed. A pale hand reaches out slowly, and a faint whisper calls your name.","hospital_beneath_investigate")
    # --- Step 6: Hospital Beneath Back Away ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_beneath_backaway":
        non_twist("You take cautious steps backward, the shadows beneath the bed stirring ominously...","Retreat to the doorway and watch silently","You step back toward the doorway, peering carefully. A shadowy figure shifts beneath the bed, almost like it’s aware of your presence.","hospital_beneath_watch","Slowly crouch and try to peek under the bed","You crouch low, eyes fixed under the bed. Something stirs — a pale hand? — before disappearing back into the darkness.","hospital_beneath_peek")
    # --- Step 6: Hospital Listen Follow ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_listen_follow":
        non_twist("You strain your ears and follow the faint, eerie sounds echoing through the hall...","Approach the source cautiously","You move slowly toward the whispers, each step echoing in the empty hallway. A shadow shifts ahead, drawing your attention.","hospital_whisper_source","Hide and observe the corridor silently","You press against the wall, holding your breath as the whispers grow louder. Shapes move in the dim light, but you remain unseen.","hospital_hide_observe")
    # --- Step 6: Hospital Listen Wait ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_listen_wait":
        non_twist("You remain frozen, listening intently to the faint sounds around you...","Step toward the origin of the sound slowly","Carefully, you step toward the source of the whispers. A shadow flits across the wall, and your pulse quickens.","hospital_sound_source","Stay hidden and let the sound pass","You press yourself against the wall, hoping the mysterious noises will pass by. The air grows colder, and the whispers seem to swirl around you.","hospital_sound_hidden")
    # --- Step 6: Hospital Peek Step ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_peek_step":
        non_twist("You lean closer to peek beneath the sheets, your heart pounding...","Quickly pull the sheet aside to see what’s underneath","You yank the sheet away and catch a glimpse of something moving, a pale hand or a shadowy figure.","hospital_peek_reveal","Step back slowly and observe from a distance","You retreat a little, trying to watch without being noticed. The shadows beneath the sheet seem to twitch as if aware of your gaze.","hospital_peek_watch")
    # --- Step 6: Hospital Peek Hide ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_peek_hide":
        non_twist("You crouch low, hiding behind the gurney, watching the shadows shift beneath the sheet...","Move closer to get a better look","You edge closer, careful not to make a sound.The sheet twitches as if something beneath it senses you.","hospital_hide_reveal","Stay hidden and wait silently","You hold your position, eyes fixed on the sheet. A faint whisper echoes, sending chills down your spine.","hospital_hide_listen")
    # --- Step 6: Hospital Equipment Investigate --
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_equipment_investigate":
        non_twist("You approach the medical equipment, some tools gleaming under the flickering lights...","Examine the surgical tools closely","You inspect the instruments carefully. Suddenly, a scalpel moves slightly, as if guided by an unseen hand.","hospital_tools_movement","Step back and look around the room","You take a few steps back, scanning the room. Shadows shift oddly, and the lights flicker more violently.","hospital_tools_shadow")
    # --- Step 6: Hospital Equipment Exit ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_equipment_exit":
        non_twist("You decide it’s best to leave the eerie room behind...","Exit through the main door cautiously","You step toward the door, careful not to make a sound. The shadows behind the equipment seem to stretch as you move.","hospital_exit_hallway","Use the side corridor to sneak out","You slip into the side corridor, the air thick and cold. Faint whispers follow you as you move quickly.","hospital_exit_side")
    # --- Step 6: Hospital Bed Lift ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_bed_lift":
        non_twist("You lift the sheets on the patient bed, heart racing...","Reveal what’s under the sheets immediately","You pull the sheets away and are met with a horrifying sight — a pale, lifeless form that twitches unnaturally.","hospital_bed_reveal","Step back cautiously and observe first","You hesitate, watching carefully. Something beneath the sheets shifts as if it knows you are there.","hospital_bed_watch")
    # --- Step 6: Hospital Bed Observe ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_bed_observe":
        non_twist("You carefully observe the bed, noticing subtle movements beneath the sheets...","Move closer to inspect the movements","You lean in, trying to see clearly. The shadows beneath the sheets seem to reach for you.","hospital_bed_inspect","Step back and remain hidden","You retreat slightly, hiding behind a gurney. A faint whisper echoes, raising goosebumps.","hospital_bed_hidden")
    # --- Step 6: Hospital Shadow Follow ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_shadow_follow":
        non_twist("You decide to follow the shadow that slipped past the doorway...","Follow the shadow deeper into the hallway","You creep down the hallway, each step echoing. The shadow twists unnaturally, as if inviting you further.","hospital_shadow_deeper","Hide and observe the shadow from afar","You stay hidden, peering around the corner. The shadow pauses, then moves in a way that defies logic.","hospital_shadow_watch")
    # --- Step 6: Hospital Shadow Hide ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_shadow_hide":
        non_twist("You hide behind the corner, holding your breath as the shadow moves silently...","Peek around the corner to follow the shadow","You carefully peek, noticing the shadow twist and contort unnaturally as it glides forward.","hospital_shadow_peek","Stay hidden and wait","You remain hidden, listening. The faintest whisper of movement passes by, sending chills down your spine.","hospital_shadow_wait")
    # --- Step 6: Hospital Hallway Creep ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_hallway_creep":
        non_twist("You creep along the dimly lit hallway, every step echoing in the silence...","Move forward cautiously toward the source of the noise","You inch forward, noticing shadows stretching unnaturally across the peeling walls.","hospital_hallway_source","Hide behind the gurney and observe","You duck behind a gurney, watching silently as something moves in the distance, almost human but not.","hospital_hallway_hidden")
    # --- Step 6: Hospital Hallway Wait ---
    if st.session_state.current_step == 6 and st.session_state.branch == "hospital_hallway_wait":
        non_twist("You wait silently in the hallway, listening to every creak and whisper...","Step forward slowly to investigate the source of the noise","You step cautiously, your eyes adjusting to the flickering light. Shadows seem to move against logic.","hospital_hallway_investigate","Remain in place and observe longer","You stay put, feeling the hairs on your neck stand up. Something unseen brushes past you, leaving a cold trace.","hospital_hallway_observe")
    # --- Step 7: Hospital Sheet Peek Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sheet_peek":
       twist_hospital("You confront the sheet, and the final revelation awaits...", "Pull the sheet completely to uncover the mystery","With a deep breath, you yank the sheet away, revealing a shadowy figure frozen in place.","Step back and let it reveal itself slowly", "You hesitate, letting the shadows beneath the sheet shift and twist as if alive.")
    # --- Step 7: Hospital Sheet Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sheet_observe":
       twist_hospital("The shadow beneath the sheet reveals its secret as you observe...","Step closer to finally see what's under the sheet","You inch forward cautiously, peering under the sheet, heart racing with anticipation.","Move back slightly and watch it from a distance","You retreat a few steps, observing the sheet as it writhes strangely, almost alive.")
    # --- Step 7: Hospital Sheet Attack Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sheet_attack":
       twist_hospital("The shadow lunges as you face it directly...","Defend yourself against the shadowy figure","You brace yourself, ready to confront the shadow, your hands shaking.","Run back and avoid the shadow","Heart pounding, you sprint backward, hoping to escape the shadow's grasp.")
    # --- Step 7: Hospital Sheet Brace Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sheet_brace":
       twist_hospital("You brace yourself as the shadow stirs violently...","Stand your ground and confront the shadow","Gathering every ounce of courage, you face the shadow, muscles tense and eyes fixed.","Take a cautious step back and watch its movement","You slowly step back, observing as the shadow shifts unpredictably beneath the sheet.")
    # --- Step 7: Hospital Beneath Escape Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_beneath_escape":
       twist_hospital("You try to escape from beneath the sheet, the shadows closing in...","Dash toward the nearest exit","Heart racing, you sprint toward the nearest exit, the eerie whispers chasing you.","Hide quickly behind nearby equipment","You dive behind a medical cart, holding your breath as the shadow glides past.")
    # --- Step 7: Hospital Beneath Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_beneath_investigate":
       twist_hospital("You cautiously investigate the area beneath the sheet...","Lift the sheet carefully to see what's underneath","With trembling hands, you lift the sheet, revealing a shadowy, shifting form.","Step back and observe silently", "You retreat a few steps, watching the sheet move as if alive, holding your breath.")
    # --- Step 7: Hospital Beneath Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_beneath_watch":
       twist_hospital("You watch the shadow beneath the sheet, unsure of what will happen next...","Keep watching, ready to react","You remain frozen, eyes tracking every subtle movement of the shadow beneath the sheet.","Retreat slowly and find a safer spot","You quietly step back, searching for a corner to observe from a safer distance.")
    # --- Step 7: Hospital Beneath Peek Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_beneath_peek":
       twist_hospital("You peek beneath the sheet cautiously, every sound amplified in the quiet room...","Quickly glance to identify the source","You lift the edge of the sheet just enough to see a faint, moving silhouette beneath.","Step back and wait silently","You move back a little, observing the sheet's movement from a safer distance, your heart pounding.")
    # --- Step 7: Hospital Whisper Source Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_whisper_source":
       twist_hospital("You follow the faint whispers, trying to locate their source...","Approach the source cautiously","You move closer to the whispering sound, your footsteps barely making a sound on the cold floor.","Hide and observe the surroundings","You crouch behind a nearby gurney, watching as shadows twist and contort around the source of the whispers.")
    # --- Step 7: Hospital Hide Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hide_observe":
       twist_hospital("You stay hidden, carefully observing the eerie happenings around you...","Remain perfectly still and watch","You freeze in place, your eyes tracking every subtle movement in the shadowed corridor.","Creep slightly forward for a closer look","You inch forward carefully, trying to get a better view of the strange figure lurking ahead.")
    # --- Step 7: Hospital Sound Source Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sound_source":
       twist_hospital("You follow the mysterious sound, each step echoing through the empty wing...","Investigate the source directly","You approach the source cautiously, straining to identify its origin among the shadows.","Observe from a distance, staying hidden","You keep your distance, watching how the shadows shift around the source of the sound.")
    # --- Step 7: Hospital Sound Hidden Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_sound_hidden":
       twist_hospital("You stay hidden, listening intently to the eerie sounds echoing through the hallways...","Remain completely still and track the sound","You freeze in place, focusing on the subtle shifts and movements that reveal the sound's source.","Creep closer to the sound while staying hidden","You carefully inch forward, the shadows concealing your presence as you approach the mysterious noise.")
    # --- Step 7: Hospital Peek Reveal Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_peek_reveal":
       twist_hospital("You finally peek around the corner, revealing what lurks in the shadows...","Step forward to confront the figure","Gathering courage, you step closer to confront the shadowy figure, heart pounding.","Retreat silently and observe","You quietly step back, keeping your eyes on the figure as it moves through the eerie hallway.")
    # --- Step 7: Hospital Peek Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_peek_watch":
       twist_hospital("You watch intently from your hiding spot, trying to understand the strange events unfolding...","Move closer slowly to get a better view","You inch forward carefully, eyes fixed on the shadowy figure moving in the corridor.","Stay put and observe silently","You remain hidden, noting every subtle movement and sound, heart racing with anticipation.")
    # --- Step 7: Hospital Hide Reveal Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hide_reveal":
       twist_hospital("From your hiding spot, the figure finally steps into view, revealing something unexpected...","Step out to confront the figure","You cautiously step forward, facing the figure head-on as the tension mounts.","Stay hidden and silently observe","You remain hidden, studying the figure as it moves, uncovering chilling details from the shadows.")
    # --- Step 7: Hospital Hide Listen Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hide_listen":
       twist_hospital("You strain your ears, trying to catch every sound in the eerie silence of the hospital...","Move closer quietly to investigate the sound","You carefully creep forward, each step measured, following the faint, unsettling noises.","Stay hidden and listen carefully","You remain perfectly still, focusing on every creak and whisper, your pulse racing.")
    # --- Step 7: Hospital Tools Movement Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_tools_movement":
       twist_hospital("The surgical tools begin to shift on their own, clattering softly in the dim light...","Approach the tools to see what’s causing the movement","You step closer to the table, each tool moving slightly as if guided by an unseen hand.","Step back and observe from a distance","You retreat slightly, keeping your eyes on the tools as they move unpredictably.")
    # --- Step 7: Hospital Tools Shadow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_tools_shadow":
       twist_hospital("A shadow flickers across the wall, moving independently of any light source...","Follow the shadow cautiously","You quietly follow the shadow along the walls, trying to anticipate its next movement.","Stay put and watch the shadow","You freeze in place, carefully observing the shadow's movements as it dances eerily on the walls.")
    # --- Step 7: Hospital Exit Hallway Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_exit_hallway":
       twist_hospital("The hallway stretches endlessly, flickering lights revealing peeling walls and shadowy corners...","Move quickly toward the exit","You sprint down the hallway, adrenaline pumping, trying to escape the unsettling ambiance.","Proceed cautiously, checking every room","You move carefully down the corridor, peeking into each room, every shadow making you jump.")
    # --- Step 7: Hospital Exit Side Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_exit_side":
       twist_hospital("A narrow side corridor beckons, dimly lit and lined with abandoned equipment...","Venture down the side corridor","You step into the side corridor, every creak of the floorboards echoing ominously.","Peek into the adjacent room first","You cautiously peer into the adjacent room, shadows flickering across broken medical tools.")
    # --- Step 7: Hospital Bed Reveal Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_bed_reveal":
       twist_hospital("The sheets twitch violently, revealing a shape that shouldn’t exist...","Pull the sheets back fully","You gather your courage and pull the sheets back, revealing a horrifying figure staring back at you.","Step back and observe silently","You take a step back, watching in frozen terror as the sheets shift on their own.")
    # --- Step 7: Hospital Bed Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_bed_watch":
       twist_hospital("The figure under the sheets stirs, and the room feels colder than ever...","Approach slowly to inspect the figure","You inch closer to the bed, each breath fogging in the cold air, revealing a ghastly sight.","Step back and hide in the shadows","You retreat to the corner of the room, barely breathing, as the figure stirs mysteriously.")
    # --- Step 7: Hospital Bed Inspect Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_bed_inspect":
       twist_hospital("You lean closer to inspect the bed, heart pounding in the eerie silence...","Lift the sheets carefully","With trembling hands, you lift the sheets, revealing a horrifying figure with hollow eyes staring at you.","Step back and watch silently","You take a cautious step back, watching as the figure under the sheets moves on its own.")
    # --- Step 7: Hospital Bed Hidden Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_bed_hidden":
       twist_hospital("From your hiding spot, you notice movement beneath the sheets...","Peek from your hiding spot","You cautiously peek, and a ghastly figure slowly lifts its head, eyes glowing in the dim light.","Stay hidden and hold your breath","You remain perfectly still, heart racing, as the figure beneath the sheets stirs mysteriously.")
    # --- Step 7: Hospital Shadow Deepen Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_shadow_deeper":
       twist_hospital("The shadow deepens around you, and the hallway seems to stretch endlessly...","Step closer into the shadow","You step cautiously forward, feeling the air grow colder, and notice a ghostly figure forming within the darkness.","Retreat into the shadows and observe","You retreat slightly, trying to make sense of the shapes moving within the darkness around you.")
    # --- Step 7: Hospital Shadow Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_shadow_watch":
       twist_hospital("You keep watch as the shadow seems to move on its own, the silence broken only by faint whispers...","Move closer to the shadow","Gathering courage, you step closer, feeling an icy chill as the shadow responds to your presence.","Stay hidden and continue observing","You remain in the shadows, heart racing, as the eerie figure slowly drifts across the room.")
    # --- Step 7: Hospital Shadow Peek Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_shadow_peek":
       twist_hospital("You cautiously peek from behind the corner, noticing the shadow shifting unnaturally...","Step closer into the shadow","You inch forward, and the shadow suddenly stretches toward you, whispering your name.","Retreat and observe silently","You step back slightly, holding your breath, as the shadow seems to merge with the walls.")
    # --- Step 7: Hospital Shadow Wait Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_shadow_wait":
       twist_hospital("You hold your position, waiting as the shadow looms closer and the temperature drops...","Advance slowly toward the shadow","Summoning courage, you step forward, the shadow flickering with each heartbeat, almost alive.","Stay hidden and wait for it to pass","You crouch low, heart pounding, as the shadow drifts past you silently, leaving an icy trail behind.")
    # --- Step 7: Hospital Hallway Source Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hallway_source":
       twist_hospital("You follow the faint sound echoing through the hallway, each step making your heart race...","Move closer to the sound source","You creep forward, the whispers growing louder, until you glimpse a shadowy figure moving rapidly.","Stay back and observe silently","You hide in the shadows, eyes fixed on the figure, noting how it glides eerily across the hallway.")
    # --- Step 7: Hospital Hallway Hidden Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hallway_hidden":
       twist_hospital("You crouch in the shadows, holding your breath as the hallway seems to stretch endlessly...","Creep forward quietly","You move silently, each footstep careful, until a cold hand seems to brush past your shoulder.","Stay hidden and wait for any movement","You remain perfectly still, listening as faint whispers echo past you, shadows dancing along the walls.")
    # --- Step 7: Hospital Hallway Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hallway_investigate":
       twist_hospital("You cautiously move down the hallway, noticing eerie sounds echoing from empty rooms...","Inspect the room with flickering lights","You step closer, the flickering light revealing walls smeared with unknown stains and shadows that twitch unnaturally.","Peek into the adjacent room silently","You lean towards the slightly open door, catching glimpses of shapes moving where no one should be.")
    # --- Step 7: Hospital Hallway Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "hospital_hallway_observe":
       twist_hospital("You stay hidden in the shadows, carefully observing the hallway...","Follow the shadow silently","You move silently, keeping your eyes on the shifting shadow that glides along the walls.","Stay put and listen closely","You remain in the shadows, straining to hear distant footsteps and faint whispers echoing through the hallway.")


    # --- Step 2: Forest Branch ---
    if st.session_state.current_step == 2 and st.session_state.branch == "forest_beginning":
        non_twist("The forest trail twists unnaturally, and the wind carries voices that mimic your own. What do you do?","Follow the strange voices deeper into the forest","You step cautiously toward the sound. The voices echo around you, repeating your own words back with a delay that shouldn't exist.","forest_voices","Turn back toward the entrance of the trail","You decide to head back, but the path behind you seems longer than before—trees have shifted, and the trail bends the wrong way.","forest_return")
    # --- Step 3: Forest Voices ---
    if st.session_state.current_step == 3 and st.session_state.branch == "forest_voices":
        non_twist( "The forest seems alive — every tree leans closer, and the air hums with whispers repeating your name. What do you do?","Call out to the voices","You shout into the darkness, your own voice echoing back — but the echo doesn’t match your words anymore.","forest_call","Stay silent and keep moving deeper","You hold your breath and move forward. The whispers fade... replaced by the sound of footsteps that aren’t yours.","forest_silent")
    # --- Step 3: Forest Return ---
    if st.session_state.current_step == 3 and st.session_state.branch == "forest_return":
        non_twist("You retrace your steps carefully, but the trail looks different now — trees seem to have shifted positions.","Call out to see if anyone responds","Your voice echoes strangely, coming back distorted, as though someone else is mimicking you deeper in the forest.","forest_echo","Stay silent and follow the path cautiously","You move quietly through the twisted trees, noticing faint footprints — your own, looping back.","forest_loop" )
    # --- Step 4: Forest Call ---
    if st.session_state.current_step == 4 and st.session_state.branch == "forest_call":
        non_twist("You call out again, but this time the reply is immediate — your own voice answers from behind the trees.","Follow the voice deeper into the woods","You push through the branches, chasing the sound. The forest grows darker, and the voice becomes a whisper right beside you.","forest_voice_follow","Stay still and listen carefully","You freeze in place, hearing faint breathing close by. The echo fades, replaced by silence heavy enough to hurt.","forest_voice_listen")
    # --- Step 4: Forest Silent ---
    if st.session_state.current_step == 4 and st.session_state.branch == "forest_silent":
        non_twist("You decide to remain silent, letting the forest sounds surround you. The whispers fade, replaced by an eerie stillness.","Move quietly toward the nearest tree line","You slip between the trees, noticing faint footprints that seem to appear and vanish in the dirt.","forest_tree_move","Stand still and observe your surroundings","You stay rooted to the spot. The forest feels like it’s watching you, branches swaying without wind.","forest_tree_observe")
    # --- Step 4: Forest Echo ---
    if st.session_state.current_step == 4 and st.session_state.branch == "forest_echo":
        non_twist("The echoes grow louder, repeating your own voice in distorted tones. A chill runs down your spine.","Follow the echoes deeper into the forest","You cautiously move toward the source of the echo, noticing shadows that shift unnaturally between the trees.","forest_echo_deep","Try to locate the source without moving","You freeze, straining your ears to pinpoint the origin of the strange, repeating sounds.","forest_echo_listen")
    # --- Step 4: Forest Loop ---
    if st.session_state.current_step == 4 and st.session_state.branch == "forest_loop":
        non_twist("The path seems to circle back on itself, each turn eerily familiar.","Keep walking and try to find a new path","You force yourself forward, hoping the forest will reveal a different route, but the scenery repeats unsettlingly.","forest_loop_continue","Pause and observe the surroundings carefully","You stop, examining the trees and the trail, hoping to notice any clue that breaks the loop.","forest_loop_observe")
    # --- Step 5: Forest Voice Follow ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_voice_follow":
        non_twist("The whispers grow louder, pulling you deeper into the forest's heart.","Follow the voice cautiously","You step forward carefully, trying to trace the source of the mysterious voices without alerting whatever is there.","forest_deep_path","Ignore the voices and stick to the main trail","You decide to trust your instincts and continue along the main trail, leaving the haunting whispers behind—for now.","forest_main_trail")
    # --- Step 5: Forest Voice Listen ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_voice_listen":
        non_twist("You pause, straining your ears to catch the faintest hint of meaning in the whispers.","Focus intently on the voices","Closing your eyes, you concentrate, discerning patterns and strange words that seem almost familiar.","forest_decipher","Ignore and move cautiously forward","You decide not to dwell on the whispers, moving forward carefully while the forest shadows shift around you.","forest_shadow_path")
    # --- Step 5: Forest Tree Move ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_tree_move":
        non_twist("The trees around you shudder and creak as if alive, their branches reaching out like fingers.","Investigate the moving trees","You cautiously approach, noticing that the shadows cast by the branches form shapes that seem almost human.","forest_branch_shapes","Keep walking and ignore the movement","You move forward quickly, focusing on the path, though the branches seem to sway more urgently as you pass.","forest_rushing_path")
    # --- Step 5: Forest Tree Observe ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_tree_observe":
        non_twist("You stop to observe the trees, noticing strange patterns in the way their shadows move.","Focus on the shadows closely","You watch intently, realizing the shadows seem to mimic your movements with a delayed, eerie precision.","forest_shadow_mimic","Look up at the swaying branches","You glance up, seeing the branches twisting unnaturally as if reacting to your presence.","forest_branch_twist")
    # --- Step 5: Forest Echo Deep ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_echo_deep":
        non_twist("The echoes grow louder, repeating words you don’t remember saying.","Follow the source of the echoes","You move cautiously toward the deeper part of the forest, each echo guiding you further into the shadows.","forest_deeper_path","Try to block out the echoes and focus","You cover your ears briefly, trying to steady your mind, but the forest seems to close in around you.","forest_focus_clearing")
    # --- Step 5: Forest Echo Listen ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_echo_listen":
        non_twist("The forest seems to whisper secrets just for you, every sound amplified strangely.","Move closer to the source of the whispers","You creep forward, heart pounding, trying to discern the origin of the ghostly echoes.","forest_whisper_source","Stay put and focus on the surrounding sounds","You remain still, listening carefully as each rustle and echo paints a clearer picture of the forest’s mystery.","forest_listen_clearing")
    # --- Step 5: Forest Loop Continue ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_loop_continue":
        non_twist("The forest path loops endlessly, and the scenery seems to shift subtly as you walk.","Try retracing your steps carefully","You backtrack cautiously, noticing faint differences that hint at something supernatural at play.","forest_loop_retrace","Pick a new path through the dense trees","You forge a new route, hoping it leads you out, but the forest seems to resist your choice.","forest_loop_newpath")
    # --- Step 5: Forest Loop Observe ---
    if st.session_state.current_step == 5 and st.session_state.branch == "forest_loop_observe":
        non_twist("You pause to observe the looping path carefully, the trees almost seeming to watch you back.","Study the patterns in the forest","You notice subtle changes in the foliage and shadows that suggest the forest is alive and aware of your presence.","forest_loop_patterns","Keep moving cautiously forward","You continue along the winding trail, feeling a sense of unease as familiar landmarks appear distorted.","forest_loop_forward")
    # --- Step 6: Forest Deep Path ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_deep_path":
        non_twist("The forest grows darker and denser, with shadows stretching unnaturally along the path.","Follow the dimly lit trail","You proceed cautiously along the trail, noticing twisted branches that seem to form unnatural shapes around you.","forest_path_follow","Venture off the trail to investigate strange sounds","You step off the main path, moving toward a series of faint whispers that seem to call your name.","forest_path_investigate")
    # --- Step 6: Forest Main Trail ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_main_trail":
        non_twist("The main trail splits into multiple directions, each shadowed by towering trees.","Take the left path where the fog thickens","You cautiously walk along the left path, the fog curling around your feet and muffling distant sounds.","forest_left_fog","Take the right path toward the faint glimmer of light","You move toward the faint light on the right path, feeling a strange pull guiding your steps.","forest_right_light")
    # --- Step 6: Forest Decipher ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_decipher":
        non_twist("You find mysterious symbols carved into the trees, glowing faintly under the moonlight.","Try to decode the symbols","You study the symbols carefully, realizing they form a cryptic message that hints at a hidden path.","forest_symbols_decode","Ignore them and continue along the trail","You decide to ignore the symbols, focusing instead on the winding trail ahead, though an uneasy feeling lingers.","forest_symbols_ignore")
    # --- Step 6: Forest Shadow Path ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_shadow_path":
        non_twist("A dark path splits from the main trail, shadows twisting unnaturally along it.","Take the shadowed path","You step cautiously onto the shadowed path, feeling the temperature drop and hearing faint whispers around you.","forest_shadow_investigate","Stay on the main trail","You continue along the main trail, but glances over your shoulder make you feel as though something is following silently.","forest_shadow_ignore")
    # --- Step 6: Forest Branch Shapes ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_branch_shapes":
        non_twist("The branches ahead twist into shapes that seem almost human, moving with the wind.","Approach the twisted branches","You move closer, noticing the shadows form fleeting faces and gestures, sending chills down your spine.","forest_branch_investigate","Avoid the twisted branches","You skirt around the strange branches, feeling uneasy as the shadows seem to follow your movement.","forest_branch_ignore")
    # --- Step 6: Forest Rushing Path ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_rushing_path":
        non_twist("A rushing path appears, the sound of wind and water echoing unnaturally through the trees.","Follow the rushing path forward","You step onto the path, the roar growing louder as the forest seems to close in around you.","forest_rushing_follow","Turn back and find another route","You retreat slightly, seeking a calmer route, but the forest seems to shift, making it hard to remember your previous steps.","forest_rushing_detour")
    # --- Step 6: Forest Shadow Mimic ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_shadow_mimic":
        non_twist("The shadow ahead mirrors your movements perfectly, sending chills down your spine.","Approach the shadow cautiously","You take careful steps toward the shadow, trying to discern its form in the dim light.","forest_shadow_approach","Step back and observe it from a distance","You keep your distance, noting how the shadow imitates every subtle motion you make.","forest_shadow_observe")
    # --- Step 6: Forest Branch Twist ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_branch_twist":
        non_twist("The branches above twist and curl as if alive, forming shapes that seem almost intentional.","Move closer to inspect the twisted branches","You step forward carefully, noticing that the branches seem to form eerie patterns in the dim light.","forest_branch_inspect","Keep your distance and observe silently","You remain at a safe distance, watching the branches writhe and twist in unsettling ways.","forest_branch_observe")
    # --- Step 6: Forest Deep Path ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_deeper_path":
        non_twist("The path grows darker and the canopy above thickens, muffling the sounds around you.","Press forward into the dense part of the forest","You move cautiously along the deepening path, shadows stretching unnaturally around you.","forest_deep_forward","Retreat slightly and reassess your surroundings","You step back a little, noticing strange movements in the periphery and the wind whispering unintelligible words.","forest_deep_reassess")
    # --- Step 6: Forest Focus Clearing ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_focus_clearing":
        non_twist("You reach a small clearing where moonlight filters through the treetops, casting eerie patterns.","Move cautiously into the center of the clearing","You step into the clearing, feeling the hairs on your arms stand on end as shadows seem to stretch toward you.","forest_clearing_center","Circle the edge of the clearing, staying in the shadows","You skirt the perimeter, observing strange shapes among the trees, almost like they are watching you.","forest_clearing_edge")
    # --- Step 6: Forest Whisper Source ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_whisper_source":
        non_twist("The whispers grow louder, seeming to come from multiple directions at once.","Follow the whispers deeper into the forest","You move cautiously toward the source, every rustle of leaves making your heart race.","forest_follow_whispers","Try to locate the origin from your current spot","You pause, listening intently, discerning subtle patterns in the whispers that hint at their origin.","forest_locate_whispers")
    # --- Step 6: Forest Listen Clearing ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_listen_clearing":
        non_twist("You pause in the clearing, straining to catch every subtle sound around you.","Focus on the faint rustling among the trees","You zero in on the soft rustling, trying to discern if it’s animal or something else.","forest_rustle_focus","Scan the surroundings silently","You stand perfectly still, noticing shadows shifting and shapes moving in the periphery.","forest_shadow_scan")
    # --- Step 6: Forest Loop Retrace ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_loop_retrace":
        non_twist("You realize the path loops back on itself, and the forest seems eerily aware of your movements.","Retrace your steps carefully","You walk back along the trail, noting how each landmark seems subtly altered from before.","forest_loop_stepback","Investigate the twisting trail","You examine the trail closely, seeing strange patterns in the foliage that weren’t there before.","forest_loop_investigate")
    # --- Step 6: Forest Loop New Path ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_loop_newpath":
        non_twist("A new path emerges from the undergrowth, shrouded in mist and whispering leaves.","Take the new path cautiously","You step onto the new path, feeling the cool mist brush against your skin as the forest deepens.","forest_newpath_cautious","Ignore the path and stay on the familiar trail","You stick to the old trail, though the sounds around you suggest the forest wants you to follow the new path.","forest_newpath_ignore")
    # --- Step 6: Forest Loop Patterns ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_loop_patterns":
        non_twist("The trees form strange, repeating patterns as you advance, almost like a natural labyrinth.","Follow the pattern carefully","You trace the shapes of the trees, noticing subtle markings that guide your path deeper into the forest.","forest_patterns_follow","Avoid the pattern and move randomly","You ignore the repeating shapes, moving freely, but the forest seems to shift subtly to disorient you.","forest_patterns_ignore")
    # --- Step 6: Forest Loop Forward ---
    if st.session_state.current_step == 6 and st.session_state.branch == "forest_loop_forward":
        non_twist("The path ahead twists unpredictably, and the forest seems alive with movement.","Press forward despite the uncertainty","You move carefully along the winding path, each step making the shadows seem to stretch and shift.","forest_forward_press","Pause and observe the surroundings","You stop to look around, noting the strange movements and sounds among the trees, feeling the forest watching you.","forest_forward_observe")
    # --- Step 7: Forest Path Follow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_path_follow":
        twist_forest("You follow the eerie path deeper into the forest, unsure what awaits…",        "Press forward bravely into the unknown",        "You steel yourself and continue along the winding path, the trees whispering secrets as you pass.",        "Hesitate and observe the forest carefully",        "You pause, heart racing, noticing shadows that shift unnaturally, as if alive.")
    # --- Step 7: Forest Path Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_path_investigate":
        twist_forest("You cautiously investigate the twisted path, every rustle making you jump…",         "Move closer to inspect the strange markings",         "You approach the markings carefully, noticing patterns that seem almost intentional.",         "Step back and analyze from a distance",         "You observe quietly, trying to make sense of the shifting shadows and shapes along the path.")
    # --- Step 7: Forest Left Fog Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_left_fog":
        twist_forest("You veer left into the thickening fog, the path disappearing into gray…",         "Push forward into the dense fog bravely",         "You step carefully, the fog wrapping around you as whispers echo faintly from unseen sources.",         "Hesitate and listen to the sounds around you",         "You pause, straining to hear, catching faint movements and soft murmurs just beyond sight.")
    # --- Step 7: Forest Right Light Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_right_light":
        twist_forest("You head right, drawn toward a mysterious light flickering through the trees…",         "Approach the light boldly",         "You move closer, the light revealing twisted branches and shifting shadows that seem almost alive.",         "Step back and observe the light from a distance",         "You keep your distance, watching as the light dances and flickers, hinting at hidden shapes within the forest.")
    # --- Step 7: Forest Symbols Decode Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_symbols_decode":
        twist_forest("You study the strange symbols carved into the trees, their meaning elusive…",         "Attempt to decode the symbols immediately",         "You trace the markings with your fingers, a chilling pattern emerging that hints at an ancient forest secret.",         "Step back and observe the symbols carefully",         "You take a cautious stance, noting the carvings and their placement, feeling an uncanny energy emanate from them.")
    # --- Step 7: Forest Symbols Ignore Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_symbols_ignore":
        twist_forest("You decide to ignore the strange symbols, pressing onward through the dense forest…",         "Continue walking without paying attention to the symbols",         "You stride past the carved trees, yet a sense of unease follows, as if the forest itself is watching.",         "Glance back at the symbols cautiously",         "You take a quick look at the carvings behind you, feeling their silent warning linger in the shadows.")
    # --- Step 7: Forest Shadow Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_shadow_investigate":
        twist_forest("You approach the moving shadow cautiously, trying to discern its origin…",         "Step closer to confront the shadow",         "You edge forward, heart pounding, as the shadow shifts and flickers among the trees, almost sentient.",         "Observe the shadow from a safe distance",         "You hang back, watching the shadow's movements carefully, noting patterns that feel unnaturally deliberate.")
    # --- Step 7: Forest Shadow Ignore Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_shadow_ignore":
        twist_forest("You decide to ignore the shadow, focusing on the path ahead…",         "Keep moving forward without looking back",         "You push onward, trying to ignore the unsettling presence, though the shadow seems to follow your every step.",         "Pause and observe the shadow silently",         "You stop briefly, watching the shadow shift subtly in the distance, a cold chill running down your spine.")
    # --- Step 7: Forest Branch Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_branch_investigate":
        twist_forest("You approach the strange fork in the forest, curious about where each branch leads…",         "Take the left branch bravely",         "You step onto the left path, the forest thickening around you, whispers growing louder with each step.",         "Take the right branch cautiously",         "You move along the right path, noticing unusual patterns in the trees and shadows that seem almost deliberate.")
    # --- Step 7: Forest Branch Ignore Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_branch_ignore":
        twist_forest("You choose to ignore the peculiar fork, continuing along the main trail…",         "Keep moving forward without hesitation",         "You stride ahead, the forest seeming to watch you, the wind carrying unsettling whispers.",         "Slow down and observe the surroundings",         "You walk cautiously, noticing fleeting shadows and the eerie rustling of leaves that seem alive.")
    # --- Step 7: Forest Rushing Follow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_rushing_follow":
        twist_forest("You follow the sound of rushing water deeper into the forest…",         "Move quickly toward the sound",         "You dash through the undergrowth, the roar of the stream growing louder, shadows flitting past.",         "Approach cautiously, observing carefully",         "You tread lightly, each step revealing strange patterns in the moving foliage, as if the forest itself guides you.")
    # --- Step 7: Forest Rushing Detour Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_rushing_detour":
        twist_forest("You take a detour away from the rushing water, the forest growing denser…",         "Forge ahead through the thickening trees",         "You push through tangled branches, feeling an eerie presence watching your every move.",         "Step back and study the surroundings",         "You carefully navigate the twisted path, noticing shadows that shift unnaturally among the foliage.")
    # --- Step 7: Forest Shadow Approach Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_shadow_approach":
        twist_forest("A dark shadow moves along the forest floor, drawing closer with each step…",         "Approach the shadow cautiously",         "You move forward slowly, heart pounding, as the shadow twists and stretches unnaturally.",         "Step back and observe from a safe distance",         "You hold your ground, watching the shadow’s movements, every instinct screaming that it’s alive.")
    # --- Step 7: Forest Shadow Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_shadow_observe":
        twist_forest("You freeze, eyes fixed on the shifting shadow ahead, trying to make sense of its movements…",         "Focus intently and follow its motion",         "Every flicker and stretch of the shadow seems purposeful, leading you deeper into the forest’s mysteries.",         "Stay still and watch silently",         "You remain hidden, observing the shadow as it twists and dances, heart racing with anticipation.")
    # --- Step 7: Forest Branch Inspect Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_branch_inspect":
        twist_forest("You approach the twisted branch, noticing strange markings etched into its bark…",         "Examine the markings closely",         "The symbols on the branch seem to pulse with an eerie energy, guiding your path forward.",         "Step back and observe from a distance",         "You keep your distance, trying to discern the pattern in the markings while staying safe.")
    # --- Step 7: Forest Branch Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_branch_observe":
        twist_forest("You carefully observe the unusual branch, feeling a strange presence nearby…",         "Move closer to investigate the branch",         "As you approach, the branch seems to twist and shift, revealing hidden symbols among the leaves.",         "Step back and watch silently",         "You maintain your distance, noting subtle movements and listening to whispers carried by the wind.")
    # --- Step 7: Forest Deep Forward Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_deep_forward":
        twist_forest("You press forward into the deeper part of the forest, shadows closing around you…",         "Continue bravely deeper into the darkness",         "The path narrows and the trees seem alive, their twisted forms guiding you toward an unseen fate.",         "Pause and take in your surroundings",         "You stop for a moment, listening carefully to the forest, sensing faint whispers and rustling branches nearby.")
    # --- Step 7: Forest Deep Reassess Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_deep_reassess":
        twist_forest("You stop to reassess your position, the forest thick and foreboding around you…",         "Forge ahead despite the unease",         "You push forward, each step crunching on dry leaves, shadows flickering at the edge of your vision.",         "Step back and observe carefully",         "You take a moment to watch the forest, noticing strange movements and patterns that unsettle you.")
    # --- Step 7: Forest Clearing Center Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_clearing_center":
        twist_forest("You enter the center of the clearing, the air thick with tension and whispers…",         "Move boldly into the center to confront whatever awaits",         "You step forward, feeling the energy of the clearing press around you as unseen eyes seem to watch.",         "Hesitate at the edge and scan the surroundings",         "You linger at the clearing's perimeter, noting every subtle movement of shadows and light, heart pounding.")
    # --- Step 7: Forest Clearing Edge Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_clearing_edge":
        twist_forest("You approach the edge of the clearing, where darkness seems to gather unnaturally…",         "Step cautiously to the edge and peer into the darkness",         "You inch forward, the trees casting long, twisted shadows that seem to stretch toward you.",         "Stay back and observe the clearing from a safe distance",         "You hold your ground at the edge, watching as the shadows writhe and whisper, the forest alive with secrets.")
    # --- Step 7: Forest Follow Whispers Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_follow_whispers":
        twist_forest("You decide to follow the haunting whispers that float through the trees…",         "Move deeper into the forest, tracking the whispers closely",         "You carefully step forward, each whisper guiding you through the dense, shadowed undergrowth.",         "Pause and listen from your current spot",         "You remain still, straining your ears, as the whispers twist and echo around you, hinting at something unseen.")
    # --- Step 7: Forest Locate Whispers Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_locate_whispers":
        twist_forest("You attempt to pinpoint the source of the eerie whispers that haunt the forest…",         "Advance cautiously toward the faint sound",         "You step quietly, branches crunching underfoot, closing in on the origin of the whispers as shadows dance around you.",         "Stay put and observe carefully",         "You remain hidden, analyzing every movement and echo, sensing that the forest itself is alive with secrets.")
    # --- Step 7: Forest Rustle Focus Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_rustle_focus":
        twist_forest("You hear a sudden rustle in the underbrush, drawing your attention…",         "Move closer to investigate the rustling",         "You carefully push aside branches, revealing fleeting shadows that dart away, sending chills down your spine.",         "Step back and watch from a distance",         "You keep your distance, observing the movement cautiously, trying to discern if it’s friend or foe.")
    # --- Step 7: Forest Shadow Scan Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_shadow_scan":
        twist_forest("You notice shadows shifting unnaturally among the trees…",         "Step forward to get a closer look",         "You move cautiously, the shadows twisting and elongating as if alive, whispering in the wind.",         "Stay back and observe silently",         "You keep your distance, noting the strange movements while your heart races, unsure of what may happen next.")
    # --- Step 7: Forest Loop Stepback Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_loop_stepback":
        twist_forest("The looping path seems endless, and retracing your steps feels unnerving…",         "Press onward despite the disorienting trail",         "You push forward, feeling the forest close in around you as the trees seem to whisper warnings.",         "Step back and observe the looping path carefully",         "You retreat slightly, trying to understand the strange patterns of the twisting trail, every sound amplified in the silence.")
    # --- Step 7: Forest Loop Investigate Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_loop_investigate":
        twist_forest("You notice strange patterns on the ground and decide to investigate…",         "Examine the patterns closely to decipher their meaning",         "You kneel to study the markings, realizing they form a cryptic message, almost alive in the fading light.",         "Step back and observe from a distance",         "You watch the patterns cautiously, feeling an eerie presence as if the forest itself is aware of your actions.")
    # --- Step 7: Forest New Path Cautious Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_newpath_cautious":
        twist_forest("You cautiously take the new path, each step echoing in the silent forest…",         "Move forward carefully, eyes scanning for any danger",         "You tread lightly along the path, noticing shadows that slither between the trees, whispering your name.",         "Pause and observe the surroundings before proceeding",         "You stop briefly, feeling the wind shift unnaturally, as if the forest is breathing around you.")
    # --- Step 7: Forest New Path Ignore Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_newpath_ignore":
        twist_forest("You choose to ignore the new path, focusing on the main trail ahead…",         "Keep walking along the main trail with determination",         "You continue along the familiar trail, though the forest seems to react, branches creaking as if warning you.",         "Glance at the new path occasionally but do not divert",         "You cast brief glances at the side path, feeling a chill run down your spine, but stay your course.")
    # --- Step 7: Forest Patterns Follow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_patterns_follow":
        twist_forest("You follow the strange patterns etched into the forest floor, curiosity and fear intertwining…",         "Trace the patterns closely, trying to understand their meaning",         "You carefully step along the markings, each step resonating with a faint whisper that seems to guide you deeper.",         "Proceed cautiously while observing surroundings",         "You move forward slowly, eyes darting around as shadows shift in rhythm with the patterns, sending shivers down your spine.")
    # --- Step 7: Forest Patterns Ignore Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_patterns_ignore":
        twist_forest("You notice the strange patterns in the forest but choose to ignore them, pressing on…",         "Continue walking forward without paying attention",         "You focus on your path, ignoring the subtle, unnerving shapes that seem to shift around you.",         "Pause and observe the forest patterns carefully",         "You take a moment to glance at the unusual patterns, feeling a chill as they appear to move subtly.")
    # --- Step 7: Forest Forward Press Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_forward_press":
        twist_forest("You press forward through the dense undergrowth, each step making the forest seem more alive…",         "Push ahead bravely despite the unsettling sounds",         "You push through the thick foliage, feeling the branches brush against you as whispers swirl around.",         "Hesitate and take in your surroundings carefully",         "You pause, listening intently as shadows seem to move just beyond your vision, heightening the tension.")
    # --- Step 7: Forest Forward Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "forest_forward_observe":
        twist_forest("You move cautiously forward, eyes scanning the shifting shadows and eerie shapes ahead…",         "Advance slowly, keeping alert for any movement",         "You step carefully, noticing subtle changes in the forest canopy as the wind carries strange echoes.",         "Stay in place and watch the forest carefully",         "You freeze, taking in the unnatural patterns of the branches and the fleeting shapes that dart in the corners of your eyes.")  


    # --- Step 2: Carnival Beginning ---
    if st.session_state.current_step == 2 and st.session_state.branch == "carnival_beginning":
        non_twist(    "Walking into the dimly lit carnival, you notice the rides are rusted, but laughter echoes faintly in the distance.",    "Investigate the rusted Ferris wheel",    "You cautiously approach the Ferris wheel, its carriages creaking eerily with the wind.",    "carnival_ferris",    "Walk toward the shadowy funhouse",    "You make your way to the funhouse entrance, its mirrors warped and reflecting strange distortions.",    "carnival_funhouse")
    # --- Step 3: Carnival Ferris ---
    if st.session_state.current_step == 3 and st.session_state.branch == "carnival_ferris":
        non_twist(    "The Ferris wheel towers above you, its gears slowly turning as if moved by unseen hands.",    "Climb into one of the creaking carriages",    "You step into a carriage, the wood groaning under your weight as it sways gently.",    "carnival_ferris_ride",    "Examine the base of the Ferris wheel",    "You inspect the rusted gears and faded control panel, noticing strange handprints smeared across the metal.",    "carnival_ferris_base")
    # --- Step 3: Carnival Funhouse ---
    if st.session_state.current_step == 3 and st.session_state.branch == "carnival_funhouse":
        non_twist(    "The funhouse mirrors distort your reflection, some faces moving independently of your own.",    "Step inside and explore the hall of mirrors",    "You carefully walk between the mirrors, catching glimpses of shadows that mimic you with a delay.",    "carnival_funhouse_mirrors",    "Peek through a side window to observe the interior first",    "You glance through a cracked window, noticing reflections that seem alive and not entirely yours.",    "carnival_funhouse_window")
    # --- Step 4: Carnival Ferris Ride ---
    if st.session_state.current_step == 4 and st.session_state.branch == "carnival_ferris_ride":
        non_twist(    "You climb into the rusted Ferris wheel gondola, the carnival lights flickering ominously below.",    "Take the ride slowly to observe the surroundings",    "The wheel creaks as it rises, giving you a view of the entire eerily empty carnival, shadows moving strangely.",    "carnival_ferris_slow",    "Jump off quickly and run to another ride",    "You leap off the gondola and dash across the carnival, the laughter growing louder and more sinister.",    "carnival_ferris_escape")
    # --- Step 4: Carnival Ferris Base ---
    if st.session_state.current_step == 4 and st.session_state.branch == "carnival_ferris_base":
        non_twist(    "Standing at the base of the Ferris wheel, you notice the rusted gears turning slowly on their own.",    "Inspect the machinery closely",    "You approach the gears, noticing strange symbols etched into the metal, almost glowing faintly.",    "carnival_ferris_inspect",    "Walk around the Ferris wheel cautiously",    "You circle the Ferris wheel, keeping an eye on the moving shadows cast by the flickering lights.",    "carnival_ferris_cautious")
    # --- Step 4: Carnival Funhouse Mirrors ---
    if st.session_state.current_step == 4 and st.session_state.branch == "carnival_funhouse_mirrors":
        non_twist(    "Inside the funhouse, the distorted mirrors reflect twisted versions of yourself, some moving independently.",    "Step closer to the mirror that seems alive",    "You lean in and notice a faint whisper coming from the glass, calling your name softly.",    "carnival_funhouse_whisper",    "Walk past the mirrors quickly",    "You move along the corridor, feeling the temperature drop as the reflections seem to reach out toward you.",    "carnival_funhouse_cold")
    # --- Step 4: Carnival Funhouse Window ---
    if st.session_state.current_step == 4 and st.session_state.branch == "carnival_funhouse_window":
        non_twist(    "A dusty, cracked window lets in a sliver of moonlight, revealing shadows that flicker unnaturally.",    "Peer through the window cautiously",    "You carefully look outside, noticing figures moving silently among the carnival stalls.",    "carnival_funhouse_outside",    "Step away from the window and continue down the hall",    "You move forward, the wooden floorboards creaking beneath your feet, each step echoing eerily.",    "carnival_funhouse_corridor")
    # --- Step 5: Carnival Ferris Slow ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_ferris_slow":
        non_twist(    "The Ferris wheel moves sluggishly, groaning with each rotation, casting long shadows.",    "Climb carefully onto the Ferris wheel",    "You step into a rusty gondola, the wind whistling as the wheel creaks and sways.",    "carnival_ferris_up",    "Stay on the ground and watch the wheel turn",    "From below, you observe the wheel turning slowly, the shadows creating strange patterns across the carnival.",    "carnival_ferris_watch")
    # --- Step 5: Carnival Ferris Escape ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_ferris_escape":
        non_twist(    "The Ferris wheel seems unstable, and the shadows around it twist unnaturally.",    "Run toward the exit of the Ferris wheel area",    "You dash past the rusty metal beams, heart racing as the wheel groans behind you.",    "carnival_ferris_exit",    "Hide behind a nearby stall and observe",    "You crouch behind a creaking stall, watching the Ferris wheel sway ominously, shadows flickering around it.",    "carnival_ferris_hide")
    # --- Step 5: Carnival Ferris Inspect ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_ferris_inspect":
        non_twist(    "You notice something strange at the base of the Ferris wheel, a faint glow in the shadows.",    "Investigate the glowing object closely",    "Cautiously, you approach the glow, finding an old, cracked carnival token that hums faintly.",    "carnival_ferris_token",    "Step back and watch the Ferris wheel cautiously",    "You keep your distance, observing as the wheel slowly rotates, the lights flickering like ghostly eyes.",    "carnival_ferris_forward")
    # --- Step 5: Carnival Ferris Cautious ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_ferris_cautious":
        non_twist(    "You proceed carefully along the Ferris wheel platform, every creak echoing ominously.",    "Move forward slowly, keeping your eyes on the shadows",    "Each step is deliberate, the metal groaning under your weight as you try to stay alert to any movement.",    "carnival_ferris_reassess",    "Step back and reassess the situation",    "You retreat slightly, examining the Ferris wheel from a safer distance, noticing shapes shifting in the dark.",    "carnival_ferris_watching")
    # --- Step 5: Carnival Funhouse Whisper ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_funhouse_whisper":
        non_twist(    "A faint whisper seems to echo from the mirrors, sending chills down your spine.",    "Follow the whisper deeper into the funhouse",    "You cautiously navigate the warped corridors, mirrors reflecting distorted versions of yourself at every turn.",    "carnival_funhouse_deep",    "Ignore the whisper and explore the nearby window",    "You turn your attention to the cracked window, noticing shadows moving outside, detached from the carnival lights.",    "carnival_funhouse_window_focus")
    # --- Step 5: Carnival Funhouse Cold ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_funhouse_cold":
        non_twist(    "A sudden cold draft chills you to the bone as you step further inside the funhouse.",    "Move forward bravely despite the cold",    "You press onward, each step echoing ominously, the mirrors reflecting fleeting glimpses of shadowy figures.",    "carnival_funhouse_deeper",    "Retreat toward the entrance to find warmth",    "You step back cautiously, shivering as you notice strange shapes lingering near the windows.",    "carnival_funhouse_entrance")
    # --- Step 5: Carnival Funhouse Outside ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_funhouse_outside":
        non_twist(    "Stepping outside the funhouse, the carnival seems quieter, but the shadows stretch unnaturally.",    "Approach the nearest ride cautiously",    "You move toward the carousel, the painted horses appearing almost alive in the dim light.",    "carnival_carousel_near",    "Walk along the empty midway to the food stalls",    "You navigate the deserted stalls, the faint smell of popcorn mixing with the damp night air.",    "carnival_stalls_near")
    # --- Step 5: Carnival Funhouse Corridor ---
    if st.session_state.current_step == 5 and st.session_state.branch == "carnival_funhouse_corridor":
        non_twist(    "Inside the funhouse corridor, distorted reflections make it hard to tell which way is forward.",    "Move carefully toward the next mirror",    "You inch forward, each mirror reflecting a slightly different version of yourself, some with unsettling expressions.",    "carnival_mirror_next",    "Retreat to the entrance and observe",    "You step back, watching the corridor stretch strangely as if alive, shadows dancing along the walls.",    "carnival_funhouse_enter")
    # --- Step 6: Carnival Ferris Up ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_up":
        non_twist(    "From the top of the Ferris wheel, the carnival sprawls beneath you like a forgotten dream, lights flickering in odd patterns.",    "Scan the carnival for any signs of movement",    "You peer down, spotting shadows that seem to twist independently of the carnival rides, almost as if they are alive.",    "carnival_ferris_focus",    "Climb down carefully to explore the base of the Ferris wheel",    "You descend cautiously, feeling the metal tremble slightly under your weight, noticing strange symbols etched into the rusty beams.",    "carnival_ferris_base_focus")
    # --- Step 6: Carnival Ferris Watch ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_watch":
        non_twist(    "Observing the Ferris wheel from the ground, you notice that some gondolas move as if propelled by unseen hands.",    "Approach the Ferris wheel to inspect it closely",    "You walk toward the wheel, feeling a low hum in the air, and notice that the shadows around it seem to stretch unnaturally.",    "carnival_ferris_token_spot",    "Step back and watch the carnival midway for any unusual activity",    "From your vantage point, the empty stalls flicker with phantom lights, and faint laughter drifts through the night.",    "carnival_midway_watch")
    # --- Step 6: Carnival Ferris Exit ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_exit":
        non_twist(    "You move quickly away from the Ferris wheel, the rusted metal groaning behind you with every step.",    "Head toward the carousel to investigate the faint light",    "You make your way across the uneven ground, noticing the painted horses' eyes glinting unnaturally in the dim light.",    "carnival_carousel_focus",    "Find shelter behind the food stalls to observe the surroundings",    "You duck behind a stall, heart racing, as distant laughter and faint music echo across the carnival.",    "carnival_stalls_observe")
    # --- Step 6: Carnival Ferris Hide ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_hide":
        non_twist(    "Crouching behind the stall, the shadows around you seem to shift and flicker with a life of their own.",    "Stay hidden and watch for any movement",    "You hold your breath, noticing that a gondola on the Ferris wheel swings unnaturally, almost as if aiming to follow you.",    "carnival_ferris_spot",    "Quietly slip out from behind the stall and move toward the funhouse",    "You step lightly onto the gravel, the funhouse mirrors reflecting flashes of movement that aren't yours.",    "carnival_funhouse_approach")
    # --- Step 6: Carnival Ferris Token ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_token":
        non_twist(    "The old carnival token glows faintly in your hand, humming as though it has a hidden purpose.",    "Examine the token closely for engravings or symbols",    "You notice tiny etched symbols that seem to shift as you tilt the token, revealing a path toward the carousel.",    "carnival_carousel_mystery",    "Pocket the token and continue along the Ferris wheel platform",    "You keep the token with you, feeling a subtle vibration guiding your steps as you approach the center of the carnival.",    "carnival_center_approach")
    # --- Step 6: Carnival Ferris Forward ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_forward":
        non_twist(    "You move carefully forward along the Ferris wheel platform, the wind carrying distorted echoes of carnival music.",    "Step onto the next gondola to get a higher view of the carnival",    "From above, you see faint shadows flitting across the midway, moving in ways that don’t match the rides’ creaks.",    "carnival_aerial_watch",    "Move to the base of the Ferris wheel and inspect the surrounding ground",    "You notice odd footprints and scattered tickets leading toward the funhouse, hinting at where others might have gone before you.",    "carnival_funhouse_trail")
    # --- Step 6: Carnival Ferris Reassess ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_reassess":
        non_twist(    "You pause on the Ferris wheel platform, feeling the shadows lengthen and the music warp around you.",    "Survey the carnival from your spot to find a safer path",    "From your vantage point, you notice a flickering light coming from the carousel, drawing your attention.",    "carnival_carousel_mysteries",    "Step back toward the entrance of the Ferris wheel area",    "You retreat slightly, spotting a narrow alley between stalls that seems oddly untouched by the dim carnival lights.",    "carnival_stalls_alley")
    # --- Step 6: Carnival Ferris Watch ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_ferris_watching":
        non_twist(    "Watching the Ferris wheel turn slowly, you notice strange shadows twisting around the gondolas.",    "Follow the movement of the shadows along the carnival grounds",    "The shadows seem to guide you toward a neglected game booth, its paint faded but lights flickering faintly.",    "carnival_gamebooth_mystery",    "Shift focus to the Ferris wheel base and examine the surroundings",    "You spot a trail of broken tickets and confetti, leading toward the funhouse’s warped entrance.",    "carnival_funhouse_trails")
    # --- Step 6: Carnival Funhouse Deep ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_funhouse_deep":
        non_twist(    "The warped mirrors seem to twist reality itself as you move deeper into the funhouse.",    "Step carefully toward a dimly lit doorway at the end of the hall",    "You push open the creaking door, revealing a small room filled with old carnival masks, each staring blankly at you.",    "carnival_mask_room",    "Turn back and explore a side passage filled with flickering lights",    "The side corridor pulses with shadows, and you notice reflections that don’t match your movements.",    "carnival_side_corridor")
    # --- Step 6: Carnival Funhouse Window Focus ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_funhouse_window_focus":
        non_twist(    "Peering through the cracked window, the carnival looks distorted, colors bleeding unnaturally into one another.",    "Climb out the window onto a narrow ledge to get a closer look",    "You step carefully along the ledge, seeing faint footsteps leading toward the carousel, though no one is there.",    "carnival_carousel_mysteryy",    "Step back and examine the reflections in the nearby mirrors",    "The mirrors ripple slightly as if alive, showing fleeting images of figures disappearing behind the funhouse walls.",    "carnival_funhouse_mirror_glimpse")
    # --- Step 6: Carnival Funhouse Deep ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_funhouse_deeper":
        non_twist(    "The warped mirrors distort everything, creating a maze of reflections that seem almost alive.",    "Move toward a faint glowing doorway at the end of the hall",    "You push open the door, revealing a room filled with floating carnival balloons that sway as if moved by invisible hands.",    "carnival_balloon_room",    "Investigate the strange shadows flickering along the side walls",    "You follow the shadows cautiously, realizing they form a pathway deeper into the funhouse's hidden corridors.",    "carnival_shadow_corridor")
    # --- Step 6: Carnival Funhouse Entrance ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_funhouse_entrance":
        non_twist(    "Returning to the funhouse entrance, the distorted mirrors now seem to whisper faintly.",  "Step back inside and explore a corridor to the left",    "You enter the left corridor, the floorboards creaking underfoot, revealing mirrors that reflect moments from your past.",    "carnival_mirror_memory",    "Look around the entrance area for clues outside",    "Peering outside, you notice the carnival tents swaying strangely, as if reacting to some unseen presence.",    "carnival_tent_outside")
    # --- Step 6: Carnival Carousel Near ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_carousel_near":
        non_twist(    "The carousel horses appear almost lifelike, their eyes glinting in the dim carnival light.",    "Climb onto one of the horses to get a better view",    "You mount a painted horse, feeling the faint vibrations as the carousel slowly creaks to life, shadows dancing across the ground.",    "carnival_carousel_up",    "Circle the carousel on foot, inspecting the surrounding area",    "Walking around, you notice the horses' shadows moving independently, hinting at something strange hidden beneath.",    "carnival_carousel_shadow")
    # --- Step 6: Carnival Stalls Near ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_stalls_near":
        non_twist(    "The deserted stalls seem innocent at first, but the scent of popcorn lingers too strongly, almost hypnotically.",    "Peek inside the nearest food stall",    "Inside, you find jars of oddly glowing candies and a ledger with cryptic symbols scribbled on it.",    "carnival_candy_mystery",    "Walk along the midway to the next row of stalls",    "You move carefully, noticing the shadows of stuffed animals twitching, as if alive and watching your every move.",    "carnival_stuffed_shadow")
    # --- Step 6: Carnival Mirror Next ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_mirror_next":
        non_twist(    "The next mirror shimmers strangely, your reflection slightly delayed as if it has a life of its own.",    "Step closer and touch the mirror",    "Your fingers graze the cold surface, and the reflection smiles in a way you did not, the air growing thick around you.",    "carnival_mirror_portal",    "Step back and watch the mirror from a distance",    "Keeping your distance, you notice the reflection moving independently, gestures mocking your own cautiously.",    "carnival_mirror_observe")
    # --- Step 6: Carnival Funhouse Entrance ---
    if st.session_state.current_step == 6 and st.session_state.branch == "carnival_funhouse_enter":
        non_twist(    "The entrance to the funhouse creaks with each gust of wind, the warped doorway seeming to breathe.",    "Enter the funhouse cautiously",    "You step inside, the air thick and mirrors reflecting impossible angles, making the corridor feel endless.",    "carnival_funhouse_corridor_deep",    "Circle around the entrance and inspect the outer walls",    "Outside, you notice faint footsteps in the dust that vanish as soon as you approach, leaving an eerie silence.",    "carnival_funhouse_outer")
    # --- Step 7: Carnival Ferris Focus Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_ferris_focus":
        twist_carnival(    "Focusing on the Ferris wheel, you notice shadows shifting unnaturally among the gondolas…",    "Climb up and investigate the top gondola",    "You ascend carefully, the wind howling as the top gondola creaks. Something moves inside, unseen but watching.",    "Stay hidden and observe from below",    "You crouch behind a stall, eyes fixed on the gondolas as shapes appear and disappear, almost teasing you.")
    # --- Step 7: Carnival Ferris Base Focus Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_ferris_base_focus":
        twist_carnival(    "At the base of the Ferris wheel, the ground seems to ripple, like the shadows themselves are alive…",    "Examine the ground closely",    "You bend down and notice strange footprints that vanish as soon as you look away, a faint whisper echoing in your ears.",    "Step back and keep watch on the surroundings",    "From a safe distance, you see lights flickering in rhythm with the shadows, casting a haunting pattern across the carnival floor.")
    # --- Step 7: Carnival Ferris Token Spot Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_ferris_token_spot":
        twist_carnival(    "The cracked carnival token glows faintly, pulsing like a heartbeat in your hand…",    "Follow the glow to its source",    "You trace the light to a hidden trapdoor beneath the Ferris wheel, shadows flickering around its edges as if alive.",    "Pocket the token and retreat cautiously",    "You tuck the token into your pocket, but the shadows seem to stretch toward you, whispering your name softly in the wind.")
    # --- Step 7: Carnival Midway Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_midway_watch":
        twist_carnival(    "Watching the empty midway, you notice faint figures moving between the stalls, barely visible in the dim light…",    "Approach the figures cautiously",    "You step forward, each footstep echoing loudly, as the figures scatter and the laughter grows eerily louder.",    "Hide behind a stall and observe silently",    "You crouch behind a popcorn stall, heart racing, as the shadows seem to dance and merge with the flickering carnival lights.")
    # --- Step 7: Carnival Carousel Focus Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_focus":
        twist_carnival(    "The painted horses on the carousel start moving slowly on their own, eyes gleaming in the dim light…",    "Climb onto a moving horse bravely",    "You mount the horse, and it carries you around the carousel as shadows stretch unnaturally, whispering secrets of the carnival.",    "Step back and observe the carousel carefully",    "You stay on the ground, noticing each horse’s eyes following you, and the music playing faintly, though no one is around.")
    # --- Step 7: Carnival Stalls Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_stalls_observe":
        twist_carnival(    "The empty stalls seem to shimmer, and faint laughter echoes from within each one…",    "Investigate the nearest stall closely",    "You peek inside, finding objects moving on their own, and the faint glow of lights forming strange symbols on the walls.",    "Keep your distance and watch silently",    "You stay hidden, noticing shadows moving and shifting between the stalls, creating shapes that almost look alive.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_ferris_spot":
        twist_carnival(    "The carousel horses begin to move on their own, creaking in a slow, hypnotic rhythm…",    "Mount a horse and ride despite the eerie movement",    "You climb onto a painted horse, and as it spins, the world around you distorts, colors blending into shadows that whisper secrets.",    "Step back and watch cautiously",    "You remain on the ground, observing as the horses’ eyes seem to follow you, and faint laughter drifts from nowhere.")
    # --- Step 7: Carnival Center Approach Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_approach":
        twist_carnival(    "The center of the carnival seems alive, with lights flickering in impossible patterns and the air vibrating with faint music…",    "Move toward the center boldly",    "You stride forward, feeling the ground pulse beneath you, and the lights dance across faces that aren’t quite human.",    "Circle around and observe from the edges",    "You keep your distance, watching shadows twist unnaturally around the glowing center, sensing something waiting for you inside.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_mystery":
        twist_carnival(    "The carousel horses begin to move on their own, creaking in a slow, hypnotic rhythm…",    "Mount a horse and ride despite the eerie movement",    "You climb onto a painted horse, and as it spins, the world around you distorts, colors blending into shadows that whisper secrets.",    "Step back and watch cautiously",    "You remain on the ground, observing as the horses’ eyes seem to follow you, and faint laughter drifts from nowhere.")
    # --- Step 7: Carnival Center Approach Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_center_approach":
        twist_carnival(    "The center of the carnival seems alive, with lights flickering in impossible patterns and the air vibrating with faint music…",    "Move toward the center boldly",    "You stride forward, feeling the ground pulse beneath you, and the lights dance across faces that aren’t quite human.",    "Circle around and observe from the edges",    "You keep your distance, watching shadows twist unnaturally around the glowing center, sensing something waiting for you inside.")
    # --- Step 7: Carnival Aerial Watch Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_aerial_watch":
        twist_carnival(    "From above, the carnival stretches endlessly, but the lights flicker strangely, revealing figures that vanish when looked at directly…",    "Climb higher to get a better view",    "You ascend carefully, feeling the air grow colder, and notice shadows moving in patterns that shouldn’t exist.",    "Stay hidden and observe from the current height",    "You crouch among the beams, watching the carnival below shift unnaturally, and hear faint whispers riding the wind.")
    # --- Step 7: Carnival Funhouse Trail Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_trail":
        twist_carnival(    "The funhouse trail twists endlessly, mirrors reflecting impossible corridors and distorted laughter echoing from all directions…",    "Press forward deeper into the trail",    "You navigate the warped hallways, each reflection showing a version of yourself that moves independently, almost mocking you.",    "Step back and explore another section carefully",    "You retreat slightly, noticing a hidden door behind a cracked mirror, shadows flickering across the walls as if alive.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_mysteries":
        twist_carnival(    "The carousel spins slowly, but the painted horses’ eyes seem to follow you, glowing faintly in the dark…",    "Mount a horse and ride carefully",    "You take a seat on a carved horse, feeling the platform tremble as if alive, the carnival around you warping subtly.",    "Step back and observe the carousel cautiously",    "You watch the horses, noticing strange movements in the shadows and hearing faint, distorted laughter coming from the ride.")
    # --- Step 7: Carnival Stalls Alley Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_stalls_alley":
        twist_carnival(    "The alley between the stalls narrows unnaturally, and the dim lights flicker, revealing figures that vanish when approached…",    "Move forward into the alley cautiously",    "You step into the alley, shadows stretching and twisting along the walls, and faint whispers brush against your ears.",    "Retreat to the open midway and observe",    "You pull back slightly, noticing movement among the stalls as if unseen hands are rearranging them, and the carnival sounds distort.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_gamebooth_mystery":
        twist_carnival(    "The carousel spins slowly, but the painted horses’ eyes seem to follow you, glowing faintly in the dark…",    "Mount a horse and ride carefully",    "You take a seat on a carved horse, feeling the platform tremble as if alive, the carnival around you warping subtly.",    "Step back and observe the carousel cautiously",    "You watch the horses, noticing strange movements in the shadows and hearing faint, distorted laughter coming from the ride.")
    # --- Step 7: Carnival Stalls Alley Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_trails":
        twist_carnival(    "The alley between the stalls narrows unnaturally, and the dim lights flicker, revealing figures that vanish when approached…",    "Move forward into the alley cautiously",    "You step into the alley, shadows stretching and twisting along the walls, and faint whispers brush against your ears.",    "Retreat to the open midway and observe",    "You pull back slightly, noticing movement among the stalls as if unseen hands are rearranging them, and the carnival sounds distort.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_mask_room":
        twist_carnival(    "The carousel spins slowly, but the painted horses’ eyes seem to follow you, glowing faintly in the dark…",    "Mount a horse and ride carefully",    "You take a seat on a carved horse, feeling the platform tremble as if alive, the carnival around you warping subtly.",    "Step back and observe the carousel cautiously",    "You watch the horses, noticing strange movements in the shadows and hearing faint, distorted laughter coming from the ride.")
    # --- Step 7: Carnival Stalls Alley Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_side_corridor":
        twist_carnival(    "The alley between the stalls narrows unnaturally, and the dim lights flicker, revealing figures that vanish when approached…",    "Move forward into the alley cautiously",    "You step into the alley, shadows stretching and twisting along the walls, and faint whispers brush against your ears.",    "Retreat to the open midway and observe",    "You pull back slightly, noticing movement among the stalls as if unseen hands are rearranging them, and the carnival sounds distort.")
    # --- Step 7: Carnival Carousel Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_mysteryy":
        twist_carnival(    "The carousel spins slowly, though no one seems to be operating it, and the horses’ eyes glint unnaturally…",    "Climb onto a horse and try to ride it",    "As you mount the horse, it jerks forward on its own, carrying you toward the shadows at the edge of the carnival.",    "Step back and watch the carousel carefully",    "From the ground, you notice the horses shifting positions subtly, their shadows stretching like fingers across the ground.")
    # --- Step 7: Carnival Funhouse Mirror Glimpse Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_mirror_glimpse":
        twist_carnival(    "The mirrors reflect more than your own image; fleeting figures appear behind you, disappearing when you turn…",    "Step closer to investigate the figures",    "You approach cautiously, and one of the reflections reaches out, brushing your shoulder, sending chills down your spine.",    "Ignore the figures and focus on your reflection",    "You concentrate on your own reflection, but it slowly morphs into a distorted version of yourself, smiling in ways you don’t.")
    # --- Step 7: Carnival Balloon Room Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_balloon_room":
        twist_carnival(    "The room is filled with floating balloons, each reflecting strange, distorted faces as they bob gently in the air…",    "Reach for a balloon and pop it",    "As you pop one, a rush of cold air envelopes you, and a whisper seems to echo your own name from somewhere in the room.",    "Step carefully through the balloons without touching them",    "You weave between the floating spheres, noticing that the faces in the reflections seem to follow your every move.")
    # --- Step 7: Carnival Shadow Corridor Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_shadow_corridor":
        twist_carnival(    "The corridor stretches endlessly, shadows shifting along the walls as if alive, beckoning you forward…",    "Follow the moving shadows cautiously",    "You step forward, feeling the walls pulse subtly, the shadows stretching toward you in almost human shapes.",    "Avoid the shadows and move along the edge of the corridor",    "You hug the wall, trying not to touch the moving darkness, but whispers seem to leak from the shadows, speaking in a language you almost understand.")
    # --- Step 7: Carnival Mirror Memory Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_mirror_memory":
        twist_carnival(    "The mirror shows your reflection, but your movements seem slightly delayed, as if another version of you exists…",    "Step closer and touch the mirror",    "Your fingers meet cold glass, and suddenly the reflection smirks independently, hinting at secrets hidden within the carnival.",    "Step back and observe your reflection carefully",    "You watch intently as the reflection mimics you, but subtle differences appear—gestures that you did not make, leading you to wonder what lurks beyond the glass.")
    # --- Step 7: Carnival Tent Outside Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_tent_outside":
        twist_carnival(    "Outside the main tent, the carnival lights flicker, casting twisted shadows across the empty stalls…",    "Enter the tent cautiously",    "You step inside, the fabric brushing against you, and a strange sense of being watched sends chills down your spine.",    "Circle around the tent and inspect the surroundings",    "You cautiously move around, noticing footprints that vanish mysteriously, and distant laughter that seems just out of reach.")
    # --- Step 7: Carnival Carousel Up Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_up":
        twist_carnival(    "The carousel spins faster than it should, lights blurring into streaks of color, and faint music whispers your name…",    "Climb onto a horse and ride",    "As you mount the painted horse, it jerks unexpectedly, and the world around you seems to stretch and bend in impossible ways.",    "Step back and watch the carousel carefully",    "You observe from the ground, noticing shadows flicker between the horses and strange figures moving in the corners of your vision.")
    # --- Step 7: Carnival Carousel Shadow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_carousel_shadow":
        twist_carnival(    "A shadow moves independently on the carousel, defying the patterns of light and the ride itself…",    "Follow the shadow toward the center of the carousel",    "You approach cautiously, heart pounding, and the shadow seems to swirl around you, beckoning you deeper into the carnival's mysteries.",    "Step back and stay near the edge",    "You keep your distance, the shadow twisting unnaturally, hinting at secrets hidden in plain sight on the spinning ride.")
    # --- Step 7: Carnival Candy Mystery Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_candy_mystery":
        twist_carnival(    "The candy stand glows eerily, the sweets almost pulsing as if alive…",    "Reach out and pick a candy",    "As you touch the candy, a tingling sensation runs through your fingers, and the carnival around you seems to warp subtly.",    "Step back and observe the stand cautiously",    "You watch as the candies shift and glimmer, some forming shapes that look disturbingly like faces.")
    # --- Step 7: Carnival Stuffed Shadow Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_stuffed_shadow":
        twist_carnival(    "A stuffed animal in the corner moves on its own, eyes glinting in the dim light…",    "Approach the stuffed animal bravely",    "You step closer, and it twitches as if alive, the shadows around it lengthening and curling like hands.",    "Keep your distance and watch silently",    "From afar, you notice other stuffed figures beginning to stir, the shadows linking them together in an unnatural pattern.")
    # --- Step 7: Carnival Mirror Portal Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_mirror_portal":
        twist_carnival(    "The mirror shimmers unnaturally, revealing a shadowy portal within its surface…",    "Step through the mirror bravely",    "You step into the portal, feeling the carnival dissolve around you into swirling lights and distant laughter.",    "Step back and study the portal carefully",    "You observe the portal from a safe distance, noticing faint figures moving inside as if beckoning you.")
    # --- Step 7: Carnival Mirror Observe Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_mirror_observe":
        twist_carnival(    "The mirror reflects not only your image, but faint movements behind you that shouldn't exist…",    "Investigate the reflections closely",    "You focus on the reflections, realizing they mimic actions you haven't made yet, twisting reality around you.",    "Step away from the mirror cautiously",    "You retreat slightly, feeling the reflections follow your movements, shadows stretching unnaturally behind you.")
    # --- Step 7: Carnival Funhouse Corridor Deep Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_corridor_deep":
        twist_carnival(    "The warped mirrors stretch endlessly, and the corridor seems to pulse with a life of its own…",    "Push forward deeper into the corridor",    "You step carefully, mirrors bending your reflection into eerie shapes, and a whisper seems to guide you forward.",    "Retreat toward the outer funhouse entrance",    "You step back, noticing the mirrors now reflect fleeting shadows of something moving behind you.")

    # --- Step 7: Carnival Funhouse Outer Twist ---
    if st.session_state.current_step == 7 and st.session_state.branch == "carnival_funhouse_outer":
        twist_carnival(    "Outside the funhouse, the carnival lights flicker unnaturally, casting long, twisting shadows…",    "Move toward the flickering lights boldly",    "You advance through the shadowy midway, the laughter of unseen visitors echoing around you.",    "Step back and observe from the funhouse doorway","From the doorway, you see strange movements between the stalls, almost as if the carnival itself is alive." )
    
    if "story_progress" in st.session_state and st.session_state.story:  # Check if story exists
        st.subheader("🎭 Your Horror Story Summary")

        with st.expander("🔒 View and download your completed story (password protected)"):
            password_check = st.text_input("Enter your password to unlock story:", type="password")
            if st.button("Unlock Story"):
                if password_check == st.session_state.password:
                    st.success("✅ Access granted! Here's your story:")
                    st.text_area("Your Story:", st.session_state.story, height=600)
                    st.download_button(
                        label="⬇️ Download Final Story",
                        data=st.session_state.story,
                        file_name=f"{st.session_state.username}_{st.session_state.branch}_story.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Incorrect password! Try again.")
        if st.button("🔄 Start Over / Reset"):
            for key in [
                "user_authenticated", "username", "password", "story",
                "story_progress", "current_step", "branch", "rerun"
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("Session cleared. You can start again!")
            st.stop()
    if st.session_state.story_complete:
        if st.session_state.step == 4:
            st.markdown("**🎃👻💀 You survived the quick scare… but the shadows still whisper.**")
        else:
            if st.session_state.branch == "hospital_beginning":
                st.markdown("**🏥🩸😱 You survived… but the hospital still whispers.**")
            elif st.session_state.branch == "forest_beginning":
                st.markdown("**🌲🌫️👹 The forest story concludes with this chilling twist!**")
            elif st.session_state.branch == "carnival_beginning":
                st.markdown("**🎡🤡🎠 You escaped the carnival… but the laughter still follows you.**")