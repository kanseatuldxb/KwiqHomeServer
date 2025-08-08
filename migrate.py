import sqlite3
import time

from django.contrib.auth.hashers import make_password

from client_API.models import Client, SearchFilter
from home_API.models import Project, Unit, Units, Area
from organization.models import Organization, Employee

def create_areas(sour):
    Area.objects.all().delete()
    sour.execute('SELECT * FROM home_API_area')
    areas = sour.fetchall()
    for area in areas:
        print(area)
        Area.objects.create(name=area[0], formatted_version=area[1])
    print('Areas migrated successfully')

def create_units(sour):
    Units.objects.all().delete()
    sour.execute('SELECT * FROM home_API_units')
    units = sour.fetchall()
    for unit in units:
        print(unit)
        Units.objects.create(value=unit[0], name=unit[1])
    print('Units migrated successfully')

def create_projects(source_cursor, org, e):
    Project.objects.all().delete()
    Unit.objects.all().delete()
    source_cursor.execute('''SELECT 
                                     id,
                                     area,
                                     projectName,
                                     projectType,
                                     developerName,
                                     landParcel,
                                     landmark,
                                     areaIn,
                                     waterSupply,
                                     floors,
                                     flatsPerFloors,
                                     totalUnit,
                                     availableUnit,
                                     amenities,
                                     parking,
                                     longitude,
                                     latitude,
                                     transport,
                                     readyToMove,
                                     power,
                                     goods,
                                     rera,
                                     possession,
                                     contactPerson,
                                     contactNumber,
                                     marketValue,
                                     lifts,
                                     brokerage,
                                     incentive,
                                     url
                                     from home_API_project''')
    projects = source_cursor.fetchall()
    for project in projects:
        print(project)
        p = Project.objects.create(area=project[1], projectName=project[2], projectType=project[3],
                                   developerName=project[4], landParcel=project[5], landmark=project[6],
                                   areaIn=project[7],
                                   waterSupply=project[8], floors=project[9], flatsPerFloors=project[10],
                                   totalUnit=project[11], availableUnit=project[12], amenities=project[13],
                                   parking=project[14], longitude=project[15], latitude=project[16],
                                   transport=project[17],
                                   readyToMove=project[18], power=project[19], goods=project[20], rera=project[21],
                                   possession=project[22], contactPerson=project[23], contactNumber=project[24],
                                   marketValue=project[25], lifts=project[26], brokerage=project[27],
                                   incentive=project[28],
                                   url=project[29], added_by=e, organization=org)
        source_cursor.execute('''SELECT 
                                id,
                                unit,
                                CarpetArea,
                                price,
                                project_id_id
                               FROM home_API_unit WHERE project_id_id = ?''', (project[0],))
        units = source_cursor.fetchall()
        for unit in units:
            Unit.objects.create(project_id=p, unit=unit[1], CarpetArea=unit[2], price=unit[3], organization=org)
        #         source_cursor.execute('SELECT * FROM home_API_unit WHERE project_id = ?', (project[0],))
        #         units = source_cursor.fetchall()
        #         for unit in units:
        #             Unit.objects.create(project_id=p, unit=unit[1], CarpetArea=unit[2], price=unit[3], organization=org)
        print('Project and units migrated successfully')

def create_client(source_cursor, org, e):
    Client.objects.all().delete()
    SearchFilter.objects.all().delete()
    source_cursor.execute('''SELECT 
                                 id,
                                 fname,
                                 lname,
                                 phoneNO,
                                 massageNO,
                                 email
                                 from client_API_client''')
    clients = source_cursor.fetchall()
    for client in clients:
        c = Client.objects.create(fname=client[1], lname=client[2], phoneNO=client[3], massageNO=client[4], email=client[5],
                              added_by=e, organization=org)
        source_cursor.execute('''SELECT  id, startBudget, stopBudget, startCarpetArea, stopCarpetArea, possession, requirements, client_id
         FROM client_API_searchfilter WHERE client_id = ?''', (client[0],))
        search_filters = source_cursor.fetchall()
        for search_filter in search_filters:
            s = SearchFilter.objects.create(client_id=c.id, startBudget=search_filter[1], stopBudget=search_filter[2],
                                            startCarpetArea=search_filter[3], stopCarpetArea=search_filter[4],
                                            possession=search_filter[5], requirements=search_filter[6])
            source_cursor.execute('SELECT * FROM client_API_searchfilter_Area WHERE searchfilter_id = ?', (search_filter[0],))
            areas = source_cursor.fetchall()
            for area in areas:
                print("Area -->", area[2])
                a = Area.objects.get(formatted_version=area[2])
                print(a)
                s.Area.add(a)
            source_cursor.execute('SELECT * FROM client_API_searchfilter_units WHERE searchfilter_id = ?', (search_filter[0],))
            units = source_cursor.fetchall()
            for unit in units:
                u = Units.objects.get(value=unit[2])
                s.units.add(u)
                print('Units -->', u)
    print('Clients migrated successfully')

def migrate_organization():
    Organization.objects.all().delete()
    Employee.objects.all().delete()
    source_conn = sqlite3.connect('a1db.sqlite3')
    source_cursor = source_conn.cursor()
    create_areas(source_cursor)
    print('-' * 50)
    create_units(source_cursor)
    print(Units.objects.all())
    print('-' * 50)

    org = Organization.objects.create(name='TakeAhome', is_active=True)
    e = Employee.objects.create(email="akash@gmail.com", organization=org, user_type='CEO', name='Akash',
                                phone_number='4567890123',
                                username='akash', password=make_password('Admin@1234'))
    e1 = Employee.objects.create(email="akshay@gmail.com", organization=org, user_type='CEO', name='Akshay',
                                 phone_number='1234567890',
                                 username='akshay', password=make_password('Admin@1234'), assigned_to=e)

    create_projects(source_cursor, org, e)
    create_client(source_cursor, org, e)

    source_conn.close()
    print('Migration completed successfully')
    print('-' * 50)
    print(f'Organization: {org.id}\nusername: {e.username}\nemail: {e.email}\npassword: Admin@1234')
migrate_organization()
# give django migration command
