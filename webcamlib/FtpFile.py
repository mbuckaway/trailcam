import ftplib
import logging
from pathlib import PosixPath
import datetime
from webcamlib.FileRestClient import FileRestClient
class FtpFile:
    """ 
    Ftp File uploads the webcam image to the remote directory, after archiving the old image
    """
    def __init__(self, config, data):
        self.logger = logging.getLogger('ftpfile')
        self.config = config
        self.data = data
        
    def ftpmkdir(self, directory):
        path = PosixPath(directory)
        parts = path.parts
        length = len(parts)-1
        i = 0
        root = parts[0]
        while (i < length)  :
            search = parts[i+1]
            newroot = PosixPath(root).joinpath(search).as_posix()
            dirlist = self.session.nlst(root)
            if search not in dirlist : #check if 'foo' exist inside 'www'
                self.session.mkd(newroot) #Create a new directory called foo on the server.
            i=i+1
            root = newroot

    def dispose(self):
        if (self.session):
            self.session.close()

    def sendfile(self):
        if (self.config.ftp.enabled):
            self.logger.info("Uploading file to " + self.config.ftp.server)
            try:
                now = datetime.datetime.now()
                localfileobj = PosixPath(self.config.image.filename)
                remotepathobj = PosixPath(self.config.ftp.archive_dir).joinpath(now.strftime("%Y%m/%d"))
                remotepath = remotepathobj.as_posix()
                remotefilename =  localfileobj.stem + "-" + now.strftime("%Y%m%d-%H%M%S") + localfileobj.suffix
                remotefullpath = PosixPath(remotepath).joinpath(remotefilename).as_posix()
                self.logger.debug("Remote path: " + remotepath)
                self.logger.debug("Remote file: " + remotefilename)
                self.logger.debug("Remote fullpath: " + remotefullpath)
                self.session = ftplib.FTP(self.config.ftp.server,self.config.ftp.user,self.config.ftp.password)
                # make a new directory and don't complain if it's already there
                self.logger.info("Storing image in " + remotefullpath)
                try:
                    self.ftpmkdir(remotepath)
                except Exception as e:
                    self.logger.error("Error creating directory file: " + str(e.args))
                    self.data.lasterror = "creating directory failed"

                photo = open(self.config.image.filename,'rb')                  # file to send
                self.session.storbinary('STOR ' + remotefullpath, photo)     # send the file
                photo.close()                                    # close file and FTP
                self.session.quit()
                self.session.close()
                self.logger.info("Upload completed successfully.")

                # Update remote database
                if (self.config.restapi.enabled):
                    restclient = FileRestClient(self.config)
                    restclient.new_file(remotefilename, remotepath, self.data.annotation_photo)
                    self.logger.info("Updated website successfully.")
                else:
                    self.logger.warn("Updating website disabled.")
                
            except NameError as e:
                self.logger.exception('Failed to FTP file: NameError in script: %s', e)
                self.data.lasterror = "FTP file failed"
            except Exception as e:
                self.logger.exception('Failed to FTP file: %s', e)
                self.data.lasterror = "FTP file failed"
        else:
            self.logger.warn("FTP upload disabled")
            self.data.lasterror = "FTP upload disabled"
