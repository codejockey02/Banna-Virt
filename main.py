import part1
import part2
from flask import Flask
from flask import request
from flask import render_template
import os
from werkzeug import secure_filename

app = Flask(__name__, template_folder='templates')
Upload_Folder = './Upload_Folder'
app.config['Upload_Folder'] = Upload_Folder

@app.route('/', methods=['GET'])
def index():
    return render_template('client.html')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['Upload_Folder'], filename))
    outputFile = open('./templates/output.html', 'w')
    outputFile.write("<html><body bgcolor=aqua font-color=white>")
    with open('./Upload_Folder/addresses.txt', 'r') as addressFile:
        physicalMemory = {}
        tlb = []
        pageTable = []
        pageFaultCounter = 0
        tlbHitCounter = 0
        addressReadCounter = 0
        for line in addressFile:
            tlbHit = 0
            pageTableTrue = 0
            logicalAddress = int(line) 
            offset = logicalAddress & 255
            pageOriginal = logicalAddress & 65280
            pageNumber = pageOriginal >> 8
            # print("Logical address is: " + str(logicalAddress) + "\nPageNumber is: " + str(pageNumber) + "\nOffset: " + str(offset))
            addressReadCounter += 1
            tlbHit = part1.checkTLB(pageNumber, physicalMemory, offset, logicalAddress, tlb, addressReadCounter, outputFile)
            if tlbHit == 1:
                tlbHitCounter += 1
            if tlbHit != 1:
                pageTableTrue = part1.checkPageTable(pageNumber, logicalAddress, offset, addressReadCounter, pageTable, physicalMemory, outputFile)
            if pageTableTrue != 1 and tlbHit != 1:
                stro='this is a page fault'
                print(stro)
                part2.pageFaultHandler(pageNumber, tlb, pageTable, physicalMemory)
                pageFaultCounter += 1
                part1.checkTLB(pageNumber, physicalMemory, offset, logicalAddress, tlb, addressReadCounter, outputFile)
    pageFaultRate = pageFaultCounter / addressReadCounter
    tlbHitRate = tlbHitCounter / addressReadCounter
    outStr = 'Number of translated address: ' + str(addressReadCounter) + '\n' + 'Number of page fault: ' + str(pageFaultCounter) + '\n' + 'Page fault rate: ' + str(pageFaultRate) + '\n' + 'Number of TLB hits: ' + str(tlbHitCounter) + '\n' + 'TLB hit rate: ' + str(tlbHitRate) + '<BR>'
    print(outStr)
    outputFile.write(outStr)
    outputFile.write("</html></body>")
    outputFile.close()
    addressFile.close()
    return render_template('output.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
