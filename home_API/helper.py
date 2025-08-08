from datetime import datetime


class Interested:

    def __init__(self, id, unit, carpet_area, price, project_name, date):
        self.id = id  # int
        self.project_name = project_name  # str importance 0 most
        self.unit = unit  # Float importance  1
        self.carpet_area = carpet_area  # int importance  2
        self.price = price  # int  importance 3
        self.date = date  # datetime importance 4

    def match(self):
        print(type(self.id), self.id)
        print(type(self.unit), self.unit)
        print(type(self.carpet_area), self.carpet_area)
        print(type(self.price), self.price)
        print(type(self.project_name), self.project_name)
        print(type(self.date), self.date)

    def compare_objects(self, filter_obj):
        points = 0
        print(self.project_name)
        print(filter_obj.Area)
        # Compare project_name with Area
        if self.project_name in filter_obj.Area:
            points += 100

        # Compare self with units
        if self.unit in filter_obj.units:
            points += 90

        # Compare price with startBudget and stopBudget
        if filter_obj.startBudget <= self.price <= filter_obj.stopBudget:
            points += 70

        # Compare carpet_area with startCarpetArea and stopCarpetArea
        if filter_obj.startCarpetArea <= self.carpet_area <= filter_obj.stopCarpetArea:
            points += 80
        a = datetime.strptime(filter_obj.possession, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Compare date with possession
        if datetime(a.year, a.month, 1) <= datetime(a.year, a.month, 1):
            points += 60
        print(points)
        return points


class SearchFilterObject:
    def __init__(self, client, Area, startBudget, stopBudget, startCarpetArea, stopCarpetArea, possession,
                 units
                 ):
        self.client = client  # int
        self.Area = Area  # List of str compare to project_name
        self.units = units  # List of Flat compare to self
        self.startBudget = startBudget  # Float compare to price
        self.stopBudget = stopBudget  # Float compare to price
        self.startCarpetArea = startCarpetArea  # Float compare to carpet_area
        self.stopCarpetArea = stopCarpetArea  # Float compare to carpet_area
        self.possession = possession  # datetime compare to date

    def compare_objects(self, interested_obj):
        print(interested_obj.project_name)
        print(self.Area)
        points = 0
        for a in self.Area:
            print(a.formatted_version)
            # area.append(a.formatted_version)
            if interested_obj.project_name == a.formatted_version:
                points += 100
                break
        #
        # if interested_obj.project_name in area:
        #     points += 100

        for a in self.units:
            if interested_obj.unit == a.value:
                points += 90
                break

        # if interested_obj.unit in self.units:
        #     points += 90
        # print(self.units)
        if self.startBudget <= interested_obj.price:
            points += 35

        if interested_obj.price <= self.stopBudget:
            points += 35

        if self.startCarpetArea <= interested_obj.carpet_area:
            points += 40

        if interested_obj.carpet_area <= self.stopCarpetArea:
            points += 40

        a = self.possession
        b = interested_obj.date
        if datetime(a.year, a.month, 1) >= datetime(b.year, b.month, 1):
            points += 60

        print(points)
        return points

    def printValue(self):
        print(type(self.client), self.client)
        print(type(self.Area), self.Area)
        print(type(self.units), self.units)
        print(type(self.startBudget), self.startBudget)
        print(type(self.stopBudget), self.stopBudget)
        print(type(self.startCarpetArea), self.startCarpetArea)
        print(type(self.stopCarpetArea), self.stopCarpetArea)
        print(type(self.possession), self.possession)
