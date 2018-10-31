DROP DATABASE IF EXISTS mua_data;
CREATE DATABASE mua_data;
USE mua_data;

CREATE TABLE experiments (
    experiment_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    experiment_name VARCHAR(150) UNIQUE NOT NULL,
    experiment_home_dir VARCHAR(250),
    dat_file_dir VARCHAR(250),
    last_edited TIMESTAMP DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE eeg_configs (
    eeg_config_id INT AUTO_INCREMENT PRIMARY KEY,
    num_chans INT NOT NULL,
    pre_amp VARCHAR(200),
    connector VARCHAR(200)
);

CREATE TABLE eeg_chans (
    eeg_chan_id INT AUTO_INCREMENT PRIMARY KEY,
    eeg_config_id INT NOT NULL,
    chan_index INT,
    continuous_chan INT,
    region VARCHAR(150),
    FOREIGN KEY(eeg_config_id)
        REFERENCES eeg_configs(eeg_config_id)
        ON DELETE CASCADE
);

CREATE TABLE probes (
    probe_id INT AUTO_INCREMENT PRIMARY KEY,
    probe_company VARCHAR(250),
    series VARCHAR(250),
    num_shanks INT NOT NULL,
    num_channels INT NOT NULL
);

CREATE TABLE probe_chans(
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    probe_id INT NOT NULL,
    channel_index INT NOT NULL,
    shank INT NOT NULL,
    continuous_channel INT NOT NULL,
    FOREIGN KEY(probe_id)
        REFERENCES probes(probe_id)
        ON DELETE CASCADE
);

CREATE TABLE experimental_groups (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT NOT NULL,
    pretreatment VARCHAR(100),
    cond1 VARCHAR(100),
    cond2 VARCHAR(100),
    FOREIGN KEY(experiment_id)
        REFERENCES experiments(experiment_id)
        ON DELETE CASCADE
);

CREATE TABLE mice (
    mouse_id INT AUTO_INCREMENT PRIMARY KEY,
    mouse_name VARCHAR(100),
    genotype VARCHAR(100),
    SEX CHAR(1),
    virus VARCHAR(250)
);

CREATE TABLE recordings (
    recording_id INT AUTO_INCREMENT PRIMARY KEY,
    mouse_id INT NOT NULL,
    group_id INT NOT NULL,
    probe_id INT NOT NULL,
    eeg_config INT,
    recording_date DATE NOT NULL,
    recording_time TIME,
    end_time TIME,
    probe_fs INT DEFAULT 30000,
    eeg_fs INT DEFAULT 30000,
    dat_filename VARCHAR(250) NOT NULL,
    excluded INT,
    FOREIGN KEY(mouse_id)
        REFERENCES mice(mouse_id)
        ON DELETE CASCADE,
    FOREIGN KEY(group_id)
        REFERENCES experimental_groups(group_id)
        ON DELETE CASCADE,
    FOREIGN KEY(probe_id)
        REFERENCES probes(probe_id)
        ON DELETE CASCADE,
    FOREIGN KEY(eeg_config)
        REFERENCES eeg_configs(eeg_config_id)
        ON DELETE CASCADE
);

CREATE TABLE neurons(
    neuron_id INT AUTO_INCREMENT PRIMARY KEY,
    cluster_id INT NOT NULL,
    recording_id INT NOT NULL,
    channel INT,
    FOREIGN KEY(recording_id)
        REFERENCES recordings(recording_id)
        ON DELETE CASCADE
);

CREATE TABLE spike_times (
    neuron_id INT NOT NULL,
    spike_times BIGINT NOT NULL,
    FOREIGN KEY(neuron_id)
        REFERENCES neurons(neuron_id)
        ON DELETE CASCADE,
    PRIMARY KEY (neuron_id, spike_times)
);


CREATE TABLE waveform_timepoints (
    neuron_id INT NOT NULL,
    sample INT NOT NULL,
    value DOUBLE,
    FOREIGN KEY(neuron_id)
        REFERENCES neurons(neuron_id)
        ON DELETE CASCADE,
    PRIMARY KEY (neuron_id, sample)
);
