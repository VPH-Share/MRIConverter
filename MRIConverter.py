from os import basename, splitext, join
import emissary
import soaplib
from soaplib.core.service import soap, rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.model.clazz import ClassModel
from soaplib.core.server import wsgi


CMD_STR = "vendors/MRIConvert-2.0.7/usr/bin/mcverter -v -f {FORMAT} -F -PatientName,-PatientId,-SeriesTime,-StudyId,-StudyDescription,-SeriesNumber,-SequenceName,-ProtocolName,-StudyDate,-SeriesDate,SeriesDescription -o {OUTPUT_PATH} {FIXED_IMAGE} {MOVING_IMAGE}"

class ConvertorResponse(ClassModel):
    """Response object holds the commandline execution response"""
    statuscode = Integer
    command = String
    stdout = String
    stderr = String
    cwd = String

    fixed_output_path = String
    moving_output_path = String

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
    @soap(String, String, String, String, _returns=ConvertorResponse)
    def convert(self, img_format, fixed_image_path, moving_image_path, output_path):
        command = CMD_STR.format(FORMAT=img_format,
                                 FIXED_IMAGE=inputPath,
                                 MOVING_IMAGE=moving_image_path.
                                 OUTPUT_PATH=output_path)
        try:
            out = emissary.envoy.run(command)
            r = create_response(out)
            fixed_filename = basename(splitext(fixed_image_path)[0])
            moving_filename = basename(splitext(moving_image_path)[0])
            r.fixed_output_path = join(output_path, fixed_filename + ".mhd")
            r.moving_output_path = join(output_path, moving_filename + ".mhd")
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
