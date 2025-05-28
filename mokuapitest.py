from moku.instruments import FrequencyResponseAnalyzer
import numpy as np
import pandas as pd
import os  # Import os for file checking

# Connect to the Moku device
fra = FrequencyResponseAnalyzer('[fe80::7269:79ff:feb9:332%6]', force_connect=True)

# Measurement setup
fra.fra_measurement(1, mode='InOut', averaging_duration=2e-3,
                    start_frequency=20e3, stop_frequency=400e3,
                    averaging_cycles=1, output_amplitude=10)

# Sweep setup
fra.set_sweep(start_frequency=20e3, stop_frequency=200e3, num_points=2048,
              averaging_time=2e-3, settling_time=2e-3,
              averaging_cycles=1, settling_cycles=1)

# Ensure directory exists
os.makedirs('C:/Xiong/data', exist_ok=True)

try:
    # Get measurement data
    fra.start_sweep()
    data = fra.get_data(wait_complete=True)
    fra.stop_sweep()

    # Reshape for concatenation (ensure 2D)
    magnitude = np.array(data['ch1']['magnitude']).reshape(-1, 1)
    frequency = np.array(data['ch1']['frequency']).reshape(-1, 1)

    # Combine as two columns: [frequency, magnitude]
    g_w = np.concatenate((frequency, magnitude), axis=1)
    df = pd.DataFrame(g_w, columns=['Frequency (Hz)', 'Magnitude (dB)'])

    # Check for existing files and increment the filename
    i = 0
    while os.path.exists(f'C:/Xiong/data/test{i}.csv'):
        i += 1

    # Save to the next available file
    df.to_csv(f'C:/Xiong/data/test{i}.csv', index=False)
    print(f"Data saved to test{i}.csv")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection to the Moku device
    fra.relinquish_ownership()
