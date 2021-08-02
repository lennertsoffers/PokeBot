

class PvP:
    def __init__(self, playerId, opponentId, roomName, roomId):
        self.playerId = playerId
        self.opponentId = opponentId
        self.room = {
            "roomName": roomName,
            "roomId": roomId
            }
        self.ready = False

    def getPlayerId(self):
        return self.playerId

    def getOpponentId(self):
        return self.opponentId

    def getRoom(self):
        return self.room

    def isReady(self):
        return self.ready;

    def setReady(self, ready):
        self.ready = ready
