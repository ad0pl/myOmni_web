cmd2field = {
  "A": {
      "label": "vfoA",
      "unpack": lambda x: struct.unpack("!L", x)[0],
      "len": 4
      },
  "B": { 
      "label": "vfoB",
      "unpack": lambda x: struct.unpack("!L", x)[0],
      "len": 4
      },
  "G": { 
      "label": "agc",
      "unpack": lambda x: AGCMode(x[0]-ord('0')),
      "len": 1
      },
  "H": { 
      "label": "sql",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "I": { 
      "label": "rfgain",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "J": { 
      "label": "att",
      "unpack": lambda x: (x[0]-ord('0'))*6,
      "len": 1
      },
  "K": { 
      "label": "noise",
      "unpack": unpack_noise,
      "len": 3
      },
  "L": {
     "label": "rit_xit",
      "unpack": self.unpack_ritxit,
      "len": 3
     },
  "M": { 
      "label": "radio_mode",
      "unpack": self.unpackMode,
      "len": 3
      },
  "N": { 
      "label": "split_state",
      "unpack": lambda x: "Off" if x[0] == 0 else "On",
      "len": 1
      },
  "P": { 
      "label": "passband",
      "unpack": lambda x: struct.unpack("!H", x)[0],
      "len": 2
      },
  "U": { 
      "label": "volume",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "W": { 
      "label": "rx_filter",
      "unpack": self.unpack_filter,
      "len": 1
      },
  "S": { 
      "label": "strength",
      "unpack": self.unpack_signal,
      "len": 4
      },
  "C1A": { 
      "label": "audio_source",
      "unpack": self.unpack_au_source,
      "len": 1
      },
  "C1B": { 
      "label": "keyloop",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "T": { 
      "label": "eth_settings",
      "unpack": self.unpack_eth,
      "len": 3
      },
  "C1C": { 
      "label": "cw_time",
      "unpack": lambda x: x[0] + 3,
      "len": 1
      },
  "C1D": { 
      "label": "mic_gain",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1E": { 
      "label": "line_gain",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1F": { 
      "label": "speech_proc",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1G": { 
      "label": "ctcss_tone" # Who's going to use this rig for FM?
      },
  "C1H": { 
      "label": "rx_eq",
      "unpack": lambda x: int( (x[0]-1)/3.097560975 ) - 20,
      "len": 1
      },
  "C1I": { 
      "label": "tx_eq",
      "unpack": lambda x: int( (x[0]-1)/3.097560975 ) - 20,
      "len": 1
      },
  "C1J": { 
      "label": "xmit_rolloff",
      "unpack": lambda x: (x[0] * 10) + 70,
      "len": 1
      },
  "C1K": { 
      "label": "t_r_delay",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1L": { 
      "label": "sidetone_freq",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1M": { 
      "label": "cw_delay",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1N": { 
      "label": "xmit_enable",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C1O": { 
      "label": "sideband_bw",
      "unpack": lambda x: 2500 if x[0] == 8 else 4000-(x[0] * 200) if x[0] < 8 else 4000-((x[0]-1)*200),
      "len": 1
      },
  "C1P": { 
      "label": "auto_tuner",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C1Q": { 
      "label": "sidetone_vol",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1R": { 
      "label": "spot_vol",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1S": {
     "label": "fsk_mark",
      "unpack": lambda x: x[0],
      "len": 1
     },
  "C1T": { 
      "label": "if_filter",
      "unpack": self.unpack_if,
      "len": 1
      },
  "C1U": { 
      "label": "if_filter_enable",
      "unpack": self.unpack_if_filter_enable,
      "len": 1
      },
  "C1V": { 
      "label": "antenna",
      "unpack": lambda x: x[0],
      "len": 1
      },
  "C1W": { 
      "label": "monitor",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C1X": { 
      "label": "power",
      "unpack": lambda x: int( ((x[0]/127.0)*100)+0.5 ), # we can get the fwd/rev power from ?S, ignore it from here
      "len": 3
      },
  "C1Y": { 
      "label": "spot",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C1Z": { 
      "label": "preamp",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2A": { 
      "label": "tuner",
      "unpack": self.unpack_tune_state,
      "len": 1
      },
  "C2B": { 
      "label": "split_state2",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2C": { 
      "label": "vox_trip",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C2D": { 
      "label": "anti_vox",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C2E": { 
      "label": "vox_hang",
      "unpack": lambda x: (x[0]/127.0),
      "len": 1
      },
  "C2F": { 
      "label": "cw_keyer_mode",
      "unpack": self.unpack_keyer,
      "len": 1
      },
  "C2G": { 
      "label": "cw_weight",
      "unpack": lambda x: (x[0]/127.0)/2.0,
      "len": 1
      },
  "C2H": { 
      "label": "manual_notch",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2I": { 
      "label": "manual_notch_freq",
      "unpack": lambda x: (40*x)+20,
      "len": 1
      },
  "C2J": { 
      "label":  "manual_notch_width",
      "unpack": lambda x: x*( (315-10) / (127-1) ),
      "len": 1
      },
  "C2K": { 
      "label":  "cw_2_xmit",
      "unpack": lambda x: x[0],
      "len": 1
      },
  "C2L": { 
      "label": "keyer_speed",
      "unpack": lambda x:  int( (x * 63/127)+0.5),
      "len": 1
      },
  "C2M": { 
      "label": "vox",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2N": { 
      "label": "display",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2O": { 
      "label": "speaker",
      "unpack": lambda x: False if x[0] == 0 else True,
      "len": 1
      },
  "C2P": { 
      "label": "trip_gain" # Doesn't seem to be supported by the Omni-Vii
      },
}
