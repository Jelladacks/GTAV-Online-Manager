from dataclasses import dataclass

@dataclass
class BuyBonusRule:
    id : int
    triggertype_id : int
    trigger_id : int
    rewardtype_id : int
    reward_id : int
    quantity : int

@dataclass
class BuyingType:
    id : int
    key_name : str # "vehicle" "property" "p_custom"