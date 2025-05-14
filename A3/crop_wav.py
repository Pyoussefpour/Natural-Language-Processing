import os
import wave

def crop_wave_file(directory, speaker, number, output_file, start_timestamp, end_timestamp):
    # Construct the input file path
    input_file = os.path.join(directory, f'S-{speaker}/{number}.wav')

    # Open the input wave file
    with wave.open(input_file, 'rb') as input_wave:
        # Get parameters of the input wave file
        params = input_wave.getparams()

        # Calculate frame positions for start and end timestamps
        sample_width = params.sampwidth
        frame_rate = params.framerate
        num_frames = input_wave.getnframes()

        start_frame = int(start_timestamp * frame_rate)
        end_frame = int(end_timestamp * frame_rate)

        # Ensure start frame is within the range of frames
        start_frame = max(0, min(start_frame, num_frames))

        # Ensure end frame is within the range of frames
        end_frame = max(0, min(end_frame, num_frames))

        # Calculate number of frames to keep
        num_frames_to_keep = end_frame - start_frame

        # Set parameters for the output wave file
        output_params = (params.nchannels, sample_width, frame_rate, num_frames_to_keep, params.comptype, params.compname)

        # Open the output wave file
        with wave.open(output_file, 'wb') as output_wave:
            output_wave.setparams(output_params)

            # Set the position to the start frame
            input_wave.setpos(start_frame)

            # Read frames and write to the output file
            remaining_frames = num_frames_to_keep
            while remaining_frames > 0:
                frames_to_read = min(remaining_frames, 1024)
                frames = input_wave.readframes(frames_to_read)
                output_wave.writeframes(frames)
                remaining_frames -= frames_to_read

# Example usage:
directory = '/u/cs401/A3/data'
output_file = 'output.wav'

speaker = '24D'
number = '0'
start_timestamp = 76.500
end_timestamp = 76.9

# speaker = '24D'
# number = '4'
# start_timestamp = 181.889
# end_timestamp = 182.27

# speaker = '16D'
# number = '0'
# start_timestamp = 47.285
# end_timestamp = 48.25

# speaker = '22B'
# number = '4'
# start_timestamp = 42.588
# end_timestamp = 43.08

# speaker = '5A'
# number = '3'
# start_timestamp = 110.223
# end_timestamp = 110.88



crop_wave_file(directory, speaker, number, output_file, start_timestamp, end_timestamp)
