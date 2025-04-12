import pyshark
import re
import math

# Open the capture file
capture = pyshark.FileCapture('test.pcap')
packet1 = capture[34]


def compute_magnitudes(i_samples, q_samples):
    """
    Compute magnitudes from iSample and qSample arrays and return a list of objects.
    
    Args:
        i_samples (list): List of iSample float values.
        q_samples (list): List of qSample float values.
    
    Returns:
        list: List of dictionaries, each with iSample, qSample, and magnitude.
              Example: {"iSample": -0.10546875, "qSample": 0.0703125, "magnitude": ...}
    """
    # Validate inputs
    if len(i_samples) != len(q_samples):
        print(f"Error: i_samples ({len(i_samples)}) and q_samples ({len(q_samples)}) have different lengths")
        return []
    
    if not i_samples:
        print("Error: Empty input arrays")
        return []
    
    # Compute magnitudes and build objects
    result = [
        {
            "iSample": i,
            "qSample": q,
            "magnitude": math.sqrt(i * i + q * q)
        }
        for i, q in zip(i_samples, q_samples)
    ]
    
    return result

# we have to do some crazy regex solution because the data is not formatted in a convenient way. 
def extract_qsamples(packet_string):
    """
    Extract all qSample float values from the packet string into a list.
    
    Args:
        packet_string (str): String representation of the packet layer (e.g., str(oran_layer)).
    
    Returns:
        list: List of float values for all qSamples, in order.
    """
    # Remove ANSI escape codes
    ansi_pattern = r'\033\[[0-9;]*m'
    clean_string = re.sub(ansi_pattern, '', packet_string)
    
    # Extract qSample values
    pattern = r'qSample:\s+([-]?\d*\.\d+)\s+0x[0-9a-fA-F]+\s+\(qSample-\d+\s+in\s+the\s+PRB\)'
    matches = re.findall(pattern, clean_string, re.MULTILINE)
    
    # Convert to floats
    samples = [float(value) for value in matches]
    return samples


def extract_isamples(packet_string):
    """
    Extract all iSample float values from the packet string into a list.
    
    Args:
        packet_string (str): String representation of the packet layer (e.g., str(oran_layer)).
    
    Returns:
        list: List of float values for all iSamples, in order.
    """
    # Step 1: Remove ANSI escape codes
    ansi_pattern = r'\033\[[0-9;]*m'
    clean_string = re.sub(ansi_pattern, '', packet_string)
    
    # Print cleaned string snippet for debugging
    print("Cleaned string snippet (first 500 chars):")
    print(clean_string[:500])
    print("---")
    
    # Step 2: Extract iSample values
    # Match lines like: iSample: -0.007812500000  0x01fe (iSample-0 in the PRB)
    pattern = r'iSample:\s+([-]?\d*\.\d+)\s+0x[0-9a-fA-F]+\s+\(iSample-\d+\s+in\s+the\s+PRB\)'
    
    # Find all matches
    matches = re.findall(pattern, clean_string, re.MULTILINE)
    print("Regex matches:", matches)
    
    # Convert matches to floats
    if matches:
        samples = [float(value) for value in matches]
        print("Extracted samples:", samples)
    else:
        samples = []
        print("No iSample lines matched")
    
    return samples

def group_samples(samples, samples_per_prb=12):
    """
    Group a flat list of samples into lists of samples_per_prb.
    
    Args:
        samples (list): Flat list of iSample values.
        samples_per_prb (int): Number of samples per PRB (default 12).
    
    Returns:
        list: List of lists, each containing samples_per_prb values.
    """
    if not samples:
        print("Error: No samples to group")
        return []
    
    # Validate that the number of samples is divisible by samples_per_prb
    if len(samples) % samples_per_prb != 0:
        print(f"Warning: {len(samples)} samples not divisible by {samples_per_prb}")
        return []
    
    # Split into groups of samples_per_prb
    grouped = [samples[i:i + samples_per_prb] for i in range(0, len(samples), samples_per_prb)]
    print(f"Grouped {len(samples)} samples into {len(grouped)} PRBs")
    
    return grouped


def analyze_packet(packet):
    try:
        scs = 0.03
        
        final_report = {
            "prb": {}
        }

        if hasattr(packet, 'oran_fh_cus'):
            print("Found O-RAN Fronthaul C/U-plane data:")
            oran = packet.oran_fh_cus
            
            # Print basic fields
            try:
                final_report['du_port_id'] = oran.du_port_id 
                print(f"DU Port ID: {oran.du_port_id}")
            except AttributeError:
                print("DU Port ID: Not available")
            try:
                final_report['ru_port_id'] = oran.ru_port_id
                print(f"RU Port ID: {oran.ru_port_id}")
            except AttributeError:
                print("RU Port ID: Not available")
            try:
                final_report['frame_id'] = oran.frameId
                print(f"Frame ID: {oran.frameId}")
            except AttributeError:
                print("Frame ID: Not available")
            try:
                final_report['subframe_id'] = oran.subframe_id
                print(f"Subframe ID: {oran.subframe_id}")
            except AttributeError:
                print("Subframe ID: Not available")
            try:
                final_report['slot_id'] = oran.slotId
                print(f"Slot ID: {oran.slotId}")
            except AttributeError:
                print("Slot ID: Not available")
            try:
                final_report['symbol_id'] = oran.symbolId
                print(f"Symbol ID: {oran.symbolId}")
            except AttributeError:
                print("Symbol ID: Not available")


            # Data direction
            try:
                final_report['data_direction'] = oran.data_direction
                data_direction = int(oran.data_direction)
                if data_direction == 0:
                    print("Data Direction: Uplink")
                elif data_direction == 1:
                    print("Data Direction: Downlink")
                else:
                    print(f"Unexpected data_direction value: {data_direction}")
            except (AttributeError, ValueError):
                print("Data Direction: Not available or invalid")

            # Packet type
            if hasattr(oran, 'iq_user_data') or hasattr(oran, 'iSample') or hasattr(oran, 'qSample'):
                print("Packet Type: U-plane (contains IQ data)")
            else:
                print("Packet Type: Likely C-plane (no IQ data present)")

            # PRB count from dissector
            
            prb_count_matches = re.findall(r'PRB (\d+) \(12 samples\)', str(oran))
            if prb_count_matches:
                max_prb = max(int(prb) for prb in prb_count_matches)
                num_prbs = max_prb + 1
                print(f"Number of PRBs from dissector: {num_prbs}")
                print(f"Bandwidth frequency: {num_prbs * 12 * scs} MHz")
                final_report['prob_count'] = 273
                if num_prbs != 273:
                    print(f"Warning: Dissector reports {num_prbs} PRBs, expected 273")
            else:
                print("No PRBs found in dissector output.")

            # finally look at the pbr data and do magnitude calculations.
            i_samples = extract_isamples(str(oran))
            q_samples = extract_qsamples(str(oran))

            #splits up data into lists of 12 samples. This way we can select by pbr index
            better_ilist = group_samples(i_samples)
            better_qlist = group_samples(q_samples)


            #for every prb 0 272 index we need to calculate the magnitudes for their 12
            for i in range(273):
                final_report['prb'][i] = compute_magnitudes(better_ilist[i], better_qlist[i])
            
            print(final_report)
            return final_report 
        
        else:
            print("No ORAN_FH_CUS layer found in packet.")
    
    except Exception as e:
        print(f"Unexpected error analyzing packet: {e}")

# Analyze the packet
analyze_packet(packet1)


capture.close()


