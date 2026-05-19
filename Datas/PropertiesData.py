from dataclasses import dataclass

@dataclass
class PropertyType:
    id : int
    key_name : str
    max_owned : int | None
    is_abstract : bool #부동산 선택에서 보지만 차고선택에서 안보일거(slot 0인 부동산 차고에 안보임)
    is_hidden : bool #부동산에 안보임. hidden abs면 그냥 아무데서도 안보임.
    parent_id : int | None #abs면 child의 Slot은 부모꺼
    is_unchangeable : bool #아케이드끼리 바꿔지는지 / 매켄지인지
#이클립스 볼버드 차고 abstract, 5개의 분리된 차고가 child
#나이트클럽 abs아니고 3개의 추가 차고가 child
#오피스 abstract, 추가 차고가 child
#아레나워 abs아니고 추가 차고 child
#격납고가 abs아니고 매켄지가 abstract child
#코사트카 hidden임
#테러바이트 hidden임
#페가수스 hidden임
#Null Garage가 hidden abstract
#이동수단창고(특수) 차고 뷰어에선 보이지만, 차량 저장시에는 조건부로 인해 안보여야 함.
#Money Fronts를 Type으로 하고 Property들로 그 사업장 세개 넣어서 하면 될 듯

@dataclass
class Property:
    id : int
    key_name : str
    type_id : int
    price : int

@dataclass
class PropertyCustomType:
    id : int
    key : str
    name : str
    propertytype_id : int
    is_unchangeable : bool

@dataclass
class PropertyCustom:
    id : int
    key : str
    name : str
    customtype_id : int
    price : int

