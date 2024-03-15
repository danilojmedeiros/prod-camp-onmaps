from service.constants import mensagens


class ControllResponse(object):

    def __init__(self):
        print('ControllResponse class for response controll')

    @staticmethod
    def send_exception(objError, messages, status=500):
        """
        Method that handles errors without passing exception real

        :param objError: Object Error ex: TypeError.
        :param messages: Message.
        :param status: Code Http.
        :return: jsonException
        """
        jsonException = {}

        if isinstance(objError, Exception):
            jsonException['messages'] = messages
            jsonException['status'] = status

        elif isinstance(objError, BaseException):
            jsonException['messages'] = messages
            jsonException['status'] = status
        else:
            jsonException['messages'] = mensagens.ERROR_GENERIC
            jsonException['status'] = 500

        return jsonException, status

    @staticmethod
    def send_success(data, messages, status=200):
        """
        Method that handles sucess

        :param data: Response data, dado a ser enviado.
        :param messages: Message.
        :param status: Code Http.
        :return: json_sucess
        """
        json_sucess = {'resultado': data, 'messages': messages, 'status': status}
        return json_sucess
