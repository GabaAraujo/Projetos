CREATE PROCEDURE CopiarDados
AS
BEGIN
    SET NOCOUNT ON;

    -- Verificar se a tabela de destino existe; se não, criá-la
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'eqt_real_time_history')
    BEGIN
        CREATE TABLE eqt_real_time_history (
            id INT,
            state_id INT NULL,
            state_start DATETIME NULL,
            state_start_utc DATETIME NULL,
            state_category_id INT NULL,
            state_sub_category_id INT NULL,
            state_image_id INT NULL,
            hourmeter_value FLOAT NULL,
            speed TINYINT NULL,
            direction INT NULL,
            device_id INT NULL,
            device_status INT NULL,
            device_signal_level TINYINT NULL,
            destination_id INT NULL,
            related_equipment_id INT NULL,
            workplace_id INT NULL,
            last_fueling_hourmeter_value FLOAT NULL,
            time_consuming_fuel REAL NULL,
            fuel_autonomy REAL NULL,
            fuel_tank_level TINYINT NULL,
            east FLOAT NULL,
            north FLOAT NULL,
            net_id INT NULL,
            state_event_id INT NULL,
            operator_id INT NULL,
            situation INT NULL,
            creation_date DATETIME NULL,
            creation_date_utc DATETIME NULL,
            last_change_date DATETIME NULL,
            last_change_date_utc DATETIME NULL,
            operational_unit_id INT NULL,
            last_user_id INT NULL,
        )
    END

    -- Inserir dados na tabela de destino a partir da tabela de origem
    INSERT INTO eqt_real_time_history (id, state_id, state_start, state_start_utc, state_category_id, state_sub_category_id, state_image_id, hourmeter_value, speed, direction, device_id, device_status, device_signal_level, destination_id, related_equipment_id, workplace_id, last_fueling_hourmeter_value, time_consuming_fuel, fuel_autonomy, fuel_tank_level, east, north, net_id, state_event_id, operator_id, situation, creation_date, creation_date_utc, last_change_date, last_change_date_utc, operational_unit_id, last_user_id)
    SELECT id, state_id, state_start, state_start_utc, state_category_id, state_sub_category_id, state_image_id, hourmeter_value, speed, direction, device_id, device_status, device_signal_level, destination_id, related_equipment_id, workplace_id, last_fueling_hourmeter_value, time_consuming_fuel, fuel_autonomy, fuel_tank_level, east, north, net_id, state_event_id, operator_id, situation, creation_date, creation_date_utc, last_change_date, last_change_date_utc, operational_unit_id, last_user_id
    FROM eqt_real_time;
END
