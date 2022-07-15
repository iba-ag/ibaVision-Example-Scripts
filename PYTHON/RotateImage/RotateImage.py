import numpy as np

import cv2

IbaVisionInterfaceVersion = "1.0.0"

ProcedureDescriptions = [
    {"Description" : ("Init", "ExecuteInit", "Initialize some values"), 
    "InputsControl" : [
        (0, "Image width", "Image width for output image"), 
        (1, "Image height", "Image height for output image")
    ] },
    {"Description" : ("Main", "ExecuteMain", "Performs some image manipulation according to the input data and returns the resulting image and output data for testing"),
    "InputsControl" : [
        (0, "Input rotation angle", "Rotation angle applied to the image"), 
        (1, "Input scaling factor", "Scale factor (float) for image transformation"),
        (2, "Input Digital signal", "Digital signal for testing booleans"),
        (3, "Input Text signal", "Input Text signal to display and process")
    ],
    "InputsIconic" : [(0, "Input image", "Any input image")],
    "OutputsControl" : [
        (0, "Image brightness int", "The int average brightness of the image"), 
        (1, "Image brightness float", "The float average brightness of the image"), 
        (2, "Text output", "The reversed input string"),
        (3, "Output Digital signal", "Inverted digital signal value from input")
    ], 
    "OutputsIconic" : [(0, "Output image", "The scaled and rotated output image")], }
    ]

# Input and Output values
# =======================
# Inputs and Outputs can be defined both for control and iconic values.
# The Python dictionaries need to be initialized. If the script is also supposed 
# to be executed outside ibaVision, the initial values - that are currently 
# commented out - need to be set.

# Inputs
InputsIconic = {}
# InputsIconic["Main"] = []
# InputsIconic["Main"].append((128, 128, 3, np.ones([128,128,3], dtype='uint8'))) # Add a dummy 128x128 RGB image that allows the script to run standalone.

InputsControl = {}
# InputsControl["Init"] = []
# InputsControl["Init"].append(640)
# InputsControl["Init"].append(480)
# InputsControl["Main"] = []
# InputsControl["Main"].append(0) # Add a dummy control value that allows the script to run standalone.
# InputsControl["Main"].append(0.0) # Add a dummy control value that allows the script to run standalone.
# InputsControl["Main"].append(False) # Add a dummy control value that allows the script to run standalone.
# InputsControl["Main"].append("ABCDEFGH") # Add a dummy control value that allows the script to run standalone.

# Outputs
OutputsIconic = {}
# OutputsIconic["Main"] = []
# OutputsIconic["Main"].append((128, 128, 3, np.ones([128,128,3], dtype='uint8'))) # Add a dummy 128x128 RGB image that allows the script to run standalone.

OutputsControl = {}
# OutputsControl["Main"] = []
# OutputsControl["Main"].append(0) # Add a dummy control value that allows the script to run standalone.
# OutputsControl["Main"].append(0.0) # Add a dummy control value that allows the script to run standalone.
# OutputsControl["Main"].append("HGFEDCBA") # Add a dummy control value that allows the script to run standalone.
# OutputsControl["Main"].append(True) # Add a dummy control value that allows the script to run standalone.

def ExecuteInit():
    global init_width, init_height
    init_width = InputsControl["Init"][0]
    init_height = InputsControl["Init"][1]

def ExecuteMain():
    global init_width, init_height
    # Unpack input image from index 0 of iconic inputs
    # (width, height, numChannels, pixelData)
    # the following lines show how the width and height can be read from the input image
    width = InputsIconic["Main"][0][0]
    height = InputsIconic["Main"][0][1]
    numChannels = InputsIconic["Main"][0][2]
    pixelData = InputsIconic["Main"][0][3]
    
    # Get input parameter from index 0 of control inputs
    rotationAngleInDegrees = InputsControl["Main"][0]
    scaleFactorFloat = float(InputsControl["Main"][1])
    
    # Calculate average brightness of the image
    averageBrightness = np.sum(pixelData) / pixelData.size

    # Rotate and scale input image
    rotM = cv2.getRotationMatrix2D((width / 2, height / 2), rotationAngleInDegrees, scaleFactorFloat)
    outputPixelData = cv2.warpAffine(pixelData, rotM, (init_width, init_height))

    # write input text to image
    inputType = type(InputsControl["Main"][3]).__name__
    inputText = str(InputsControl["Main"][3])
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    textColor = (0, 255, 0)
    cv2.putText(
        outputPixelData, 
        inputType + ' ' + inputText, 
        (20, 60), 
        fontType, 
        2, 
        textColor, 
        2, 
        cv2.LINE_AA)

    # convert color space of outputPixelData for output in display window
    # outputimage_RGB = cv2.cvtColor(outputPixelData, cv2.COLOR_BGR2RGB)
    # open a display window for debugging
    # cv2.imshow('Show image stream for debugging purposes', outputimage_RGB)
    # cv2.waitKey(1)

    # Set rotated output image
    # (width, height, numChannels, pixelData)
    OutputsIconic["Main"][0] = (init_width, init_height, numChannels, outputPixelData)

    # Set control output values
    # Calling 'int', 'float' or 'bool' ensures proper data transfers
    OutputsControl["Main"][0] = int(averageBrightness)
    OutputsControl["Main"][1] = float(averageBrightness)
    OutputsControl["Main"][3] = not bool(InputsControl["Main"][2])
    # avoid issues with empty strings
    if len(str(InputsControl["Main"][3])) == 0:
        InputsControl["Main"][3] = "NO INPUT"
    # input string is reversed for output (Python array manipulation)
    OutputsControl["Main"][2] = str(InputsControl["Main"][3])[::-1]

