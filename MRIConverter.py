import os
import emissary
import soaplib
from soaplib.core.service import soap, rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.model.clazz import ClassModel
from soaplib.core.server import wsgi


CMD_STR = "vendors/MRIConvert-2.0.7/usr/bin/mcverter -v -f {FORMAT} -F -PatientName,-PatientId,-SeriesTime,-StudyId,-StudyDescription,-SeriesNumber,-SequenceName,-ProtocolName,-StudyDate,-SeriesDate,SeriesDescription -o {OUTPUT_PATH} {INPUT_PATH}"

class ConvertorResponse(ClassModel):
    """Response object holds the commandline execution response"""
    statuscode = Integer
    command = String
    stdout = String
    stderr = String
    cwd = String

    outputPath = String

    def __init__(self, command=None):
        self.command = command
        self.cwd = '.'
        self.statuscode = 0
        self.stdout = ""
        self.stderr = "Error: I'm sorry I cannot do that, Dave!"

def create_response(out):
    if out:
        r = ConvertorResponse(' '.join(out.command))
        r.statuscode = out.status_code
        r.stdout = out.std_out
        r.stderr = out.std_err
    return r

class MRIConverter(DefinitionBase):
    @soap(String, String, String, _returns=ConvertorResponse)
    def convert(self, img_format, inputPath, outputPath):
        command = CMD_STR.format(FORMAT=img_format, INPUT_PATH=inputPath,OUTPUT_PATH=outputPath)
        try:
            out = emissary.envoy.run(command)
            r = create_response(out)
            filename = os.path.basename(os.path.splitext(inputPath)[0])
            r.outputPath = os.path.join(outputPath, filename + ".mhd")
            return r
        except OSError, e:
            pass
            r = ConvertorResponse(command)
            r.statuscode = e.errno
            return e.strerror
        return r

soap_app = soaplib.core.Application([MRIConverter], 'mri', name='MRIConverter')
application = wsgi.Application(soap_app)

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        server = make_server(host='0.0.0.0', port=8080, app=application)
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"
