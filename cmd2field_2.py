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
      "label": "agc"
      },
  "H": { 
      "label": "sql"
      },
  "I": { 
      "label": "rfgain"
      },
  "J": { 
      "label": "att"
      },
  "K": { 
      "label": "noise"
      },
  "L": {
     "label": "rit_xit"
     },
  "M": { 
      "label": "radio_mode"
      },
  "N": { 
      "label": "split_state"
      },
  "P": { 
      "label": "passband"
      },
  "T": { 
      "label": "xmit"
      },
  "U": { 
      "label": "volume"
      },
  "W": { 
      "label": "rx_filter"
      },
  "S": { 
      "label": "strength"
      },
  "C1A": { 
      "label": "audio_source"
      },
  "C1B": { 
      "label": "keyloop"
      },
  "T": { 
      "label": "eth_settings"
      },
  "C1C": { 
      "label": "cw_time"
      },
  "C1D": { 
      "label": "mic_gain"
      },
  "C1E": { 
      "label": "line_gain"
      },
  "C1F": { 
      "label": "speech_proc"
      },
  "C1G": { 
      "label": "ctcss_tone"
      },
  "C1H": { 
      "label": "rx_eq"
      },
  "C1I": { 
      "label": "tx_eq"
      },
  "C1J": { 
      "label": "xmit_rolloff"
      },
  "C1K": { 
      "label": "t_r_delay"
      },
  "C1L": { 
      "label": "sidetone_freq"
      },
  "C1M": { 
      "label": "cw_delay"
      },
  "C1N": { 
      "label": "xmit_enable"
      },
  "C1O": { 
      "label": "sideband_bw"
      },
  "C1P": { 
      "label": "auto_tuner"
      },
  "C1Q": { 
      "label": "sidetone_vol"
      },
  "C1R": { 
      "label": "spot_vol"
      },
  "C1S": {
     "label": "fsk_mark"
     },
  "C1T": { 
      "label": "if_filter"
      },
  "C1U": { 
      "label": "if_filter_enable"
      },
  "C1V": { 
      "label": "antenna"
      },
  "C1W": { 
      "label": "monitor"
      },
  "C1X": { 
      "label": "power"},
  "C1Y": { 
      "label": "spot"
      },
  "C1Z": { 
      "label": "preamp"
      },
  "C2A": { 
      "label": "tuner"
      },
  "C2B": { 
      "label": "split_state2"
      },
  "C2C": { 
      "label": "vox_trip"
      },
  "C2D": { 
      "label": "anti_vox"
      },
  "C2E": { 
      "label": "vox_hang"
      },
  "C2F": { 
      "label": "cw_keyer_mode"
      },
  "C2G": { 
      "label": "cw_weight"
      },
  "C2H": { 
      "label": "manual_notch"
      },
  "C2I": { 
      "label": "manual_notch_freq"
      },
  "C2J": { 
      "label":  "manual_notch_width"
      },
  "C2K": { 
      "label":  "cw_2_xmit"
      },
  "C2L": { 
      "label": "keyer_speed"
      },
  "C2M": { 
      "label": "vox"
      },
  "C2N": { 
      "label": "display"
      },
  "C2O": { 
      "label": "speaker"
      },
  "C2P": { 
      "label": "trip_gain"
      },
}
