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
            'driver_name': self.name,
            'your_telemetry': self.yourTelemetry,
            'show_online_names': self.showOnlineNames,
            'platform': self.platform
        }

        return data_dict
