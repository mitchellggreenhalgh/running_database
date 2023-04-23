from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from widget_formats import universal_format as formats
from backup_database import db_backupper
from split_conversions import split_converter
import sqlite3


# Instantiate app
root = Tk()
root.title('Data Entry Tool')

# Instantiate notebook
nb = ttk.Notebook(root)
nb.pack(fill='both', expand = 1)

# Database Connection
db_name = db_backupper().db_name

# Backup Database
create_backup = db_backupper()
try: 
    create_backup._backup()

except:
    override_backup = messagebox.askyesno(title = 'Database Updater', message = 'Recent backup within last 30 days found. Backup database anyway?')
    if override_backup:
        create_backup._backup_override()
        # TODO: app won't work if override completes?
    else:
        messagebox.showinfo(title = 'Database Updater', message = 'No backup created')

#region <Athlete Tab>
athlete_frame = ttk.Frame(nb, padding = formats.frame_padding)
athlete_frame.grid(column = 0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_athlete(*args):
    athlete_info = athlete_name.get().lower()    
    try:
        if athlete_school_year.get() != 0:
            entry_confirmation_athlete.set(f"Submitted {athlete_info}'s \ninformation to the database")
            enter_data_athlete()
        else:
            entry_confirmation_athlete.set(f"Please enter data")
            raise Exception
                
    except ValueError:
        pass

def enter_data_athlete():
    insert_query = '''
    INSERT INTO athletes (
        athlete, 
        school_year_beginning, 
        grade,
        sex
    ) VALUES (?, ?, ?, ?)
    '''

    insert_data = (athlete_name.get().lower(), 
                   athlete_school_year.get(), 
                   athlete_grade.get(), athlete_sex.get())
    
    running_db = sqlite3.connect(db_name)
    cursor = running_db.cursor()
    cursor.execute(insert_query, insert_data)
    running_db.commit()
    running_db.close()

ttk.Label(athlete_frame, text = 'Athlete [first last]').grid(column = 0, row = 0, sticky = formats.label_sticky)
athlete_name = StringVar()
athlete_name_entry = ttk.Entry(athlete_frame, width = 10, textvariable = athlete_name).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(athlete_frame, text = 'School Year (fall semester year) [yyyy]').grid(column = 1, row = 0, sticky = formats.label_sticky)
athlete_school_year = IntVar()
athlete_school_year_entry = ttk.Entry(athlete_frame, width = 10, textvariable = athlete_school_year).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(athlete_frame, text = 'Grade [#, 9-12]').grid(column = 2, row = 0, sticky = formats.label_sticky)
athlete_grade = IntVar()
athlete_grade_entry = ttk.Entry(athlete_frame, width = 10, textvariable = athlete_grade).grid(column = 2, row = 1, sticky = formats.entry_sticky)

ttk.Label(athlete_frame, text = 'Sex [m/f]').grid(column = 3, row = 0, sticky = formats.label_sticky)
athlete_sex = StringVar()
athlete_sex_entry = ttk.Entry(athlete_frame, width = 5, textvariable = athlete_sex).grid(column = 3, row = 1, sticky = formats.entry_sticky)

entry_confirmation_athlete = StringVar()    
ttk.Label(athlete_frame, textvariable = entry_confirmation_athlete).grid(column = 0, row = 2, sticky = formats.label_sticky)
ttk.Button(athlete_frame, text = 'Submit', command = confirm_entries_athlete).grid(column = 4, row = 1, sticky = formats.button_sticky)

for child in athlete_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)
#endregion

#region <Splits Tab>
splits_frame = ttk.Frame(nb, padding = formats.frame_padding)
splits_frame.grid(column = 0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_splits(*args):
    athlete_info = splits_athlete.get()
    
    try:
        entry_confirmation_splits.set(f"Submitted {athlete_info}'s splits to the database.")
        enter_data_splits()
        
    except ValueError:
        pass

def enter_data_splits():
    insert_query = '''
    INSERT INTO race_laps (
        athlete, event_distance_m, date, meet_name, relay_y_n,
        lap_1, lap_2, lap_3, lap_4,
        lap_5, lap_6, lap_7, lap_8,
        total_time
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    converted_splits, total_time = split_converter.split_to_lap([splits_split_1.get(), splits_split_2.get(),
                                                     splits_split_3.get(), splits_split_4.get(),
                                                     splits_split_5.get(), splits_split_6.get(),
                                                     splits_split_7.get(), splits_split_8.get()])
    
    insert_data = (splits_athlete.get().lower(), splits_event.get(), splits_date.get(), splits_meet.get(), splits_relay.get()) + tuple(converted_splits) + tuple(total_time)
                   
    running_db = sqlite3.connect(db_name)
    cursor = running_db.cursor()
    cursor.execute(insert_query, insert_data)
    running_db.commit()
    running_db.close()

ttk.Label(splits_frame, text = 'Athlete [first last]').grid(column = 0, row = 0, sticky = formats.label_sticky)
splits_athlete = StringVar()
splits_athlete_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_athlete).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Event Distance [#### meters]').grid(column = 1, row = 0, sticky = formats.label_sticky)
splits_event = IntVar()
splits_event_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_event).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Date [yyyy-mm-dd]').grid(column = 2, row = 0, sticky = formats.label_sticky)
splits_date = StringVar()
splits_date_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_date).grid(column = 2, row = 1, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Meet Name [aaa bbb]').grid(column = 3, row = 0, sticky = formats.label_sticky)
splits_meet = StringVar()
splits_meet_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_meet).grid(column = 3, row = 1, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Relay Split? (y/n) [1/0]').grid(column = 4, row = 0, sticky = formats.label_sticky)
splits_relay = IntVar()
splits_relay_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_relay).grid(column = 4, row = 1, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Split 1 [mm:ss.dd]').grid(column = 0, row = 2, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 2 [mm:ss.dd]').grid(column = 1, row = 2, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 3 [mm:ss.dd]').grid(column = 2, row = 2, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 4 [mm:ss.dd]').grid(column = 3, row = 2, sticky = formats.label_sticky)
splits_split_1 = StringVar()
splits_split_2 = StringVar()
splits_split_3 = StringVar()
splits_split_4 = StringVar()
splits_split_1_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_1).grid(column = 0, row = 3, sticky = formats.entry_sticky)
splits_split_2_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_2).grid(column = 1, row = 3, sticky = formats.entry_sticky)
splits_split_3_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_3).grid(column = 2, row = 3, sticky = formats.entry_sticky)
splits_split_4_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_4).grid(column = 3, row = 3, sticky = formats.entry_sticky)

ttk.Label(splits_frame, text = 'Split 5 [mm:ss.dd]').grid(column = 0, row = 4, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 6 [mm:ss.dd]').grid(column = 1, row = 4, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 7 [mm:ss.dd]').grid(column = 2, row = 4, sticky = formats.label_sticky)
ttk.Label(splits_frame, text = 'Split 8 [mm:ss.dd]').grid(column = 3, row = 4, sticky = formats.label_sticky)
splits_split_5 = StringVar()
splits_split_6 = StringVar()
splits_split_7 = StringVar()
splits_split_8 = StringVar()
splits_split_5_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_5).grid(column = 0, row = 5, sticky = formats.entry_sticky)
splits_split_6_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_6).grid(column = 1, row = 5, sticky = formats.entry_sticky)
splits_split_7_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_7).grid(column = 2, row = 5, sticky = formats.entry_sticky)
splits_split_8_entry = ttk.Entry(splits_frame, width = 10, textvariable = splits_split_8).grid(column = 3, row = 5, sticky = formats.entry_sticky)

entry_confirmation_splits = StringVar()    
ttk.Label(splits_frame, textvariable = entry_confirmation_splits).grid(column = 4, row = 4, sticky = formats.label_sticky)
ttk.Button(splits_frame, text = 'Submit', command = confirm_entries_splits).grid(column = 4, row = 5, sticky = formats.button_sticky)

for child in splits_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)
#endregion

#region <Laps Tab>  #TODO: functionality
laps_frame = ttk.Frame(nb, padding = formats.frame_padding)
laps_frame.grid(column = 0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_laps(*args):
    raise NotImplementedError

def enter_data_laps(_distance):
    # race_distance_m.get(): make dictionary of key:distance, value:entry fxn specific for that distance (do the math before entering it into a database?)
    raise NotImplementedError

ttk.Label(laps_frame, text = 'Athlete [first last]').grid(column = 0, row = 0, sticky = formats.label_sticky)
laps_athlete = StringVar()
laps_athlete_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_athlete).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Event Distance [#### meters]').grid(column = 1, row = 0, sticky = formats.label_sticky)
laps_event = IntVar()
laps_event_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_event).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Date [yyyy-mm-dd]').grid(column = 2, row = 0, sticky = formats.label_sticky)
laps_date = StringVar()
laps_date_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_date).grid(column = 2, row = 1, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Meet Name [aaa bbb]').grid(column = 3, row = 0, sticky = formats.label_sticky)
laps_meet = StringVar()
laps_meet_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_meet).grid(column = 3, row = 1, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Relay Split? (y/n) [1/0]').grid(column = 4, row = 0, sticky = formats.label_sticky)
laps_relay = IntVar()
laps_relay_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_relay).grid(column = 4, row = 1, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Lap 1 [mm:ss.dd]').grid(column = 0, row = 2, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 2 [mm:ss.dd]').grid(column = 1, row = 2, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 3 [mm:ss.dd]').grid(column = 2, row = 2, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 4 [mm:ss.dd]').grid(column = 3, row = 2, sticky = formats.label_sticky)
laps_lap_1 = StringVar()
laps_lap_2 = StringVar()
laps_lap_3 = StringVar()
laps_lap_4 = StringVar()
laps_lap_1_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_1).grid(column = 0, row = 3, sticky = formats.entry_sticky)
laps_lap_2_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_2).grid(column = 1, row = 3, sticky = formats.entry_sticky)
laps_lap_3_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_3).grid(column = 2, row = 3, sticky = formats.entry_sticky)
laps_lap_4_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_4).grid(column = 3, row = 3, sticky = formats.entry_sticky)

ttk.Label(laps_frame, text = 'Lap 5 [mm:ss.dd]').grid(column = 0, row = 4, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 6 [mm:ss.dd]').grid(column = 1, row = 4, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 7 [mm:ss.dd]').grid(column = 2, row = 4, sticky = formats.label_sticky)
ttk.Label(laps_frame, text = 'Lap 8 [mm:ss.dd]').grid(column = 3, row = 4, sticky = formats.label_sticky)
laps_lap_5 = StringVar()
laps_lap_6 = StringVar()
laps_lap_7 = StringVar()
laps_lap_8 = StringVar()
laps_lap_5_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_5).grid(column = 0, row = 5, sticky = formats.entry_sticky)
laps_lap_6_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_6).grid(column = 1, row = 5, sticky = formats.entry_sticky)
laps_lap_7_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_7).grid(column = 2, row = 5, sticky = formats.entry_sticky)
laps_lap_8_entry = ttk.Entry(laps_frame, width = 10, textvariable = laps_lap_8).grid(column = 3, row = 5, sticky = formats.entry_sticky)

entry_confirmation_laps = StringVar()    
ttk.Label(laps_frame, textvariable = entry_confirmation_laps).grid(column = 4, row = 4, sticky = formats.label_sticky)
ttk.Button(laps_frame, text = 'Submit', command = confirm_entries_laps).grid(column = 4, row = 5, sticky = formats.button_sticky)

for child in laps_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)
#endregion

#region <800m Tab>
db_800_frame = ttk.Frame(nb, padding = formats.frame_padding)
db_800_frame.grid(column = 0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_800(*args):
    athlete_info = athlete_800.get().lower()    
    try:
        
        if first_200.get() != 0 and first_400.get() == 0:
            entry_confirmation_800.set(f"Submitted {athlete_info}'s 200s to the database")
            enter_data_800()

        elif first_400.get() != 0 and first_200.get() == 0:
            entry_confirmation_800.set(f"Submitted {athlete_info}'s 400s to database")
            enter_data_800()

        elif first_200.get() != 0 and first_400.get() != 0:
            entry_confirmation_800.set(f"Submitted {athlete_info}'s results to database")
            enter_data_800()

        else:
            entry_confirmation_800.set('All Zeros')
            raise Exception('No data entered')
                
    except ValueError:
        pass

def enter_data_800():
    insert_query = '''
    INSERT INTO db800 (
        athlete, 
        first_200, second_200, third_200, fourth_200,
        first_400, second_400
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    insert_data = (athlete_800.get().lower(), 
                   first_200.get(), second_200.get(), third_200.get(), fourth_200.get(),
                   first_400.get(), second_400.get())
    
    running_db = sqlite3.connect(db_name)
    cursor = running_db.cursor()
    cursor.execute(insert_query, insert_data)
    running_db.commit()
    running_db.close()
    

ttk.Label(db_800_frame, text = 'Athlete [first last]').grid(column = 0, row = 0, sticky = formats.label_sticky)
athlete_800 = StringVar()
athlete_800_entry = ttk.Entry(db_800_frame, width = 10, textvariable = athlete_800).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '200 #1 [#.##]').grid(column = 1, row = 0, sticky = formats.label_sticky)
first_200 = DoubleVar()
first_200_entry = ttk.Entry(db_800_frame, width = 10, textvariable = first_200).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '200 #2 [#.##]').grid(column = 2, row = 0, sticky = formats.label_sticky)
second_200 = DoubleVar()
second_200_entry = ttk.Entry(db_800_frame, width = 10, textvariable = second_200).grid(column = 2, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '200 #3 [#.##]').grid(column = 3, row = 0, sticky = formats.label_sticky)
third_200 = DoubleVar()
third_200_entry = ttk.Entry(db_800_frame, width = 10, textvariable = third_200).grid(column = 3, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '200 #4 [#.##]').grid(column = 4, row = 0, sticky = formats.label_sticky)
fourth_200 = DoubleVar()
fourth_200_entry = ttk.Entry(db_800_frame, width = 10, textvariable = fourth_200).grid(column = 4, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '400 #1 [#.##]').grid(column = 1, row = 2, sticky = formats.label_sticky)
first_400 = DoubleVar()
first_400_entry = ttk.Entry(db_800_frame, width = 10, textvariable = first_400).grid(column = 1, row = 3, sticky = formats.entry_sticky)

ttk.Label(db_800_frame, text = '400 #2 [#.##]').grid(column = 2, row = 2, sticky = formats.label_sticky)
second_400 = DoubleVar()
second_400_entry = ttk.Entry(db_800_frame, width = 10, textvariable = second_400).grid(column = 2, row = 3, sticky = formats.entry_sticky)

entry_confirmation_800 = StringVar()
ttk.Label(db_800_frame, textvariable = entry_confirmation_800).grid(column = 0, row = 6, sticky = formats.label_sticky)
ttk.Button(db_800_frame, text = 'Submit', command = confirm_entries_800).grid(column = 3, row = 6, sticky = formats.button_sticky)

for child in db_800_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)

root.bind('<Control-Return>', confirm_entries_800)  # https://stackoverflow.com/questions/46345039/python-tkinter-binding-keypress-event-to-active-tab-in-ttk-notebook

#endregion

#region <400m Tab>
db_400_frame = ttk.Frame(nb, padding = formats.frame_padding)
db_400_frame.grid(column = 0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_400(*args):
    athlete_info = athlete_400.get().lower()    
    try:
        if first_200_400.get() != 0:
            entry_confirmation_400.set(f"Submitted {athlete_info}'s 200s to the database")
            enter_data_400()
            
        else:
            entry_confirmation_400.set('All Zeros')
            raise Exception('No data entered')
                
    except ValueError:
        pass

def enter_data_400():
    insert_query = '''
    INSERT INTO db400 (
        athlete, 
        first_200, second_200
    ) VALUES (?, ?, ?)
    '''

    insert_data = (athlete_400.get().lower(), 
                   first_200_400.get(), second_200_400.get())
    
    running_db = sqlite3.connect(db_name)
    cursor = running_db.cursor()
    cursor.execute(insert_query, insert_data)
    running_db.commit()
    running_db.close()
    

ttk.Label(db_400_frame, text = 'Athlete [first last]').grid(column = 0, row = 0, sticky = formats.label_sticky)
athlete_400 = StringVar()
athlete_400_entry = ttk.Entry(db_400_frame, width = 10, textvariable = athlete_400).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_400_frame, text = '200 #1 [#.##]').grid(column = 1, row = 0, sticky = formats.label_sticky)
first_200_400 = DoubleVar()
first_200_400_entry = ttk.Entry(db_400_frame, width = 10, textvariable = first_200_400).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(db_400_frame, text = '200 #2 [#.##]').grid(column = 2, row = 0, sticky = formats.label_sticky)
second_200_400 = DoubleVar()
second_200_400_entry = ttk.Entry(db_400_frame, width = 10, textvariable = second_200_400).grid(column = 2, row = 1, sticky = formats.entry_sticky)

entry_confirmation_400 = StringVar()
ttk.Label(db_400_frame, textvariable = entry_confirmation_400).grid(column = 0, row = 2, sticky = formats.label_sticky)
ttk.Button(db_400_frame, text = 'Submit', command = confirm_entries_400).grid(column = 3, row = 1, sticky = formats.button_sticky)

for child in db_400_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 5)
#endregion

#region <Meet Info tab>  # TODO: functionality
meet_frame = ttk.Frame(nb, padding = formats.frame_padding)
meet_frame.grid(column=0, row = 0, sticky = formats.frame_sticky)

def confirm_entries_meet():
    raise NotImplementedError

def enter_data_meet():
    raise NotImplementedError

ttk.Label(meet_frame, text = 'Meet Name [aaa bbb]').grid(column = 0, row = 0, sticky = formats.label_sticky)
meet_name = StringVar()
meet_name_entry = ttk.Entry(meet_frame, width = 10, textvariable = meet_name).grid(column = 0, row = 1, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Date [yyyy-mm-dd]').grid(column = 1, row = 0, sticky = formats.label_sticky)
meet_date = StringVar()
meet_date_entry = ttk.Entry(meet_frame, width = 10, textvariable = meet_date).grid(column = 1, row = 1, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Host [northridge high school]').grid(column = 2, row = 0, sticky = formats.label_sticky)
meet_host = StringVar()
meet_host_entry = ttk.Entry(meet_frame, width = 10, textvariable = meet_host).grid(column = 2, row = 1, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Location [sokol park]').grid(column = 3, row = 0, sticky = formats.label_sticky)
meet_location = StringVar()
meet_location_entry = ttk.Entry(meet_frame, width = 10, textvariable = meet_location).grid(column = 3, row = 1, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'City, State [Tuscaloosa, AL]').grid(column = 4, row = 0, sticky = formats.label_sticky)
meet_city_state = StringVar()
meet_city_state_entry = ttk.Entry(meet_frame, width = 15, textvariable = meet_city_state).grid(column = 4, row = 1, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Mean Temperature (*F) [##]').grid(column = 0, row = 2, sticky = formats.label_sticky)
meet_temp = IntVar()
meet_temp_entry = ttk.Entry(meet_frame, width = 5, textvariable = meet_temp).grid(column = 0, row = 3, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Cloud Cover [0-2]').grid(column = 1, row = 2, sticky = formats.label_sticky)
meet_clouds = IntVar()
meet_clouds_entry = ttk.Entry(meet_frame, width = 5, textvariable = meet_clouds).grid(column = 1, row = 3, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Avg. Precipitation [0-3]').grid(column = 2, row = 2, sticky = formats.label_sticky)
meet_precipitation = IntVar()
meet_precipitation_entry = ttk.Entry(meet_frame, width = 5, textvariable = meet_precipitation).grid(column = 2, row = 3, sticky = formats.entry_sticky)

ttk.Label(meet_frame, text = 'Weather Notes [aaa bbb]').grid(column = 3, row = 2, sticky = formats.label_sticky)
meet_weather = StringVar()
meet_weather_entry = ttk.Entry(meet_frame, width = 15, textvariable = meet_weather).grid(column = 3, row = 3, sticky = formats.entry_sticky)

entry_confirmation_meet = StringVar()
ttk.Label(meet_frame, textvariable = entry_confirmation_meet).grid(column = 0, row = 4, sticky = formats.label_sticky)
ttk.Button(meet_frame, text = 'Submit', command = confirm_entries_meet).grid(column = 4, row = 3, sticky = formats.button_sticky)

for child in meet_frame.winfo_children():
    child.grid_configure(padx = 5, pady = 3)
#endregion

# Add frames to notebook
nb.add(athlete_frame, text = 'Athlete Info')
nb.add(meet_frame, text = 'Meet Info')
nb.add(splits_frame, text = 'Race Splits')
nb.add(laps_frame, text = 'Lap Splits')
nb.add(db_800_frame, text = '800m Database')
nb.add(db_400_frame, text = '400m Database')

nb.select(meet_frame)  

root.mainloop()