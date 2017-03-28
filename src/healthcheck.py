from flask_restful import Resource


class HealthCheck(Resource):
    """Used to determine the running state of the web server within the container"""

    def get(self):
        """
        Unauthenticated call used to determine whether the web server is in a healthy state"
        :return: 200 OK
        """

        return 200
