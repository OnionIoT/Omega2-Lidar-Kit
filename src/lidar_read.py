# The MIT License (MIT)
#
# Copyright (c) 2019 Onion Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import serial

def checksum (frame):
    cs = int.from_bytes(frame[-2:], byteorder='big', signed=False)
    result = 0

    for i in frame[0:-2]:
        result += int(i)

    return result == cs

def parseData (payload, payloadLen):

    speed = payload[0]
    speed = speed * 0.05 #r/s
    # print ('RPM: %.2fr/s or %drpm'%(speed, speed*60))

    angOffset = int.from_bytes(payload[1:3], byteorder='big', signed=True)
    angOffset = angOffset * 0.01
    # print ('Angle Offset: %.2f'%angOffset)

    angStart = int.from_bytes(payload[3:5], byteorder='big', signed=False)
    angStart = angStart * 0.01
    # print ('Starting Angle: %.2f'%angStart)

    nSamples = int((payloadLen - 5) / 3)
    # print("N Samples: %d"%nSamples)

    for i in range(nSamples):
        index = 5 + i*3
        sampleID = payload[index]
        distance = int.from_bytes(payload[index+1:index+3], byteorder='big', signed=False)
        ang = angStart + 22.5*i/nSamples
        print ('%.2f: %.2f mm'%(ang, distance))
        pass

def parseError (payload):
    speed = payload[0]
    speed = speed * 0.05 #r/s
    print ('Error: Low RPM - %.2fr/s or %drpm'%(speed, speed*60))

def processFrame(frame):
    if len(frame) < 3: return False
    frameLen = int.from_bytes(frame[1:3], byteorder='big', signed=False)
    if len(frame) < frameLen + 2: return False #include 2bytes checksum

    if not checksum(frame): return True #checksum failed

    try:
        protocalVer = frame[3] # 0x00
        frameType = frame[4] # 0x61
        payloadType = frame[5] # 0xAE or 0XAD
        payloadLen = int.from_bytes(frame[6:8], byteorder='big', signed=False)

        if payloadType == 0xAD:
            parseData(frame[8:frameLen+1], payloadLen)
        elif payloadType == 0xAE:
            parseError(frame[8:frameLen+1])
    except:
        pass
    return True



frame = ''
def onData(x):
    global frame
    if x == b'\xaa' and len(frame) == 0:
        frame = x
    elif len(frame) > 0:
        frame += x
        if processFrame(frame):
            frame = ''

portName = '/dev/tty.SLAB_USBtoUART' # For Mac OS X
#portName = 'COM4' # For Windows
#portName = '/dev/ttyUSB0' # For Linux
with serial.Serial(portName, 230400) as ser:
    while 1:
        onData(ser.read())
