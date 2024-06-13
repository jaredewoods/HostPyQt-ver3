# command_dictionary.py

commands = {
    "MHOM": {
        "description": "Move to HOME Position.",
        "parameters": {
            "m_mode": {"description": "Motion mode ('F' for all axes, 'A' for Expansion axis only)"}
        }
    },
    "MTRS": {
        "description": "Move to Ready Position.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "next_mtn": {"description": "Next motion mode ('GA', 'PA', 'GB', 'PB' for Manipulator, 'AL' for Pre-aligner)"}
        }
    },
    "MGET": {
        "description": "Workpiece Get motion.",
        "parameters": {}
    },
    "MPUT": {
        "description": "Workpiece Put motion.",
        "parameters": {}
    },
    "MGT2": {
        "description": "Workpiece Get motion (MTRS + MGET).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MPT2": {
        "description": "Workpiece Put motion (MTRS + MPUT).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MSP2": {
        "description": "Workpiece Swap motion (MGT2 + MPT2).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"}
        }
    },
    "MPNT": {
        "description": "Motion between Transfer Points.",
        "parameters": {
            "trs_pnt": {"description": "Transfer point (e.g., 'G1', 'G2', 'Gb', 'G3', 'G4', 'G5', 'P1', 'P2', 'Pb', 'P3', 'P4')"}
        }
    },
    "MMAP": {
        "description": "Mapping.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"}
        }
    },
    "MALN": {
        "description": "Alignment.",
        "parameters": {
            "t_uno": {"description": "Unit number to be compensated ('1' for Manipulator)"},
            "angle": {"description": "Positioning angle ('000000' to '035999' with 0.01 [deg] resolution)"}
        }
    },
    "MTCH": {
        "description": "Move to Registered Position.",
        "parameters": {
            "end_effector": {"description": "End-Effector specified ('A' or 'B')"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8', 'UA' to 'UL', 'M1' to 'M8')"},
            "p_mode": {"description": "Position mode ('S' for registered position, 'R' for ready position)"},
            "z_offset": {"description": "Offset in the lifting direction ('-99999' to '999999' with 0.01 [mm] resolution)"},
            "r_offset": {"description": "Offset in the expanding direction ('-99999' to '999999' with 0.01 [mm] resolution)"}
        }
    },
    "MABS": {
        "description": "Move to Specified Coordinate Position.",
        "parameters": {
            "axis": {"description": "Axis ('S', 'E', 'A', 'B', 'Z', 'T' for Manipulator, 'X', 'Y' for Pre-aligner)"},
            "value": {"description": "Coordinate specified ('-99999' to '999999' with 0.01 [mm] or [deg] resolution)"}
        }
    },
    "MRLK": {
        "description": "Move to Specified Relative Position (LNK).",
        "parameters": {
            "axis": {"description": "Axis ('S', 'E', 'A', 'B', 'Z', 'T' for Manipulator, 'S', 'X', 'Y' for Pre-aligner)"},
            "value": {"description": "Coordinate specified ('-99999' to '999999' with 0.01 [mm] or [deg] resolution, angle range '-35999' to '035999')"}
        }
    },
    "MRLN": {
        "description": "Move to Specified Relative Position (LNR).",
        "parameters": {
            "axis": {"description": "Axis ('X1', 'X2', 'Y1', 'Y2' for Manipulator)"},
            "value": {"description": "Coordinate specified ('-99999' to '999999' with 0.01 [mm] or [deg] resolution, angle range '-35999' to '035999')"}
        }
    },
    "MACA": {
        "description": "Alignment Calibration.",
        "parameters": {
            "t_uno": {"description": "Unit number to be compensated ('1' for Manipulator)"}
        }
    },
    "MMCA": {
        "description": "Mapping Calibration.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"}
        }
    },
    "MGTW": {
        "description": "Workpiece Get Motion (with YASKAWA standard interlock).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MPTW": {
        "description": "Workpiece Put Motion (with YASKAWA standard interlock).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MGWI": {
        "description": "Workpiece Get Motion (with Customized handshake).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MPWI": {
        "description": "Workpiece Put Motion (with Customized handshake).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok": {"description": "End-Effector specified ('A' for End-Effector 1, 'B' for End-Effector 2)"}
        }
    },
    "MSWP": {
        "description": "Workpiece Swap Motion (with YASKAWA standard interlock).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"}
        }
    },
    "MSWI": {
        "description": "Workpiece Swap Motion (with Customized handshake).",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no": {"description": "Slot number ('01' to 'XX' for cassette stage, '00' for transfer stage)"}
        }
    },
    "MXTW": {
        "description": "Wafer Exchange Motion (with YASKAWA standard interlock).",
        "parameters": {
            "first_mtn": {"description": "First motion type ('G' for Get, 'P' for Put)"},
            "trs_st1": {"description": "Transfer station 1 ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no1": {"description": "Slot number 1 ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "end_effector1": {"description": "End-Effector 1 specified ('A' or 'B')"},
            "trs_st2": {"description": "Transfer station 2 ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no2": {"description": "Slot number 2 ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "end_effector2": {"description": "End-Effector 2 specified ('A' or 'B')"}
        }
    },
    "MXWI": {
        "description": "Wafer Exchange Motion (with Customized handshake).",
        "parameters": {
            "first_mtn": {"description": "First motion type ('G' for Get, 'P' for Put)"},
            "trs_st1": {"description": "Transfer station 1 ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no1": {"description": "Slot number 1 ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok1": {"description": "End-Effector 1 specified ('A' or 'B')"},
            "trs_st2": {"description": "Transfer station 2 ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "slot_no2": {"description": "Slot number 2 ('01' to 'XX' for cassette stage, '00' for transfer stage)"},
            "frok2": {"description": "End-Effector 2 specified ('A' or 'B')"}
        }
    },
    "MCDT": {
        "description": "Manipulator collision detection threshold setting command.",
        "parameters": {
            "trs_st1": {"description": "Transfer station 1 (Left station, 'P1' to 'P8')"},
            "slot_no1": {"description": "Slot number 1 ('01' to 'XX')"},
            "trs_st2": {"description": "Transfer station 2 (Right station, 'P1' to 'P8')"},
            "slot_no2": {"description": "Slot number 2 ('01' to 'XX')"}
        }
    },
    "ISYS": {
        "description": "System Initialization.",
        "parameters": {}
    },
    "MWRM": {
        "description": "Warm Up operation.",
        "parameters": {
            "time": {"description": "Warm Up time ('0001' to '9999' in seconds)"}
        }
    },
    "CHLT": {
        "description": "Motion Interruption (Deceleration to a Stop).",
        "parameters": {}
    },
    "CRSM": {
        "description": "Restart from Interruption.",
        "parameters": {}
    },
    "CEMG": {
        "description": "Deceleration to a stop and servo OFF.",
        "parameters": {}
    },
    "CSRV": {
        "description": "Servo Command.",
        "parameters": {
            "sw": {"description": "Servo command ('0' for OFF, '1' for ON)"}
        }
    },
    "CCLR": {
        "description": "Error Release (Clear).",
        "parameters": {
            "c_mode": {"description": "Clear mode ('E' for error status, 'H' for error history)"}
        }
    },
    "CSOL": {
        "description": "Solenoid Control Command for Workpiece Chucking.",
        "parameters": {
            "end_effector": {"description": "End-Effector specified ('A' for End-Effector 1/Pre-aligner, 'B' for End-Effector 2)"},
            "sw": {"description": "Chucking command ('0' for OFF, '1' for ON)"}
        }
    },
    "CCHK": {
        "description": "Chucking Control Command.",
        "parameters": {
            "end_effector": {"description": "End-Effector specified ('A' for End-Effector 1/Pre-aligner, 'B' for End-Effector 2)"},
            "sw": {"description": "Chucking command ('0' for Release, '1' for Chuck)"}
        }
    },
    "CLFT": {
        "description": "Lifter control command.",
        "parameters": {
            "sw": {"description": "Lifter Control ('U' for Up, 'D' for Down)"}
        }
    },
    "SSPP": {
        "description": "Motion Speed Setting (in [%]).",
        "parameters": {
            "axis": {"description": "Axis ('S', 'E', 'A', 'B', 'Z', 'T', 'R', 'W' for Manipulator, 'S', 'X', 'Y' for Pre-aligner)"},
            "s_mode": {"description": "Speed mode ('H' for first transfer speed, 'M' for second transfer speed, 'L' for low speed)"},
            "value": {"description": "Speed specified ('0000' to '1000' with 0.1 [%] resolution)"}
        }
    },
    "SPOS": {
        "description": "Registration of Current Position.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8', 'UA' to 'UL', 'M1' to 'M8')"},
            "end_effector": {"description": "End-Effector specified ('A' or 'B')"},
            "step": {"description": "Step specified ('STA', 'RDY', 'IM3', 'IM2', 'IM1', 'MIN')"},
            "another_end_effector": {"description": "Another End-Effector registration ('A' for update, 'N' for no update)"},
            "mapp_pos": {"description": "Mapping position registration ('Y' for update, 'N' for no update)"}
        }
    },
    "SABS": {
        "description": "Registration of Coordinate Position.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8', 'UA' to 'UL', 'M1' to 'M8')"},
            "end_effector": {"description": "End-Effector specified ('A' or 'B')"},
            "step": {"description": "Step specified ('STA', 'RDY', 'IM3', 'IM2', 'IM1', 'MIN')"},
            "value1": {"description": "Coordinate for Rotary Axis (6 bytes, '-99999' to '999999' with 0.01 [mm], [deg] resolution)"},
            "value2": {"description": "Coordinate for Expansion Axis (6 bytes, '-99999' to '999999' with 0.01 [mm], [deg] resolution)"},
            "value3": {"description": "Coordinate for End-Effector 1 (6 bytes, '-99999' to '999999' with 0.01 [mm], [deg] resolution)"},
            "value4": {"description": "Coordinate for End-Effector 2 (6 bytes, '-99999' to '999999' with 0.01 [mm], [deg] resolution)"},
            "value5": {"description": "Coordinate for Lifting Axis (6 bytes, '-99999' to '999999' with 0.01 [mm], [deg] resolution)"},
            "another_end_effector": {"description": "Another End-Effector registration ('A' for update, 'N' for no update)"},
            "mapp_pos": {"description": "Mapping position registration ('Y' for update, 'N' for no update)"}
        }
    },
    "SPSV": {
        "description": "Position Data Save.",
        "parameters": {}
    },
    "SOFS": {
        "description": "Transfer Offset Setting.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"},
            "offset1": {"description": "Downward offset ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset2": {"description": "Upward offset ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset3": {"description": "Extending direction offset ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset4": {"description": "Contracting direction offset ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset5": {"description": "Downward offset for PUT ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset6": {"description": "Contracting direction offset for GET ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset7": {"description": "Extending direction offset for GET ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset8": {"description": "Upward offset for GET ('0000' to '9999' with 0.01 [mm] resolution)"},
            "offset9": {"description": "Offset for PUT ('0000' to '9999' with 0.01 [mm] resolution)"}
        }
    },
    "SPIT": {
        "description": "Setting of Pitch Distance between Slots.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"},
            "value": {"description": "Pitch distance between slots ('000000' to '999999' with 0.0001 [mm] resolution)"}
        }
    },
    "SSLT": {
        "description": "Setting of Number of Slots.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"},
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"},
            "slot_no": {"description": "Number of slots ('01' to '30')"}
        }
    },
    "SRSV": {
        "description": "Parameter Save.",
        "parameters": {}
    },
    "SMSK": {
        "description": "Setting of Interlock Monitoring Enabled/Disabled.",
        "parameters": {
            "valid1": {"description": "Interlock information (4 bytes, see document for details)"},
            "valid2": {"description": "Interlock information (4 bytes, see document for details)"},
            "valid3": {"description": "Interlock information (4 bytes, see document for details)"},
            "valid4": {"description": "Interlock information (4 bytes, see document for details)"}
        }
    },
    "SPRM": {
        "description": "Setting the parameters.",
        "parameters": {
            "type": {"description": "Parameter type ('I' for integer, 'R' for real-number)"},
            "sign": {"description": "'U' for user parameter"},
            "num": {"description": "Parameter number (Refer to Parameter Lists for Wafer Transfer Manipulator)"},
            "value": {"description": "Parameter value (10 bytes, '-000032768' to '0000032767' for integer, '-999999999' to '9999999999' for real-number)"}
        }
    },
    "SALM": {
        "description": "Setting alignment mode.",
        "parameters": {
            "mem": {"description": "Memory used ('V' for volatile, 'N' for non-volatile)"},
            "p_mode": {"description": "Positioning mode ('F' for Non-shortcut positioning)"},
            "al_mode": {"description": "Alignment Mode ('A' for Accuracy, 'M' for Medium, 'S' for Throughput)"}
        }
    },
    "SSTD": {
        "description": "Setting standard position.",
        "parameters": {
            "value1": {"description": "Position data for S axis (11 bytes)"},
            "value2": {"description": "Position data for R/X axis (11 bytes)"},
            "value3": {"description": "Position data for End-Effector 1/Y axis (11 bytes)"},
            "value4": {"description": "Position data for End-Effector 2 (11 bytes, Manipulator only)"},
            "value5": {"description": "Position data for Z axis (11 bytes, Manipulator only)"}
        }
    },
    "SWSZ": {
        "description": "Setting wafer size.",
        "parameters": {
            "end_effector": {
                "description": "End-Effector specified ('A' for End-Effector 1/Pre-aligner, 'B' for End-Effector 2)"},
            "size": {"description": "Diameter of the wafer ('300', '200', or '150')"}
        }
    },
    "RSPP": {
        "description": "Motion Speed Reference (in [%]).",
        "parameters": {
            "axis": {
                "description": "Axis ('S', 'E', 'A', 'B', 'Z', 'T', 'R', 'W' for Manipulator, 'S', 'X', 'Y' for Pre-aligner)"},
            "s_mode": {
                "description": "Speed mode ('H' for first transfer speed, 'M' for second transfer speed, 'L' for low speed)"}
        }
    },
    "RPOS": {
        "description": "Current Position Reference/Registered Position Reference.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8', 'UA' to 'UL', 'FF' for current position)"},
            "step": {
                "description": "Step specified ('STA', 'RDY', 'IM3', 'IM2', 'IM1', 'MIN', 'FFF' for current position)"},
            "end_effector": {"description": "End-Effector specified ('A' or 'B', fixed to 'A' for current position)"}
        }
    },
    "ROFS": {
        "description": "Transfer Offset Reference.",
        "parameters": {
            "trs_st": {
                "description": "Transfer station ('P1' to 'P8' for cassette stage, 'UA' to 'UL' for transfer stage)"}
        }
    },
    "RCST": {
        "description": "Reference to Information on Cassette Stage.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"}
        }
    },
    "RMAP": {
        "description": "Mapping Result Reference.",
        "parameters": {
            "trs_st": {"description": "Transfer station ('P1' to 'P8' for cassette stage)"},
            "slot_no": {"description": "Slot number ('FF' for all slots, '01' to 'XX' for specific slot)"}
        }
    },
    "RSTS": {
        "description": "Reference to Various Statuses.",
        "parameters": {}
    },
    "RERR": {
        "description": "Error History Reference.",
        "parameters": {
            "blk_no": {"description": "Block Number (0 to 3 for 32 error codes in alarm history)"}
        }
    },
    "RMSK": {
        "description": "Reference to Information on Interlock Monitoring.",
        "parameters": {}
    },
    "RVER": {
        "description": "Software Version Reference.",
        "parameters": {}
    },
    "RCFG": {
        "description": "Reference to configuration information.",
        "parameters": {}
    },
    "RSTT": {
        "description": "Reference to status information.",
        "parameters": {}
    },
    "RPRM": {
        "description": "Reference to the parameters.",
        "parameters": {
            "type": {"description": "Parameter type ('I' for integer, 'R' for real-number)"},
            "sign": {"description": "'U' for user parameter, 'S' for system parameter"},
            "num": {"description": "Parameter number (Refer to Parameter Lists for Wafer Transfer Manipulator)"}
        }
    },
    "RCCD": {
        "description": "Reference to the CCD Sensor Data.",
        "parameters": {}
    },
    "RALM": {
        "description": "Reference alignment mode.",
        "parameters": {
            "mem": {"description": "Memory ('V' for volatile, 'N' for non-volatile)"}
        }
    },
    "RSTD": {
        "description": "Reference standard position.",
        "parameters": {}
    },
    "RWSZ": {
        "description": "Reference wafer size.",
        "parameters": {
            "end_effector": {
                "description": "End-Effector specified ('A' for End-Effector 1/Pre-aligner, 'B' for End-Effector 2)"}
        }
    },
    "RIOS": {
        "description": "Reference I/O status.",
        "parameters": {
            "io_selection": {"description": "Input/Output port selected ('1' for Input, '2' for Output)"}
        }
    },
    "ACKN": {
        "description": "Acknowledgement of Execution Completion.",
        "parameters": {}
    },
    "UPOS": {
        "description": "Registered Position Data Uploading.",
        "parameters": {}
    },
    "UPRM": {
        "description": "Internal Parameter Uploading.",
        "parameters": {}
    },
    "DPOS": {
        "description": "Registered Position Data Downloading.",
        "parameters": {
            "blk_no": {"description": "Block number ('00' to '99', '-1' for final data)"},
            "data1": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data2": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data3": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data4": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data5": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data6": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data7": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data8": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data9": {"description": "Registered position data (see 'UPOS' response data format)"},
            "data10": {"description": "Registered position data (see 'UPOS' response data format)"}
        }
    },
    "DPRM": {
        "description": "Internal Parameter Downloading.",
        "parameters": {
            "blk_no": {"description": "Block number ('00' to '99', '-1' for final data)"},
            "data1": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data2": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data3": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data4": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data5": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data6": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data7": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data8": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data9": {"description": "Internal parameter data (see 'UPRM' response data format)"},
            "data10": {"description": "Internal parameter data (see 'UPRM' response data format)"}
        }
    },
    "HRST": {
        "description": "Software Reset Command.",
        "parameters": {}
    },
    "MACR": {
        "description": "User macro communication command.",
        "parameters": {
            "com_data": {"description": "Communication data (1 to 55 bytes, user-defined)"}
        }
    }
}
