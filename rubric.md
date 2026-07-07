# Timing Transparency Rubric

Use this rubric for documentation-level scoring. Keep empirical measurements separate from author claims.

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Clock source documented | No clock source stated | Some clock terms used but incomplete | Explicit source such as GNSS, PTP, PPS, NTP, host clock, simulator clock |
| Synchronization method documented | Not stated | General synchronized/aligned claim | Method stated: hardware trigger, PPS/PTP/NTP, post-hoc alignment, shared clock |
| Timestamp semantics documented | Fields named but not explained | Some sensor/message timestamps explained | Distinguishes sensor/sample/header time from record/log/publish/receive time |
| Latency/offset/jitter quantified | Not stated | Qualitative mention | Quantitative offset, jitter, drift, or synchronization accuracy reported |
| Middleware semantics documented | Middleware named only | Some log/replay info | Explicit bag/log/container timestamp semantics documented |
| Replay semantics documented | Not stated | Playback command only | Explains whether replay uses record time, message time, simulated time, or `/clock` |
| Raw timing metadata preserved | No/unknown | Partially preserved | Raw packet/sample timestamps preserved alongside middleware times |

## Empirical flags

Flag, but do not automatically score as failure:

- Header stamps absent for sensor topics
- Header stamps present but all nanoseconds equal zero
- Middleware record/log time and header stamp diverge significantly
- Non-monotonic header/sample timestamps
- Duplicate timestamps on high-rate streams
- Sensor-local timestamps with no epoch mapping
- LiDAR scan start/end ambiguity
- Camera exposure midpoint/end ambiguity
- Event-camera timestamps converted to frame/batch time only
- PCAP packet timestamp used as sensor acquisition time without packet-level correction
- ROS 2 storage timestamp treated as acquisition time
- MCAP `log_time` treated as sensor time when `publish_time` or embedded sample time exists
- OpenDLV `received` time treated as sample time despite available `sent` or `sample time point`
