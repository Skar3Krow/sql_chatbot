CREATE TABLE job_details (
    title varchar(20),
    company varchar(10),
    location varchar(50),
    description varchar(100)
);

INSERT INTO job_details VALUES("CEO", "AllTech", "Toronto", "Just rule the company");

CREATE TABLE jhansi_hirpara_assets (
    id INTEGER NOT NULL,
    name VARCHAR(10),
    plant_name VARCHAR(10),
    plant_id INTEGER
);

CREATE TABLE timeSeriesData (
    timestamp TIMESTAMP,
    accumulated_gii_radiation INTEGER,
    ambient_temp INTEGER,
    ambient_temperature INTEGER,
    baromatic_pressure INTEGER,
    barometric_pressure INTEGER,
    communication_status INTEGER,
    gii_radiation INTEGER,
    ghi_radiation INTEGER,
    humidity INTEGER,
    module_temperature INTEGER,
    poa_radiation INTEGER,
    accumulated_poa_radiation INTEGER,
    rain INTEGER,
    wind_direction INTEGER,
    wind_speed INTEGER
);