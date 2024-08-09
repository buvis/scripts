from buvis.adapters import console, OutlookLocalAdapter

class CommandCreateTimeblock:

    def __init__(self, cfg):
        try:
            self.outlook = OutlookLocalAdapter()
        except Exception as e:
            console.panic(e)

    def execute(self):
        print(f"Would create a timeblock")
