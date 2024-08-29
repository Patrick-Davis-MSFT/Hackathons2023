# import generic base packages
import json, uuid, sys, os, datetime, time

# import azure specific packages
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import Person, TrainingStatusType, QualityForRecognition

from msrest.authentication import CognitiveServicesCredentials

# define key variables
faceEndpoint = ""
faceKey = ""

fileDir = "./facedata/known/"

# create personGroup ID and Name
personGroupId = uuid.uuid4()
personGroupName = "legends"

# create a face client
faceClient = FaceClient( faceEndpoint, CognitiveServicesCredentials( faceKey ) )

# check for existence of person group to verify successful creation
personGroups = faceClient.person_group.list()

# print( personGroups )

# clean up any existing person groups
cleanUp = input( "Enter 'Y' to delete any existing person groups: ")

if cleanUp.lower() == 'y' :

    for personGroup in personGroups :

        print( "Deleting: ", personGroup.person_group_id, " - ", personGroup.name )

        faceClient.person_group.delete( person_group_id = personGroup.person_group_id )

else :

    print( "Skipping cleanup of existing person groups." )

# create a person group to be checked and/or person objects created within
faceClient.person_group.create( person_group_id = personGroupId, name = personGroupName, recognition_model='recognition_04' )


# loop through files in local dir to populate fileList
fileList = os.listdir( fileDir )

for file in fileList :

    # print( "Discovered File : " + file )

    checkFile = fileDir + file
    print( checkFile )

    # run facial detection on the file
    foundFaces = []
    try:
        foundFaces = faceClient.face.detect_with_stream( ( open( checkFile, 'rb' ) ), detection_model='detection_03', recognition_model = 'recognition_04', return_face_landmarks = True, return_face_attributes = ['qualityForRecognition'] )
    except Exception as e:
        print( "Error processing file: ", checkFile )
        print( e )
    
    if len( foundFaces ) > 0 :

        for face in foundFaces :

            print( "Found a face!" )
            
            print(face.face_attributes)
            print(face.face_rectangle)

            # because peson group is empty, creating new person object for each face within the person group
            personId = uuid.uuid4()
            person = faceClient.person_group_person.create( person_group_id = personGroupId, name = str( personId ) )

            # wait 3 seconds to ensure person object has been created
            time.sleep( 3 )

            # add face to person object
            faceClient.person_group_person.add_face_from_stream( person_group_id = personGroupId, person_id = person.person_id, image = ( open( checkFile, 'rb' ) ) )

            print( "Image ", checkFile, " added to new Person object ", person.person_id, " in PersonGroup ", personGroupId, " named ", personGroupName )

    else :

        print( "No faces found in this file." ) 

# train persongroup for future comparison(s)
trainResponse = faceClient.person_group.train( person_group_id = personGroupId )
print( trainResponse )

while ( True ) :
        
        status = faceClient.person_group.get_training_status( personGroupId )

        print( "Current PersonGroup Training Status :", status.status )

        if ( status.status is TrainingStatusType.succeeded ) :
                    
            print( "Person Group Training has completed." )

            break
                
        elif ( status.status is TrainingStatusType.failed ) :

            faceClient.person_group.delete( personGroupId )

            sys.exit( "Person Group Training has failed." )

        else :

            print( "Person Group Training is still in progress - Checking Again in 5 seconds : " )
            # wait 5 seconds before checking again
            time.sleep( 5 )

print( "Person Group Training has completed." )
print( "Person Group ID : ", personGroupId )
print("Detect Face with Image")

# Detect faces
face_ids = []
faces = faceClient.face.detect_with_stream( ( open( "./facedata/unknown/p1.jpg", 'rb' ) ), detection_model='detection_01', recognition_model = 'recognition_04', return_face_landmarks = True, return_face_attributes = ['qualityForRecognition'] )
for face in faces:
  print(face.face_attributes)
  print(face.face_rectangle)
    # Only take the face if it is of sufficient quality.
  if face.face_attributes.quality_for_recognition == QualityForRecognition.high or face.face_attributes.quality_for_recognition == QualityForRecognition.medium:
    face_ids.append(face.face_id)
    print("Face ID: {}".format(face.face_id))

# Identify faces
results = faceClient.face.identify(face_ids, personGroupId, return_face_id=False)
print('Identifying faces in image')
if not results:
    print('No person identified in the person group')
for identifiedFace in results:
    if len(identifiedFace.candidates) > 0:
        print('Person is identified with {} in images.'.format(len(identifiedFace.candidates) ))
        for candidate in identifiedFace.candidates:
            print('Person is identified for face ID {} in image, with a confidence of {}.'.format(identifiedFace.face_id, candidate.confidence)) # Get topmost confidence score

            # Verify faces
            verify_result = faceClient.face.verify_face_to_person(identifiedFace.face_id, candidate.person_id, personGroupId)
            #print(verify_result)
            #print(identifiedFace)
            #print(candidate)
            print('verification result: {}. confidence: {} with face: {}'.format(verify_result.is_identical, verify_result.confidence, candidate.person_id))
    else:
        print('No person identified for face ID {} in image with stored face.'.format(identifiedFace.face_id))
 
