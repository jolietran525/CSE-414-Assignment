CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Appointments (
    AppointmentID INT IDENTITY(1,1),
    cg_name varchar(255),
    Time date,
    p_name varchar(255) REFERENCES Patients,
    vaccine varchar(255),
    FOREIGN KEY (Time, cg_name) REFERENCES Availabilities,
    PRIMARY KEY (AppointmentID)
);