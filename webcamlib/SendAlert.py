from twilio.rest import Client
import logging

class SendAlert:
    """ Class to send a twilio message using information from the config file """
    def __init__(self, hwmonconfig):
        self.hwmonconfig = hwmonconfig
        self.client = Client(hwmonconfig.twilio_account_sid, hwmonconfig.twilio_auth_token)

    def SendWarning(self, voltage):
        message = self.hwmonconfig.message_warning
        msgstr = message.replace('%%VOLTS%%', str(voltage))
        self._sendMsg(msgstr)

    def SendShutdown(self, voltage):
        message = self.hwmonconfig.message_shutdown
        msgstr = message.replace('%%VOLTS%%', str(voltage))
        self._sendMsg(msgstr)

    def _sendMsg(self, msgstr):
        try:
            for number in self.hwmonconfig.phone_numbers:
                message = self.client.messages.create(
                    to=number, 
                    from_=self.hwmonconfig.twilio_phone_number,
                    body=msgstr)
                logging.info('Sent message to ' + number + ' and Twilio SID: ' + message.sid)
        except Exception as e:
            logging.error('Error sending message' + str(e.args))
            raise e




