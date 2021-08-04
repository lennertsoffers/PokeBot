

class PvP:
    def __init__(self, playerId, opponentId, roomName, roomId, challenger=False):
        self.playerId = playerId
        self.opponentId = opponentId
        self.room = {
            "roomName": roomName,
            "roomId": roomId
            }
        self.ready = False
        self.challenger = challenger

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

    def isChallenger(self):
        return self.challenger
