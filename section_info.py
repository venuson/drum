class SectionInfo:
    def __init__(self, section_id, speed=60, divide_num=1, sound_data=[]):
        if speed < 30 or speed > 200:
            raise ValueError("speed must be between 30 and 200")
        if divide_num not in [1,2,3,4,6,8,12]:
            raise ValueError("divide_num must be 1, 2, 3, 4, 6, 8 or 12")
        
        self.section_id = section_id
        self.speed = speed
        self.divide_num = divide_num
        self.sound_data = sound_data

    def __str__(self):
        return f"SectionInfo(section_id={self.section_id}, speed={self.speed}, divide_num={self.divide_num}, sound_data={self.sound_data})"
    
    
    def to_json(self):
        return json.dumps(self.__dict__)    