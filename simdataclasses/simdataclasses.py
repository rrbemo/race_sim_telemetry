from dataclasses import dataclass, field

# TODO: build data classes for each data type I want to store which might make it easier to understand?
# The parent class for all dataclasses in RaceSimTelemetry. This
@dataclass
class RaceSimData:
    _tableName: str = field(init=False)

    @staticmethod
    def packet_to_data(packet):
        raise NotImplementedError("Subclasses must implement packet_to_data as a static method")

    def insert_string(self):
        data_dict = self._data_dictionary()
        columns = ",".join(data_dict.keys())
        values = ",".join(str(value) for value in data_dict.values())
        return f"INSERT INTO {self._tableName} ({columns}) VALUES ({values})"

    def _data_dictionary(self):
        raise NotImplementedError("Subclasses must implement _data_dictionary")

# class Session(RaceSimData):
#     sessionUID: int
#     formula: int
#     ruleset: int
#     trackId: int
#     gameMode: int
#     totalLaps: int
#     sessionType: int
#     trackLength: int
#     aiDifficulty: int



@dataclass
class LapData(RaceSimData):
    sessionUID: int
    participantIndex: int
    playerOneIndex: int # This is the index of the player (if this = participantIndex, then it is the player's telemetry)
    frameId: int
    sessionTime: float
    lastLapTimeInMS: int
    currentLapTimeInMS: int
    sector1TimeInMS: int
    sector2TimeInMS: int
    deltaToCarInFrontInMS: int
    deltaToRaceLeaderInMS: int
    lapDistance: float
    totalDistance: float
    safetyCarDelta: float
    carPosition: int
    currentLapNum: int
    pitStatus: int
    numPitStops: int
    sector: int
    currentLapInvalid: int
    penalties: int
    totalWarnings: int
    cornerCuttingWarnings: int
    numUnservedDriveThroughPens: int
    numUnservedStopGoPens: int
    gridPosition: int
    driverStatus: int
    resultStatus: int
    pitLaneTimerActive: int
    pitLaneTimeInLaneInMS: int
    pitStopTimerInMS: int
    pitStopShouldServePen: int

    _tableName = 'car_lap'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['lapData'])):
            this_participant = packet['lapData'][i]
            # Build this participant
            this_data = LapData(header['sessionUID'],
                                i, # participant index
                                header['playerCarIndex'],
                                header['frameIdentifier'],
                                header['sessionTime'],
                                this_participant['lastLapTimeInMS'],
                                this_participant['currentLapTimeInMS'],
                                this_participant['sector1TimeInMS'],
                                this_participant['sector2TimeInMS'],
                                this_participant['deltaToCarInFrontInMS'],
                                this_participant['deltaToRaceLeaderInMS'],
                                this_participant['lapDistance'],
                                this_participant['totalDistance'],
                                this_participant['safetyCarDelta'],
                                this_participant['carPosition'],
                                this_participant['currentLapNum'],
                                this_participant['pitStatus'],
                                this_participant['numPitStops'],
                                this_participant['sector'],
                                this_participant['currentLapInvalid'],
                                this_participant['penalties'],
                                this_participant['totalWarnings'],
                                this_participant['cornerCuttingWarnings'],
                                this_participant['numUnservedDriveThroughPens'],
                                this_participant['numUnservedStopGoPens'],
                                this_participant['gridPosition'],
                                this_participant['driverStatus'],
                                this_participant['resultStatus'],
                                this_participant['pitLaneTimerActive'],
                                this_participant['pitLaneTimeInLaneInMS'],
                                this_participant['pitStopTimerInMS'],
                                this_participant['pitStopShouldServePen'])

            # Append this participant to a list which will be returned
            data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'player_one_index': self.playerOneIndex,
            'frame_id': self.frameId,
            'session_time': self.sessionTime,
            'last_lap_time': self.lastLapTimeInMS,
            'current_lap_time': self.currentLapTimeInMS,
            'sector_1_time': self.sector1TimeInMS,
            'sector_2_time': self.sector2TimeInMS,
            'delta_to_car_in_front': self.deltaToCarInFrontInMS,
            'delta_to_race_leader': self.deltaToRaceLeaderInMS,
            'lap_distance': self.lapDistance,
            'total_distance': self.totalDistance,
            'safety_car_delta': self.safetyCarDelta,
            'car_position': self.carPosition,
            'current_lap_num': self.currentLapNum,
            'pit_status': self.pitStatus,
            'num_pit_stops': self.numPitStops,
            'sector': self.sector,
            'current_lap_invalid': self.currentLapInvalid,
            'penalties': self.penalties,
            'total_warnings': self.totalWarnings,
            'corner_cutting_warnings': self.cornerCuttingWarnings,
            'num_unserved_drive_through_pens': self.numUnservedDriveThroughPens,
            'num_unserved_stop_go_pens': self.numUnservedStopGoPens,
            'grid_position': self.gridPosition,
            'driver_status': self.driverStatus,
            'result_status': self.resultStatus,
            'pit_lane_timer_active': self.pitLaneTimerActive,
            'pit_lane_time_in_lane': self.pitLaneTimeInLaneInMS,
            'pit_stop_timer': self.pitStopTimerInMS,
            'pit_stop_should_serve_pen': self.pitStopShouldServePen
        }

        return data_dict

@dataclass
class Telemetry(RaceSimData):
    sessionUID: int
    participantIndex: int
    playerOneIndex: int # This is the index of the player (if this = participantIndex, then it is the player's telemetry)
    frameId: int
    sessionTime: float
    speed: int
    throttle: float
    steer: float
    brake: float
    clutch: int
    gear: int
    engineRPM: int
    drs: int
    revLightsPercent: int
    brakeTempRL: int      #0
    brakeTempRR: int     #1
    brakeTempFL: int     #2
    brakeTempFR: int    #3
    tyreSurfaceTempRL: int
    tyreSurfaceTempRR: int
    tyreSurfaceTempFL: int
    tyreSurfaceTempFR: int
    tyreInnerTempRL: int
    tyreInnerTempRR: int
    tyreInnerTempFL: int
    tyreInnerTempFR: int
    engineTemp: int
    tyrePressureRL: float
    tyrePressureRR: float
    tyrePressureFL: float
    tyrePressureFR: float
    surfaceTypeRL: int
    surfaceTypeRR: int
    surfaceTypeFL: int
    surfaceTypeFR: int

    _tableName = 'car_telemetry'

    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['carTelemetryData'])):
            this_participant = packet['carTelemetryData'][i]
            # Build this participant
            this_data = Telemetry(header['sessionUID'],
                                  i, # participant index
                                  header['playerCarIndex'],
                                  header['frameIdentifier'],
                                  header['sessionTime'],
                                  this_participant['speed'],
                                  this_participant['throttle'],
                                  this_participant['steer'],
                                  this_participant['brake'],
                                  this_participant['clutch'],
                                  this_participant['gear'],
                                  this_participant['engineRPM'],
                                  this_participant['drs'],
                                  this_participant['revLightsPercent'],
                                  this_participant['brakesTemperature'][0],
                                  this_participant['brakesTemperature'][1],
                                  this_participant['brakesTemperature'][2],
                                  this_participant['brakesTemperature'][3],
                                  this_participant['tyresSurfaceTemperature'][0],
                                  this_participant['tyresSurfaceTemperature'][1],
                                  this_participant['tyresSurfaceTemperature'][2],
                                  this_participant['tyresSurfaceTemperature'][3],
                                  this_participant['tyresInnerTemperature'][0],
                                  this_participant['tyresInnerTemperature'][1],
                                  this_participant['tyresInnerTemperature'][2],
                                  this_participant['tyresInnerTemperature'][3],
                                  this_participant['engineTemperature'],
                                  this_participant['tyresPressure'][0],
                                  this_participant['tyresPressure'][1],
                                  this_participant['tyresPressure'][2],
                                  this_participant['tyresPressure'][3],
                                  this_participant['surfaceType'][0],
                                  this_participant['surfaceType'][1],
                                  this_participant['surfaceType'][2],
                                  this_participant['surfaceType'][3])

            # Append this participant to a list which will be returned
            data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'player_one_index': self.playerOneIndex,
            'frame_id': self.frameId,
            'session_time': self.sessionTime,
            'speed': self.speed,
            'throttle': self.throttle,
            'steer': self.steer,
            'brake': self.brake,
            'clutch': self.clutch,
            'gear': self.gear,
            'engine_rpm': self.engineRPM,
            'drs': self.drs,
            'rev_lights_percent': self.revLightsPercent,
            'brake_temp_rl': self.brakeTempRL,
            'brake_temp_rr': self.brakeTempRR,
            'brake_temp_fl': self.brakeTempFL,
            'brake_temp_fr': self.brakeTempFR,
            'tyre_surface_temp_rl': self.tyreSurfaceTempRL,
            'tyre_surface_temp_rr': self.tyreSurfaceTempRR,
            'tyre_surface_temp_fl': self.tyreSurfaceTempFL,
            'tyre_surface_temp_fr': self.tyreSurfaceTempFR,
            'tyre_inner_temp_rl': self.tyreInnerTempRL,
            'tyre_inner_temp_rr': self.tyreInnerTempRR,
            'tyre_inner_temp_fl': self.tyreInnerTempFL,
            'tyre_inner_temp_fr': self.tyreInnerTempFR,
            'engine_temp': self.engineTemp,
            'tyre_pressure_rl': self.tyrePressureRL,
            'tyre_pressure_rr': self.tyrePressureRR,
            'tyre_pressure_fl': self.tyrePressureFL,
            'tyre_pressure_fr': self.tyrePressureFR,
            'surface_type_rl': self.surfaceTypeRL,
            'surface_type_rr': self.surfaceTypeRR,
            'surface_type_fl': self.surfaceTypeFL,
            'surface_type_fr': self.surfaceTypeFR
        }

        return data_dict


@dataclass
class SessionParticipant(RaceSimData):
    sessionUID: int
    participantIndex: int
    aiControlled: int
    driverId: int
    networkId: int
    teamId: int
    myTeam: int
    raceNumber: int
    nationality: int # should be string from enum?
    name: str
    yourTelemetry: int # not sure if I need this
    showOnlineNames: int # if 0 this is not the actual name and "player" will be given
    platform: int # should be string from enum?

    _tableName = 'session_participant'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['participants'])):
            this_participant = packet['participants'][i]
            # Build this participant
            this_data = SessionParticipant(header['sessionUID'],
                                           i, # participant index
                                           this_participant['aiControlled'],
                                           this_participant['driverId'],
                                           this_participant['networkId'],
                                           this_participant['teamId'],
                                           this_participant['myTeam'],
                                           this_participant['raceNumber'],
                                           this_participant['nationality'],
                                           this_participant['name'],
                                           this_participant['yourTelemetry'],
                                           this_participant['showOnlineNames'],
                                           this_participant['platform'])

            # Append this participant to a list which will be returned
            data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'ai_controlled': self.aiControlled,
            'driver_id': self.driverId,
            'network_id': self.networkId,
            'team_id': self.teamId,
            'my_team': self.myTeam,
            'race_number': self.raceNumber,
            'nationality': self.nationality,
            'driver_name': str("\'" + self.name + "\'"),
            'your_telemetry': bool(self.yourTelemetry),
            'show_online_names': bool(self.showOnlineNames),
            'platform': self.platform
        }

        return data_dict


@dataclass
class CarStatusData(RaceSimData):
    sessionUID: int
    participantIndex: int
    playerOneIndex: int
    frameId: int
    sessionTime: float
    tractionControl: int
    antiLockBrakes: int
    fuelMix: int
    frontBrakeBias: int
    pitLimiterStatus: int
    fuelInTank: float
    fuelCapacity: float
    fuelRemainingLaps: float
    maxRPM: int
    idleRPM: int
    maxGears: int
    drsAllowed: int
    drsActivationDistance: int
    actualTyreCompound: int
    visualTyreCompound: int
    tyresAgeLaps: int
    vehicleFiaFlags: int
    enginePowerICE: float
    enginePowerMGUK: float
    ersStoreEnergy: float
    ersDeployMode: int
    ersHarvestedThisLapMGUK: float
    ersHarvestedThisLapMGUH: float
    ersDeployedThisLap: float
    networkPaused: int

    _tableName = 'car_status_data'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['carStatusData'])):
            packet_data = packet['carStatusData'][i]
            # Build this participant
            this_data = CarStatusData(header['sessionUID'],
                                i, # participant index
                                header['playerCarIndex'],
                                header['frameIdentifier'],
                                header['sessionTime'],
                                packet_data['tractionControl'],
                                packet_data['antiLockBrakes'],
                                packet_data['fuelMix'],
                                packet_data['frontBrakeBias'],
                                packet_data['pitLimiterStatus'],
                                packet_data['fuelInTank'],
                                packet_data['fuelCapacity'],
                                packet_data['fuelRemainingLaps'],
                                packet_data['maxRPM'],
                                packet_data['idleRPM'],
                                packet_data['maxGears'],
                                packet_data['drsAllowed'],
                                packet_data['drsActivationDistance'],
                                packet_data['actualTyreCompound'],
                                packet_data['visualTyreCompound'],
                                packet_data['tyresAgeLaps'],
                                packet_data['vehicleFiaFlags'],
                                packet_data['enginePowerICE'],
                                packet_data['enginePowerMGUK'],
                                packet_data['ersStoreEnergy'],
                                packet_data['ersDeployMode'],
                                packet_data['ersHarvestedThisLapMGUK'],
                                packet_data['ersHarvestedThisLapMGUH'],
                                packet_data['ersDeployedThisLap'],
                                packet_data['networkPaused'])

            # Append this participant to a list which will be returned
            data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'player_one_index': self.playerOneIndex,
            'frame_id': self.frameId,
            'session_time': self.sessionTime,
            'traction_control': self.tractionControl,
            'anti_lock_brakes': self.antiLockBrakes,
            'fuel_mix': self.fuelMix,
            'front_brake_bias': self.frontBrakeBias,
            'pit_limiter_status': self.pitLimiterStatus,
            'fuel_in_tank': self.fuelInTank,
            'fuel_capacity': self.fuelCapacity,
            'fuel_remaining_laps': self.fuelRemainingLaps,
            'max_rpm': self.maxRPM,
            'idle_rpm': self.idleRPM,
            'max_gears': self.maxGears,
            'drs_allowed': self.drsAllowed,
            'drs_activation_distance': self.drsActivationDistance,
            'actual_tyre_compound': self.actualTyreCompound,
            'visual_tyre_compound': self.visualTyreCompound,
            'tyres_age_laps': self.tyresAgeLaps,
            'vehicle_fia_flags': self.vehicleFiaFlags,
            'engine_power_ice': self.enginePowerICE,
            'engine_power_mguk': self.enginePowerMGUK,
            'ers_store_engergy': self.ersStoreEnergy,
            'ers_deploy_mode': self.ersDeployMode,
            'ers_harvested_this_lap_mguk': self.ersHarvestedThisLapMGUK,
            'ers_harvested_this_lap_mguh': self.ersHarvestedThisLapMGUH,
            'ers_deployed_this_lap': self.ersDeployedThisLap,
            'network_paused': self.networkPaused
        }

        return data_dict

@dataclass
class SessionOutcome(RaceSimData):
    sessionUID: int
    participantIndex: int
    playerOneIndex: int
    position: int
    numLaps: int
    gridPosition: int
    points: int
    numPitStops: int
    resultStatus: int
    bestLapTimeInMS: int
    totalRaceTime: float
    penaltiesTime: int
    numPenalties: int

    _tableName = 'session_outcome'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['classificationData'])):
            packet_data = packet['classificationData'][i]
            # Build this participant
            this_data = SessionOutcome(header['sessionUID'],
                                       i, # participant index
                                       header['playerCarIndex'],
                                       packet_data['position'],
                                       packet_data['numLaps'],
                                       packet_data['gridPosition'],
                                       packet_data['points'],
                                       packet_data['numPitStops'],
                                       packet_data['resultStatus'],
                                       packet_data['bestLapTimeInMS'],
                                       packet_data['totalRaceTime'],
                                       packet_data['penaltiesTime'],
                                       packet_data['numPenalties'])

            # Append this participant to a list which will be returned
            data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'player_one_index': self.playerOneIndex,
            'pos': self.position,
            'num_laps': self.numLaps,
            'grid_position': self.gridPosition,
            'points': self.points,
            'num_pit_stops': self.numPitStops,
            'result_status': self.resultStatus,
            'best_lap_time': self.bestLapTimeInMS,
            'total_race_time': self.totalRaceTime,
            'penalties_time': self.penaltiesTime,
            'num_penalties': self.numPenalties
        }

        return data_dict

@dataclass
class SessionTyreStint(RaceSimData):
    sessionUID: int
    participantIndex: int
    playerOneIndex: int
    tyreStint: int
    numTyreStints: int
    tyreStintActual: int
    tyreStintVisual: int
    tyreStintEndLaps: int

    _tableName = 'session_tyre_stint'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        for i in range(0, len(packet['classificationData'])):
            packet_data = packet['classificationData'][i]
            for j in range(0, int(packet_data['numTyreStints'])):
                this_data = SessionTyreStint(header['sessionUID'],
                                             i, # participant index
                                             header['playerCarIndex'],
                                             j + 1, # stint number
                                             packet_data['numTyreStints'],
                                             packet_data['tyreStintsActual'][j],
                                             packet_data['tyreStintsVisual'][j],
                                             packet_data['tyreStintsEndLaps'][j])

                # Append this participant to a list which will be returned
                data.append(this_data)

        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'participant_index': self.participantIndex,
            'player_one_index': self.playerOneIndex,
            'tyre_stint': self.tyreStint,
            'num_tyre_stints': self.numTyreStints,
            'tyre_stint_actual': self.tyreStintActual,
            'tyre_stint_visual': self.tyreStintVisual,
            'tyre_stint_end_laps': self.tyreStintEndLaps
        }

        return data_dict

@dataclass
class SessionDetails(RaceSimData):
    sessionUID: int
    frameId: int
    sessionTime: float
    weather: int
    trackTemperature: int
    airTemperature: int
    totalLaps: int
    trackLength: int
    sessionType: int
    trackId: int
    formula: int
    sessionTimeLeft: int
    sessionDuration: int
    pitSpeedLimit: int
    gamePaused: int
    safetyCarStatus: int
    networkGame: int
    aiDifficulty: int
    seasonLinkIdentifier: int
    weekendLinkIdentifier: int
    sessionLinkIdentifier: int
    gameMode: int
    ruleSet: int
    timeOfDay: int
    sessionLength: int
    numSafetyCarPeriods: int
    numVirtualSafetyCarPeriods: int
    numRedFlagPeriods: int

    _tableName = 'session_details'

    # Create (a) new data structure(s) for the given packet
    @staticmethod
    def packet_to_data(packet):
        header = packet['header']
        data = list()
        packet_data = packet
        # Build this participant
        this_data = SessionDetails(header['sessionUID'],
                                   header['frameIdentifier'],
                                   header['sessionTime'],
                                   packet_data['weather'],
                                   packet_data['trackTemperature'],
                                   packet_data['airTemperature'],
                                   packet_data['totalLaps'],
                                   packet_data['trackLength'],
                                   packet_data['sessionType'],
                                   packet_data['trackId'],
                                   packet_data['formula'],
                                   packet_data['sessionTimeLeft'],
                                   packet_data['sessionDuration'],
                                   packet_data['pitSpeedLimit'],
                                   packet_data['gamePaused'],
                                   packet_data['safetyCarStatus'],
                                   packet_data['networkGame'],
                                   packet_data['aiDifficulty'],
                                   packet_data['seasonLinkIdentifier'],
                                   packet_data['weekendLinkIdentifier'],
                                   packet_data['sessionLinkIdentifier'],
                                   packet_data['gameMode'],
                                   packet_data['ruleSet'],
                                   packet_data['timeOfDay'],
                                   packet_data['sessionLength'],
                                   packet_data['numSafetyCarPeriods'],
                                   packet_data['numVirtualSafetyCarPeriods'],
                                   packet_data['numRedFlagPeriods'])

        #print(this_data)
        # Append this participant to a list which will be returned
        data.append(this_data)
        return data

    def _data_dictionary(self):
        data_dict = {
            'session_uid': self.sessionUID,
            'frame_id': self.frameId,
            'session_time': self.sessionTime,
            'weather': self.weather,
            'track_temperature': self.trackTemperature,
            'air_temperature': self.airTemperature,
            'total_laps': self.totalLaps,
            'track_length': self.trackLength,
            'session_type': self.sessionType,
            'track_id': self.trackId,
            'formula': self.formula,
            'session_time_left': self.sessionTimeLeft,
            'session_duration': self.sessionDuration,
            'pit_speed_limit': self.pitSpeedLimit,
            'game_paused': self.gamePaused,
            'safety_car_status': self.safetyCarStatus,
            'network_game': self.networkGame,
            'ai_difficulty': self.aiDifficulty,
            'season_link_identifier': self.seasonLinkIdentifier,
            'weekend_link_identifier': self.weekendLinkIdentifier,
            'session_link_identifier': self.sessionLinkIdentifier,
            'game_mode': self.gameMode,
            'rule_set': self.ruleSet,
            'time_of_day': self.timeOfDay,
            'session_length': self.sessionLength,
            'num_safety_car_periods': self.numSafetyCarPeriods,
            'num_virtual_safety_car_periods': self.numVirtualSafetyCarPeriods,
            'num_red_flag_periods': self.numRedFlagPeriods
        }

        return data_dict