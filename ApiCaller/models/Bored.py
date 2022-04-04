from dataclasses import asdict, dataclass


@dataclass
class Bored:
    activity: str
    type: str
    participants: int
    price: float
    link: str
    key: str
    accessibility: float

    @property
    def _activity(self):
        return self._activity
    
    @property
    def _type(self):
        return self._type

    @property
    def _participants(self):
        return self._participants
    
    @property
    def _price(self):
        return self._price    
    
    @property
    def _link(self):
        return self._link
    
    @property
    def _key(self):
        return self._key
    
    @property
    def _accessibility(self):
        return self._accessibility

if __name__=='__main__':
    bored = Bored(activity="Watch a movie you\'d never usually watch",type="relaxation",participants=1,price=0.15,link="",key="9212950",accessibility=0.15)
    print(bored.accessibility)

    print(asdict(bored))

# {"activity":"Watch a movie you\'d never usually watch","type":"relaxation","participants":1,"price":0.15,"link":"","key":"9212950","accessibility":0.15}