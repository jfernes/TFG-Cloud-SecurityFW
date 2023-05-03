import os
import mysql.connector



xml = """<?xml version="1.0" encoding="UTF-8"?>
<wsag:AgreementOffer 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xmlns:wsag="http://schemas.ggf.org/graap/2007/03/ws-agreement" 
	xmlns:specs="http://www.specs-project.eu/resources/schemas/xml/SLAtemplate" 
	xmlns:ccm="http://www.specs-project.eu/resources/schemas/xml/control_frameworks/ccm" 
	xsi:schemaLocation="http://schemas.ggf.org/graap/2007/03/ws-agreement wsag.xsd 
	http://www.specs-project.eu/resources/schemas/xml/SLAtemplate SLAtemplate.xsd 
	http://www.specs-project.eu/resources/schemas/xml/control_frameworks/ccm ccm.xsd"
        wsag:AgreementId="{}">
        <wsag:Name>{}</wsag:Name>
        <wsag:Context>
            <wsag:ServiceProvider>{}</wsag:ServiceProvider>
            <wsag:ExpirationTime>{}</wsag:ExpirationTime>
            <wsag:TemplateName>{}</wsag:TemplateName>
            <wsag:TemplateId>{}</wsag:TemplateId>
        </wsag:Context>
        
        <wsag:ServiceDescriptionTerm wsag:Name="{}" wsag:ServiceName="{}"> 
        <specs:serviceDescription> 
            <specs:serviceResources> 
                <specs:resourcesProvider id="{}" name="{}" zone="{}" description="">
                </specs:resourcesProvider>
            </specs:serviceResources>
        </specs:serviceDescription>
        
        <specs:capabilities>
            {}
            
        </specs:capabilities>
        
        </wsag:ServiceDescriptionTerm>
</wsag:AgreementOffer>
 
"""


capability = """
            <specs:capability id="{}" name="{}" description="{}">
                <specs:controlFramework id="CCM_v4.0" frameworkName="CCM Control Framework v4.0">
                    {}

                </specs:controlFramework>
                <technology>
                    {}
                </technology>
            </specs:capability>

"""

seccontrol = """    
                    <specs:CCMsecurityControl name="{}" id="{}" control_domain="{}">
                        <ccm:description>
                            {}
                        </ccm:description>
                        <ccm:importance_weight> </ccm:importance_weight>
                    </specs:CCMsecurityControl>
"""

def connectDB():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_SERVER'),
        user="root",
        password="root",
        database="secframework"
)
    return connection


def generateSSLA(agreement_id, ssla_name, service_provider, expiration_time,
        template_name, template_id, service_description_name,
        service_name, resource_provider_id, resource_provider_name, 
        resource_provider_zone, intents, techs):
    
    connection = connectDB()
    cursor = connection.cursor(buffered=True)
    sql = """SELECT id, name, description FROM intent WHERE id = '{}'"""
    sqlsc = """SELECT name, id, control_domain, description FROM seccontrol 
            WHERE intentid = '{}'"""
    
    
    
    cap = ""
    for intent in intents:
        sc = ""
        cursor.execute(sqlsc.format(str(intent)))
        results = cursor.fetchall()
        for i in results:
            sc = sc + seccontrol.format(i[0], i[1], i[2], i[3])
        
        cursor.execute(sql.format(intent))
        result = cursor.fetchone()
        cap = cap + capability.format(result[0], result[1], result[2], sc, techs[intent])
        
        
    genxml = xml.format(agreement_id, ssla_name, service_provider, expiration_time, template_name, template_id, service_description_name, service_name,
               resource_provider_id, resource_provider_name, resource_provider_zone, cap)
        
    connection.close()    
    return genxml