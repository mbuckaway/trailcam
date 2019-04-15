import ftplib
import logging
from pathlib import PosixPath
import datetime

class FtpFile:
    """ 
    Ftp File uploads the webcam image to the remote directory, after archiving the old image
    """
    def __init__(self, config):
        self.logger = logging.getLogger('ftpfile')
        self.config = config
        
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
        pass

    def sendfile(self):
        if (self.config.ftp.enabled):
            self.logger.info("Uploading file to " + self.config.ftp.server + " as " + self.config.ftp.remotefile)
            try:
                now = datetime.datetime.now()
                remotepath = PosixPath(self.config.ftp.remotefile)
                archivepath = PosixPath(self.config.ftp.archive_dir).joinpath(now.strftime("%Y%m/%d")).as_posix()
                archivefilename =  PosixPath(archivepath).joinpath(remotepath.stem + "-" + now.strftime("%Y%m%d-%H%M%S") + remotepath.suffix).as_posix()
                self.logger.debug("Remote file: " + self.config.ftp.remotefile)
                self.logger.debug("Archive path: " + archivepath)
                self.logger.debug("Archive file: " + archivefilename)
                self.session = ftplib.FTP(self.config.ftp.server,self.config.ftp.user,self.config.ftp.password)
                # make a new directory and don't complain if it's already there
                self.logger.info("Storing old image in " + archivefilename)
                try:
                    self.ftpmkdir(archivepath)
                    self.logger.debug("Renaming " + self.config.ftp.remotefile + " to " + archivefilename)
                    self.session.rename(self.config.ftp.remotefile, archivefilename)
                except Exception as e:
                    self.logger.error("Error archiving file: " + str(e.args))

                photo = open(self.config.image.filename,'rb')                  # file to send
                self.session.storbinary('STOR ' + self.config.ftp.remotefile, photo)     # send the file
                photo.close()                                    # close file and FTP
                self.session.quit()
                self.session.close()
                self.logger.info("Upload completed successfully.")
            except NameError as e:
                self.logger.error('Failed to FTP file: NameError in script: ' + str(e.args))
            except Exception as e:
                self.logger.error('Failed to FTP file: ' + str(e.args))

