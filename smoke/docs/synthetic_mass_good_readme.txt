Synthetic MASS harbour perception dataset.

    Sensors: stereo camera, marine radar, AIS receiver, lidar, IMU, and GNSS.
    Clock source: GNSS-disciplined PTP grandmaster with PPS distributed to the
    acquisition computer. The lidar and camera are hardware triggered. IMU data
    uses sensor acquisition timestamps. ROS header.stamp represents acquisition
    time. Bag record time represents logger receipt time and must not be used as
    sensor time. Known synchronization uncertainty is below 2 ms for cameras and
    below 1 ms for IMU. rosbag replay should use /clock only for reproducing the
    original acquisition timeline.
