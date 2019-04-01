import ftplib
import logging
from pathlib import PosixPath
import datetime

class FtpFile:
    """ 
    Ftp File uploads the webcam image to the remote directory, after archiving the old image
    """
    def __init__(self, ftpconfig, imageconfig):
        self.property_ftpconfig = ftpconfig
        self.property_imageconfig = imageconfig

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
        if (self.property_ftpconfig.enabled):
            logging.info("Uploading file to " + self.property_ftpconfig.server + " as " + self.property_ftpconfig.remotefile)
            try:
                now = datetime.datetime.now()
                remotepath = PosixPath(self.property_ftpconfig.remotefile)
                archivepath = PosixPath(self.property_ftpconfig.archive_dir).joinpath(now.strftime("%Y%m/%d")).as_posix()
                archivefilename =  PosixPath(archivepath).joinpath(remotepath.stem + "-" + now.strftime("%Y%m%d-%H%M%S") + remotepath.suffix).as_posix()
                logging.debug("Remote file: " + self.property_ftpconfig.remotefile)
                logging.debug("Archive path: " + archivepath)
                logging.debug("Archive file: " + archivefilename)
                self.session = ftplib.FTP(self.property_ftpconfig.server,self.property_ftpconfig.user,self.property_ftpconfig.password)
                # make a new directory and don't complain if it's already there
                logging.info("Storing old image in " + archivefilename)
                try:
                    self.ftpmkdir(archivepath)
                    logging.debug("Renaming " + self.property_ftpconfig.remotefile + " to " + archivefilename)
                    self.session.rename(self.property_ftpconfig.remotefile, archivefilename)
                except Exception as e:
                    logging.error("Error archiving file: " + str(e.args))

                photo = open(self.property_imageconfig.filename,'rb')                  # file to send
                self.session.storbinary('STOR ' + self.property_ftpconfig.remotefile, photo)     # send the file
                photo.close()                                    # close file and FTP
                self.session.quit()
                self.session.close()
                logging.info("Upload completed successfully.")
            except NameError as e:
                logging.error('Failed to FTP file: NameError in script: ' + str(e.args))
            except Exception as e:
                logging.error('Failed to FTP file: ' + str(e.args))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
