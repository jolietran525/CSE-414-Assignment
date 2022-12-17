from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_patient is not None or current_caregiver is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # search_caregiver_schedule <date>
    #  check 1: check if the current logged-in user is a caregiver/patient
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return
    
    # check 2: the length for tokens need to be exactly 2 to include all information
    if len(tokens) != 2:
        print("Please try again!")
        return
    
    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()

    caregive_name = "SELECT Avai.Username FROM Availabilities Avai LEFT OUTER JOIN Appointments Appoint ON Avai.Time = Appoint.Time AND Avai.Username = Appoint.cg_name WHERE Avai.Time = %s AND Appoint.AppointmentID IS NULL ORDER BY Avai.Username"
    vaccine_dose = "SELECT Name, Doses FROM Vaccines"

    try:
        d = datetime.datetime(year, month, day)
        
        cursor.execute(caregive_name, d)
        caregiver_name = cursor.fetchone()

        if caregiver_name is None:
            print("No Caregiver is available!")
        else:
            while caregiver_name is not None:
                print(caregiver_name[0])
                caregiver_name = cursor.fetchone()

        cursor.execute(vaccine_dose)
        for row in cursor:
            print(str(row[0]) + " " + str(row[1]))
    
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def reserve(tokens):
    #  reserve <date> <vaccine>
    #  check 1: check if the current logged-in user is a patient
    global current_patient
    global current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    
    if current_patient is None and current_caregiver is not None:
        print("Please login as patient first!")
        return
    
    # check 2: the length for tokens need to be exactly 3 to include all information
    if len(tokens) != 3:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    vaccine_name = tokens[2]
    vaccine = None

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()

    caregive_availability = "SELECT TOP 1 Avai.Username FROM Availabilities Avai LEFT OUTER JOIN Appointments Appoint ON Avai.Time = Appoint.Time AND Avai.Username = Appoint.cg_name WHERE Avai.Time = %s AND Appoint.AppointmentID IS NULL ORDER BY Avai.Username"
    add_appointment = "INSERT INTO Appointments(cg_name, time, p_name, vaccine) VALUES (%s, %s, %s, %s)"
    appointment_info = "SELECT cg_name, AppointmentID FROM Appointments WHERE Time = %s AND cg_name = %s"

    try:
        
        # first check the availability of the vaccine dose
        vaccine = Vaccine(vaccine_name, 1).get()
        
        if vaccine.get_available_doses() == 0:
            print("Not enough available doses!")
            return
    
        else:
            d = datetime.datetime(year, month, day)
            cursor.execute(caregive_availability, d)
            caregiver_name = cursor.fetchone()

            if caregiver_name is None:
                print("No Caregiver is available!")
                return

            else:
                cursor.execute(add_appointment, (caregiver_name[0], d, current_patient.get_username(), vaccine_name))
                conn.commit()
                vaccine.decrease_available_doses(1)
                cursor.execute(appointment_info, (d, caregiver_name[0]))
                for row in cursor:
                    print("AppointmentID: " + str(row[1]) + ", Caregiver name: " + str(row[0]))
       
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    #  check 1: check if the the user is logged in
    global current_patient
    global current_caregiver

    if current_patient is None and current_caregiver is None:
        print("Please log in first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information
    if len(tokens) != 2:
        print("Please try again!")
        return

    appointmentID = int(tokens[1])

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()

    try:
        if current_caregiver is not None:
            appointment_info_cg = "SELECT AppointmentID FROM Appointments WHERE AppointmentID = %s AND cg_name = %s"
            cursor.execute(appointment_info_cg, (appointmentID, current_caregiver.get_username()))

            # check if the appointment id and the caregiver name match up
            check_appointmentID = cursor.fetchone()

            if check_appointmentID is None:
                print("There is no such appointment!")
                return
            else:
                cancel_appointment_cg = "DELETE FROM Appointments WHERE AppointmentID = %s AND cg_name = %s"
                cursor.execute(cancel_appointment_cg, (appointmentID, current_caregiver.get_username()))
                print("Appointment " + str(appointmentID) +" is succesfully canceled!")
                
        else:
            appointment_info_p = "SELECT AppointmentID FROM Appointments WHERE AppointmentID = %s AND p_name = %s"
            cursor.execute(appointment_info_p, (appointmentID, current_patient.get_username()))
            
            # check if the appointment id and the patient name match up
            check_appointmentID = cursor.fetchone()

            if check_appointmentID is None:
                print("There is no such appointment!")
                return
            
            else:
                cancel_appointment_p = "DELETE FROM Appointments WHERE AppointmentID = %s AND p_name = %s"
                cursor.execute(cancel_appointment_p, (appointmentID, current_patient.get_username()))
                print("Appointment " + str(appointmentID) +" is succesfully canceled!")
    
    except pymssql.Error:
        print("Please try again!")
        raise

    except Exception as e:
        print(e)
        return
    
    finally:
        cm.close_connection()


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    # show_appointments
    #  check 1: check if the the user is logged in
    global current_patient
    global current_caregiver

    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    
    #  If the current logged in user is a patient
    if current_patient is not None:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        appointment_info_p = "SELECT AppointmentID, vaccine, Time, cg_name FROM Appointments WHERE p_name = %s ORDER BY AppointmentID"

        try:
            cursor.execute(appointment_info_p, current_patient.get_username())

            for row in cursor:
                print(str(row['AppointmentID']) + " " + str(row['vaccine']) + " " + str(row['Time']) + " " + str(row['cg_name']))

        except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()
        
        finally:
            cm.close_connection()

    #  If the current logged in user is a caregiver
    elif current_caregiver is not None:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        appointment_info_cg = "SELECT AppointmentID, vaccine, Time, p_name FROM Appointments WHERE cg_name = %s ORDER BY AppointmentID"

        try:
            cursor.execute(appointment_info_cg, current_caregiver.get_username())

            for row in cursor:
                print(str(row['AppointmentID']) + " " + str(row['vaccine']) + " " + str(row['Time']) + " " + str(row['p_name']))

        except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()

        finally:
            cm.close_connection()


def logout(tokens):
    # logout
    #  check 1: check if the the user is logged in
    global current_patient
    global current_caregiver

    if current_patient is None and current_caregiver is None:
        print("Please log in first!")
        return

    try:
        if current_patient is not None:
            current_patient = None
            print("Successfully logged out!")
        elif current_caregiver is not None:
            current_caregiver = None
            print("Successfully logged out!")
    
    except:
        print("Please try again!")
        quit()


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == 'cancel':
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()