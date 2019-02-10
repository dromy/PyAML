from values import PointFeature

class Building(PointFeature):
   def __init__(self,id,file):
      PointFeature.__init__(self,'building',file)
      self.id = id

class Spring(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'spring',file)

class Tank(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'tank_dam_p',file)

class Bore(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'bore',file)

class Windpump(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'windpump',file)

class Waterpoint(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'waterpoint',file)

class Trig(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'trig_station',file)

class BenchMark(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'bench_mark',file)

class RoadBridgePt(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'bridge_rd_p',file)

class RoadTunnelPt(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'tunnel_rd_p',file)

class Gate(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'gate',file)

class Grid(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'grid',file)

class Ford(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'ford',file)

class GasWell(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'gas_well',file)

class StorageTank(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'stor_tank_p',file)

class Yard(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'yard',file)

class Mine(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'mine',file)

class Landmark(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'landmark_p',file)

class RailBridgePt(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'bridge_rl_p',file)

class RailTunnelPt(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'tunnel_rl_p',file)

class RailStation(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'rail_station',file)

class Lighthouse(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'lighthouse',file)

class Wreck(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'wreck',file)

class OffshoreRock(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'rock_offshor',file)

class Locality(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'locality',file)

class Pinnacle(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'pinnacle',file)

class Cave(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'cave',file)

class Waterfall(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'waterfall',file)

class  Lock(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'lock',file)

class Waterhole(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'waterhole',file)

class SpotElevation(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'spot_elevatn',file)

class AircraftFacility(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'aircrft_flty',file)

class TransitionPt(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'transition_p',file)

class NatRoute(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'route_nat',file)

class StateRoute(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'route_state',file)

class DistanceInd(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'distance_ind',file)

class Pylon(PointFeature):
   def __init__(self,file):
      PointFeature.__init__(self,'pylon',file)


x = Building(10,'test')
for i in x.items:
   print i.name
   print i.type

